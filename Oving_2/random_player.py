"""
this is one of the player classes
"""
import random
from player_interface import PlayerInterface


class RandomPlayer(PlayerInterface):
    """
    this is the player that chooses on random what to pick
    """
    def __init__(self, name):
        super().__init__(name)

    def select_action(self):
        return random.choice(["rock", "paper", "scissors"])

    def receive_result(self, result):
        if result.winner is not None:
            if self.name == result.winner.name:
                self.points += 1
        else:
            self.points += 0.5
