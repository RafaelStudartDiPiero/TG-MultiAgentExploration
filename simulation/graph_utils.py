import csv
from typing import Tuple

import matplotlib.pyplot as plt
import networkx as nx

from pyamaze import maze


def construct_graph(n_lines: int, n_columns: int):
    # TODO Change this to use nx
    m = maze(n_lines, n_columns)
    m.CreateMaze(loopPercent=0, theme="light")
    return m


def load_graph(n_lines: int, n_columns: int, file_path: str):
    # TODO Change this to use nx
    m = maze(n_lines, n_columns)
    m.CreateMaze(loopPercent=0, theme="light", loadMaze=file_path)
    return m


def convert_maze(file_path: str) -> Tuple[nx.Graph, int, int]:
    # Create an empty graph
    maze_graph = nx.Graph()

    # Read the CSV file and add nodes and edges to the graph
    with open(file_path, mode="r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        csv_rows = []
        for row in csv_reader:
            csv_rows.append(row)

    last_cell = csv_rows[-1]["cell"].strip("()").split(",")
    rows = int(last_cell[0])
    columns = int(last_cell[1])

    for i in range(1, rows + 1):
        for j in range(1, columns + 1):

            position = (i - 1) + (j - 1) * rows
            cell = csv_rows[position]

            cell_id = f"{i},{j}"
            east = bool(int(cell["E"]))
            west = bool(int(cell["W"]))
            north = bool(int(cell["N"]))
            south = bool(int(cell["S"]))
            edges = []

            if east:
                east_cell = f"{i},{j+1}"
                edges.append((cell_id, east_cell))
            if west:
                west_cell = f"{i},{j-1}"
                edges.append((cell_id, west_cell))
            if north:
                north_cell = f"{i-1},{j}"
                edges.append((cell_id, north_cell))
            if south:
                south_cell = f"{i+1},{j}"
                edges.append((cell_id, south_cell))

            maze_graph.add_node(cell_id)
            if len(edges) > 0:
                maze_graph.add_edges_from(edges)

    return maze_graph, rows, columns


def display_maze(maze_graph: nx.Graph, rows: int, columns: int):
    pos = {
        node_id: (int(node_id.split(",")[1]), rows - int(node_id.split(",")[0]))
        for node_id in maze_graph.nodes()
    }
    # Draw the maze graph using NetworkX and matplotlib with grid layout
    nx.draw(
        maze_graph,
        pos,
        with_labels=True,
        node_size=500,
        node_color="lightblue",
        font_size=8,
    )
    plt.title("Maze Graph (Grid Layout)")
    plt.show()
