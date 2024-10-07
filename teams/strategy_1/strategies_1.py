import abc
import random
from typing import List

from CardGame import Card, Deck, Player


class PlayingStrategy(abc.ABC):
    @abc.abstractmethod
    def guess(self, player: Player, cards, round) -> List[int]:
        pass
    
    @abc.abstractmethod
    def play(self, player: Player, deck: Deck) -> int:
        pass


class DefaultPlayingStrategy(PlayingStrategy):
    def guess(self, player: Player, cards, round) -> List[int]:
        return random.sample(cards, 13 - round)

    def play(self, player: Player, deck: Deck) -> int:
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




# util / TODO: separate to own file

suit_offset = {"Hearts": 0, "Diamonds": 13, "Clubs": 26, "Spades": 39}
card_val = {
    "2": 0,
    "3": 1,
    "4": 2,
    "5": 3,
    "6": 4,
    "7": 5,
    "8": 6,
    "9": 7,
    "10": 8,
    "J": 9,
    "Q": 10,
    "K": 11,
    "A": 12,
}


def card_to_idx(card: Card) -> int:
    suit_offset = suit_offset[card.suit]
    card_val = card_val[card.value]
    return suit_offset + card_val