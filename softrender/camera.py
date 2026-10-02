import math

import numpy as np

from .geometry import matrices
from .geometry.point import Point


FOV = 50  # vertical field of view, degrees


def view_projection(eye, target, width, height, fov=FOV):
    # TODO: split camera/world transform and object transform
    t = math.tan(math.radians(fov) / 2)
    return (
        matrices.screen(width, height) *
        matrices.frustrum(-t, t, t, -t) *
        matrices.look_at(eye, target)
    )


def frame(positions, width, height, fov=FOV, direction=(0, 2, 5), fill=0.9):
    """Camera position and target that frame the mesh.

    The camera looks at the bounding box center from `direction` and moves
    back until every vertex is inside `fill` of the view.
    """
    t = math.tan(math.radians(fov) / 2) * fill  # half view height at distance 1
    positions = np.asarray(positions, dtype=float)
    center = (positions.min(axis=0) + positions.max(axis=0)) / 2

    back = np.asarray(direction, dtype=float)
    back /= np.linalg.norm(back)
    right = np.cross((0, 1, 0), back)
    right /= np.linalg.norm(right)
    up = np.cross(back, right)

    v = positions - center
    z = v @ back  # towards the camera
    distance = max(
        np.max(z + np.abs(v @ right) / (t * width / height)),
        np.max(z + np.abs(v @ up) / t),
    )

    return (center + back * distance).view(Point), center.view(Point)


def project(vertex, transform_matrix):
    """Sets vertex.tposition (screen space) and vertex.w (for perspective-correct interpolation)."""
    vertex_project = np.concatenate((vertex.position, [1]))[:,None]
    vertex_transformed = transform_matrix @ vertex_project
    vertex.w = float(vertex_transformed[3])
    vertex_transformed /= vertex_transformed[3]
    vertex_unproject = np.asarray(vertex_transformed).flatten()[:3]

    vertex.tposition = vertex_unproject.view(Point)
