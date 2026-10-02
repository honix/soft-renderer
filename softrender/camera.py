import numpy as np

from .geometry import matrices
from .geometry.point import Point


def view_projection(position, width, height):
    # TODO: split camera/world transform and object transform
    return (
        matrices.screen(width, height) *
        matrices.frustrum() *
        #matrices.rotate_y(-1/6 * math.pi) *
        matrices.transpose(*-position)
    )


def project(vertex, transform_matrix):
    """Sets vertex.clip (before the divide, for near-plane clipping), vertex.tposition
    (screen space) and vertex.w (for perspective-correct interpolation)."""
    vertex_project = np.concatenate((vertex.position, [1]))[:,None]
    vertex_transformed = transform_matrix @ vertex_project
    vertex.clip = np.asarray(vertex_transformed, dtype=float).flatten()
    vertex.w = float(vertex_transformed[3])
    # Only meaningful in front of the camera, the renderer clips the rest
    if vertex.w != 0: vertex_transformed /= vertex_transformed[3]
    vertex_unproject = np.asarray(vertex_transformed).flatten()[:3]

    vertex.tposition = vertex_unproject.view(Point)
