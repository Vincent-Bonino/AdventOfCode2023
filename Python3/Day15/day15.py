from collections import defaultdict
from dataclasses import dataclass
from typing import *

@dataclass
class Lens:
    label: str
    focal_length: int

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, str):
            return __value == self.label
        return NotImplemented

def hash(value: str) -> int:
    """HASH implementation."""
    result: int = 0
    for el in value:
        result = ((result + ord(el)) * 17) % 256
    return result


def part_one() -> int:
    with open("input.txt", mode='r') as f_input:
        line: str = f_input.readline().strip()
    return sum(hash(seq) for seq in line.split(","))


def part_two() -> int:
    with open("input.txt", mode='r') as f_input:
        line: str = f_input.readline().strip()

    hashmap: DefaultDict[int, List[Lens]] = defaultdict(list)

    for seq in line.split(","):
        if seq.endswith("-"):
            label, _sep, _empty = seq.partition("-")
            hsh: int = hash(label)
            if label in hashmap[hsh]:
                hashmap[hsh].remove(label)

        else:
            label, _eq, focal_length = seq.partition("=")
            lens: Lens = Lens(label, int(focal_length))
            hsh: int = hash(label)
            if label in hashmap[hsh]:
                hashmap[hsh][hashmap[hsh].index(label)] = lens
            else:
                hashmap[hsh].append(lens)
   
    return sum(
        (hsh+1) * (index+1) * lens.focal_length
        for hsh, lenses in hashmap.items()
        for index, lens in enumerate(lenses)
    )


print("Part one:", part_one())
print("Part two:", part_two())
