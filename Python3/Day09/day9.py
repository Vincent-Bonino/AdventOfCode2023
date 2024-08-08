from typing import *


class History:
    """Represent the evolution on one value."""

    history: List[int]

    def __init__(self, line: str) -> None:
        self.history: List[int] = [int(x) for x in line.strip().split(" ")]

        # self.extrapolate_next()
        self.extrapolate_prev()

    def get_first(self) -> int:
        return self.history[0]

    def get_last(self) -> int:
        return self.history[-1]

    def extrapolate_next(self) -> None:
        tmp: Dict[int, List[int]] = {
            0: self.history
        }

        line_counter: int = 0
        # Compute sub values
        while not all(x == 0 for x in tmp[line_counter]):

            # pylint: disable=unsubscriptable-object  # Zip if not subscripted, it is the values given to it
            it_list: zip[Tuple[int, int]] = zip(tmp[line_counter][:-1], tmp[line_counter][1:])

            line_counter += 1
            tmp[line_counter] = [y - x for x, y in it_list]

        # Rebuild values
        for idx in range(line_counter - 1, -1, -1):
            value_to_add: int = tmp[idx][-1] + tmp[idx + 1][-1]
            tmp[idx].append(value_to_add)

        # for k, v in tmp.items():
        #    print(f"({len(v):2}) {k}: {v}")

    def extrapolate_prev(self) -> None:
        tmp: Dict[int, List[int]] = {
            0: self.history
        }

        line_counter: int = 0
        # Compute sub values
        while not all(x == 0 for x in tmp[line_counter]):

            # pylint: disable=unsubscriptable-object  # Zip if not subscripted, it is the values given to it
            it_list: zip[Tuple[int, int]] = zip(tmp[line_counter][:-1], tmp[line_counter][1:])

            line_counter += 1
            tmp[line_counter] = [y - x for x, y in it_list]

        # Rebuild values
        for idx in range(line_counter - 1, -1, -1):
            value_to_add: int = tmp[idx][0] - tmp[idx + 1][0]
            tmp[idx].insert(0, value_to_add)

        #for k, v in tmp.items():
        #   print(f"({len(v):2}) {k}: {v}")


histories: List[History] = []
with open("input.txt", mode='r') as f_input:
    for line in f_input.readlines():
        histories.append(History(line))


def part_one(histories: List[History]) -> int:
    return sum(hist.get_last() for hist in histories)


def part_two(histories: List[History]) -> int:
    return sum(hist.get_first() for hist in histories)


#print("Part one:", part_one(histories))
print("Part two:", part_two(histories))
