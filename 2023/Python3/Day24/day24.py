from dataclasses import dataclass
from typing import *


@dataclass
class Point2:
    x: Union[int, float]
    y: Union[int, float]


@dataclass
class Point3:
    x: Union[int, float]
    y: Union[int, float]
    z: Union[int, float]


@dataclass
class Hailstone:
    start_point: Point3
    speed: Point3

    @property
    def a2(self) -> float:
        return self.speed.y / self.speed.x

    @property
    def b2(self) -> float:
        return self.start_point.y - self.a2*self.start_point.x

    def get_future_intersection_2d(self, other: 'Hailstone') -> Optional[Point2]:
        """Solve equations for intersection."""
        if self.a2 == other.a2:
            return None

        int_x: float = (other.b2 - self.b2) / (self.a2 - other.a2)
        int_y: float = self.a2 * int_x + self.b2
        intersection_point: Point2 = Point2(int_x, int_y)

        # Is in self's future ?
        dx: float = (intersection_point.x - self.start_point.x) / self.speed.x
        dy: float = (intersection_point.x - self.start_point.x) / self.speed.x
        if dx < 0 or dy < 0:
            return None

        # Is in other's future ?
        dx: float = (intersection_point.x - other.start_point.x) / other.speed.x
        dy: float = (intersection_point.x - other.start_point.x) / other.speed.x
        if dx < 0 or dy < 0:
            return None

        return intersection_point



def part_one() -> int:
    MIN_VALUE: int = 200000000000000
    MAX_VALUE: int = 400000000000000

    result: int = 0
    stones: List[Hailstone] = []

    with open("input.txt", mode='r') as f_input:
        for line in f_input.readlines():
            line = line.strip()
            pos, _sep, vel = line.partition(" @ ")
            start_point: Point3 = Point3(*[int(x) for x in pos.split(", ")])
            velocity: Point3 = Point3(*[int(x) for x in vel.split(", ")])

            stones.append(Hailstone(start_point, velocity))

    # Compute intersection points
    for idx1, stone1 in enumerate(stones):
        for idx2, stone2 in enumerate(stones):
            if idx2 <= idx1:
                continue
            intersection_point: Optional[Point2] = stone1.get_future_intersection_2d(stone2)
            if intersection_point is None:
                continue
            if MIN_VALUE <= intersection_point.x <= MAX_VALUE and MIN_VALUE <= intersection_point.y <= MAX_VALUE:
                result += 1

    return result


print("Part one:", part_one())
#print("Part two:", part_two())
