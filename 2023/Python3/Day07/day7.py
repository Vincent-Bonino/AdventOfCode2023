from enum import Enum
from typing import *


class Card(Enum):
    ACE =   "A"
    KING =  "K"
    QUEEN = "Q"
    TEN =   "T"
    NINE =  "9"
    EIGHT = "8"
    SEVEN = "7"
    SIX =   "6"
    FIVE =  "5"
    FOUR =  "4"
    THREE = "3"
    TWO =   "2"
    JOKER = "J"

    def get_value(self) -> int:
        return [
            "J",  # 0
            "2",  # 1
            "3",  # 2
            "4",  # 3
            "5",  # 4
            "6",  # 5
            "7",  # 6
            "8",  # 7
            "9",  # 8
            "T",  # 9
            "Q",  # 10
            "K",  # 11
            "A",  # 12
        ].index(self.value)

class Hand:
    """Mother class for all poker hands."""

    rank: int  # The higher the better
    pattern: List[int]

    raw_cards: List[Card]
    cards: List[Card]
    score: int
    bid: int

    UPGRADE_MAPPING: Dict[str, Dict[int, int]] = {}

    subclasses: Set[Type['Hand']] = set()

    def __init__(self, cards: List[Card], bid: int) -> None:
        self.raw_cards = cards
        self.cards = sorted(cards, key=lambda x: cards.count(x) * pow(2, 5) + x.get_value(), reverse=True)
        self.bid: int = bid

        # Handle Joker
        joker_nbr: int = cards.count(Card.JOKER)
        if joker_nbr != 0:
            self.rank = self.cast_rank(joker_nbr)

        self.score: int = 0
        for ind, crd in enumerate(reversed(cards)):
            self.score += crd.get_value() * pow(2, 4 * ind)
        self.score += self.rank * pow(2, 4 * (len(cards) + 1))

    def __init_subclass__(cls) -> None:
        Hand.subclasses.add(cls)

    def cast_rank(self, joker_nbr: int) -> int:
        return self.UPGRADE_MAPPING[type(self).__name__][joker_nbr]

    @classmethod
    def determine_hand(cls, hand: List[Card]) -> Type['Hand']:
        hand_pattern: List[int] = sorted((hand.count(crd) for crd in hand), reverse=True)
        # Find the correponding hand
        for subcls in cls.subclasses:
            if hand_pattern == subcls.pattern:
                return subcls
        raise ValueError(f"No hand found for {hand} (pattern={hand_pattern})")


class Five(Hand):
    """Five of a kind."""
    rank: int = 6
    pattern: List[int] = [5, 5, 5, 5, 5]


class Four(Hand):
    """Four of a kind."""
    rank: int = 5
    pattern: List[int] = [4, 4, 4, 4, 1]


class House(Hand):
    """Full house."""
    rank: int = 4
    pattern: List[int] = [3, 3, 3, 2, 2]


class Three(Hand):
    """Three of a kind."""
    rank: int = 3
    pattern: List[int] = [3, 3, 3, 1, 1]


class TwoPair(Hand):
    """Two pairs."""
    rank: int = 2
    pattern: List[int] = [2, 2, 2, 2, 1]


class OnePair(Hand):
    """One pair."""
    rank: int = 1
    pattern: List[int] = [2, 2, 1, 1, 1]


class HighCard(Hand):
    """High card."""
    rank: int = 0
    pattern: List[int] = [1, 1, 1, 1, 1]


Hand.UPGRADE_MAPPING.update(
    {
        'Five':     {5: Five.rank},
        'Four':     {1: Five.rank,  4: Five.rank},
        'House':    {2: Five.rank,  3: Five.rank},
        'Three':    {1: Four.rank,  3: Four.rank},
        'TwoPair':  {1: House.rank, 2: Four.rank},
        'OnePair':  {1: Three.rank, 2: Three.rank},
        'HighCard': {1: OnePair.rank},
    }
)


def part_two() -> int:
    all_hand: List[Hand] = []

    with open("input.txt", mode="r") as f_input:
        for line in f_input.readlines():
            cards, _, bid = line.strip().partition(" ")

            card_list: List[Card] = [Card(x) for x in cards]
            hand_type: Type[Hand] = Hand.determine_hand(card_list)

            hand: Hand = hand_type(card_list, int(bid))
            all_hand.append(hand)

    sorted_hands: List[Hand] = sorted(all_hand, key=lambda x: x.score)

    return sum((idx + 1) * hand.bid for idx, hand in enumerate(sorted_hands))

# To switch between parts one and two, I changed manually the cards order
# and added the hand upgrade code

# print("Part one:", part_one())
print("Part two:", part_two())
