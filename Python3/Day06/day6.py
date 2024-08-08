"""Problem data.
T = total time of the race
d = achieved distance (what we want to optimize)

pressing_time = p
speed = T - p
d = v * t = (T - p) * p
d = T*p - p2

We want to win the race, so let R be the record
We want d > R
d > R
d - R > 0
(-1)*p² + T*p - R > 0

a = -1
b =  T
c = -R

Win if there is one or two solution:
solutions:
-b +- sqrt(delta) / 2a
delta = b² - 4ac

Here:
-T +- sqrt(delta) / -2  <=>  +- sqrt(delta) + T / 2
delta = T² - 4(-1)(-R) = T² - 4R

"""

from typing import *
import math


def solve_race(time: int, record: int) -> Tuple[Optional[float], Optional[float]]:
    delta: float = time * time - 4 * record

    if delta < 0:
        return (None, None)
    if delta == 0:
        solution = time / 2
        return (solution, None)

    solution1 = (-math.sqrt(delta) + time) / 2
    solution2 = (math.sqrt(delta) + time) / 2
    return (solution1, solution2)


def part_one() -> int:
    total_time: List[int] = []
    best_dist: List[int] = []

    with open("input.txt", mode="r") as f_input:
        lines: List[str] = f_input.readlines()

    total_time = [int(x) for x in lines[0].strip().partition(":")[2].split(" ") if x != ""]
    best_dist = [int(x) for x in lines[1].strip().partition(":")[2].split(" ") if x != ""]

    results: List[int] = []

    for time, record in zip(total_time, best_dist):
        sol1, sol2 = solve_race(time, record)

        if sol1 is None or sol2 is None:
            raise RuntimeError("No solution")

        min_sol: int = math.ceil(sol1)
        max_sol: int = math.floor(sol2)

        # Small tweak to take into account integer solutions which reduce the number of solutions
        range_delta: int = 1
        if int(sol1) == sol1:
            range_delta -= 1
        if int(sol2) == sol2:
            range_delta -= 1

        results.append(max_sol - min_sol + range_delta)

    res = 1
    for x in results:
        res = res * x
    return res


def part_two() -> int:
    """Exactly the same thing with a modified input (which I did manually)."""
    total_time: List[int] = []
    best_dist: List[int] = []

    with open("input-2.txt", mode="r") as f_input:
        lines: List[str] = f_input.readlines()

    total_time = [int(x) for x in lines[0].strip().partition(":")[2].split(" ") if x != ""]
    best_dist = [int(x) for x in lines[1].strip().partition(":")[2].split(" ") if x != ""]

    results: List[int] = []

    for time, record in zip(total_time, best_dist):
        sol1, sol2 = solve_race(time, record)

        if sol1 is None or sol2 is None:
            raise RuntimeError("No solution")

        min_sol: int = math.ceil(sol1)
        max_sol: int = math.floor(sol2)

        # Small tweak to take into account integer solutions which reduce the number of solutions
        range_delta: int = 1
        if int(sol1) == sol1:
            range_delta -= 1
        if int(sol2) == sol2:
            range_delta -= 1

        results.append(max_sol - min_sol + range_delta)

    res = 1
    for x in results:
        res = res * x
    return res

print("Part one:", part_one())
print("Part two:", part_two())
