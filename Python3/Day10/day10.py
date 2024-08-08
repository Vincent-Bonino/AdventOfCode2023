from enum import Enum
from typing import *

from tqdm import tqdm


class Coordinate:
    row: int
    col: int

    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col

    def get_direction_to_coordinate(self, coord: 'Coordinate') -> 'Direction':
        delta_row: int = coord.row - self.row
        delta_col: int = coord.col - self.col
        return Direction((delta_row, delta_col))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Coordinate):
            return NotImplemented
        return self.row == other.row and self.col == other.col

    def __add__(self, other: Any) -> 'Coordinate':
        if isinstance(other, Coordinate):
            return Coordinate(self.row + other.row, self.col + other.col)
        if isinstance(other, Direction):
            return Coordinate(self.row + other.value[0], self.col + other.value[1])
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"({self.row}, {self.col})"


class Direction(Enum):
    UPPER_LEFT =    (-1, -1)
    UPPER =         (-1, +0)
    UPPER_RIGHT =   (-1, +1)
    LEFT =          (+0, -1)
    RIGHT =         (+0, +1)
    LOWER_LEFT =    (+1, -1)
    LOWER =         (+1, +0)
    LOWER_RIGHT =   (+1, +1)

    @classmethod
    def get_direct_directions(cls) -> List['Direction']:
        return [Direction.UPPER, Direction.RIGHT, Direction.LOWER, Direction.LEFT]


class Pipe(Enum):
    """Enumeration of all possible types of items on the map (mostly pipes)."""
    NONE = "."
    START = "S"
    VERTICAL = "|"
    HORIZONTAL = "-"
    UP_LEFT = "J"
    UP_RIGHT = "L"
    DOWN_RIGHT = "F"
    DOWN_LEFT = "7"

    def is_pipe(self) -> bool:
        return self is not Pipe.NONE

    def is_start(self) -> bool:
        return self is Pipe.START

    def is_left(self) -> bool:
        return self in [Pipe.UP_LEFT, Pipe.DOWN_LEFT]

    def is_right(self) -> bool:
        return self in [Pipe.UP_RIGHT, Pipe.DOWN_RIGHT]

    def is_corner(self) -> bool:
        return self in [Pipe.UP_LEFT, Pipe.UP_RIGHT, Pipe.DOWN_LEFT, Pipe.DOWN_RIGHT]

    def is_vertical_pipe(self) -> bool:
        return self is not Pipe.NONE and self is not Pipe.START and self is not Pipe.HORIZONTAL

    def get_vertical_direction(self) -> str:
        if self in [Pipe.UP_LEFT, Pipe.UP_RIGHT]:
            return "UP"
        if self in [Pipe.DOWN_LEFT, Pipe.DOWN_RIGHT]:
            return "DOWN"
        return ""


PIPES_LINKABLE_DIRECTION: Dict[Pipe, List[Direction]] = {
    Pipe.NONE: [],
    Pipe.START:         list(Direction),
    Pipe.VERTICAL:      [Direction.UPPER, Direction.LOWER],
    Pipe.HORIZONTAL:    [Direction.LEFT, Direction.RIGHT],
    Pipe.UP_LEFT:       [Direction.UPPER, Direction.LEFT],
    Pipe.UP_RIGHT:      [Direction.UPPER, Direction.RIGHT],
    Pipe.DOWN_RIGHT:    [Direction.LOWER, Direction.RIGHT],
    Pipe.DOWN_LEFT:     [Direction.LOWER, Direction.LEFT],
}


class GridMap:
    """Represent the pipes map."""

    lines: List[str]
    max_row: int
    max_col: int

    start_coordinates: Optional[Coordinate]

    def __init__(self, lines: List[str]) -> None:
        self.lines = [line.strip() for line in lines]
        self.max_row = len(self.lines)
        self.max_col = len(self.lines[0])
        self.start_coordinates = None

    def get_adjacent_linkable_pipes_coordinates(self, coord: Coordinate) -> List[Coordinate]:
        pipe: Pipe = Pipe(self.get_pipe(coord))

        result: List[Coordinate] = []
        for ajd_pip_coord in self.get_adjacent_pipe_coordinates(coord):
            delta_dir: Direction = coord.get_direction_to_coordinate(ajd_pip_coord)
            if delta_dir in PIPES_LINKABLE_DIRECTION[pipe]:
                result.append(ajd_pip_coord)

        if pipe is not Pipe.START and len(result) != 2:
            raise RuntimeError(f"More than 2 linkable pipes: {coord}")
        return result

    def get_adjacent_pipe_coordinates(self, coord: Coordinate) -> List[Coordinate]:
        return [
            coord
            for coord in self.get_adjacent_coordinates(coord)
            if self.get_pipe(coord).is_pipe()
        ]

    def get_adjacent_coordinates(self, coord: Coordinate) -> List[Coordinate]:
        full_list: List[Coordinate] = [coord + dir for dir in Direction.get_direct_directions()]
        return [coord for coord in full_list if self.get_pipe(coord) is not None]

    def get_pipe(self, coord: Coordinate) -> Pipe:
        # pylint: disable=superfluous-parens
        if not (0 <= coord.row < self.max_row) or not (0 <= coord.col < self.max_col):
            return Pipe.NONE
        return Pipe(self.lines[coord.row][coord.col])

    def get_start_coordinate(self) -> Coordinate:
        if self.start_coordinates is not None:
            return self.start_coordinates

        for row_idx, row in enumerate(self.lines):
            for col_idx, _col in enumerate(row):
                coord: Coordinate = Coordinate(row_idx, col_idx)
                if self.get_pipe(coord) is Pipe.START:
                    self.start_coordinates = coord
                    return coord
        raise RuntimeError("No start found.")

    def extrapolate_start_pipe(self) -> None:
        start_coord: Coordinate = self.get_start_coordinate()
        all_adj_coords: List[Coordinate] = self.get_adjacent_linkable_pipes_coordinates(start_coord)

        adj_coords: List[Coordinate] = [
            coord
            for coord in all_adj_coords
            if coord.get_direction_to_coordinate(start_coord) in PIPES_LINKABLE_DIRECTION[self.get_pipe(coord)]
        ]
        adj_directions: List[Direction] = [start_coord.get_direction_to_coordinate(adj) for adj in adj_coords]

        for pipe, directions in PIPES_LINKABLE_DIRECTION.items():
            if set(directions) == set(adj_directions):
                print(f"> Chose pipe {pipe} for start")
                row: int = start_coord.row
                col: int = start_coord.col
                original_line: str = self.lines[row]
                new_line: str = original_line[:col] + pipe.value + original_line[col+1:]
                self.lines[row] = new_line
                break
        else:
            raise RuntimeError("Unable to find a starting pipe")

    def print_map(self) -> None:
        for line in self.lines:
            print(f"{line}")


