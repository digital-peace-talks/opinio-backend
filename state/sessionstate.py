from collections import defaultdict

import numpy as np
import uuid

from data.static_defaults import default_nodes, default_edges
from layout.layout import determine_radii, determine_angles, determine_coordinates


class SessionState:
    def __init__(self):
        self.session_id = uuid.uuid4()
        self.nodes = default_nodes.copy()
        self.node_groups = self._collect_node_groups()
        self.edges = {
            self._canonical_edge_descriptor(edge): edge for edge in default_edges
        }
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

    def get(self):
        coordinates = determine_coordinates(self.angles, self.radii)
        return dict(
            nodes=[
                self.nodes[idx]
                | dict(
                    coord=coordinates[idx],
                    group=self.node_groups[self.nodes[idx]["label"]],
                )
                for idx in range(self.angles.size)
            ],
            edges=self.edges.values(),
        )

    def update_edge(self, edge_update):
        if "left" not in edge_update or "right" not in edge_update:
            raise Exception(f"Edge update is missing left and/or right property")
        if "dissent" not in edge_update and "respect" not in edge_update:
            raise Exception(f"Edge update is missing either a dissent or respect score")
        desc = self._canonical_edge_descriptor(edge_update)
        if desc not in self.edges:
            raise Exception(f"No such edge: {edge_update}")
        self.edges[desc] = self.edges[desc] | edge_update
        self._update()
        return self.get()

    def _canonical_edge_descriptor(self, edge):
        # Create a stable edge descriptor where left is always <= right
        if edge["left"] <= edge["right"]:
            return edge["left"], edge["right"]
        return edge["right"], edge["left"]
