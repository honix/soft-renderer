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

            polygon.normal /= max(polygon.normal.max(), -polygon.normal.min())
            polygon.normal = polygon.normal.view(Point)

    def calculate_vertices_normals(self):
        for vertex in self.vertices:
            vertex.normal = np.array([0, 0, 0], dtype=np.float)

        for polygon in self.polygons:
            for index in polygon.indices:
                self.vertices[index].normal += polygon.normal

        for vertex in self.vertices:
            vertex.normal /= max(vertex.normal.max(), -vertex.normal.min())
            vertex.normal = vertex.normal.view(Point)

