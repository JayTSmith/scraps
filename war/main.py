"""
This module allows the computer to play War with itself.
Author: Justin Smith
"""

import itertools

from random import randint

WIN_ORDER = (None, 2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace')
SUITS = ('Spades', 'Clubs', 'Hearts', 'Diamond')

BASE_DECK = tuple(itertools.product(WIN_ORDER[1:], SUITS))


def shuffle(a_list: list, times: int = 1):
    """
    Scrambles a list's elements.

    This method actually makes n moves. (n = amount of elements in the a_list)

    :param a_list: The list to scramble.
    :param times: The amount of times to scramble.
    :return: Returns the supplied list.
    """
    length = len(a_list)
    for i in range(times):
        for j in range(length):
            a_list.append(a_list.pop(randint(0, length - 1)))
    return a_list


class Player:
    """
    A modal class for holding player data.
    Properties:
        deck: A list of tuples that contain value and suit.
        lost: A boolean that says if the player has lost their game.
        win_pile: A list of "cards" that has been won by the player.
        total_cards: An int of how many cards are in the player's
                     win_pile and deck.

    Methods:
        add_win_to_deck
            Moves the cards from win_pile to deck. Optionally, shuffles
            the win_pile before adding it.
        play
            Gets the next card that the player will play. This will not
            return the same card twice so store the result after calling.
            Can get multiple cards.

    """

    def __init__(self, deck: list):
        self.deck = deck
        self.lost = False
        self.win_pile = []

    def add_win_to_deck(self, shuf: bool = True):
        """
        Adds the player's win_pile to their deck and then clears the
        win_pile.

        :param shuf: A boolean that tells whether to shuffle the win_pile
        before adding to the end of deck.
        :return: Nothing
        """
        if shuf:
            shuffle(self.win_pile)
        self.deck.extend(self.win_pile)
        self.win_pile.clear()

    def play(self, cards: int = None):
        """
        This retrieves the next cards to be played by popping them from
         the player's deck.

        Warning: store the result because if the result is not stored,
         it will be lost.
        :param cards: The number of cards to get.
        :return: A list of cards that the player will use.
        """
        result = self.deck[:cards or 1]
        self.deck = self.deck[cards or 1:]
        return result

    @property
    def total_cards(self):
        """
        A property method that returns the total count of a player's cards.
        :return: Returns the length of a player's deck and their win pile.
        """
        return len(self.deck) + len(self.win_pile)


class Game:
    """
    This class moderates and facilitates playing of the War game.
    This builds the players and the deck that is used in the game.

    Properties:
        deck: The deck that is used throughout the game. Immutable.
        players: Every player that is in this game. Called in many methods.
        pot: Every players' card contribution for the round.

    Methods:
        award_pot: Awards every players' pot to a single player.
        check_players_decks: Makes sure every player's deck count is above
         a certain number.
        count_player_cards: Quickly counts every players' cards and returns that.
        get_card_value: A helper method to get a card's winning value.
        get_pot_value: A helper method to get the value of the last card in
         each players' pot.
        war: A method that does the tiebreaker between specified players.
        step: Steps through a single turn of War.
        play_game: Loops the game until a winner has occurred or it reaches the
         time limit.

    """

    def __init__(self, player_count: int = 2, deck_count: int = 1):
        if (52 * deck_count) % player_count != 0:
            raise ValueError('Unable to split cards evenly between players!')
        cards = (52 * deck_count) // player_count
        self.deck = tuple(shuffle(list(BASE_DECK * deck_count)))
        self.players = []
        self.pot = tuple(([] for i in range(player_count)))

        print('Each player has {} cards in their decks.'.format(cards))
        for i in range(player_count):
            start = i * cards
            end = (i + 1) * cards
            self.players.append(Player(list(self.deck[start:end])))

    def award_pot(self, player_index: int):
        """
        Gives every players' pot to one player.
        :param player_index: The index of the player to award the spoils to.
        :return: Nothing.
        """
        for i, winnings in enumerate(self.pot):
            self.players[player_index].win_pile.extend((x for x in winnings if x[0] is not None))
            self.pot[i].clear()

    def check_players_decks(self, desired_count: int = None):
        """
        Makes sure that every player has the desired_count of cards in their decks.
        If they don't have the right amount of cards, calls their add_win_to_deck.
        :param desired_count: The desired amount of cards of every player.
        :return: Nothing
        """
        for i, player in enumerate(self.players):
            print('Player {} has {} cards in their deck.'.format(i + 1, len(player.deck)))
            if len(player.deck) < (desired_count or 4):
                print('Player {} added {} cards in to their deck.'.format(i + 1, len(player.deck)))
                player.add_win_to_deck(shuf=True)

    def count_player_cards(self):
        """
        A helper method that gets all of the players' card count.
        :return: A list of the players' card count.
        """
        return [player.total_cards for player in self.players]

    @staticmethod
    def get_card_value(card):
        """
        A helper method for getting the priority of the card.
        :param card: A tuple containing value and suit.
        :return: The int that dedicates the winning power.
        """
        return WIN_ORDER.index(card[0])

    def get_pot_value(self, players: list = None):
        """
        Gathers the value of the players' pot.
        :param players: A list of indices of players' pot. If None: defaults to all the players.
        :return: A list of the pot's values.
        """
        if players:
            pot_value = []
            for player in players:
                pot_value.append(self.get_card_value(self.pot[player][-1]))
            return pot_value

        return list(map(self.get_card_value, (player_pot[-1] for player_pot in self.pot)))

    # Game Methods

    def war(self, players: list):
        """
        This method is called in order to break a tie between players.
        :param players: The indices of the players involved
        :return: The index of the player that won; if another tie occurred, returns -1
        """
        self.check_players_decks()

        for player in players:
            played_cards = self.players[player].play(cards=4)
            self.pot[player].extend(played_cards)

        pot_value = self.get_pot_value(players)
        best_card = max(pot_value)
        if pot_value.count(best_card) > 1:
            return -1
        return pot_value.index(best_card)

    def step(self):
        """
        Runs one turn of the War Game.
        :return: Nothing
        """
        for index, player in enumerate(self.players):
            if not player.lost:
                active_card = player.play(cards=1)[0]
                print('Player {} played a {} of {}.'.format(index + 1, *active_card))
                self.pot[index].append(active_card)
            else:
                print('Player {} couldn\'t play anything!'.format(index + 1))
                self.pot[index].append([None])

        pot_values = self.get_pot_value()
        best_card = max(pot_values)

        if pot_values.count(best_card) > 1:
            # Builds and adds the participants of the war.
            war_party = []
            for i, val in enumerate(pot_values):
                if val == best_card:
                    war_party.append(i)

            war_count = 1
            war_result = self.war(war_party)

            while war_result < 0:
                # Get the pot values of the war.
                pot_values = self.get_pot_value(war_party)
                best_card = max(pot_values)

                # Builds and adds the participants of the war.
                war_party = []
                for i, val in enumerate(pot_values):
                    if val == best_card:
                        war_party.append(i)

                war_result = self.war(war_party)

                war_count += 1

            print('A war broke out ({} time(s)) and Player {} was the victor!'.format(war_count,
                                                                                      war_result + 1))
            self.award_pot(war_result)
        else:
            winner = pot_values.index(best_card)
            print('Player {} has won this turn without contest!'.format(winner + 1))
            self.award_pot(winner)

        self.check_players_decks(desired_count=1)
        for player in self.players:
            if not player.deck:
                player.lost = True

    def play_game(self):
        """
        Plays the game until a winner is declared or 1000 turns for every deck have passed.
        :return: Nothing
        """
        iterations = 0
        active_players = [player for player in self.players if not player.lost]
        while len(active_players) != 1 and iterations < (1000 * len(self.deck) / 52):
            # Active code sections
            self.step()

            # Increment sections
            active_players = [player for player in self.players if not player.lost]
            iterations += 1

        if iterations >= 1000:
            print('The game timed out!')
            return
        print('After {} turns, Player {} has won the game!'.format(iterations + 1,
                                                                   self.players.index(active_players[0]) + 1))


class GameFactory:
    """
    A class for quickly building games. It will be able to supply default
    parameters for rapid testing.

    Properties:
        player_count: the int supplied to Game's constructor for player_count
        deck_count: the int supplied to Game's constructor for deck_count

    Methods:
        create_game:
            Returns a new instance of Game with the supplied arguments.
    """

    def __init__(self, player_count: int = None, deck_count: int = None):
        self.player_count = player_count or 2
        self.deck_count = deck_count or 1

    def create_game(self, player_count=None, deck_count=None):
        """
        Quickly builds a new instance of Game with supplied arguments.

        :param player_count: Overrides the class' parameter
        :param deck_count: Overrides the class' parameter
        :return: A new instance of Game pre-configured.
        """
        return Game(player_count=player_count or self.player_count,
                    deck_count=deck_count or self.deck_count)


def quick_test():
    """
    Testing method should be removed afterwards
    :return: An object with properties.
    """
    obj = dict()

    obj['fact'] = GameFactory()
    obj['classic'] = obj['fact'].create_game()
    obj['free'] = obj['fact'].create_game(player_count=4)

    return obj
