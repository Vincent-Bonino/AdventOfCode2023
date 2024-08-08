from dataclasses import dataclass
from enum import Enum
from typing import *

import numpy as np


class Direction(Enum):
    NORTH = (-1, 0)
    EAST  = (0, +1)
    SOUTH = (+1, 0)
    WEST  = (0, -1)

    @property
    def x(self) -> int:
        return self.value[0]

    @property
    def y(self) -> int:
        return self.value[1]

    def __repr__(self) -> str:
        return f"{self.name}"


STR_TO_DIR: Dict[str, Direction] = {
    "U": Direction.NORTH,
    "R": Direction.EAST,
    "D": Direction.SOUTH,
    "L": Direction.WEST,
}


INT_TO_DIR: Dict[int, Direction] = {
    0: STR_TO_DIR["R"],
    1: STR_TO_DIR["D"],
    2: STR_TO_DIR["L"],
    3: STR_TO_DIR["U"],
}


def compute_area(x, y):
    """Compute area of a polygon from its vertices.

    Found on https://stackoverflow.com/a/30408825
    """
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))


def solve(part_two: bool = False) -> int:
    with open("input.txt", mode='r') as f_input:
        lines: List[str] = [line.strip() for line in f_input.readlines()]

    list_of_x: List[int] = [0]  # Init with starting point
    list_of_y: List[int] = [0]  # Init with starting point
    list_of_l: List[int] = []

    current_x: int = 0
    current_y: int = 0
    for line in lines:
        # Parse
        dir, len, color = line.split(" ")
        if part_two is False:
            direction = STR_TO_DIR[dir]
            length = int(len)
        else:
            color = color[2:-1]  # Remove symbols
            direction = INT_TO_DIR[int(color[-1:], base=16)]
            length = int(color[:5], base=16)

        # Move
        current_x += length * direction.x
        current_y += length * direction.y

        # Register
        list_of_x.append(current_x)
        list_of_y.append(current_y)
        list_of_l.append(length)

    xs = np.array(list_of_x, dtype=np.float64)
    ys = np.array(list_of_y, dtype=np.float64)
    area = compute_area(xs, ys)
    t_len = sum(list_of_l)

    # Computed area must be adjusted to the trenches making the border
    return int(area + t_len/2 + 1)


print("Part one:", solve(part_two=False))
print("Part two:", solve(part_two=True))
