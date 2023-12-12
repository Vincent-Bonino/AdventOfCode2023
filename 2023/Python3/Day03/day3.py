from collections import defaultdict
from typing import DefaultDict, List, Optional, Pattern, Tuple
import re

DIGITS_REGEX: Pattern[str] = re.compile("[0-9]+")
SYMBOL_REGEX: Pattern[str] = re.compile("[^0-9.]")


class Schematic:

    lines: List[str]
    max_row: int
    max_col: int

    def __init__(self, lines: List[str]) -> None:
        self.lines = [line.strip() for line in lines]
        self.max_row = len(self.lines)
        self.max_col = len(self.lines[0])

    def get_symbols_coordinates(self) -> List[Tuple[int, int]]:
        results: List[Tuple[int, int]] = []
        for row in range(self.max_row):
            for col in range(self.max_col):
                val = self.get_char(row, col)

                if val is None:
                    continue

                if SYMBOL_REGEX.fullmatch(val):
                    results.append((row, col))

        return results

    def get_adjacent_coordinates(self, row: int, col: int) -> List[Tuple[int, int]]:
        full_list: List[Tuple[int, int]] = [
            (row-1, col-1), # Upper left
            (row-1, col),   # Upper
            (row-1, col+1), # Upper right
            (row, col-1),   # Left
            (row, col+1),   # Right
            (row+1, col-1), # Lower left
            (row+1, col),   # Lower
            (row+1, col+1), # Lower
        ]
        return [coord for coord in full_list if self.get_char(*coord) is not None]

    def get_char(self, row: int, col: int) -> Optional[str]:
        if not (0 <= row < self.max_row) or not (0 <= col < self.max_col):  # pylint: disable=superfluous-parens
            return None
        return self.lines[row][col]


# Execution

schematic: Schematic

with open("../input.txt", mode='r') as f_input:
    schematic = Schematic(f_input.readlines())


def part_one(schematic: Schematic) -> int:
    result: int = 0

    for symb_x, symb_y in schematic.get_symbols_coordinates():

        # Dict of all found numbers y-position range, to prevent adding multiple times the same value
        # Ex:
        # .123.  # 123 is 3 times next to the gear but should be added only once
        # ..*..
        # .....
        added_ranges: DefaultDict[int, List[Tuple[int, int]]] = defaultdict(list)

        for adj_x, adj_y in schematic.get_adjacent_coordinates(symb_x, symb_y):
            char: Optional[str] = schematic.get_char(adj_x, adj_y)
            if char is None:
                continue
            if SYMBOL_REGEX.fullmatch(char):
                continue

            # Find all numbers in this line
            for num_match in DIGITS_REGEX.finditer(schematic.lines[adj_x]):
                # Find the only one that include the 'y' coordinate
                if adj_y in range(*num_match.span()):
                    # Do not add already added files
                    if num_match.span() in added_ranges[adj_x]:
                        continue

                    result += int(num_match.group())
                    added_ranges[adj_x].append(num_match.span())
    return result


def part_two(schematic: Schematic) -> int:
    result: int = 0

    for symb_x, symb_y in schematic.get_symbols_coordinates():

        if schematic.get_char(symb_x, symb_y) != "*":
            continue

        added_ranges: DefaultDict[int, List[Tuple[int, int]]] = defaultdict(list)
        gear_numbers: List[int] = []  # Remember values found around the current gear

        for adj_x, adj_y in schematic.get_adjacent_coordinates(symb_x, symb_y):
            char: Optional[str] = schematic.get_char(adj_x, adj_y)
            if char is None:
                continue
            if SYMBOL_REGEX.fullmatch(char):
                continue

            # Find all numbers in this line
            for num_match in DIGITS_REGEX.finditer(schematic.lines[adj_x]):
                # Find the only one that include the 'y' coordinate
                if adj_y in range(*num_match.span()):
                    # Do not add already added files
                    if num_match.span() in added_ranges[adj_x]:
                        continue

                    # print(f"Adding: {num_match.group()} ({adj_x};{adj_y})")
                    gear_numbers.append( int(num_match.group()) )
                    added_ranges[adj_x].append(num_match.span())

        if len(gear_numbers) == 2:
            result += gear_numbers[0] * gear_numbers[1]
    return result


print("Part one:", part_one(schematic))
print("Part two:", part_two(schematic))
