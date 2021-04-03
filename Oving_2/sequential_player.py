"""
This is one of the player classes
"""
from player_interface import PlayerInterface


class SequentialPlayer(PlayerInterface):
    """
    this is the player class that chooses based on what is chose last time
    """
    previous = []

    def __init__(self, name):
        super().__init__(name)

    def select_action(self):
        if len(self.previous) != 0:
            if self.previous[-1] == "rock":
                self.previous.append("scissors")
                return "scissors"
            elif self.previous[-1] == "scissors":
                self.previous.append("paper")
                return "paper"
            else:
                self.previous.append("rock")
                return "rock"
        else:
            self.previous.append("rock")
            return "rock"

    def receive_result(self, result):
        if result.winner is not None:
            if self.name == result.winner.name:
                self.points += 1
        else:
            self.points += 0.5
