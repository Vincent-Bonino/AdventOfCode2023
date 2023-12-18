from datetime import timedelta
from enum import Enum
from queue import PriorityQueue
from time import time
from typing import *

from tqdm import tqdm

Coordinates = Tuple[int, int]


class CheckableQueue(PriorityQueue):
    def __contains__(self, item):
        with self.mutex:
            return item in self.queue


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

    move_limit: int

    def __init__(self, lines: List[str], move_limit: int) -> None:
        self.city_blocks = [[int(chr) for chr in line] for line in lines]
        self.max_x = len(self.city_blocks)
        self.max_y = len(self.city_blocks[0])
        self.move_limit = move_limit

    def is_out_of_bounds(self, coord: Coordinates) -> bool:
        x, y = coord
        return x < 0 or y < 0 or self.max_x <= x or self.max_y <= y

    def get_value(self, coord: Coordinates) -> Optional[int]:
        return None if self.is_out_of_bounds(coord) else self.city_blocks[coord[0]][coord[1]]

    def get_value_unsafe(self, coord: Coordinates) -> int:
        return self.city_blocks[coord[0]][coord[1]]

    def get_adjacent_nodes(self, node: Node) -> List[Node]:
        result: List[Node] = []

        prev_dir: List[Direction] = node.previous_directions
        for next_dir in Direction:
            new_position: Coordinates = (node.position[0] + next_dir.x, node.position[1] + next_dir.y)

            if self.is_out_of_bounds(new_position):
                continue

            if len(prev_dir) >= self.move_limit:
                if next_dir in prev_dir or next_dir.opposite() in prev_dir:
                    # Last moves were all in the same direction, cannot continue
                    # Or attempty a U turn, which is forbidden
                    continue

            if next_dir in prev_dir:
                # Continuing in the same direction
                result.append(Node(new_position, list(prev_dir) + [next_dir]))
            else:
                # Turning
                result.append(Node(new_position, [next_dir]))

        # Return the result
        return result

    def find_shortest_path(self, start_coord: Coordinates, end_coord: Coordinates) -> Tuple[List[Node], int]:
        """Dijkstra algorithm"""
        queue: PriorityQueue = PriorityQueue()
        distances: Dict[Node, int] = DISTANCES
        previous: Dict[Node, Node] = {}

        node_index: Dict[Node, Node] = {}

        for i in range(self.max_x):
            for j in range(self.max_y):
                for dir in Direction:
                    for f in range(1, self.move_limit + 1):
                        last_dir: List[Direction] = [dir] * f
                        node: Node = Node((i, j), last_dir)
                        node_index[node] = node
                        distances[node] = 1_000_000_000  # Almost infinity right ?
                        queue.put(node)

        # Special start node in "neutral" position
        start_node: Node = Node((0, 0), [])
        node_index[start_node] = start_node
        distances[start_node] = 0
        queue.put(start_node)

        start: float = time()
        rate: float = 0
        solved: int = -1
        stats: str = ""
        while bool(queue) is True:
            # ===== STATS
            solved += 1
            if False and solved % 100 == 99:
                rate = solved / (time() - start)
                stats = f"rate: {rate}/s, ETA: {timedelta(seconds=(len(queue.queue) / rate))}"
            print(f"Remaining {len(queue.queue)} items, {stats}",  end="\r", flush=True)
            # ====

            current_node: Node = queue.get()

            # print("\nCurrent node:", current_node, self.get_value(current_node.position))

            for adj in self.get_adjacent_nodes(current_node):
                if node_index[adj] not in queue.queue:
                    continue

                adj = node_index[adj]
                tmp: int = distances[current_node] + self.get_value_unsafe(adj.position)

                if tmp < distances[adj]:
                    distances[adj] = tmp
                    previous[adj] = current_node
                    node_index[adj].previous_directions = list(adj.previous_directions)

        # Find out node
        min_dist: int = 1_000_000_000
        end_node: Optional[Node] = None
        for hsh, node in node_index.items():
        #for hsh, node in tqdm(node_index.items()):
            if node.position != end_coord:
                continue
            dist: int = distances[hsh]
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
        self.print_path(path)

        path = path[::-1]
        # print("Path:", "\n".join(repr(x) for x in path))

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

    graph: MetaGraph = MetaGraph(lines, 3)
    start: Coordinates = (0, 0)
    end: Coordinates = (graph.max_x-1, graph.max_y-1)
    path, disance = graph.find_shortest_path(start, end)

    return disance


print("Part one:", part_one())
