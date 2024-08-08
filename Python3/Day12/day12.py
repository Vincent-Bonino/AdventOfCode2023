from enum import Enum
from typing import *
import functools

from tqdm import tqdm


class Spring(Enum):
	DAMAGED = "#"
	OPERATIONAL = "."
	UNKNOWN = "?"


class Line:
	"""Represent a line, with expected results and computational statuses."""

	springs: List[Spring]
	next_change_idx: int

	current_result: List[int]
	expected_result: List[int]

	last_is_damaged: bool

	def __init__(
		self,
		springs: List[Spring],
		results: List[int],
		index: int = 0,
		current_result: Optional[List[int]] = None,
		last_is_damaged: bool = False
	) -> None:
		self.springs = springs
		self.next_change_idx = index

		self.expected_result = results
		self.current_result = [] if current_result is None else current_result
		self.last_is_damaged = last_is_damaged

	def is_done(self) -> bool:
		return self.next_change_idx == len(self.springs)

	def update(self) -> None:
		next_spring: Spring = self.springs[self.next_change_idx]

		if next_spring is Spring.DAMAGED:
			if not self.current_result or not self.last_is_damaged:
				self.current_result.append(0)  # Add a new value if last one is 0 (operational)
			self.current_result[-1] += 1
			self.last_is_damaged = True

		elif next_spring is Spring.OPERATIONAL:
			self.last_is_damaged = False

		else:
			raise ValueError(f"Updating an on an Unknown spring (next_index={self.next_change_idx})")

		self.next_change_idx += 1

	def generate_next_lines(self) -> List['Line']:
		next_spring: Spring = self.springs[self.next_change_idx]

		if next_spring is not Spring.UNKNOWN:
			self.update()
			return [self]

		# Found Unknown, splitting in two branches
		before_springs: List[Spring] = self.springs[:self.next_change_idx]
		after_springs: List[Spring] = self.springs[self.next_change_idx+1:]

		alt_springs_1: List[Spring] = before_springs + [Spring.DAMAGED] + after_springs
		alt_springs_2: List[Spring] = before_springs + [Spring.OPERATIONAL] + after_springs

		alt_line_1: Line = Line(
			alt_springs_1, self.expected_result, index=self.next_change_idx,
			current_result=self.current_result.copy(), last_is_damaged=self.last_is_damaged,
		)
		alt_line_2: Line = Line(
			alt_springs_2, self.expected_result, index=self.next_change_idx,
			current_result=self.current_result, last_is_damaged=self.last_is_damaged,
		)

		alt_line_1.update()
		alt_line_2.update()
		return [alt_line_1, alt_line_2]

	def check_final_integrity(self) -> bool:
		result: bool = self.current_result == self.expected_result
		# print("[+]" if result else "[-]", self, self.current_result)
		return result

	def check_line_integrity(self) -> bool:
		"""Ensure the current result is compatible with the expected result."""
		if len(self.current_result) > len(self.expected_result):
			# Discard when finding more concurent springs than expected
			return False

		if not self.current_result:
			# Too soon to decide
			return True

		previous_ok: bool = all(self.expected_result[idx] == el for idx, el in enumerate(self.current_result[:-1]))
		last_ok: bool = self.current_result[-1] <= self.expected_result[len(self.current_result) - 1]

		if not (last_ok and previous_ok):
			# print("[-]", self, self.current_result)
			pass

		return last_ok and previous_ok

	def __repr__(self) -> str:
		return "".join(x.value for x in self.springs)

def count_all_possible_alternatives(line: Line) -> int:
	"""Recursive function generating and evaluation alternative version of the line.

	Its aim is to cut possibilities tree's branches as soon a possible.
	"""
	# Stop condition	
	if line.is_done():
		return 1 if line.check_final_integrity() else 0

	# Generate next lines
	next_lines: List[Line] = line.generate_next_lines()
	next_lines = [line for line in next_lines if line.check_line_integrity()]
	return sum(count_all_possible_alternatives(line) for line in next_lines)


def part_one() -> int:
	result: int = 0

	with open("input.txt", mode='r') as f_input:
		for idx, l in enumerate(f_input.readlines()):
			# print("============== Line", idx, l.strip())
			springs, _sep, results = l.strip().partition(" ")
			springs_list = [Spring(x) for x in springs]
			expected_result = [int(x) for x in results.split(",")]

			line: Line = Line(springs_list, expected_result)
			count: int = count_all_possible_alternatives(line)

			result += count

			# print(f"> Result = {count}")
	return result

# ==== Part two ====

@functools.cache
def count_possible_values(springs: str, expected: Tuple[int, ...], current_group_length: int = 0) -> int:
	"""Compute the number of possible value of given springs corresponding to expected values.

	Based on the idea that we know each time how to solve the smaller problem.
	We only have to determine how to use this result while "adding" one spring to it.

	Using cache to gain execution performances. Prevents having to re-compute the same thing multiple times.
	Using tuple instead of list becuase functools.cache require hasable types.
	
	Inspired by Allan Taylor's solution
	https://github.com/AllanTaylor314/AdventOfCode/blob/main/2023/12.py
	"""
	#print("[REC]", springs, expected, current_group_length)

	# Stop condition
	if not springs:
		if len(expected) > 1:
			# Unable to compute enough groups
			return 0
		if current_group_length != (expected[0] if expected else 0):
			# Unable to compute a long enough last group
			return 0
		return 1 

	current_spring: Spring = Spring(springs[0])
	remaining_springs: str = springs[1:]

	current_group_expected_length: int = expected[0] if expected else 0
	remaining_expected: Tuple[int, ...] = expected[1:]

	# Compute solution depending on small problems' solution
	if current_spring is Spring.UNKNOWN:  # ?
		# Create two smaller problems
		return (
			count_possible_values(Spring.DAMAGED.value + remaining_springs, expected, current_group_length) +
			count_possible_values(Spring.OPERATIONAL.value + remaining_springs, expected, current_group_length)
		)

	if current_spring is Spring.OPERATIONAL:  # .
		# If an expected group if finished, compute for smaller problem
		if current_group_expected_length == current_group_length:
			return count_possible_values(remaining_springs, remaining_expected)
		# If between two groups, compute for smaller problem
		if 0 == current_group_length:
			return count_possible_values(remaining_springs, expected)
		# Current group length is compatible with a solution
		return 0

	if current_spring is Spring.DAMAGED:
		# If we are about to create a too long group
		if current_group_length == current_group_expected_length:
			return 0
		return count_possible_values(remaining_springs, expected, current_group_length + 1)

	raise ValueError("Found unexpected spring value")


def part_two() -> int:
	result: int = 0

	with open("input.txt", mode='r') as f_input:
		#for idx, l in tqdm(enumerate(f_input.readlines()), unit="line", total=1000):
		for idx, l in enumerate(f_input.readlines()):
			springs, _sep, results = l.strip().partition(" ")

			# Make it 5 times longer
			springs = "?".join(spr for spr in [springs] * 5)
			results = ",".join(spr for spr in [results] * 5)

			expected_result: List[int] = [int(x) for x in results.split(",")]

			count: int = count_possible_values(springs, tuple(expected_result))
			result += count

			#print(f"> Result {idx:3} = {count}")
	return result

print("Part one:", part_one())
print("Part two:", part_two())
