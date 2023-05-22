import numpy as np
from scipy.optimize import minimize
import math

NORM_DISSENT = 10.0
NORM_RESPECT = 5


def _angle_distance(angles_vec, left, right):
    sin_comp = math.sin(angles_vec[left] - angles_vec[right])
    cos_comp = math.cos(angles_vec[left] - angles_vec[right])
    return abs(math.atan2(sin_comp, cos_comp)) / math.pi  # max 180 deg


def determine_angles(angles, edges):
    # Angles array
    x0 = angles.copy()

    def error_func(angle_vec: np.ndarray):
        error = 0
        for edge in edges.values():
            distance = _angle_distance(angle_vec, edge["left"], edge["right"])
            # error += abs(distance - _normalize_dissent(edge))  # pow?
            error += math.pow(distance - _normalize_dissent(edge), 2)  # pow?
        return error

    res = minimize(
        error_func,
        x0,
        method="SLSQP",
        options={"disp": False, "maxiter": 500},
        tol=0.001,
    )
    return res.x


def determine_radii(radii, edges):
    num_nodes = radii.size

    # Determine non-connected nodes
    non_connected_nodes = set(range(0, num_nodes))
    for edge in edges.values():
        non_connected_nodes.discard(edge["left"])
        non_connected_nodes.discard(edge["right"])

    # Collect statistics for average respect * dissent
    sums = np.zeros(num_nodes)
    counts = np.zeros(num_nodes)
    for edge in edges.values():
        score = _normalize_respect(edge) * (1.0 - _normalize_dissent(edge))
        counts[edge["left"]] += 1
        counts[edge["right"]] += 1
        sums[edge["left"]] += score
        sums[edge["right"]] += score

    # Calculate radii
    radii = np.zeros(num_nodes)
    for i in range(0, num_nodes):
        if i in non_connected_nodes or counts[i] == 0:
            radii[i] = 1
        else:
            radii[i] = 1 - sums[i] / counts[i]
    return radii


def determine_coordinates(angles, radii):
    def _round(coord):
        return int(10000 * coord) / 10000.0

    def _node_coords(idx):
        angle = angles[idx]
        radius = radii[idx]
        return dict(
            x=_round(radius * math.cos(angle)), y=_round(radius * math.sin(angle))
        )

    return [_node_coords(idx) for idx in range(angles.size)]


def _normalize_dissent(edge):
    return edge["dissent"] / NORM_DISSENT


def _normalize_respect(edge):
    return (NORM_RESPECT + edge["respect"]) / (2 * NORM_RESPECT)
