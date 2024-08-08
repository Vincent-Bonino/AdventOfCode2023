from math import log2
from itertools import zip_longest
from typing import *
import functools

def transpose_string_array(array: List[str]) -> List[str]:
    """Require all strings to be the same length."""
    return [''.join(s) for s in zip(*array)]


class Valley:
    """Represent a valley with rocks and ashes."""

    ground: List[str]

    # Identify rock placements
    row_ids: List[int]
    col_ids: List[int]

    def __init__(self, lines: List[str]) -> None:
        self.ground = lines
        self.build_inner_values()

    def build_inner_values(self) -> None:
        # Compute rows
        self.row_ids = [sum(1 << idx if el == "#" else 0 for idx, el in enumerate(row)) for row in self.ground]

        # Compute cols by transposing
        transposed_lines: List[str] = transpose_string_array(self.ground)
        self.col_ids = [sum(1 << idx if el == "#" else 0 for idx, el in enumerate(row)) for row in transposed_lines]

    def compute_self_values(self) -> List[Tuple[int, int]]:
        return Valley.compute_values(self.row_ids, self.col_ids)

    @staticmethod
    def test_value(ids: List[int], first_value: int, debug: str = "") -> bool:
        length: int = min(first_value + 1, len(ids) - first_value - 1)
        for ind in range(length):
            if ids[first_value - ind] != ids[first_value + 1 + ind]:
                return False
        return True

    @staticmethod
    def compute_values(row_ids: List[int], col_ids: List[int]) -> List[Tuple[int, int]]:
        mirror_row_number: List[int] = []
        mirror_col_number: List[int] = []

        # Find two consecutive equal rows
        for ind in range(len(row_ids)-1):
            if not row_ids[ind] == row_ids[ind+1]:
                continue
            if Valley.test_value(row_ids, ind, debug="row"):
                mirror_row_number.append(ind + 1)

        # Find two consecutive equal cols
        for ind in range(len(col_ids)-1):
            if not col_ids[ind] == col_ids[ind+1]:
                continue
            if Valley.test_value(col_ids, ind, debug="col"):
                mirror_col_number.append(ind + 1)

        return [(x, y) for x, y in zip_longest(mirror_row_number, mirror_col_number, fillvalue=0)]

def process(current_lines: List[str]) -> List[Tuple[int, int]]:
    if not current_lines:
        return [(0, 0)]
    valley: Valley = Valley(current_lines)
    results: List[Tuple[int, int]] = valley.compute_self_values()
    return results


def part_one() -> int:
    above_rows: int = 0
    left_cols: int = 0

    with open("input.txt", mode='r') as f_input:
        current_lines: List[str] = []

        for line in f_input.readlines():
            line = line.strip()
            if line:
                current_lines.append(line)
                continue

            # Process
            row_nbr, col_nbr = process(current_lines)[0]
            above_rows += row_nbr
            left_cols += col_nbr
            # Reset !
            current_lines.clear()

        # Final process, just in case ;)
        row_nbr, col_nbr = process(current_lines)[0]
        above_rows += row_nbr
        left_cols += col_nbr
    return left_cols + 100*above_rows


def replace_value(lines: List[str], i: int, j: int) -> List[str]:
    new_lines: List[str] = lines.copy()
    new: str = '#' if new_lines[i][j] == "." else '.'
    new_lines[i] = new_lines[i][:j] + new + new_lines[i][j+1:]
    return new_lines

def process_2(current_lines: List[str]) -> Tuple[int, int]:
    original_result: Tuple[int, int] = process(current_lines)[0]

    for i in range(len(current_lines)):
        for j in range(len(current_lines[0])):
            new_results: List[Tuple[int, int]] = process(replace_value(current_lines, i, j))
            # print(i, j, original_result, new_results)
            for nres in new_results:
                if nres == original_result:
                    # Ignoring when result to not change
                    continue
                if nres[0] != original_result[0]:
                    return (nres[0], 0)
                if nres[1] != original_result[1]:
                    return (0, nres[1])     

    raise ValueError("Found no new reflexion")

def part_two() -> int:
    above_rows: int = 0
    left_cols: int = 0

    with open("input.txt", mode='r') as f_input:
        current_lines: List[str] = []

        for line in f_input.readlines():
            line = line.strip()
            if line:
                current_lines.append(line)
                continue

            # Process
            row_nbr, col_nbr = process_2(current_lines)
            above_rows += row_nbr
            left_cols += col_nbr
            # Reset !
            current_lines.clear()

        # Final process, just in case ;)
        row_nbr, col_nbr = process_2(current_lines)
        above_rows += row_nbr
        left_cols += col_nbr
    return left_cols + 100*above_rows


print("Part one:", part_one())
print("Part two:", part_two())
