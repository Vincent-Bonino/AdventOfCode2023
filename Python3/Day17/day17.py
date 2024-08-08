"""Basically, this is bad python code."""
from datetime import timedelta
from enum import Enum
from queue import PriorityQueue
from typing import *

Coordinates = Tuple[int, int]

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


DISTANCES: Dict['Node', int] = {}


class Node:
    position: Coordinates

    previous_directions: List[Direction]

    @property
    def dist(self) -> int:
        return DISTANCES[self]

    def __init__(self, position: Coordinates, previous_directions: List[Direction]) -> None:
        self.position = position
        self.previous_directions = previous_directions

    def get_str(self) -> str:
        dct = {
            Direction.NORTH: "^",
            Direction.EAST: ">",
            Direction.WEST: "<",
            Direction.SOUTH: "V",
        }
        if not self.previous_directions:
            return "."
        return dct[self.previous_directions[-1]]

    def __lt__(self, __value: object) -> bool:
        if not isinstance(__value, Node):
            return NotImplemented
        return self.dist < __value.dist

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Node):
            return NotImplemented
        return self.position == __value.position and self.previous_directions == __value.previous_directions

    def __hash__(self) -> int:
        return hash(self.position) + hash(tuple(self.previous_directions))

    def __repr__(self) -> str:
        return f"Node({self.position}; {self.previous_directions})"


class MetaGraph:
    """Contain any number of graph necessary to simulate the constraints."""
    city_blocks: List[List[int]]
    max_x: int
    max_y: int

    min_move_limit: int
    max_move_limit: int

    def __init__(self, lines: List[str], max_move_limit: int, min_move_limit: int) -> None:
        self.city_blocks = [[int(chr) for chr in line] for line in lines]
        self.max_x = len(self.city_blocks)
        self.max_y = len(self.city_blocks[0])
        self.min_move_limit = min_move_limit
        self.max_move_limit = max_move_limit

    def is_out_of_bounds(self, coord: Coordinates) -> bool:
        x, y = coord
        return x < 0 or y < 0 or self.max_x <= x or self.max_y <= y

    def get_value(self, coord: Coordinates) -> Optional[int]:
        return None if self.is_out_of_bounds(coord) else self.city_blocks[coord[0]][coord[1]]

    def get_value_unsafe(self, coord: Coordinates) -> int:
        return self.city_blocks[coord[0]][coord[1]]

    def get_adjacent_nodes(self, node: Node, end_coord: Coordinates) -> List[Node]:
        result: List[Node] = []

        prev_dir: List[Direction] = node.previous_directions
        for next_dir in Direction:
            new_position: Coordinates = (node.position[0] + next_dir.x, node.position[1] + next_dir.y)

            if self.is_out_of_bounds(new_position):
                continue

            if next_dir.opposite() in prev_dir:
                # Attempting a U turn, which is forbidden♂
                continue

            if next_dir in prev_dir and len(prev_dir) >= self.max_move_limit:
                # Last moves were all in the same direction, cannot continue
                continue

            if next_dir not in prev_dir and 0 < len(prev_dir) < self.min_move_limit:
                # Not moving enough, cannot turn
                # '0 <' for start_node
                continue

            if new_position == end_coord:
                futur_direction: List[Direction] = [next_dir] if next_dir not in prev_dir else prev_dir + [next_dir]
                if not (self.min_move_limit <= len(futur_direction) <= self.max_move_limit):
                    # Reaching the end with a too short path
                    continue

            if next_dir in prev_dir:
                # Continuing in the same direction
                result.append(Node(new_position, list(prev_dir) + [next_dir]))
            else:
                # Turning
                result.append(Node(new_position, [next_dir]))

        # Return the result
        # print(" > Adj nodes:", "\n\t".join([repr(x) for x in result]))
        return result

    def find_shortest_path(self, start_coord: Coordinates, end_coord: Coordinates) -> Tuple[List[Node], int]:
        """Dijkstra algorithm"""
        queue: PriorityQueue = PriorityQueue()
        distances: Dict[Node, int] = DISTANCES
        previous: Dict[Node, Node] = {}

        node_index: Dict[Node, bool] = {}

        for i in range(self.max_x):
            for j in range(self.max_y):
                for dir in Direction:
                    for f in range(1, self.max_move_limit + 1):
                        last_dir: List[Direction] = [dir] * f
                        node: Node = Node((i, j), last_dir)
                        node_index[node] = False
                        distances[node] = 1_000_000_000  # Almost infinity right ?

        # Special start node in "neutral" position
        start_node: Node = Node(start_coord, [])
        node_index[start_node] = False
        distances[start_node] = 0
        queue.put((0, start_node))

        while not queue.empty():
            current_score: int
            current_node: Node
            (current_score, current_node) = queue.get()

            if node_index[current_node]:
                continue

            # print("\nCurrent node:", current_node, self.get_value(current_node.position))

            for adj in self.get_adjacent_nodes(current_node, end_coord):
                tmp: int = distances[current_node] + self.get_value_unsafe(adj.position)

                if tmp < distances[adj]:
                    distances[adj] = tmp
                    previous[adj] = current_node
                    queue.put((tmp, adj))

        # Find out node
        min_dist: int = 1_000_000_000
        end_node: Optional[Node] = None
        for node, dist in distances.items():
            if node.position != end_coord:
                continue
            if dist < min_dist:
                min_dist = dist
                end_node = node

        if end_node is None:
            raise ValueError("No exit found")

        # Build path
        path: List[Node] = []
        last_node: Node = end_node
        while previous.get(last_node) is not None:
            path.append(last_node)
            last_node = previous[last_node]

        # Show
        # self.print_path(path)

        path = path[::-1]
        return path, distances[end_node]

    def print_path(self, path: List[Node], pp: bool = True) -> None:
        grid: List[List[Any]] = self.city_blocks.copy()
        for node in path:
            x: int = node.position[0]
            y: int = node.position[1]
            grid[x][y] = node.get_str() if pp else "#"
        # Display
        for line in grid:
            print("".join(str(x) for x in line))


def part_one() -> int:
    with open("input.txt", mode='r') as f_input:
        lines: List[str] = [l.strip() for l in f_input.readlines()]

    graph: MetaGraph = MetaGraph(lines, min_move_limit=1, max_move_limit=3)
    start: Coordinates = (0, 0)
    end: Coordinates = (graph.max_x-1, graph.max_y-1)

    _path, disance = graph.find_shortest_path(start, end)
    # graph.print_path(_path)
    return disance


def part_two() -> int:
    with open("input.txt", mode='r') as f_input:
        lines: List[str] = [l.strip() for l in f_input.readlines()]

    graph: MetaGraph = MetaGraph(lines, min_move_limit=4, max_move_limit=10)
    start: Coordinates = (0, 0)
    end: Coordinates = (graph.max_x-1, graph.max_y-1)

    _path, disance = graph.find_shortest_path(start, end)
    # graph.print_path(_path)
    return disance


print("Part one:", part_one())
print("Part two:", part_two())
