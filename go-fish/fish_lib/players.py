from random import choice


class BasePlayer(object):
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
        for c in self.hand:
            result += 1 if c[0] == face else 0
        return result

    def ask_for_card(self, *args, **kwargs):
        """
        This method is intended to be called when a player asks for a card.

        Raises NotImplementedError if called.
        """
        raise NotImplementedError('This method should be replaced by subclasses.')

    def confirm_ask(self, *args, **kwargs):
        """
        This method is intended to be called when a player is asked for a card.

        Raises NotImplementedError if called.
        """
        raise NotImplementedError('This method should be replaced by subclasses.')

    def hear_ask(self, *args, **kwargs):
        """
        This method is intended to be called when a player asks another player for a card. This
        simulates overhearing of others.

        Keyword Arguments:
            a_player: The active player at the time of call.
            face: The face value of the requested card.
            r_player: The player that was asked for face.

        Raises NotImplementedError if called.
        """
        raise NotImplementedError('This method should be replaced by subclasses.')

    def hear_confirm(self, *args, **kwargs):
        """
        This method is intended to be called as a result of another player's confirm_ask method.
        This simulates overhearing of others.

        Keyword Arguments:
            a_player: The active player at the time of call.
            face: The face value of the requested card.
            r_player: The player that was asked for face.
            result: If r_player had any cards that had a face value equal to face.

        Raises NotImplementedError if called.
        """
        raise NotImplementedError('This method should be replaced by subclasses.')


class DumbPlayer(BasePlayer):
    def __init__(self, hand, **kwargs):
        super(DumbPlayer, self).__init__(hand, **kwargs)

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
        for i in (card for card in self.hand if card[0] == face):
            self.hand.remove(i)
            given_cards.append(i)
        return given_cards

    def hear_ask(self, *args, **kwargs):
        """
        This method does nothing. This is intended behavior.

        See BasePlayer.hear_ask for description.
        """
        pass

    def hear_confirm(self, *args, **kwargs):
        """
        This method does nothing. This is intended behavior.

        See BasePlayer.hear_confirm for description.
        """
        pass


class TryingPlayer(DumbPlayer):
    def __init__(self, hand, **kwargs):
        super(TryingPlayer, self).__init__(hand, **kwargs)
        self.seen = {}  # Data is stored as face value: player last seen with it.

    def ask_for_card(self, players: list):
        """
        This method is intended to be called when a player asks for a card.

        This method will attempt to locate other players that have possible combinations
        with this player's hand. If none are found, resort back to random guessing.
        :param players:
        :return:
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
        for i in (card for card in self.hand if card[0] == face):
            self.hand.remove(i)
            given_cards.append(i)
        return given_cards

    def hear_ask(self, *args, **kwargs):
        """
        This method will log whoever ask for a card as the latest owner of that face value.

        This sets the dictionary value of face equal to a_player.

        See BasePlayer.hear_ask for detailed description of arguments.
        """
        self.seen[kwargs.get('face')] = kwargs.get('a_player')

    def hear_confirm(self, *args, **kwargs):
        """
        This method will determine whether or not to clear the entry in seen for face.

        If result is true, then their entry will be clear from seen if they have the book.

        See BasePlayer.hear_confirm for detailed description of arguments.
        """

        if kwargs.get('result') and kwargs.get('a_player').count_copies(kwargs.get('face')) == 4:
            self.seen[kwargs.get('face')] = None
