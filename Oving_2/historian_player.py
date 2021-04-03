"""
this is one of the player classes
"""
import random
from player_interface import PlayerInterface


class HistorianPlayer(PlayerInterface):
    """
    This is the player that looks for patterns in what the opponent plays and looks to counter it
    """
    opponents_previous = []
    remember = None

    def __init__(self, name, remember=1):
        self.remember = remember
        super().__init__(name)


    def select_action(self):
        most_common_next = self.most_common_next()
        if most_common_next is None:
            return random.choice(["rock", "paper", "scissors"])

        else:
            if most_common_next == 0:
                return "paper"
            elif most_common_next == 1:
                return "scissors"
            else:
                return "rock"

    def most_common_next(self):
        """
        looks at the last plays the opponent made, and checks if it has done it before
        and what the probable next play are
        :return:
        """
        pattern = self.opponents_previous[-self.remember:]
        counter = [0, 0, 0]
        for number in range(len(self.opponents_previous)-self.remember):
            for i in range(self.remember):
                if not self.opponents_previous[number+i] == pattern[i]:
                    break
                else:
                    if i == self.remember-1:
                        if self.opponents_previous[number+self.remember] == "rock":
                            counter[0] += 1
                        elif self.opponents_previous[number+self.remember] == "paper":
                            counter[1] += 1
                        else:
                            counter[2] += 1
        largest = 0
        largest_index = None
        for number in range(len(counter)):
            if counter[number] > largest:
                largest = counter[number]
                largest_index = number
        most_common_next = largest_index
        return most_common_next

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
