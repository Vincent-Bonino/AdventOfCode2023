from collections import defaultdict
from typing import *


def part_one() -> int:
    result: int = 0

    with open("input.txt", mode="r") as f_input:
        for line in f_input.readlines():
            _game, _separator, values = line.strip().partition(":")
            winning_numbers_str, _separator, my_numbers_str = values.partition("|")

            # From string to int
            winning_numbers: Set[int] = {int(x) for x in winning_numbers_str.strip().split(" ") if x != ""}
            my_numbers: Set[int] = {[int(x) for x in my_numbers_str.strip().split(" ") if x != ""]}

            # Find all common numbers
            common_numbers = winning_numbers.intersection(my_numbers)
            if common_numbers:
                result += pow(2, len(common_numbers) - 1)

    return result


def part_two() -> int:
    card_number: DefaultDict[int, int] = defaultdict(lambda : 1)

    with open("input.txt", mode="r") as f_input:
        for index, line in enumerate(f_input.readlines()):
            _game, _separator, values = line.strip().partition(":")
            winning_numbers_str, _separator, my_numbers_str = values.partition("|")

            # Init line count if one
            card_number[index]  # pylint: disable=pointless-statement

            # From string to int
            winning_numbers = {int(x) for x in winning_numbers_str.split(" ") if x != ""}
            my_numbers = {int(x) for x in my_numbers_str.split(" ") if x != ""}

            # Find all common numbers
            common_numbers = winning_numbers.intersection(my_numbers)

            for ind in range(len(common_numbers)):
                card_number[index + ind + 1] += card_number[index]

    return sum(card_number.values())


print("Part one:", part_one())
print("Part two:", part_two())
