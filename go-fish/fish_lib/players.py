from random import choice


class BasePlayer(object):
    def __init__(self, hand: list, **kwargs):
        self.books = []
        self.hand = hand
        self.name = kwargs.get('name', repr(self))

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

    @property
    def playing(self):
        """
        Returns True if hand is not empty, otherwise returns False.
        :return: True if instance's hand is not empty otherwise returns false.
        """
        return bool(self.hand)

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

        Raises NotImplementedError if called.
        """
        raise NotImplementedError('This method should be replaced by subclasses.')

    def hear_confirm(self, *args, **kwargs):
        """
        This method is intended to be called as a result of another player's confirm_ask method.
        This simulates overhearing of others.

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
