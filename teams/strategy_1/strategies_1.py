import abc
import random
from typing import List

from CardGame import Deck, Player

class Strategy:
    def __init__(self):
        # Initialize the remaining_cards dictionary as an empty dictionary
        self.remaining_cards = {}

    def initialize_totals(self, deck):
        """
        Initializes the remaining_cards dictionary with all cards in the deck,
        setting their initial probability value to 0.
        """
        for card in deck.copyCards:
            self.remaining_cards[card] = 0

    def remove_seen(self, exposed_cards):
        """
        Removes all seen cards from the remaining_cards by setting their
        value to -1 for each exposed card.
        """
        for player in exposed_cards:
            self.remove_card(exposed_cards[player])

    def remove_card(self, hand):
        """
        Removes cards from the remaining_cards by setting their value to -1.
        """
        for card in hand:
            self.remaining_cards[card] = -1

    def update_probabilities(self, player):
        """
        Updates the remaining_cards dictionary with probabilities based on the last
        guess and cVals. The probability for each card is calculated as the last value
        of cVals divided by the number of guesses in the last round.
        """

        if not player.cVals or not player.guesses:
            return

        # Calculate the probability
        probability = player.cVals[-1] / len(player.guesses[-1])

        # Update the remaining_cards with the probability
        for guess in player.guesses[-1]:
            if guess in self.remaining_cards and self.remaining_cards[guess] != -1:
                self.remaining_cards[guess] = probability

        # for card, prob in self.remaining_cards.items():
        #     print(f"Card: {card}, Probability: {prob}")


class PlayingStrategy(abc.ABC):
    @abc.abstractmethod
    def guess(self, player: Player, cards, round) -> List[int]:
        pass
    
    @abc.abstractmethod
    def play(self, player: Player, deck: Deck) -> int:
        pass


class DefaultPlayingStrategy(PlayingStrategy):
    def __init__(self):
        # Initialize an instance of Strategy class
        self.strategy = Strategy()

    def guess(self, player: Player, cards, round) -> List[int]:
        """
        Return the top (13 - round) cards from the remaining_cards dictionary,
        based on the highest probability values.
        """
        if not self.strategy.remaining_cards:
            return random.sample(cards, 13 - round)  # Fallback to random if no remaining cards

        # Sort remaining_cards by value (probabilities) in descending order
        sorted_cards = sorted(self.strategy.remaining_cards.items(), key=lambda x: x[1], reverse=True)

        # Get the top (13 - round) cards
        top_cards = [card for card, prob in sorted_cards[:13 - round]]

        return top_cards

    def play(self, player: Player, deck: Deck) -> int:
        # Ensure remaining_cards are initialized when needed
        if not self.strategy.remaining_cards:
            self.strategy.initialize_totals(deck)

        # Remove played and seen cards
        self.strategy.remove_card(player.hand)
        self.strategy.remove_seen(player.exposed_cards)

        # Update the probabilities
        self.strategy.update_probabilities(player)

        if not player.hand:
            return None

        # Find the card with the highest value and suit
        value_order = deck.values
        max_index = 0
        max_value = -1

        for i, card in enumerate(player.hand):
            value = value_order.index(card.value)
            if value > max_value:
                max_value = value
                max_index = i
        return max_index

def playing(player, deck):
    return DefaultPlayingStrategy().play(player, deck)

def guessing(player, cards, round):
    return DefaultPlayingStrategy().guess(player, cards, round)
