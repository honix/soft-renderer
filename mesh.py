import numpy as np

from point import Point

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

    def calculate_vertices_normals(self):
        print("calculate_vertices_normals not implemented")
