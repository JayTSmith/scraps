from random import choice


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

    def ask_for_card(self, players: list):
        """
        This method is intended to be called when a player asks for a card.

        There is no strategy here: throws out a random card to a random player.

        Parameters:
            players:
                A list of players in the same game with him.

        :return: A tuple with 2 elements, a face value and the player to request the card from.
        """
        return choice(self.hand)[0], choice(players)

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
