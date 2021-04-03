"""
This is the interface for the player classes
"""
class PlayerInterface:
    """
    This is the superclass for all the players, that define which functions they need to have
    """
    points = 0
    name = ""

    def __init__(self, name):
        self.name = name

    def select_action(self):
        """
        Desides what the player are chosing
        :return: "rock", "paper" or "scissors"
        """

    def receive_result(self, result):
        """
        returns the result of the last game to the player
        :param result:
        :return:
        """
