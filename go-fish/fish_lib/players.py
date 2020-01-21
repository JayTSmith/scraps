"""
The types of players that can be found in a game of Go Fish.

Author: Justin Smith
Date: 1/23/18
"""
from random import choice


class BasePlayer(object):
    """
    This class shows the method that every Player subclass should implement.
    """

    LIMIT = float('inf')

    def __init__(self, hand: list, **kwargs):
        self.books = []
        self.hand = hand
        self.name = kwargs.get('name', repr(self))
        self.playing = True

    def count_copies(self, face):
        """
        Counts how many copies we have of a certain face card.
        :param face: A face value of a card.
        :return: the number of copies.
        """
        result = 0
        for card in self.hand:
            result += 1 if card[0] == face else 0
        return result

    def ask_for_card(self, players: list):
        """
        This method is intended to be called when a player asks for a card.

        Raises NotImplementedError if called.
        """
        raise NotImplementedError('This method should be replaced by subclasses.')

    def confirm_ask(self, face):
        """
        This method is intended to be called when a player is asked for a card.

        Raises NotImplementedError if called.
        """
        raise NotImplementedError('This method should be replaced by subclasses.')

    def hear_ask(self, a_player, face, r_player):
        """
        This method is intended to be called when a player asks another player for a card. This
        simulates overhearing of others.

        Arguments:
            a_player:
                The active player at the time of call.
            face:
                The face value of the requested card.
            r_player:
                The player that was asked for face.

        Raises NotImplementedError if called.
        """
        raise NotImplementedError('This method should be replaced by subclasses.')

    def hear_confirm(self, a_player, face, r_player, result):
        """
        This method is intended to be called as a result of another player's confirm_ask method.
        This simulates overhearing of others.

        Arguments:
            a_player:
                The active player at the time of call.
            face:
                The face value of the requested card.
            r_player:
                The player that was asked for face.
            result:
                If r_player had any cards that had a face value equal to face.

        Raises NotImplementedError if called.
        """
        raise NotImplementedError('This method should be replaced by subclasses.')


class DumbPlayer(BasePlayer):
    """
    This type of player will use no strategy to play the game. It just makes
    calls and follows the rules.
    """

    def ask_for_card(self, players: list):
        """
        This method is intended to be called when a player asks for a card.

        There is no strategy here: throws out a random card to a random player.

        Parameters:
            players:
                A list of players in the same game with him.

        :return: A tuple with 2 elements, a face value and the player to request the card from.
        """
        return choice(self.hand)[0], choice([x for x in players if x != self])

    def confirm_ask(self, face):
        """
        This method is intended to be called when a player is asked for a card.

        This method will hand over all of the cards as asked.

        Parameters:
            face:
                The requested face value.

        :return: All of the cards that have the same face value.
        """
        given_cards = []
        for i in list(filter(lambda c: c[0] == face, self.hand)):
            self.hand.remove(i)
            given_cards.append(i)
        return given_cards

    def hear_ask(self, a_player, face, r_player):
        """
        This method does nothing. This is intended behavior.

        See BasePlayer.hear_ask for description.
        """
        pass

    def hear_confirm(self, a_player, face, r_player, result):
        """
        This method does nothing. This is intended behavior.

        See BasePlayer.hear_confirm for description.
        """
        pass


