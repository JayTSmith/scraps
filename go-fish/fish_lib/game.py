"""
This sets the framework for a game of GoFish.

Author: Justin Smith
Date: 1/23/18
"""
import itertools
from random import choice, randint

from . import players

RANKS = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace')
SUITS = ('Spades', 'Clubs', 'Hearts', 'Diamond')

BASE_DECK = tuple(itertools.product(RANKS, SUITS))

class GoFish(object):
    """
    This is the class that runs the game of Go Fish.

    Keyword Parameters:
        player_count: int
            The number of players to create to start the game.
            Bounds: 2 <= player_count <= 10
        player_types: Player
            The classes of players that we can create.
    """
    def __init__(self, player_count=2, player_types=(players.DumbPlayer, players.TryingPlayer)):
        if player_count > 10 or player_count < 2:
            raise ValueError('Player count is out of range! 2 <= player_count <= 10.')

        self.deck = list(BASE_DECK)
        self.shuffle_deck()

        self.active_player_idx = 0
        self.players = []

        card_count = 5 if player_count > 4 else 7
        for i in range(player_count):
            player_hand = self.deck[:card_count]
            player_type = choice(player_types)(player_hand, name=str(i + 1))

            self.players.append(player_type)
            self.deck = self.deck[card_count:]

    @staticmethod
    def card_to_string(card):
        """
        Prints a card tuple in a human-readable string.
        :param card: The card tuple in format (RANK, SUIT).
        :return: A string in how a person would say it.
        """
        return '{} of {}'.format(card[0], card[1])

    def check_player_for_book(self, player_idx):
        """
        Checks if a certain player has a book. If one is found,
        then it is removed from the player's hand and added to their book list.
        """
        player = self.players[player_idx]
        for book in filter(lambda f: player.count_copies(f) == 4, RANKS):
            for card in itertools.product((book,), SUITS):
                player.hand.remove(card)
            player.books.append(book)

    def check_all_players_for_books(self):
        """
        Checks every players' hand for a book (group of matching faces). If one is found,
        then it is removed from the player's hand and added to their book list.
        """
        _map = map(self.check_player_for_book, range(0, len(self.players)))
        while 1:
            try:
                next(_map)
            except StopIteration:
                break

    def do_turn(self):
        """
        Does the active player's turn and then rotates the index to the next player.
        """
        for player in filter(lambda p: not p.hand, self.players):
            player.playing = self.draw_card(player)

        valid_players = list(filter(lambda p: p.playing, self.players))

        # We pass the players in case the Player is keeping tracking of that.
        # requested face and requested player.
        active_player = valid_players[self.active_player_idx]
        r_face, r_player = active_player.ask_for_card(valid_players)

        print('Player {} asked for a {} from Player {}.'.format(active_player.name, r_face,
                                                                r_player.name))
        won_cards = r_player.confirm_ask(r_face)

        # Gotta inform the players who just asked for one.
        for idx, player in enumerate(self.players):
            if idx != self.active_player_idx and player != r_player:
                player.hear_ask(a_player=active_player, face=r_face, r_player=r_player)
                player.hear_confirm(a_player=active_player, result=bool(won_cards), face=r_face,
                                    r_player=r_player)

        if won_cards:
            print('Player {} gained {} {}(s) with {} in hand.'.format(active_player.name,
                                                                      len(won_cards),
                                                                      r_face,
                                                                      active_player.count_copies(r_face)))
            active_player.hand.extend(won_cards)
        else:  # If won cards is empty, then we 'go fish.'
            print('Player {} didn\'t have a {}.'.format(r_player.name, r_face))
            self.draw_card(active_player)

        # Increment the player index safely.
        self.active_player_idx = (self.active_player_idx + 1) % len(valid_players)

        # Check for books
        self.check_all_players_for_books()

    def do_full_round(self):
        """
        This method calls do_turn until done is True.

        This simulates an actual game of Go Fish.

        :return: the winning player obj
        """
        iterations = 0
        while not self.done and iterations < 100000:
            self.do_turn()
            iterations += 1

    @property
    def done(self):
        """
        Returns true if none of the players are playing and if deck list is empty.
        """
        return not ([player for player in self.players if player.playing] and self.deck)

    def draw_card(self, player, draw_amount=1):
        """
        Draws a specified number of cards to a player's hand.
        :param player: The player who is drawing card(s).
        :param draw_amount: The number of cards to draw.
        :return: True if the player was able to draw. Otherwise, returns False.
        """
        if len(self.deck) >= draw_amount:
            for i in range(draw_amount):
                player.hand.append(self.deck.pop(0))
                print('Player {} drew a {}.'.format(player.name,
                                                    player.hand[-1][0]))
            return True
        return False

    def shuffle_deck(self):
        """
        Quickly scrambles the order of the deck list.
        """
        for i in range(len(self.deck)):
            self.deck.insert(i, self.deck.pop(randint(0, len(self.deck) - 1)))

    @property
    def winner(self):
        """
        The winner(s) of the game.

        If the game is not done, this will return None. This can also return multiple players
        because of ties.

        :return: The player(s) objects that won.
        """
        if not self.done:
            return None

        best_score = max((len(play.books) for play in self.players))
        winners = []
        # Possible tie, so let's return everyone with the best score.
        for player in self.players:
            if len(player.books) == best_score:
                winners.append(player)

        return winners
