from typing import *


class ValueRange:
    """Represent a range."""

    start: int
    end: int
    length: int

    def __init__(self, start: int, end: int) -> None:
        self.start: int = start
        self.end: int = end
        self.length: int = end - start

    # Comparison

    def intersects(self, other: 'ValueRange') -> bool:
        """Determine if two ranges intersect."""
        # 1. No intersection
        if self.end <= other.start or other.end <= self.start:
            return False
        return True

    def is_overlapped_by(self, other: 'ValueRange') -> bool:
        return other.start <= self.start and self.end <= other.end

    # Operations

    def apply_mapping(self, src_range: 'ValueRange', dst_range: 'ValueRange') -> Set['ValueRange']:
        """Return ranges defined by applying the mapping to this range."""
        # 1. Self is contained in the mapping
        if self.is_overlapped_by(src_range):
            start_delta: int = self.start - src_range.start
            # print(f"> Input {self} overlapped by src_range {src_range}", start_delta)
            # print("> Returning", ValueRange(dst_range.start + start_delta, dst_range.start + start_delta + self.length))
            return {ValueRange(dst_range.start + start_delta, dst_range.start + start_delta + self.length)}

        result: Set['ValueRange'] = set()

        # 2. The mapping is contained in self.
        # We want to map already mapped values (in self) to their new values
        # Thus, we are looking for values in self we can also find in src_range
        # Other values (in self but not in src_range) will be mapped to themselves
        if src_range.is_overlapped_by(self):
            # print(f"> src_range {src_range} overlapped by input {self}")
            result.add(ValueRange(self.start, src_range.start))  # Values before mapping
            result.add(ValueRange(src_range.end, self.end))  # Values after mapping
            result.add(dst_range)  # Mapped values
            return result

        # 3. The two ranges are partially overlapping.
        # This will produce two ranges, a subpart of the dst_range and a subpart of self
        if self.start < src_range.start:
            overlap_length: int = self.end - src_range.start  # self.end can't be higher than src_range.end (case 2)
            result.add(ValueRange(self.start, src_range.start))  # Unmapped values smaller than mapping
            result.add(ValueRange(dst_range.start, dst_range.start + overlap_length))
        else:  # src_range.start < self.start
            overlap_length = src_range.end - self.start  # src_range.end can't be higher than self.end (case 1)
            result.add(ValueRange(src_range.end, self.end))  # Unmapped values higher than mapping
            result.add(ValueRange(dst_range.start + (dst_range.length - overlap_length), dst_range.end))
        return result

    def __repr__(self) -> str:
        return f"ValueRange(start={self.start}, end={self.end})"


class RangeManager:

    ranges: Set[ValueRange]

    def __init__(self, input_ranges: Set[ValueRange]) -> None:
        self.ranges: Set[ValueRange] = input_ranges

    def apply_range(self, dst_start, src_start, length) -> None:
        _before_state = self.ranges.copy()

        src_range: ValueRange = ValueRange(src_start, src_start + length)
        dst_range: ValueRange = ValueRange(dst_start, dst_start + length)

        # Look for intersection, and remove from list
        intersecting_ranges: Set[ValueRange] = set()
        for rng in self.ranges:
            if rng.intersects(src_range):
                intersecting_ranges.add(rng)
        self.ranges = self.ranges - intersecting_ranges

        # Compute the produced ranges
        produced_ranges: Set[ValueRange] = set()
        for int_range in intersecting_ranges:
            for prod_range in int_range.apply_mapping(src_range, dst_range):
                produced_ranges.add(prod_range)

        # Add them back
        self.ranges = self.ranges.union(produced_ranges)

        if False and self.ranges.difference(_before_state):
            print("Mapping src:", src_range)
            print("Mapping dst:", dst_range)
            print("Previousstate:",  " - ".join(repr(x) for x in sorted(_before_state, key=lambda x: x.start)))
            self.print_state()
            print()
            #input()
            #breakpoint()


    def print_state(self) -> None:
        print("Current state:", " - ".join(repr(x) for x in sorted(self.ranges, key=lambda x: x.start)))

class Maping:
    """Represent a X to Y mapping."""

    # Input range, dst_start
    map: Dict[range, int]

    def __init__(self) -> None:
        self.map = {}

    def add_range(self, dst_start, src_start, length) -> None:
        self.map[range(src_start, src_start + length)] = dst_start

    def map_value(self, value: int) -> int:
        for rang, dst_start in self.map.items():
            if value in rang:
                return dst_start + (value - rang.start)
        return value

    def map_range(self, value_range: List[int]):
        return [self.map_value(val) for val in value_range]


def part_one() -> int:
    seeds: List[int] = []
    mapings: List[Maping] = []

    with open("input.txt", mode='r') as f_input:
        for line in f_input.readlines():
            line = line.strip()

            # Ignore empty lines
            if not line:
                continue

            if line.startswith("seeds:"):
                raw_seeds = line.partition(":")[2]
                seeds = [int(x) for x in raw_seeds.split(" ") if x != ""]

            elif line.endswith("map:"):
                mapings.append(Maping())  # add a new mapping

            else:  # Adding a range to the last Maping
                values: List[int] = [int(x) for x in line.split(" ") if x != ""]
                if len(values) != 3:
                    raise ValueError(f"Unable to find 3 digits in line {line}")

                mapings[-1].add_range(*values)

    # Compute minimum
    current_range: List[int] = list(seeds)
    for mp in mapings:
        current_range = mp.map_range(current_range)

    return min(current_range)


def part_two() -> int:
    range_manager: Optional[RangeManager] = None

    with open("example.txt", mode='r') as f_input:
        for line in f_input.readlines():
            line = line.strip()

            # Ignore empty lines
            if not line:
                continue

            if line.startswith("seeds:"):
                raw_seeds: str = line.partition(":")[2]
                raw_int_seeds: List[int] = [int(x) for x in raw_seeds.split(" ") if x != ""]
                seeds: Set[ValueRange] = {
                    ValueRange(raw_int_seeds[idx], raw_int_seeds[idx] + raw_int_seeds[idx+1])
                    for idx in range(0, len(raw_int_seeds), 2)
                }
                range_manager = RangeManager(seeds)

            elif line.endswith("map:"):
                range_manager.print_state()
                print("\n", line)
                continue  # Ignore these lines

            else:  # Create a ValueRange
                values: List[int] = [int(x) for x in line.split(" ") if x != ""]
                if len(values) != 3:
                    raise ValueError(f"Unable to find 3 digits in line {line}")
                if range_manager is None:
                    raise RuntimeError("Range manager should be initialized")
                range_manager.apply_range(*values)

    if range_manager is None:
        raise RuntimeError("Range manager should be initialized")
    print("\n".join(repr(x) for x in range_manager.ranges))
    return min(range.start for range in range_manager.ranges)


#print("Part one:", part_one())
print("Part two:", part_two())