class TryingPlayer(DumbPlayer):
    """
    This player will track who made what calls for cards. If they've heard a
    call for a card they need, they mark the player who made it as a target.
    Also, this player follows the rules of the game.
    """
    def __init__(self, hand, **kwargs):
        super(TryingPlayer, self).__init__(hand, **kwargs)
        self.seen = {}  # Data is stored as face value: player last seen with it.

    def ask_for_card(self, players: list):
        """
        This method is intended to be called when a player asks for a card.

        This method will attempt to locate other players that have possible combinations
        with this player's hand. If none are found, resort back to random guessing.
        Parameters:
            players:
                A list of valid players to choose from. Please note, self is more than
                likely included.
        :return: A tuple with 2 elements, a face value and the player to request the card from.
        """
        # Find out which targets have cards that we've seen before.
        poss_targets = set(self.seen.keys()).intersection((card[0] for card in self.hand))

        # Also find out if they are still in the game.
        poss_targets = list(filter(lambda f: self.seen.get(f) in players, poss_targets))

        # If the targets have cards that we have, let's try to go for them.
        if poss_targets:
            selected_face = choice(poss_targets)
            selected_player = self.seen.pop(selected_face)
            return selected_face, selected_player

        # If we can't make a informed play, make a unpredictable play.
        return super().ask_for_card(players)

    def hear_ask(self, a_player, face, r_player):
        """
        This method will log whoever ask for a card as the latest owner of that face value.

        This sets the dictionary value of face equal to a_player.

        See BasePlayer.hear_ask for detailed description of arguments.
        """
        self.seen[face] = a_player

    def hear_confirm(self, a_player, face, r_player, result):
        """
        This method will determine whether or not to clear the entry in seen for face.

        If result is true, then their entry will be clear from seen if they have the book.

        See BasePlayer.hear_confirm for detailed description of arguments.
        """

        if result and a_player.count_copies(face) == 4:
            self.seen[face] = None


class StingyPlayer(DumbPlayer):
    """
    This player will lie about having cards in order to hold on to them. (aka be stingy.)
    They will deny having the same face up to 2 times in the same game before giving up.
    Games should limit themselves to one StringyPlayer in case of deadlock.
    """

    LIMIT = 1

    def __init__(self, hand, limit=2, **kwargs):
        super(StingyPlayer, self).__init__(hand, **kwargs)
        self.deny_limit = limit
        self.denied = {}

    def confirm_ask(self, face):
        """
        Returns nothing if they haven't denied it twice already.

        The player will have to deny the face while they have it to count as a denial.
        Once the player goes over their limit for denials, they will hand over the card(s)
        for the rest of the game.

        Parameters:
            face:
                The requested face value.

        :return: An empty list or a list of the cards requested.
        """
        if self.count_copies(face) and self.denied.get(face, 0) < self.deny_limit:
            self.denied[face] = self.denied.get(face, 0) + 1
            return []
        return super().confirm_ask(face)


class UserPlayer(DumbPlayer):
    """
    This player will be controlled by the user.
    There will be prompts and the user will have to type in the input in order to react.
    """

    LIMIT = 1

    def ask_for_card(self, players: list):
        """
        Allows the user to ask any valid player for a card.

        Valid players are players that still playing and that are not the user themselves.
        The user can type the letter 'h' at any prompt to display the options again.

        Parameters:
            players:
                A list of valid players to choose from. Please note, self is more than
                likely included.
        :return: A tuple with 2 elements, a face value and the player to request the card from.
        """
        # Let's get the faces in the hand.
        faces = {}

        for card in self.hand:
            faces[card[0]] = self.count_copies(card[0])

        def print_info():
            for idx, player in enumerate(players):
                print('{0}) Player {1}'.format(idx, player.name))
            face_str_args = ('{1} {0}\'s'.format(*item) for item in faces.items())
            print('Your hand: {}'.format(', '.join(face_str_args)))

        players = [player for player in players if player != self]
        print_info()

        player_index = len(players)
        while player_index >= len(players):
            try:
                player_index = int(input('What player would you like to ask for a card? '))
            except ValueError:
                if player_index == 'h':
                    print_info()
                else:
                    print('That wasn\'t a number.')

        r_card = None
        while r_card not in faces:
            if r_card == 'h':
                print_info()
            elif r_card is not None:
                print('That card is not in your hand!')
            r_card = input('What card would you like to ask for? ')

        return r_card, players[player_index]

    def confirm_ask(self, face):
        """
        This method is called when the player is asked for a card.

        The user can either confirm or deny if they have the requested face value.
        If they do not or they deny it, returns an empty list.
        If they give up their cards, it returns a list of cards with a matching face value.

        Parameters:
            face:
                The requested face value.

        :return: An empty list or a list of the cards requested.
        """
        print('You were asked for a {}.'.format(face))
        posess = self.count_copies(face)
        print('You have {}.'.format(posess))

        if posess:
            if input('Do you give up your cards? [Y/n] ').lower().strip() == 'n':
                print('You denied that you have a {}.'.format(face))
                return []
            else:
                print('You gave up your {} {}(s).'.format(posess, face))
                return super().confirm_ask(face)
