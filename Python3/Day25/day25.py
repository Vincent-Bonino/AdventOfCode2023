from collections import defaultdict
from queue import Queue
from typing import *

import networkx as nx
import matplotlib.pyplot as plt 


class Graph:
    neighbours: DefaultDict[str, Set[str]]

    def __init__(self) -> None:
        self.neighbours = defaultdict(set)

    def visualize(self) -> None:
        edges: List[List[str]] = []
        for key, values in self.neighbours.items():
            for val in values:
                edges.append([key, val])
        
        G = nx.Graph() 
        G.add_edges_from(edges) 
        nx.draw_networkx(G) 
        plt.show()

    def add_edge(self, node1: str, node2: str) -> None:
        self.neighbours[node1].add(node2)
        self.neighbours[node2].add(node1)

    def remove_edge(self, node1: str, node2: str) -> None:
        if node1 in self.neighbours[node2]:
            self.neighbours[node2].remove(node1)
            self.neighbours[node1].remove(node2)
        else:
            print(f"Unable to remove edge {node1}-{node2}")

    def get_result(self) -> int:
        start: str = list(self.neighbours.keys())[0]
        visited: Set[str] = set()
        queue: Queue[str] = Queue()

        queue.put(start)
        while not queue.empty():
            current: str = queue.get()
            if current in visited:
                continue

            visited.add(current)
            for val in self.neighbours[current]:
                queue.put(val)

        # If split in two, we visited the complement of node to the other part
        half_one_nbr: int = len(visited)
        half_two_nbr: int = len(self.neighbours) - half_one_nbr

        return half_one_nbr * half_two_nbr

def part_one() -> int:
    graph: Graph = Graph()

    # Parse input
    with open("input.txt", mode='r') as f_input:
        for line in f_input.readlines():
            key, _sep, values_str = line.strip().partition(": ")
            values: Set[str] = set(values_str.split(" "))
            for val in values:
                graph.add_edge(key, val)

    # == SPOILER ==
    # Infer (with ease) the three edges to cut
    # graph.visualize()

    # Example
    # graph.remove_edge("hfx", "pzl")
    # graph.remove_edge("bvb", "cmg")
    # graph.remove_edge("nvd", "jqt")

    graph.remove_edge("sxx", "zvk")
    graph.remove_edge("njx", "pbx")
    graph.remove_edge("pzr", "sss")

    # graph.visualize()
    return graph.get_result()


print("Part one:", part_one())