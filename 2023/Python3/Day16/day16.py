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


class MirrorType(Enum):
    EMPTY = "."
    MIRROR1 = "\\"
    MIRROR2 = "/"
    SPLITTER1 = "|"
    SPLITTER2 = "-"

    def is_mirror(self) -> bool:
        return self in [MirrorType.MIRROR1, MirrorType.MIRROR2]

    def is_splitter(self) -> bool:
        return self in [MirrorType.SPLITTER1, MirrorType.SPLITTER2]

    def reflect(self, dir: Direction) -> Direction:
        splitter_conversion_table: Dict[Direction, Direction]
        if self is MirrorType.MIRROR1:
            splitter_conversion_table = {
                Direction.NORTH: Direction.WEST,
                Direction.EAST: Direction.SOUTH,
                Direction.SOUTH: Direction.EAST,
                Direction.WEST: Direction.NORTH,
            }
        elif self is MirrorType.MIRROR2:
            splitter_conversion_table = {
                Direction.NORTH: Direction.EAST,
                Direction.EAST: Direction.NORTH,
                Direction.SOUTH: Direction.WEST,
                Direction.WEST: Direction.SOUTH,
            }
        else:
            raise ValueError("Can not reflect")
        return splitter_conversion_table[dir]

class Tile:
    type: MirrorType
    visisted: bool

    seen_ray_dir: List[Direction]

    def __init__(self, mirror: MirrorType) -> None:
        self.type = mirror
        self.visisted = False
        self.seen_ray_dir = []

    def act_on_ray(self, ray: 'Ray') -> Optional['Ray']:
        """Return the new ray in case of a split."""
        self.seen_ray_dir.append(ray.direction)
        self.visisted = True

        if self.type is MirrorType.EMPTY:
            ray.move()
            return None

        if self.type.is_mirror():
            ray.direction = self.type.reflect(ray.direction)
            ray.move()
            return None

        if self.type.is_splitter():
            as_empty_dir: List[Direction] = (
                [Direction.NORTH, Direction.SOUTH] if self.type is MirrorType.SPLITTER1  # |
                else [Direction.EAST, Direction.WEST]
            )
            # Continue, as if empty
            if ray.direction in as_empty_dir:
                ray.move()
                return None

            # Split
            ray.direction = as_empty_dir[0]
            new_ray: Ray = Ray(ray.position, as_empty_dir[1])
            ray.move()
            new_ray.move()
            return new_ray

    def reset(self) -> None:
        self.visisted = False
        self.seen_ray_dir = []

class Ray:
    position: Tuple[int, int]
    direction: Direction

    def __init__(self, position: Tuple[int, int], direction: Direction) -> None:
        self.position = position
        self.direction = direction

    def move(self) -> None:
        self.position = (self.position[0] + self.direction.x, self.position[1] + self.direction.y)

    def __repr__(self) -> str:
        return f"{self.position} {self.direction.name}"


class Contraption:
    layout: List[List[Tile]]
    rays: List[Ray]

    max_x: int
    max_y: int

    def __init__(self, lines: List[str]) -> None:
        self.max_x = len(lines)
        self.max_y = len(lines[0])

        self.rays = [Ray((0, 0), Direction.EAST)]
        self.layout = [
            [Tile(MirrorType(chr)) for chr in line]
            for line in lines
        ]

    def is_out_of_bounds(self, position: Tuple[int, int]) -> bool:
        x: int = position[0]
        y: int = position[1]
        return x < 0 or y < 0 or self.max_x <= x or self.max_y <= y

    def get_tile(self, position: Tuple[int, int]) -> Tile:
        return self.layout[position[0]][position[1]]

    def move_all_rays_once(self) -> bool:
        rays_to_remove: List[Ray] = []

        for index in range(len(self.rays)):  # Won't take new array
            ray: Ray = self.rays[index]

            # Discard arrays out of bounds
            if self.is_out_of_bounds(ray.position):
                rays_to_remove.append(ray)
                continue

            tile: Tile = self.get_tile(ray.position)

            # Discard if future path is already known
            if ray.direction in tile.seen_ray_dir:
                rays_to_remove.append(ray)
                continue

            new_ray: Optional[Ray] = tile.act_on_ray(ray)
            if new_ray is not None:
                self.rays.append(new_ray)

        # Remove rays after to prevent messing up with indexes
        for rm_ray in rays_to_remove:
            self.rays.remove(rm_ray)

        return bool(self.rays)

    def count(self) -> int:
        return len([tile for line in self.layout for tile in line if tile.visisted])

    def reset(self) -> None:
        for line in self.layout:
            for tile in line:
                tile.reset()

    def show_visited(self) -> str:
        return "\n".join(
            "".join('#' if tile.visisted else "." for tile in line)
            for line in self.layout
        )

    def __repr__(self) -> str:
        return "\n".join(
            "".join(tile.type.value for tile in line)
            for line in self.layout
        )

def part_one() -> int:
    with open("input.txt", mode='r') as f_input:
        lines: List[str] = [line.strip() for line in f_input.readlines()]

    contraption: Contraption = Contraption(lines)
    while contraption.move_all_rays_once():
        pass  # Move rays until nothing happens
    return contraption.count()


def generate_starting_rays(max_x: int, max_y: int) -> Iterator[Ray]:
    # Top line
    for y in range(max_y):
        yield Ray((0, y), Direction.SOUTH)
    # Left col
    for x in range(max_x):
        yield Ray((x, 0), Direction.EAST)
    # Bottom line
    for y in range(max_y):
        yield Ray((max_x-1, y), Direction.NORTH)
    # Right col
    for x in range(max_x):
        yield Ray((x, max_y-1), Direction.WEST)


def part_two() -> int:
    with open("input.txt", mode='r') as f_input:
        lines: List[str] = [line.strip() for line in f_input.readlines()]

    contraption: Contraption = Contraption(lines)

    current_max: int = -1
    for ray in generate_starting_rays(contraption.max_x, contraption.max_y):
        contraption.reset()
        contraption.rays = [ray]
        while contraption.move_all_rays_once():
            pass  # Move rays until nothing happens
        current_max = max(current_max, contraption.count())

    return current_max


print("Part one:", part_one())
print("Part two:", part_two())
