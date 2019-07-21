import numpy as np
import math
import random
import time

import matrices
from renderer import Renderer
from point import Point
from mesh import Mesh


def lerp(a, b, t):
    return a + (b - a) * t


def test_persp_render():
    start = time.time_ns()

    # cube.png
    cube = Mesh(
        vertices = [
            [-1, -1,  1], # 0
            [ 1, -1,  1], # 1
            [ 1,  1,  1], # 2
            [-1,  1,  1], # 3

            [-1, -1, -1], # 4
            [ 1, -1, -1], # 5
            [ 1,  1, -1], # 6
            [-1,  1, -1], # 7

            [ 0, -1,  0], # 8
        ],
        triangles=[
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

    renderer = Renderer(1024, 512)

    # TODO: split camera/world transform and object transform
    def transform(numpy_vertex):
        transform = (matrices.screen(renderer.width, renderer.height) *
                     matrices.frustrum() *
                     matrices.transpose(0, 0, -3) *
                     matrices.rotate_y(-1/6 * math.pi))

        numpy_vertex = transform * numpy_vertex
        numpy_vertex /= numpy_vertex[3]

        return Point.from_numpy(numpy_vertex)

    screen_points = list(map(transform, cube.numpy_vertices))

    # TODO: move those routines to mesh class (?)
    for triangle in cube.triangles:
        points = list(map(lambda x: screen_points[x], triangle))
        renderer.draw_fill_triangle(*points, (25, 25, random.randint(25, 125)))
        renderer.draw_wire_triangle(*points, (25, 25, 255))

    for point in screen_points:
        renderer.draw_pixel(point.x, point.y, point.z, (255, 25, 25))

    end = time.time_ns()
    print("{} seconds ellapsed".format((end - start) / 1000000000))

    renderer.show()

test_persp_render()


# Perspective projection
# https://en.wikipedia.org/wiki/3D_projection#Mathematical_formula
