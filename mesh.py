import numpy as np

from point import Point

class Mesh:
    def __init__(self, vertices=[], polygons=[]):
        self.vertices = vertices
        self.polygons = polygons

        self.create_numpy_vertices()
        self.calculate_polygons_normals()
        self.calculate_vertices_normals()

        print(f'Mesh created with {len(self.polygons)} polygons')

    def create_numpy_vertices(self):
        def to_numpy(vertex):
            return np.array([
                [vertex.position.x],
                [vertex.position.y],
                [vertex.position.z],
                [1],
            ])

        self.numpy_vertices = list(map(to_numpy, self.vertices))

    def calculate_polygons_normals(self):
        def xyz(numpy_vertice):
            return numpy_vertice.T[0][:3]

        for polygon in self.polygons:
            polygon.normal = np.cross(
                xyz(self.numpy_vertices[polygon.indices[1]]) - xyz(self.numpy_vertices[polygon.indices[0]]),
                xyz(self.numpy_vertices[polygon.indices[2]]) - xyz(self.numpy_vertices[polygon.indices[0]])
            )

    def calculate_vertices_normals(self):
        print("calculate_vertices_normals not implemented")

def cube():
    # cube.png
    return Mesh(
        vertices = map(lambda v: map(lambda x: x * 40, v), [
            [-1, -1,  1], # 0
            [ 1, -1,  1], # 1
            [ 1,  1,  1], # 2
            [-1,  1,  1], # 3

            [-1, -1, -1], # 4
            [ 1, -1, -1], # 5
            [ 1,  1, -1], # 6
            [-1,  1, -1], # 7

            [ 0, -1,  0], # 8
        ]),
        polygons=[
            # TODO: will be triangle a class? (normal calculation, etc)
            # anti clock-wice
            [0, 2, 1],  # back face
            [0, 3, 2],

            [4, 6, 5],  # front face
            [4, 7, 6],

            [4, 1, 5],  # up face
            [4, 0, 1],

            [7, 2, 6],  # down face
            [7, 3, 2],

            [4, 3, 0],  # left face
            [4, 7, 3],

            [1, 6, 5],  # right face
            [1, 2, 6],
        ]
    )