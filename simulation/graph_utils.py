import csv
from typing import Tuple, Optional

import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout


def load_graph(file_path) -> nx.Graph:
    return nx.read_graphml(file_path)


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


def preprocess_node_ids(graph: nx.Graph):
    """Replace commas with spaces in all node IDs of the graph."""
    for node_id in graph.nodes():
        new_node_id = node_id.replace(",", " ")
        if new_node_id != node_id:
            # Update the node ID if it was modified
            graph = nx.relabel_nodes(graph, {node_id: new_node_id})
    return graph


def get_node_label(graph: nx.Graph, node_id: str) -> str:
    label = f"{node_id}"
    if graph.nodes[node_id].get("status"):
        if (
            graph.nodes[node_id].get("status") == "DFS"
            or graph.nodes[node_id].get("status") == "DFS-BT"
        ):
            label += f"\n{graph.nodes[node_id].get('status')}"
            return label
        else:
            if graph.nodes[node_id].get("index"):
                label += f"\n{graph.nodes[node_id].get('index')[0]}"
            if graph.nodes[node_id].get("radix"):
                label += f"\n{graph.nodes[node_id].get('radix')[0]}"
            if graph.nodes[node_id].get("status"):
                label += f"\n{graph.nodes[node_id].get('status')}"
    return label


def display_graph(
    graph: nx.Graph,
    root_id: str,
    ax=None,
    square=Optional[bool],
    title=None,
):
    # Node Colors
    node_colors = []
    for node_id in graph.nodes():
        if "color" in graph.nodes[node_id]:
            node_colors.append(graph.nodes[node_id]["color"])
        else:
            node_colors.append("lightblue")

    if ax is not None:
        ax.clear()

    pos = graphviz_layout(graph, prog="dot", root=root_id)  # Display as Tree

    # Create a labels dictionary to include node attributes in labels
    if square:
        labels = {node_id: get_node_label(graph, node_id) for node_id in graph.nodes()}

    nx.draw_networkx(
        graph,
        pos,
        with_labels=True,
        labels=labels if square else None,
        node_size=1000,
        node_color=node_colors,
        font_size=8,
        ax=ax,
        node_shape="s" if square else None,
    )
    plt.title(title if title is not None else "Tree")
    plt.show()


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
    plt.title("Maze Graph")
    plt.show()


def add_edge_to_graph(
    origin_node_id: str,
    dest_node_id: str,
    graph: nx.Graph,
    index: Tuple[str, str],
    radix: Tuple[str, str],
    status: str,
) -> nx.Graph:
    # Checking if the id already exists
    if graph.has_node(dest_node_id):
        # Rename older node id
        graph = nx.relabel_nodes(graph, {dest_node_id: f"{dest_node_id}_0"})

    graph.add_edge(origin_node_id, dest_node_id)
    graph.nodes[dest_node_id]["index"] = index
    graph.nodes[dest_node_id]["radix"] = radix
    graph.nodes[dest_node_id]["status"] = status
    return graph
