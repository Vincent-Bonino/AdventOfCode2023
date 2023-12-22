from collections import defaultdict
from dataclasses import dataclass
from typing import *

# x, y, z
Position: TypeAlias = Tuple[int, int, int]

def substract_z(pos: Position, dz: int) -> Position:
    return (pos[0], pos[1], pos[2] - dz)


class Brick:
    edge1: Position
    edge2: Position

    def __init__(self, pos1: Position, pos2: Position) -> None:
        self.edge1 = pos1
        self.edge2 = pos2

    @property
    def x1(self) -> int:
        return self.edge1[0]
    @property
    def y1(self) -> int:
        return self.edge1[1]
    @property
    def z1(self) -> int:
        return self.edge1[2]
    @property
    def x2(self) -> int:
        return self.edge2[0]
    @property
    def y2(self) -> int:
        return self.edge2[1]
    @property
    def z2(self) -> int:
        return self.edge2[2]

    def get_min_z(self) -> int:
        return min(self.z1, self.z2)

    def shift_z(self, value: int) -> None:
        self.edge1 = (self.x1, self.y1, self.z1 - value)
        self.edge2 = (self.x2, self.y2, self.z2 - value)

    def __repr__(self) -> str:
        return f"Brick<{self.edge1}-{self.edge2}"

    def get_bottom_cubes(self) -> List[Position]:
        if self.y1 != self.y2:
            y_min: int = min(self.y1, self.y2)
            y_max: int = max(self.y1, self.y2)
            return [
                (self.x1, y, self.z1)
                for y in range(y_min, y_max + 1)
            ]

        if self.x1 != self.x2:
            x_min: int = min(self.x1, self.x2)
            x_max: int = max(self.x1, self.x2)
            return [
                (x, self.y1, self.z1)
                for x in range(x_min, x_max + 1)
            ]

        return [(self.x1, self.y1, self.get_min_z())]

    def get_cubes(self) -> List[Position]:
        if self.x1 != self.x2:
            x_min: int = min(self.x1, self.x2)
            x_max: int = max(self.x1, self.x2)
            return [
                (x, self.y1, self.z1)
                for x in range(x_min, x_max + 1)
            ]

        if self.y1 != self.y2:
            y_min: int = min(self.y1, self.y2)
            y_max: int = max(self.y1, self.y2)
            return [
                (self.x1, y, self.z1)
                for y in range(y_min, y_max + 1)
            ]

        if self.z1 != self.z2:
            z_min: int = min(self.z1, self.z2)
            z_max: int = max(self.z1, self.z2)
            return [
                (self.x1, self.y1, z)
                for z in range(z_min, z_max + 1)
            ]

        return [self.edge1]

class TileIndex:
    floor_level: int = 0
    floor: Brick = Brick((0, 0, 0), (0, 0, 0))

    tile_index: Dict[Position, Brick]

    def __init__(self) -> None:
        self.tile_index = {}

    def get(self, position: Position) -> Optional[Brick]:
        if position[2] <= self.floor_level:
            return self.floor
        return self.tile_index.get(position)

    def register_brick(self, brick: Brick) -> None:
        for cube in brick.get_cubes():
            self.tile_index[cube] = brick

    def is_floor(self, brick: Brick) -> bool:
        return brick is self.floor


def part_one() -> int:
    bricks: List[Brick] = []

    with open("input.txt", mode='r') as f_input:
        for line in f_input.readlines():
            line = line.strip()
            pos1_str, _sep, pos2_str = line.partition("~")
            pos1: Position = tuple(int(x) for x in pos1_str.split(","))  # type: ignore
            pos2: Position = tuple(int(x) for x in pos2_str.split(","))  # type: ignore

            bricks.append(Brick(pos1, pos2))
    
    bricks.sort(key=lambda br: br.get_min_z())

    # Bricks, sorted in the right order, can now be placed the lowest possible
    tile_index: TileIndex = TileIndex()
    supporting_bricks_index: DefaultDict[Brick, Set[Brick]] = defaultdict(set)

    for brick in bricks:
        current_shift: int = 0

        while True:
            new_shift: int = current_shift + 1
            supporting_bricks: Set[Brick] = {
                tile_index.get(substract_z(cube, new_shift)) for cube in brick.get_cubes() if tile_index.get(substract_z(cube, new_shift)) is not None  # type: ignore
            }
            if supporting_bricks:
                break
            # Can fall further down
            current_shift = new_shift

        brick.shift_z(current_shift)
        tile_index.register_brick(brick)
        supporting_bricks_index[brick] = supporting_bricks

    # Compute the bricks that can be removed
    unremovable_bricks: Set[Brick] = {
        sup.pop() for sup in supporting_bricks_index.values() if len(sup) == 1
    }
    unremovable_bricks.remove(TileIndex.floor)

    return len(bricks) - len(unremovable_bricks)


def part_two() -> int:
    bricks: List[Brick] = []

    with open("input.txt", mode='r') as f_input:
        for line in f_input.readlines():
            line = line.strip()
            pos1_str, _sep, pos2_str = line.partition("~")
            pos1: Position = tuple(int(x) for x in pos1_str.split(","))  # type: ignore
            pos2: Position = tuple(int(x) for x in pos2_str.split(","))  # type: ignore

            bricks.append(Brick(pos1, pos2))
    
    bricks.sort(key=lambda br: br.get_min_z())

    # Bricks, sorted in the right order, can now be placed the lowest possible
    tile_index: TileIndex = TileIndex()
    supporting_bricks_index: DefaultDict[Brick, Set[Brick]] = defaultdict(set)

    for brick in bricks:
        current_shift: int = 0

        while True:
            new_shift: int = current_shift + 1
            supporting_bricks: Set[Brick] = {
                tile_index.get(substract_z(cube, new_shift)) for cube in brick.get_cubes() if tile_index.get(substract_z(cube, new_shift)) is not None  # type: ignore
            }
            if supporting_bricks:
                break
            # Can fall further down
            current_shift = new_shift

        brick.shift_z(current_shift)
        tile_index.register_brick(brick)
        supporting_bricks_index[brick] = supporting_bricks

    # Remove each brick
    result: int = 0
    for brick in bricks:
        moved_bricks: Set[Brick] = {brick}
        found: bool = True

        while found is True:
            found = False
            for br, sup in supporting_bricks_index.items():
                if br not in moved_bricks and sup.issubset(moved_bricks):
                    found = True
                    moved_bricks.add(br)
        
        result += len(moved_bricks) - 1  # Do not count removed brick

    return result


print("Part one:", part_one())
print("Part two:", part_two())
