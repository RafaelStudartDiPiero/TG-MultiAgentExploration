from typing import List, Optional, Tuple


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
