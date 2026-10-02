"""Scene graph: a tree of nodes, each with a local transform.

A node's world transform is its parent's world transform times its own, so
moving a node moves all of its children with it. A node may hold a mesh
(in the mesh's own model space) and a material: keyword arguments for the
shader, like albedo=(0.2, 0.5, 0.8).

Shaders work in world space, so before drawing every mesh is copied into
world space with its node's transform (see Node.world_meshes).
"""
import numpy as np

from .geometry import matrices
from .geometry.mesh import Mesh
from .geometry.point import Point
from .geometry.polygon import Polygon
from .geometry.vertex import Vertex


class Node:
    def __init__(self, name='', mesh=None, transform=None, material=None, children=()):
        self.name = name
        self.mesh = mesh
        self.transform = np.identity(4) if transform is None else np.asarray(transform, dtype=float)
        self.material = material or {}
        self.children = list(children)

    def add(self, *children):
        self.children.extend(children)
        return self

    def walk(self, parent=np.identity(4)):
        """Yields (node, world transform) for this node and everything below it."""
        world = parent @ self.transform
        yield self, world
        for child in self.children:
            yield from child.walk(world)

    def world_meshes(self):
        """Yields (node, mesh in world space) for every node that has a mesh."""
        for node, world in self.walk():
            if node.mesh is not None:
                yield node, transform_mesh(node.mesh, world)


def transform_mesh(mesh, matrix):
    """A copy of the mesh with every vertex moved by matrix. Normals are
    recomputed from the moved positions, so non-uniform scale works too."""
    positions = np.array([v.position for v in mesh.vertices], dtype=float)
    positions = np.c_[positions, np.ones(len(positions))] @ np.asarray(matrix).T
    vertices = [Vertex(p[:3].view(Point)) for p in positions]
    polygons = [Polygon(list(p.indices)) for p in mesh.polygons]
    return Mesh(vertices, polygons)


def plane(size=1, cells=16):
    """A flat square on the xz plane, facing up (+y), centered on the origin.

    Split into cells x cells squares: flat and Gouraud shading light a face or
    a vertex at a time, a single big quad would be all lit or all shadowed.
    """
    steps = np.linspace(-size / 2, size / 2, cells + 1)
    vertices = [Vertex(Point(x, 0, z)) for x in steps for z in steps]
    polygons = []
    for i in range(cells):
        for j in range(cells):
            a, b = i * (cells + 1) + j, (i + 1) * (cells + 1) + j  # a -> b is +x
            polygons += [Polygon([a, a + 1, b + 1]), Polygon([a, b + 1, b])]
    return Mesh(vertices, polygons)


def translate(x, y, z):
    return np.asarray(matrices.transpose(x, y, z))


def rotate_y(degrees):
    return np.asarray(matrices.rotate_y(np.radians(degrees)))


def scale(x, y=None, z=None):
    return np.asarray(matrices.scale(x, y, z))
