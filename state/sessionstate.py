from collections import defaultdict

import numpy as np
import uuid

from data.static_defaults import default_nodes, default_edges
from layout.layout import determine_radii, determine_angles, determine_coordinates


def _canonical_edge_descriptor(edge):
    # Create a stable edge descriptor where left is always <= right
    left = int(edge["left"])
    right = int(edge["right"])
    if left <= right:
        return left, right
    return right, left


class SessionState:
    def __init__(self):
        self.session_id = str(uuid.uuid4())
        self.nodes = default_nodes.copy()
        self.node_groups = self._collect_node_groups()
        self.edges = {_canonical_edge_descriptor(edge): edge for edge in default_edges}
        num_nodes = max(v["id"] for v in self.nodes) + 1
        self.angles = np.zeros(num_nodes)
        self.radii = np.zeros(num_nodes)
        self._update()

    def _collect_node_groups(self):
        collected_labels = {}
        for node in self.nodes:
            if node["label"] not in collected_labels:
                collected_labels[node["label"]] = len(collected_labels)
        return collected_labels

    def _update(self):
        self.angles = determine_angles(self.angles, self.edges)
        self.radii = determine_radii(self.radii, self.edges)

    def get_layout(self):
        coordinates = determine_coordinates(self.angles, self.radii)
        non_connected = self._get_non_connected_nodes()
        return dict(
            nodes=[
                self.nodes[idx]
                | dict(
                    coord=coordinates[idx],
                    group=self.node_groups[self.nodes[idx]["label"]],
                    connected=idx not in non_connected,
                )
                for idx in range(self.angles.size)
            ],
            edges=list(self.edges.values()),
        )

    def _get_non_connected_nodes(self):
        num_nodes = self.radii.size
        non_connected_nodes = set(range(0, num_nodes))
        for edge in self.edges.values():
            non_connected_nodes.discard(edge["left"])
            non_connected_nodes.discard(edge["right"])
        return non_connected_nodes

    def get_edge(self, edge):
        desc = _canonical_edge_descriptor(edge)
        if desc not in self.edges:
            return edge
        return self.edges[desc]

    def update_edge(self, edge_update):
        if "left" not in edge_update or "right" not in edge_update:
            raise Exception(f"Edge update is missing left and/or right property")
        if edge_update["dissent"] is None and edge_update["respect"] is None:
            raise Exception(f"Edge update is missing either a dissent or respect score")
        desc = _canonical_edge_descriptor(edge_update)
        if (
            desc not in self.edges
            and edge_update["dissent"] is None
            and edge_update["respect"] is None
        ):
            raise Exception(
                f"Adding new edges requires both dissent and respect parameters"
            )
        self.edges[desc] = self.edges.get(desc, {}) | {
            k: v for k, v in edge_update.items() if v is not None
        }
        self._update()
        return self.get_layout()
