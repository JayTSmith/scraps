import itertools

from random import choice
from . import players


RANKS = (None, 2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace')
SUITS = ('Spades', 'Clubs', 'Hearts', 'Diamond')

BASE_DECK = tuple(itertools.product(RANKS[1:], SUITS))


class GoFish(object):

    def __init__(self, player_count=2, player_types=(players.DumbPlayer, )):
        if player_count > 8 or player_count < 2:
            raise ValueError('Player count is out of range! 2 <= player_count <= 8.')

        self.players = []
        player_count = player_count
        valid_types = player_types

        card_count = 5 if player_count > 4 else 7
        for i in range(player_count):
            player_hand = list(BASE_DECK[card_count * i:card_count * (i + 1)])
            player = choice(valid_types)(player_hand)
            self.players.append(player)