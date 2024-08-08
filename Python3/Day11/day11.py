from enum import Enum
from typing import *


class SpaceItem(Enum):
    VOID = "."
    GALAXY = "#"


class Galaxy:
    """Represent a galaxy on the map."""

    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def compute_distance(self, other: 'Galaxy') -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)


class SpaceLine:
    """Represent a line (row or col) in space."""

    is_empty: bool

    def __init__(self, emptyness: bool) -> None:
        self.is_empty = emptyness


class Space:
    """Represent space with all its galaxies."""

    raw_map: List[str]
    max_row: int
    max_col: int

    galaxies: List[Galaxy]

    space_rows: List[SpaceLine]
    space_cols: List[SpaceLine]

    expansion_factor: int = 1

    def __init__(self, lines: List[str]) -> None:
        self.raw_map = [line.strip() for line in lines]
        self.max_row = len(self.raw_map)
        self.max_col = len(self.raw_map[0])

        self.galaxies = []

        # Find galaxies and build SpaceLines
        row_is_empty: List[bool] = [True] * self.max_row
        col_is_empty: List[bool] = [True] * self.max_col

        for row in range(self.max_row):
            for col in range(self.max_col):
                if SpaceItem(self.raw_map[row][col]) is SpaceItem.GALAXY:
                    self.galaxies.append(Galaxy(row, col))
                    row_is_empty[row] = False
                    col_is_empty[col] = False
        self.space_rows = [SpaceLine(emptyness) for emptyness in row_is_empty]
        self.space_cols = [SpaceLine(emptyness) for emptyness in col_is_empty]

    def compute_distance_between(self, gal1: Galaxy, gal2: Galaxy) -> int:
        distance: int = 0

        min_x: int = min(gal1.x, gal2.x)
        max_x: int = max(gal1.x, gal2.x)
        min_y: int = min(gal1.y, gal2.y)
        max_y: int = max(gal1.y, gal2.y)

        for x in range(min_x, max_x):
            distance += self.expansion_factor if self.space_rows[x].is_empty else 1
        for y in range(min_y, max_y):
            distance += self.expansion_factor if self.space_cols[y].is_empty else 1

        return distance

    def compute_all_distances_sum(self) -> int:
        result: int = 0
        for i, gal_i in enumerate(self.galaxies):
            for _j, gal_j in enumerate(self.galaxies[i+1:]):
                result += self.compute_distance_between(gal_i, gal_j)
        return result


space: Space
with open("input.txt", mode='r') as f_input:
    space = Space(f_input.readlines())


def part_one(space: Space) -> int:
    space.expansion_factor = 2
    return space.compute_all_distances_sum()


def part_two(space: Space) -> int:
    space.expansion_factor = 1_000_000
    return space.compute_all_distances_sum()


print("Part one:", part_one(space))
print("Part two:", part_two(space))
