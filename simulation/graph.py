from typing import List, Optional, Tuple

import gmpy2

import gmpyconfig


class Node:
    def __init__(
        self, id: str, color: str, finish: Optional[bool], edges: List[Tuple[str, str]]
    ):
        self.id = id
        self.color = color
        self.finish = finish if finish is not None else False
        self.edges = edges

    def node_view(self) -> Tuple[str, dict]:
        node_data = {
            "color": self.color,
            "finish": self.finish,
        }
        return (self.id, node_data)


def sort_neighbors(neighbor_ids: List[str], node_id: str) -> List[str]:
    if "," not in node_id:  # If node_id is a single number
        return sorted(neighbor_ids)

    # Extract the row and column numbers from the node_id
    row, col = map(int, node_id.split(","))

    # Define a custom sorting key function
    def custom_sort_key(node):
        n_row, n_col = map(int, node.split(","))
        if n_row == row - 1 and n_col == col:  # North
            return 0
        elif n_row == row and n_col == col + 1:  # East
            return 1
        elif n_row == row + 1 and n_col == col:  # South
            return 2
        elif n_row == row and n_col == col - 1:  # West
            return 3
        else:
            return 4

    return sorted(neighbor_ids, key=custom_sort_key)