def compute_loop(map: GridMap) -> List[Coordinate]:
    loop: List[Coordinate] = []
    start_coord: Coordinate = map.get_start_coordinate()

    # Attempt to find a loop, starting in all four directions
    for dir in Direction.get_direct_directions():
        loop = []  # Reset a potential previous attempt

        previous_coord: Coordinate = start_coord
        current_coord: Coordinate = start_coord + dir

        loop.append(start_coord)
        loop.append(current_coord)

        if not map.get_pipe(current_coord).is_pipe():
            # Ignore ground around the start
            continue

        if not current_coord.get_direction_to_coordinate(previous_coord) in PIPES_LINKABLE_DIRECTION[map.get_pipe(current_coord)]:
            # Ignore impossible starts
            continue

        print(f"Attempting {dir.name} from start")
        try:
            while not map.get_pipe(current_coord).is_start():
                ajd_pipe_coordinates: List[Coordinate] = map.get_adjacent_linkable_pipes_coordinates(current_coord)
                # Must be length == 2

                option_1: Coordinate = ajd_pipe_coordinates[0]
                option_2: Coordinate = ajd_pipe_coordinates[1]
                new_current_coord: Coordinate
                if option_1 == previous_coord:
                    new_current_coord = option_2
                else:
                    new_current_coord = option_1

                # Step once
                previous_coord = current_coord
                current_coord = new_current_coord
                loop.append(current_coord)

            # Current coord is the start
            return loop

        except RuntimeError:
            # It might not be the right way, try another one
            print("Error")
            continue
    raise RuntimeError("Unable to loop")


def part_one() -> int:
    map: GridMap

    # Load map from file
    with open("input.txt", mode='r') as f_input:
        map = GridMap(f_input.readlines())

    loop: List[Coordinate] = compute_loop(map)
    return len(loop) // 2


def part_two() -> int:
    base_map: GridMap
    loop_map: GridMap

    # Load map from file
    with open("input.txt", mode='r') as f_input:
        lines: List[str] = list(f_input.readlines())
        base_map = GridMap(lines)
        loop_map = GridMap(lines)

    # Compute loop
    loop: List[Coordinate] = compute_loop(base_map)

    # Transform the loop map, replace every non loop pipe by ground
    for row in tqdm(range(base_map.max_row), desc="Erasing non-loop pipes", unit="line"):
        for col in range(base_map.max_col):  # This is terribly not optimized
            # Removing pipes out of the loop
            # Also removing horizontal pipes since we will be counting pipes on each line, line by line
            if Coordinate(row, col) not in loop: # or loop_map.get_pipe(Coordinate(row, col)) is Pipe.HORIZONTAL:
                original_line: str = loop_map.lines[row]
                new_line: str = original_line[:col] + Pipe.NONE.value + original_line[col+1:]
                loop_map.lines[row] = new_line

    loop_map.extrapolate_start_pipe()
    # loop_map.print_map()

    # Write loop to another file for debug (and quicker recovery)
    if False:
        with open("input-loop.txt", mode='w+') as f_loop:
            f_loop.writelines(f"{line}\n" for line in loop_map.lines)

    # Determine in/out on each line
    counter: int = 0

    is_in: bool = False
    vert_dir: str = ""
    for row, line in enumerate(loop_map.lines):
        is_in = False

        for col, pipe_str in enumerate(line):
            pipe: Pipe = Pipe(pipe_str)

            # Inside None: count it
            if pipe is Pipe.NONE and is_in is True:
                counter += 1
                continue
            # Outside None: ignore it
            if pipe is Pipe.NONE and is_in is False:
                continue
            # Vertical pipes: always changes in/out state
            if pipe is Pipe.VERTICAL:
                is_in = not is_in
            # Horizontal and right pipes: does not change in/out state
            if pipe is Pipe.HORIZONTAL:
                continue
            # If is_left, we remember the vertical direction
            if pipe.is_right():
                vert_dir = pipe.get_vertical_direction()
                continue
            # If is_left, we are crossing a new border and maybe changing in/out state
            if pipe.is_left():
                new_vert_dir = pipe.get_vertical_direction()

                if vert_dir != new_vert_dir:
                    # Not coming back where it comes from, changing in/out state
                    is_in = not is_in

                vert_dir = ""
                continue
        print("Line n°", row, line, "score=", counter)

    return counter


print("Part one:", part_one())
print("Part two:", part_two())
