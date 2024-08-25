from collections import defaultdict, deque
from dataclasses import dataclass
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
    
    @property
    def distance(self) -> int:
        return self.steps_from_start

    def walk(self, direction: Direction) -> 'Step':
        return Step((self.x + direction.x, self.y + direction.y), self.steps_from_start + 1)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Step):
            return NotImplemented
        return self.coordinates == other.coordinates

    def __hash__(self) -> int:
        return hash(self.coordinates)

    def __repr__(self) -> str:
        return f"Step<{self.coordinates}; {self.steps_from_start}>"


def part_one() -> DefaultDict[int, Set[Step]]:

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

    while current_dist < len(lines):
        for current_step in steps[current_dist]:

            # Add neighbors
            for dir in Direction:
                new_step: Step = current_step.walk(dir)

                # Stop if rock
                if not garden_index.get(new_step.coordinates, TileType.ROCK).is_garden():
                    continue

                # Continue to walk
                steps[new_step.steps_from_start].add(new_step)
        
        # One step further
        current_dist += 1
    
    # Start does not count
    steps[0] = set()

    return steps

PART_ONE_MAX_STEP_NBR: int = 64

# print("Part one:", len(part_one()[PART_ONE_MAX_STEP_NBR]))


# ====== Part 2 ====

def compute_distances() -> Dict[Tuple[int, int], int]:
    with open("input.txt", mode='r') as f_input:
        lines: List[str] = [x.strip() for x in f_input.readlines() if x.strip()]

    gardens: Set[Tuple[int, int]] = set()
    start_position: Tuple[int, int] = (-1, -1)

    for i, line in enumerate(lines):
        for j, chr in enumerate(line):
            if chr == TileType.ROCK.value:
                continue
            if chr == TileType.START.value:
                start_position = (i, j)
            gardens.add((i, j))

    # coord: dist_to_start
    visited: Dict[Tuple[int, int], int] = {}
    queue: deque[Tuple[int, Tuple[int, int]]] = deque([(0, start_position)])  # type: ignore

    while queue:
        dist, tile = queue.popleft()

        if tile in visited:
            continue

        visited[tile] = dist

        for dir in Direction:
            new_tile: Tuple[int, int] = (tile[0] + dir.value[0], tile[1] + dir.value[1])

            if new_tile in visited or new_tile not in gardens:
                continue

            queue.append((dist+1, new_tile))
    
    return visited


def part_two() -> int:
    """Solve part 2.

    Inspired by xavdid's write-up. https://advent-of-code.xavd.id/writeups/2023/day/21/

    """
    MAX_STEP_NBR: int = 26_501_365

    with open("input.txt", mode='r') as f_input:
        lines: List[str] = [x.strip() for x in f_input.readlines() if x.strip()]

    GRID_LENGTH: int = len(lines)

    META_SQUARE_LENGTH: int = ((MAX_STEP_NBR - GRID_LENGTH//2) // GRID_LENGTH)
    print(f"N={META_SQUARE_LENGTH}")

    META_GRID_FULL_EVEN_NBR: int = META_SQUARE_LENGTH**2
    META_GRID_FULL_ODD_NBR: int = (META_SQUARE_LENGTH+1)**2

    META_GRID_CORNERS_EVEN_NBR: int = META_SQUARE_LENGTH
    META_GRID_CORNERS_ODD_NBR: int = -(META_SQUARE_LENGTH + 1)


    visited: Dict[Tuple[int, int], int] = compute_distances()

    def count_points(f: Callable[[int], bool]) -> int:
        return sum(f(v) for v in visited.values())

    print("Part 1:",  count_points(lambda v: v < GRID_LENGTH//2 and v % 2 == 0))

    full_even_value: int = count_points(lambda v: v % 2 == 0)
    full_odd_value: int  = count_points(lambda v: v % 2 == 1)

    corner_even_value: int = count_points(lambda v: v > GRID_LENGTH//2 and v % 2 == 0)
    corner_odd_value: int =  count_points(lambda v: v > GRID_LENGTH//2 and v % 2 == 1)

    return (
        (META_GRID_FULL_EVEN_NBR     * full_even_value)   +
        (META_GRID_FULL_ODD_NBR      * full_odd_value)    +
        (META_GRID_CORNERS_EVEN_NBR  * corner_even_value) +
        (META_GRID_CORNERS_ODD_NBR   * corner_odd_value)
    )


print("Part two:", part_two())
