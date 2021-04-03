"""
This is one of the player classes
"""
from player_interface import PlayerInterface
import random


class MostCommonPlayer(PlayerInterface):
    """
    This player looks at what the opponent has picked the most often,
    and assumes it will pick it again and then counter that pick
    """
    opponents_previous = []

    def __init__(self, name):
        super().__init__(name)

    def select_action(self):
        if len(self.opponents_previous) == 0:
            return random.choice(["rock", "paper", "scissors"])
        else:
            most_common = self.find_most_common()
            if most_common == 0:
                return "paper"
            elif most_common == 1:
                return "scissors"
            else:
                return "rock"

    def find_most_common(self):
        """
        Findes the opponents most common pick
        :return:
        """
        counter = [0, 0, 0]
        for play in self.opponents_previous:
            if play == "rock":
                counter[0] += 1
            elif play == "paper":
                counter[1] += 1
            else:
                counter[2] += 1
        largest = 0
        largest_index = None
        for number in range(len(counter)):
            if counter[number] > largest:
                largest = counter[number]
                largest_index = number
        return largest_index

    def receive_result(self, result):
        if result.winner is not None:
            if self.name == result.winner.name:
                self.points += 1
        else:
            self.points += 0.5

        if result.player_1.name == self.name:
            self.opponents_previous.append(result.p2_choice)
        else:
            self.opponents_previous.append(result.p1_choice)
