from typing import *
import math
import re


class Map:
    """Represents the map."""

    parsing_regex: Pattern[str] = re.compile(r"(?P<loc>\w{3}) = \((?P<left>\w{3}), (?P<right>\w{3})\)")

    directions: Dict[str, Tuple[str, str]]

    def __init__(self) -> None:
        self.directions = {}

    def register_line(self, line: str) -> None:
        match = self.parsing_regex.match(line)
        if match is None:
            raise RuntimeError(line)
        self.directions[match.group("loc")] = (match.group("left"), match.group("right"))

    def get_next(self, loc: str, direction: str) -> str:
        if direction == "L":
            return self.get_left(loc)
        if direction == "R":
            return self.get_right(loc)
        raise NotImplementedError

    def get_left(self, loc: str) -> str:
        return self.directions[loc][0]

    def get_right(self, loc: str) -> str:
        return self.directions[loc][1]


def part_one() -> int:
    map: Map = Map()
    pattern: str

    with open("alt-input.txt", mode='r') as f_input:
        pattern = f_input.readline().strip()
        f_input.readline()  # Skip empty line
        for line in f_input.readlines():
            map.register_line(line.strip())

    # Run through the map
    start: str = "AAA"
    end: str = "ZZZ"
    pattern_length: int = len(pattern)

    move_counter: int = 0
    current_pos: str = start
    while current_pos != end:
        current_pos = map.get_next(current_pos, pattern[move_counter % pattern_length])
        move_counter += 1

    return move_counter


def part_two() -> int:
    map: Map = Map()
    pattern: str

    with open("alt-input.txt", mode='r') as f_input:
        pattern = f_input.readline().strip()
        f_input.readline()  # Skip empty line
        for line in f_input.readlines():
            map.register_line(line.strip())

    # Run through the map
    pattern_length: int = len(pattern)
    starts: List[str] = [pos for pos in map.directions if pos.endswith("A")]

    # VERY STRONG HYPOTHESIS HERE
    # I assumed (wondering how to solve the problem but mostly how it was made)
    # that all ghosts' paths were a loop (after the end position, the following position is the start).
    # This allows a computation around solutions like "sol = k*x", with k being the length of the path.
    # If the solutions were more general ("sol = k*x + delta"), it would have required significantly more math.
    periodicity: List[int] = []
    for start_pos in starts:
        move_counter: int = 0
        current_pos: str = start_pos
        while not current_pos.endswith("Z"):
            current_pos = map.get_next(current_pos, pattern[move_counter % pattern_length])
            move_counter += 1
        periodicity.append(move_counter)

    return math.lcm(*periodicity)

print("Part one:", part_one())
print("Part two:", part_two())
