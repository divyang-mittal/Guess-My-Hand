import abc
import random
from typing import List

from CardGame import Deck, Player

remaining_cards = {}

def initialize_totals(deck):
    for card in deck.copyCards:
        remaining_cards[card] = 0

def remove_seen(exposed_cards):
    for player in exposed_cards:
        remove_card(exposed_cards[player])

def remove_card(hand):
    for card in hand:
        remaining_cards[card] = -1

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



def playing(player, deck):
    if not deck:
        initialize_totals(deck)
    
    remove_card(player.hand)

    remove_seen(player.exposed_cards)

    return DefaultPlayingStrategy().play(player, deck)


def guessing(player, cards, round):
    return DefaultPlayingStrategy().guess(player, cards, round)

