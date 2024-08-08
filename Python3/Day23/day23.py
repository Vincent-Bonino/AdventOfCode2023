from collections import defaultdict
from enum import Enum
from queue import LifoQueue, PriorityQueue
from typing import *


Coordinates: TypeAlias = Tuple[int, int]

def add_coord(coord1: Coordinates, coord2: Coordinates) -> Coordinates:
    return (coord1[0] + coord2[0], coord1[1] + coord2[1])


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

    def opposite(self) -> 'Direction':
        return Direction((-self.x, -self.y))

    def __repr__(self) -> str:
        return f"{self.name}"


def add_coord_and_dir(coord1: Coordinates, dir: Direction) -> Coordinates:
    return (coord1[0] + dir.x, coord1[1] + dir.y)


class TileType(Enum):
    FOREST =      "#"
    PATH =        "."
    SLOPE_NORTH = "^"
    SLOPE_EAST =  ">"
    SLOPE_SOUTH = "v"
    SLOPE_WEST =  "<"

    def is_slope(self) -> bool:
        return self in [TileType.SLOPE_EAST, TileType.SLOPE_NORTH, TileType.SLOPE_SOUTH, TileType.SLOPE_WEST]

    def get_in_directions(self) -> List[Direction]:
        return IN_DIRECTIONS[self]

    def get_out_directions(self) -> List[Direction]:
        return OUT_DIRECTIONS[self]


IN_DIRECTIONS: Dict[TileType, List[Direction]] = {
    TileType.FOREST: [],
    TileType.PATH: list(Direction),
    TileType.SLOPE_NORTH: list(set(Direction) - {Direction.NORTH.opposite()}),
    TileType.SLOPE_EAST: list(set(Direction) - {Direction.EAST.opposite()}),
    TileType.SLOPE_SOUTH: list(set(Direction) - {Direction.SOUTH.opposite()}),
    TileType.SLOPE_WEST: list(set(Direction) - {Direction.WEST.opposite()}),
}

OUT_DIRECTIONS: Dict[TileType, List[Direction]] = {
    TileType.FOREST: [],
    TileType.PATH: list(Direction),
    TileType.SLOPE_NORTH: [Direction.NORTH],
    TileType.SLOPE_EAST: [Direction.EAST],
    TileType.SLOPE_SOUTH: [Direction.SOUTH],
    TileType.SLOPE_WEST: [Direction.WEST],
}


class Step:
    coordinates: Coordinates
    walk_length: int
    direction: Direction

    visited_tiles: Set[Coordinates]
    last_node: Coordinates

    def __init__(self, coordinates: Coordinates, direction: Direction, walk_length: int = 0) -> None:
        self.coordinates = coordinates
        self.direction = direction
        self.walk_length = walk_length
        self.visited_tiles = {coordinates}

    @property
    def x(self) -> int:
        return self.coordinates[0]

    @property
    def y(self) -> int:
        return self.coordinates[1]

    def walk(self, direction: Direction) -> 'Step':
        new_step: Step = Step((self.x + direction.x, self.y + direction.y), direction, self.walk_length + 1)
        new_step.visited_tiles |= self.visited_tiles
        new_step.last_node = self.last_node
        return new_step

    def __lt__(self, other) -> bool:
        if not isinstance(other, Step):
            return NotImplemented
        return self.walk_length < other.walk_length

    def __repr__(self) -> str:
        return f"Step<{self.coordinates}, {self.walk_length}, {self.direction}>"


def generate_all_paths(
    graph: Dict[Coordinates, Dict[Coordinates, int]],
    current: Coordinates,
    dest: Coordinates,
    visited: Dict[Coordinates, bool],
    path: List[Coordinates],
    results: List[List[Coordinates]],
) -> None:
    """Shamelessly adapted from https://www.geeksforgeeks.org/find-paths-given-source-destination."""
    # Mark the current node as visited and store in path
    visited[current]= True
    path.append(current)

    # If current vertex is same as destination, then print
    # current path[]
    if current == dest:
        results.append(list(path))
    else:
        # If current vertex is not destination
        # Recur for all the vertices adjacent to this vertex
        for i in graph[current]:
            if visited[i]== False:
                generate_all_paths(graph, i, dest, visited, path, results)

    # Remove current vertex from path[] and mark it as unvisited
    path.pop()
    visited[current]= False


