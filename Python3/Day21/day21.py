from collections import defaultdict
from enum import Enum
from typing import *


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


class TileType(Enum):
    GARDEN = "."
    START = "S"
    ROCK = "#"

    def is_garden(self) -> bool:
        return self is TileType.START or self is TileType.GARDEN


class Step:
    coordinates: Tuple[int, int]
    steps_from_start: int

    def __init__(self, coordinates: Tuple[int, int], steps_from_start: int = 0) -> None:
        self.coordinates = coordinates
        self.steps_from_start = steps_from_start

    @property
    def x(self) -> int:
        return self.coordinates[0]

    @property
    def y(self) -> int:
        return self.coordinates[1]

    def walk(self, direction: Direction) -> 'Step':
        return Step((self.x + direction.x, self.y + direction.y), self.steps_from_start + 1)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Step):
            return NotImplemented
        return self.coordinates == other.coordinates

    def __hash__(self) -> int:
        return hash(self.coordinates)


def part_one() -> int:
    MAX_STEP_NBR: int = 64

    with open("input.txt", mode='r') as f_input:
        lines: List[str] = [x.strip() for x in f_input.readlines()]

    garden_index: Dict[Tuple[int, int], TileType] = {}

    # Find start, and index tiles for performances
    start_position: Tuple[int, int] = (-1, -1)  # For linters only
    for i, line in enumerate(lines):
        for j, chr in enumerate(line):
            garden_index[(i, j)] = TileType(chr)
            if chr == "S":
                start_position = (i, j)

    # Count garden
    steps: DefaultDict[int, Set[Step]] = defaultdict(set)

    steps[0].add(Step(start_position))
    current_dist: int = 0

    while current_dist <= MAX_STEP_NBR:
        for current_step in steps[current_dist]:

            # Add neighbors
            for dir in Direction:
                new_step: Step = current_step.walk(dir)

                # Stop if rock
                if not garden_index.get(new_step.coordinates, TileType.ROCK).is_garden():
                    continue

                # Stop if too far
                if new_step.steps_from_start > MAX_STEP_NBR:
                    continue

                # Continue to walk
                steps[new_step.steps_from_start].add(new_step)
        
        # One step further
        current_dist += 1

    return len(steps[MAX_STEP_NBR])


print("Part one:", part_one())
