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
    print("Start")

    from obj import read_obj

    mesh = read_obj('teapot.obj')

    renderer = Renderer(1024, 1024)

    camera_position = Point(3, 2, 5)

    # TODO: split camera/world transform and object transform
    transform_matrix = (
        matrices.screen(renderer.width, renderer.height) *
        matrices.frustrum() *
        matrices.rotate_y(-1/6 * math.pi) *
        matrices.transpose(*-camera_position)
    )

    def transform(vertex):
        vertex_project = np.concatenate((vertex.position, [1]))[:,None]
        vertex_transformed = transform_matrix @ vertex_project
        vertex_transformed /= vertex_transformed[3]
        vertex_unproject = np.asarray(vertex_transformed).flatten()[:3]

        vertex.tposition = vertex_unproject.view(Point)

    print("Transforming points to screen pos..")

    for vertex in mesh.vertices:
        transform(vertex)

    print("Rendering..")

    # TODO: move those routines to mesh renderer class (?)
    i = 0
    for polygon in mesh.polygons:
        if np.dot(mesh.vertices[polygon.indices[0]].position - camera_position, polygon.normal) >= 0: continue
        vertices = list(map(lambda x: mesh.vertices[x], polygon.indices))
        renderer.depth_test = True
        renderer.draw_fill_triangle_lerp(*vertices)
        renderer.depth_test = False
        #renderer.draw_wire_triangle(*vertices)

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