class SnowIsland:
    map: List[List[TileType]]

    max_x: int
    max_y: int

    start_position: Coordinates
    end_position: Coordinates

    def __init__(self, lines: List[str]) -> None:
        self.max_x: int = len(lines)
        self.max_y: int = len(lines[0])

        self.start_position = (0, lines[0].index("."))
        self.end_position = (self.max_x-1, lines[-1].index("."))

        self.map = [
            [TileType(chr) for chr in line]
            for line in lines
        ]

        print(f"\n[DBG] SnowIsland {self.max_x}x{self.max_y}, start={self.start_position}, end={self.end_position}")

    def is_out_of_bounds(self, coordinates: Coordinates) -> bool:
        x: int = coordinates[0]
        y: int = coordinates[1]
        return x < 0 or y < 0 or self.max_x <= x or self.max_y <= y

    def get_tile(self, coordinates: Coordinates) -> TileType:
        return self.map[coordinates[0]][coordinates[1]]

    def find_shortest_path(self, src: Coordinates, dst: Coordinates, nodes: List[Coordinates]) -> int:
        working_nodes: List[Coordinates] = nodes.copy()
        working_nodes.remove(src)
        working_nodes.remove(dst)

        queue: PriorityQueue[Tuple[int, Coordinates]] = PriorityQueue()
        queue.put((0, src))

        visited: Set[Coordinates] = set()
    
        result: int = -1

        while not queue.empty():
            dist, current_coordinates = queue.get()

            if current_coordinates == dst:
                result = dist
                break

            if current_coordinates in visited or current_coordinates in working_nodes:
                continue

            visited.add(current_coordinates)

            for next_dir in Direction:
                next_coord: Coordinates = add_coord_and_dir(current_coordinates, next_dir)

                if self.is_out_of_bounds(next_coord) or self.get_tile(next_coord) is TileType.FOREST:
                    continue

                queue.put((dist+1, next_coord))

        return result

    def find_longest_walk(self, ignore_slopes: bool = False) -> int:
        return self.find_longest_walk_with_slopes() if ignore_slopes is False else self.find_longest_walk_without_slopes()

    def find_longest_walk_without_slopes(self) -> int:
        nodes: List[Coordinates] = [self.start_position, self.end_position]

        # Find all nodes of the graph
        for x in range(self.max_x):
            for y in range(self.max_y):
                current_tile: TileType = self.get_tile((x, y))

                if current_tile is TileType.FOREST:
                    continue

                surroundings: List[bool] = [
                    self.get_tile(add_coord_and_dir((x, y), dir)) is not TileType.FOREST
                    for dir in Direction
                    if not self.is_out_of_bounds(add_coord_and_dir((x, y), dir))
                ]
                if surroundings.count(True) < 3:
                    continue

                # Here, the paths splits
                nodes.append((x, y))

        graph: Dict[Coordinates, Dict[Coordinates, int]] = defaultdict(dict)
        # Compute the distance between each node
        for src in nodes:
            for dst in nodes:
                if src is dst:
                    continue
                if dst in graph[src]:
                    graph[dst][src] = graph[src][dst]
                    continue
                val: int = self.find_shortest_path(src, dst, nodes)
                if val > 0:
                    graph[dst][src] = val

        # Generate all paths from start to end
        results: List[List[Coordinates]] = []
        generate_all_paths(graph, self.start_position, self.end_position, defaultdict(bool), [], results)

        # Compute the length of each of these paths
        lengths: List[int] = []
        for path in results:
            length: int = 0
            prev: Optional[Coordinates] = None

            for coord in path:
                # Init
                if prev is None:
                    prev = coord
                    continue
                # Normal case
                length += graph[prev][coord]
                prev = coord
            
            lengths.append(length)

        # From all path from start to end, pick the longest
        return max(lengths)

    def find_longest_walk_with_slopes(self) -> int:
        walk_lengths: List[int] = []

        start_step: Step = Step(self.start_position, Direction.SOUTH)
        start_step.last_node = self.start_position

        queue: LifoQueue[Step] = LifoQueue()
        queue.put(start_step)

        # Store the biggest walk on this tile, allowing to discard every others
        tile_index: Dict[Coordinates, int] = {}

        while not queue.empty():
            current_step = queue.get()
            current_tile: TileType = self.get_tile(current_step.coordinates)

            # Stop condition
            if current_step.coordinates == self.end_position:
                walk_lengths.append(current_step.walk_length)
                continue

            # If already visited, with a longer walk, ignore
            if tile_index.get(current_step.coordinates, -1) > current_step.walk_length:
                continue

            # Register this as the biggest length at this tile
            tile_index[current_step.coordinates] = current_step.walk_length

            # Attempt to walk all around
            for next_dir in current_tile.get_out_directions():

                # Do not walk backwards
                if next_dir is current_step.direction.opposite():
                    continue

                next_position: Coordinates = (current_step.x + next_dir.x, current_step.y + next_dir.y)

                # Do not walk out of the map
                if self.is_out_of_bounds(next_position):
                    continue

                # Do not walk on an already visited tile
                if next_position in current_step.visited_tiles:
                    continue

                next_tile: TileType = self.get_tile(next_position)

                # Do not walk on forests
                if next_tile is TileType.FOREST:
                    continue

                # Prevent walking a slope in the bad direction (will be backwards next time)
                if next_dir not in next_tile.get_in_directions():
                    continue

                new_step: Step = current_step.walk(next_dir)

                # If already visited, with a longer walk, ignore
                if tile_index.get(new_step.coordinates, -1) > new_step.walk_length:
                    continue

                # Walk this way
                queue.put(new_step)

        return max(walk_lengths)


def part_one() -> int:
    with open("input.txt", mode='r') as f_input:
        lines: List[str] = [l.strip() for l in f_input.readlines()]
    
    snow_island: SnowIsland = SnowIsland(lines)
    return snow_island.find_longest_walk(ignore_slopes=False)

def part_two() -> int:
    with open("input.txt", mode='r') as f_input:
        lines: List[str] = [l.strip() for l in f_input.readlines()]
    
    snow_island: SnowIsland = SnowIsland(lines)
    return snow_island.find_longest_walk(ignore_slopes=True)


print("Part one:", part_one())
print("Part two:", part_two())
