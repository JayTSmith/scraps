from random import randint


class BasePlayer(object):

    def __init__(self, hand:list):
        self.hand = hand
        self.books = []

    def ask_for_card(self, *args, **kwargs):
        """
        This method is intended to be called when a player asks for a card.
        Raises NotImplementedError if called.
        """
        raise NotImplementedError('This method is replaced by subclasses.')

    def confirm_ask(self, *args, **kwargs):
        """
        This method is intended to be called when a player is asked for a card.
        Raises NotImplementedError if called.
        """
        raise NotImplementedError('This method is replaced by subclasses.')


class DumbPlayer(BasePlayer):

    def __init__(self, hand):
        super(DumbPlayer, self).__init__(hand)

    def ask_for_card(self):
        return randint(0, len(self.hand) - 1)[0]

    def confirm_ask(self, face):
        given_cards = []
        for i in (card for card in self.hand if card[0] == face):
            self.hand.remove(i)
            given_cards.append(i)
        return given_cards
