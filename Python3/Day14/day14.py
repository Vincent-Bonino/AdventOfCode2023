from dataclasses import dataclass
from enum import Enum
from typing import *

from tqdm import tqdm


def replace_value(line: str, j: int, new: str) -> str:
    new_line = line[:j] + new + line[j+1:]
    return new_line


class RockType(Enum):
    EMPTY = "."
    CUBE = "#"
    ROUND = "O"


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


@dataclass(unsafe_hash=True)
class Rock:
    """Contain the position of a rock"""
    x: int
    y: int
    is_spherical: bool

    @property
    def position(self) -> Tuple[int, int]:
        return (self.x, self.y)

    def move(self, direction: Direction) -> None:
        self.x += direction.x
        self.y += direction.y

    def get_move_position(self, direction: Direction) -> Tuple[int, int]:
        return (self.x + direction.x, self.y + direction.y)


def sort_for_north(rocks: List[Rock]) -> List[Rock]:
    return sorted(rocks, key=lambda r: r.x, reverse=False)

def sort_for_south(rocks: List[Rock]) -> List[Rock]:
    return sorted(rocks, key=lambda r: r.x, reverse=True)

def sort_for_east(rocks: List[Rock]) -> List[Rock]:
    return sorted(rocks, key=lambda r: r.y, reverse=True)

def sort_for_west(rocks: List[Rock]) -> List[Rock]:
    return sorted(rocks, key=lambda r: r.y, reverse=False)

class Platform:
    """Represent the platform, with all the rocks on it."""
    max_x: int
    max_y: int

    cubes: List[Rock]  # Can't move
    spheres: List[Rock]  # Can move

    platform: Dict[Tuple[int, int], Rock]  # Easy access

    sort_methods: Dict[Direction, Callable[[List[Rock]], List[Rock]]] = {
        Direction.NORTH: sort_for_north,
        Direction.EAST: sort_for_east,
        Direction.SOUTH: sort_for_south,
        Direction.WEST: sort_for_west,
    }

    def __init__(self, grid: List[str]) -> None:
        self.cubes = []
        self.spheres = []
        self.platform = {}
    
        self.max_x = len(grid)
        self.max_y = len(grid[0].strip())

        for i, line in enumerate(grid):
            for j, rock_val in enumerate(line.strip()):
                if rock_val == RockType.EMPTY.value:
                    continue
                is_spherical: bool = rock_val == RockType.ROUND.value
                rock: Rock = Rock(i, j, is_spherical)
                self.platform[rock.position] = rock
                if is_spherical:
                    self.spheres.append(rock)
                else:
                    self.cubes.append(rock)

    def is_out_of_bounds(self, position: Tuple[int, int]) -> bool:
        x: int = position[0]
        y: int = position[1]
        return x < 0 or y < 0 or self.max_x <= x or self.max_y <= y

    def move_sphere(self, sphere: Rock, direction: Direction) -> None:
        while True:
            next_pos: Tuple[int, int] = sphere.get_move_position(direction)
            if self.is_out_of_bounds(next_pos) or next_pos in self.platform:
                # Something is already here
                break
            # Move once
            sphere.move(direction)
        # After it, place it back on the platform
        self.platform[sphere.position] = sphere

    def move_all_spheres(self, direction: Direction) -> None:
        for sphere in self.sort_methods[direction](self.spheres):
            origin_pos: Tuple[int, int] = sphere.position
            # Remove it from the platform
            self.platform.pop(origin_pos)
            self.move_sphere(sphere, direction)

    def move_as_cycle(self) -> None:
        self.move_all_spheres(Direction.NORTH)
        self.move_all_spheres(Direction.WEST)
        self.move_all_spheres(Direction.SOUTH)
        self.move_all_spheres(Direction.EAST)

    def score(self) -> int:
        total: int = 0
        for sphere in self.spheres:
            total += self.max_x - sphere.x
        return total

    def __hash__(self) -> int:
        return hash(tuple(self.spheres))

    def __repr__(self) -> str:
        grid: List[str] = ["." * self.max_y] * self.max_x
        for i, j in self.platform.keys():
            grid[i] = replace_value(grid[i], j, "O" if self.platform[(i, j)].is_spherical else "#")
        return "\n".join(line for line in grid)


def part_one() -> int:
    with open("input.txt", mode='r') as f_input:
        platform: Platform = Platform(f_input.readlines())

    platform.move_all_spheres(Direction.NORTH)
    return platform.score()


def part_two() -> int:
    with open("input.txt", mode='r') as f_input:
        platform: Platform = Platform(f_input.readlines())

    total_cycle_number: int = 1_000_000_000
    cache: Dict[int, Any] = {}

    counter: int = 0
    while counter < total_cycle_number:
        hsh: int = hash(tuple(sorted(platform.spheres, key=lambda r: r.position)))

        # Found a loop (who could have guessed ?)
        if hsh in cache:
            cycle_length: int = counter - cache[hsh]
            cycle_number: int = (total_cycle_number - counter) // cycle_length
            counter += cycle_length * cycle_number
        else:
            cache[hsh] = counter

        platform.move_as_cycle()
        counter += 1

    return platform.score()

if __name__ == "__main__":
    print("Part one:", part_one())
    print("Part two:", part_two())
