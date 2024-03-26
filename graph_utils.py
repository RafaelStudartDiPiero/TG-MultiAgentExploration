import csv

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


def convert_maze(file_path: str) -> nx.Graph:
    # Create an empty graph
    maze_graph = nx.Graph()

    # Read the CSV file and add nodes and edges to the graph
    with open(file_path, mode="r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            cell_str = row["cell"].strip(
                "()"
            )  # Remove parentheses from cell coordinates
            cell_coords = tuple(
                map(int, cell_str.split(", "))
            )  # Convert coordinates to tuple
            node_id = f"{cell_coords[0]},{cell_coords[1]}"  # Generate node ID
            edges = [
                (
                    (node_id, f"{cell_coords[0]+1},{cell_coords[1]}")
                    if int(row["E"])
                    else None
                ),
                (
                    (node_id, f"{cell_coords[0]-1},{cell_coords[1]}")
                    if int(row["W"])
                    else None
                ),
                (
                    (node_id, f"{cell_coords[0]},{cell_coords[1]+1}")
                    if int(row["N"])
                    else None
                ),
                (
                    (node_id, f"{cell_coords[0]},{cell_coords[1]-1}")
                    if int(row["S"])
                    else None
                ),
            ]

            # Add node to the graph
            maze_graph.add_node(node_id)

            # Add edges to the graph
            for edge in edges:
                if edge:
                    maze_graph.add_edge(*edge)

    return maze_graph
