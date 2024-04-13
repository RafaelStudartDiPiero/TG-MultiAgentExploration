import csv
from typing import Tuple

import matplotlib.pyplot as plt
import networkx as nx


# def construct_graph(n_lines: int, n_columns: int):
#     # TODO Change this to use nx
#     m = maze(n_lines, n_columns)
#     m.CreateMaze(loopPercent=0, theme="light")
#     return m


# def load_graph(n_lines: int, n_columns: int, file_path: str):
#     # TODO Change this to use nx
#     m = maze(n_lines, n_columns)
#     m.CreateMaze(loopPercent=0, theme="light", loadMaze=file_path)
#     return m


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

            if north:
                north_cell = f"{i-1},{j}"
                edges.append((cell_id, north_cell))
            if east:
                east_cell = f"{i},{j+1}"
                edges.append((cell_id, east_cell))
            if south:
                south_cell = f"{i+1},{j}"
                edges.append((cell_id, south_cell))
            if west:
                west_cell = f"{i},{j-1}"
                edges.append((cell_id, west_cell))

            maze_graph.add_node(cell_id)
            if len(edges) > 0:
                maze_graph.add_edges_from(edges)
    maze_graph.nodes["1,1"]["finish"] = True
    maze_graph.nodes["1,1"]["color"] = "green"

    maze_graph.nodes[f"{rows},{columns}"]["color"] = "red"

    return maze_graph, rows, columns


def display_maze(maze_graph: nx.Graph, rows: int, columns: int, ax=None):
    # Grid Positions
    pos = {
        node_id: (int(node_id.split(",")[1]), rows - int(node_id.split(",")[0]))
        for node_id in maze_graph.nodes()
    }

    # Node Colors
    node_colors = []
    for node_id in maze_graph.nodes():
        if "color" in maze_graph.nodes[node_id]:
            node_colors.append(maze_graph.nodes[node_id]["color"])
        else:
            node_colors.append("lightblue")

    if ax is not None:
        ax.clear()

    # Draw the maze graph using NetworkX and matplotlib with grid layout
    nx.draw(
        maze_graph,
        pos,
        with_labels=True,
        node_size=500,
        node_color=node_colors,
        font_size=8,
        ax=ax,
    )
    plt.title("Maze Graph (Grid Layout)")
    plt.show()
