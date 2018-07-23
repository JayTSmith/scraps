from io import StringIO
from random import choice
import sys

from . import players
from . import game


class GoFishFactory:
    """
    This builds instances of GoFish to make it easier to program tests.
    """

    @staticmethod
    def build_basic_game(player_count=2, player_types=(players.DumbPlayer,
                                                       players.StingyPlayer,
                                                       players.TryingPlayer)):
        """
        Builds a normal game of GoFish with all of the safe checking.

        Keyword Parameters:
            player_count: int
                The number of players to create to start the game.
                Bounds: 2 <= player_count <= 10
            player_types: Player
                The classes of players that we can create.

        :return: An instance of game.BasicGoFish
        """
        if player_count > 10 or player_count < 2:
            raise ValueError('Player count is out of range! 2 <= player_count <= 10.')

        if sum(x.LIMIT for x in player_types) < player_count:
            raise ValueError('Player types has too many limited types!')

        b_players = []
        player_type_count = {}
        for i in range(player_count):
            player_type = choice([cls for cls in player_types
                                  if player_type_count.get(cls, 0) < cls.LIMIT])
            player_type_count[player_type] = player_type_count.get(player_type, 0) + 1
            b_players.append(player_type(None, name=str(i + 1)))
        return game.BasicGoFish(b_players)

    @staticmethod
    def run_silent_game(**kwargs):
        """
        Suppresses all of the print statements made by game.BasicGoFish during a call of
        do_full_round.

        Made for testing purposes because I'm getting annoyed at scrolling.
        :return: An instance of game.BasicGoFish
        """
        b_game = GoFishFactory.build_basic_game(**kwargs)

        real_out = sys.stdout
        sys.stdout = StringIO()

        b_game.do_full_round()

        sys.stdout = real_out
        return b_game
