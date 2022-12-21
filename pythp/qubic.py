import gym
import numpy as np
from gym import spaces
from board import Board
import board
import random
import os
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import EvalCallback
from shutil import copyfile # keep track of generations

BEST_THRESHOLD = 0.5
LOGDIR = "selfplay"

class Qubic(gym.Env):

    # 4x4x4 game with each cell 4 states (X, O, ' ', *)
    reward_range = (-np.inf, np.inf)
    observation_space = spaces.MultiDiscrete([2 for _ in range(0, 4*4*4 * 4)])
    action_space = spaces.MultiDiscrete([4, 4, 4])
    nb_actions = 64

    def seed(self, seed=None):
        random.seed(seed)

    def reset(self):
        self.current_player = board.CROSS  # Cross starts first
        self.board = Board()

        self.board.add_wildcards(random.randint(0, 9))

        return self.board.to_tensor()

    def step(self, action):

        i, j, k = action

        # Illegal moves must be avoided at all times!
        if not self.board.is_move_legal(i, j, k):
            return self.board.to_tensor(), -10, True, {"state": "done", "reason": "Illegal move"}

        other_player = board.CROSS if self.current_player == board.NOUGHT else board.CROSS

        self.board.move(i, j, k, self.current_player)

        # Check if we won
        if self.board.state == self.current_player:
            exp = {"state": "done",
                   "reason": "{} has won".format(self.current_player)}
            done = True
            return self.board.to_tensor(), 1, done, exp

        # Check if we lost
        if self.board.state == other_player:
            exp = {"state": "done",
                   "reason": "{} has lost".format(self.current_player)}
            done = True
            return self.board.to_tensor(), -1, done, exp

        # Check for draws
        if self.board.get_nr_of_legal_moves() == 0:
            exp = {"state": "done",
                   "reason": "draw"}
            done = True
            return self.board.to_tensor(), 0, done, exp

        # Check if other player can win in next move

        other_count = self.board.count_winning_lines(other_player)

        if other_count[3] != 0:
            return self.board.to_tensor(), -1, False, {"state": "in progress", "reason": "{} can lose next turn".format(self.current_player)}

        # Switch player
        self.current_player = other_player

        return self.board.to_tensor(), 0, False, {"state": "in progress"}

    def render(self, mode="human"):
        print(self.board)


class SelfPlayQubic(Qubic):

    def __init__(self) -> None:
        super(SelfPlayQubic).__init__()
        self.policy = self
        self.best_model = None
        self.best_model_filename = None
        self.filename = None

    def predict(self, obs):  # the policy
        if self.best_model is None:
            return self.action_space.sample()  # return a random action
        else:
            action, _ = self.best_model.predict(obs)
            return action

    def reset(self):
        # load model if it's there
        modellist = [f for f in os.listdir(LOGDIR) if f.startswith("history")]
        modellist.sort()
        
        filename = None
        if len(modellist) > 0:
            filename = os.path.join(LOGDIR, modellist[-1])  # the latest best model
        
        if filename != self.best_model_filename:
            print("loading model: ", filename)
            self.best_model_filename = filename
            if self.best_model is not None:
                del self.best_model
            self.best_model = PPO.load(filename, env=self)
        return super(SelfPlayQubic, self).reset()

class SelfPlayCallback(EvalCallback):
  # hacked it to only save new version of best model if beats prev self by BEST_THRESHOLD score
  # after saving model, resets the best score to be BEST_THRESHOLD
  def __init__(self, *args, **kwargs):
    super(SelfPlayCallback, self).__init__(*args, **kwargs)
    self.best_mean_reward = BEST_THRESHOLD
    self.generation = 0
  def _on_step(self) -> bool:
    result = super(SelfPlayCallback, self)._on_step()
    if result and self.best_mean_reward > BEST_THRESHOLD:
      self.generation += 1
      print("SELFPLAY: mean_reward achieved:", self.best_mean_reward)
      print("SELFPLAY: new best model, bumping up generation to", self.generation)
      source_file = os.path.join(LOGDIR, "best_model.zip")
      backup_file = os.path.join(LOGDIR, "history_"+str(self.generation).zfill(8)+".zip")
      copyfile(source_file, backup_file)
      self.best_mean_reward = BEST_THRESHOLD
    return result