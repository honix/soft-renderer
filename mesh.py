import numpy as np

from point import Point

class Mesh:
    def __init__(self, vertices=[], triangles=[]):
        self.vertices = vertices
        self.triangles = triangles

        def to_numpy(vertex):
            x, y, z = vertex

            return np.array([
                [x],
                [y],
                [z],
                [1],
            ])

        self.numpy_vertices = map(to_numpy, vertices)

        print(f'Mesh created with {len(self.triangles)} triangles')