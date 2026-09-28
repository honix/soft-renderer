import numpy as np

from .point import Point


def normalized(v):
    length = np.linalg.norm(v)
    return v / length if length > 0 else v

class Mesh:
    def __init__(self, vertices=[], polygons=[]):
        self.vertices = vertices
        self.polygons = polygons

        self.calculate_polygons_normals()
        self.calculate_vertices_normals()

        print(f'Mesh created with {len(self.polygons)} polygons')

    def calculate_polygons_normals(self):
        for polygon in self.polygons:
            def pos(index):
                return self.vertices[polygon.indices[index]].position

            polygon.normal = np.cross(
                pos(1) - pos(0),
                pos(2) - pos(0)
            )

            polygon.normal = normalized(polygon.normal).view(Point)
            polygon.center = np.mean(
                [self.vertices[i].position for i in polygon.indices], axis=0
            ).view(Point)

    def calculate_vertices_normals(self):
        # Vertices at the same position (seams of a model, split for uv or
        # so) share one smooth normal, otherwise a visible crease appears
        sums = {}
        for polygon in self.polygons:
            for index in polygon.indices:
                key = tuple(np.round(self.vertices[index].position, 5))
                sums[key] = sums.get(key, 0) + polygon.normal

        for vertex in self.vertices:
            key = tuple(np.round(vertex.position, 5))
            normal = sums.get(key, np.zeros(3))
            vertex.normal = normalized(np.asarray(normal, dtype=float)).view(Point)
