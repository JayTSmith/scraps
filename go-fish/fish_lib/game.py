import itertools
from random import choice, randint

from . import players

RANKS = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace')
SUITS = ('Spades', 'Clubs', 'Hearts', 'Diamond')

BASE_DECK = tuple(itertools.product(RANKS, SUITS))

class GoFish(object):

    def __init__(self, player_count=2, player_types=(players.DumbPlayer, )):
        if player_count > 8 or player_count < 2:
            raise ValueError('Player count is out of range! 2 <= player_count <= 8.')

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
        return '{} of {}'.format(card[0], card[1])

    def check_player_for_book(self, player_idx):
        """
        Checks if a certain player has a book. If one is found,
        then it is removed from the player's hand and added to their book list.
        """
        player = self.players[player_idx]
        for book in filter(lambda f: player.count_copies(f) == 4, RANKS):
            for c in itertools.product((book,), SUITS):
                player.hand.remove(c)
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
        valid_players = [play for play in self.players if play.playing]
        if len(valid_players) == 1:  # If only one player is left, they get all of the cards left in the deck.
            valid_players[0].hand.extend(self.deck)
            self.deck.clear()

            self.check_player_for_book(self.players.index(valid_players[0]))
            return

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
                player.hear_ask(r_face, r_player)
                player.hear_confirm(bool(won_cards), r_face, r_player)

        if won_cards:
            print('Player {} gained {} {}(s) with {} in hand.'.format(active_player.name, len(won_cards),
                                                                      r_face,
                                                                      active_player.count_copies(r_face)))
            active_player.hand.extend(won_cards)
        else:  # If won cards is empty, then we 'go fish.'
            print('Player {} didn\'t have a {}.'.format(r_player.name, r_face))
            if self.deck:
                active_player.hand.append(self.deck.pop(0))
                print('Player {} drew a {}.'.format(active_player.name,
                                                    active_player.hand[-1][0]))  # Face value of this.

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

    def shuffle_deck(self):
        """
        Quickly scrambles the order of the deck list.
        """
        for i in range(len(self.deck)):
            self.deck.insert(i, self.deck.pop(randint(0, len(self.deck) - 1)))

    @property
    def winner(self):
        if not self.done:
            return None

        best_score = max((len(play.books) for play in self.players))
        winners = []
        # Possible tie, so let's return everyone with the best score.
        for player in self.players:
            if len(player.books) == best_score:
                winners.append(player)

        return winners
