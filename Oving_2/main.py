"""
The main file for organising of tournament and games of rock, paper, scissors
"""
# pylint: disable=E1101
import matplotlib.pyplot as plt

import historian_player
import player_interface
import sequential_player
import random_player
import most_common_player


class Result:
    """
    Saves the all relevant info for the outcome of a game
    """
    winner = None
    player_1 = player_interface
    player_2 = player_interface
    p1_choice = ""
    p2_choice = ""


class SingleGame:
    """
    Adds support to have to players play agains each other
    """
    result = Result
    player_1 = player_interface
    player_2 = player_interface

    def __init__(self, player_1, player_2):
        self.player_1 = player_1
        self.player_2 = player_2

    def perform_game(self):
        """
        Perform and calculate who wins a game
        """
        self.result.player_1 = self.player_1
        self.result.player_2 = self.player_2
        self.result.p1_choice = self.player_1.select_action()
        self.result.p2_choice = self.player_2.select_action()
        if (self.result.p1_choice == "paper" and self.result.p2_choice == "rock") \
                or (self.result.p1_choice == "rock" and self.result.p2_choice == "scissors") \
                or (self.result.p1_choice == "scissors" and self.result.p2_choice == "paper"):
            self.result.winner = self.player_1
        elif self.result.p1_choice == self.result.p2_choice:
            self.result.winner = None
        else:
            self.result.winner = self.player_2
        self.player_1.receive_result(self.result)
        self.player_2.receive_result(self.result)

    def show_results(self):
        """
        print the results of a game to the terminal
        """
        if self.result.winner is not None:
            print(
                f'{self.result.player_1.name} chose '
                f'{self.result.p1_choice} and {self.result.player_2.name} chose '
                f'{self.result.p2_choice} resulting in {self.result.winner.name} winning the game')
        else:
            print(
                f'{self.result.player_1.name} chose '
                f'{self.result.p1_choice} and {self.result.player_2.name} chose '
                f'{self.result.p2_choice} resulting in a draw')


class Tournament:
    """
    Adds support to make a tournament, to see how players do against each other over several games
    """
    player_1 = player_interface
    player_2 = player_interface
    number_of_games = None

    def __init__(self, player_1, player_2, number_of_games):
        self.player_1 = player_1
        self.player_2 = player_2
        self.number_of_games = number_of_games

    def arrange_singlegame(self):
        """
        arranges every single game
        """
        singlegame = SingleGame(self.player_1, self.player_2)
        singlegame.perform_game()
        singlegame.show_results()

    def arrange_tournament(self):
        """
        arranges all the games after each other and graphs the results
        """
        plotting_array = []
        for number in range(1, self.number_of_games + 1):
            self.arrange_singlegame()
            plotting_array.append(self.player_1.points / number)
        plt.plot(range(1, self.number_of_games + 1), plotting_array,)
        plt.ylim(0,1)
        plt.show()


class TextInterface:
    """
    Implements the text interface for the user to set up the games and tournaments
    """
    players_name = ["most_common", "historian", "sequential", "random_player"]
    most_common = most_common_player.MostCommonPlayer("MostCommon")
    historian = historian_player.HistorianPlayer("Historian", 2)
    sequential = sequential_player.SequentialPlayer("Sequential")
    random_player = random_player.RandomPlayer("Random")
    players = [most_common, historian, sequential, random_player]

    def __main__(self):
        print("Welcome to the rock, paper, scissor app")
        type_of_game = input(
            "Do you wish to make a tournament or just a single game? (tournament/singlegame): ")
        while type_of_game not in ["tournament", "singlegame"]:
            print("Wrong input, try again")
            type_of_game = input(
                "Do you wish to make a tournament or just a single game? (tournament/singlegame): ")
        if type_of_game == "tournament":
            player_1_name = input(
                "Who should be player_1? (most_common/historian/sequential/random_player): ")
            player_2_name = input(
                "And who should be player_2? (most_common/historian/sequential/random_player): ")
            while player_1_name not in self.players_name or player_2_name not in self.players_name:
                print("Wrong input, try again")
                player_1_name = input(
                    "Who should be player_1? (most_common/historian/sequential/random_player): ")
                player_2_name = input(
                    "And who should be player_2? "
                    "(most_common/historian/sequential/random_player): ")
            number_of_rounds = int(
                input("How many rounds should the players play? (any positive integer): "))
            while not isinstance(number_of_rounds, int):
                print("Wrong input, try again, remember to write in an integer")
                number_of_rounds = input(
                    "How many rounds should the players play? (any positive integer)")
            player_1 = self.players[self.players_name.index(player_1_name)]
            player_2 = self.players[self.players_name.index(player_2_name)]
            tournament = Tournament(player_1, player_2, number_of_rounds)
            tournament.arrange_tournament()
        else:
            player_1_name = input(
                "Who should be player_1? (most_common/historian/sequential/random_player): ")
            player_2_name = input(
                "And who should be player_2? (most_common/historian/sequential/random_player): ")
            while player_1_name not in self.players_name or player_2_name not in self.players_name:
                print("Wrong input, try again")
                player_1_name = input(
                    "Who should be player_1? (most_common/historian/sequential/random_player): ")
                player_2_name = input(
                    "And who should be player_2? "
                    "(most_common/historian/sequential/random_player): ")
            player_1 = self.players[self.players_name.index(player_1_name)]
            player_2 = self.players[self.players_name.index(player_2_name)]
            singlegame = SingleGame(player_1, player_2)
            singlegame.perform_game()
            singlegame.show_results()


if __name__ == '__main__':
    TextInterface().__main__()
