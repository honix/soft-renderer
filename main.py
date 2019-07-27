import numpy as np
import math
import random
import time

import matrices
from renderer import Renderer
from point import Point
from mesh import Mesh


def test_persp_render():
    start = time.time_ns()

    from obj import read_obj

    mesh = read_obj('teapot.obj')

    renderer = Renderer(1024, 1024)

    # TODO: split camera/world transform and object transform
    def transform(numpy_vertex):
        transform = (matrices.screen(renderer.width, renderer.height) *
                     matrices.frustrum() *
                     matrices.transpose(0, -2, -5) *
                     matrices.rotate_y(0 * math.pi))

        numpy_vertex = transform * numpy_vertex
        numpy_vertex /= numpy_vertex[3]

        return Point.from_numpy(numpy_vertex)

    print("Transforming points to screen pos..")

    screen_points = list(map(transform, mesh.numpy_vertices))

    print("Rendering..")

    # TODO: move those routines to mesh class (?)
    i = 0
    for polygon in mesh.polygons:
        # TODO: fix this face cull condition using camera
        if np.dot(polygon.normal, [1, 0, 1]) > 0:
            points = list(map(lambda x: screen_points[x], polygon.indices))
            renderer.depth_test = True
            renderer.draw_fill_triangle(*points, (25, 255, 25))
            renderer.depth_test = False
            renderer.draw_wire_triangle(*points, (25, 25, 255))

        i += 1
        if i % 50 == 0: print(f"{i} polygons drawn")

    # renderer.depth_test = False
    # for point in screen_points:
    #     renderer.draw_pixel(point.x, point.y, point.z, (255, 25, 25))

    end = time.time_ns()
    print(f"{(end - start) / 1000000000} seconds ellapsed")

    renderer.show()

test_persp_render()


# Perspective projection
# https://en.wikipedia.org/wiki/3D_projection#Mathematical_formula
