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

    #mesh = read_obj('cube.obj') # simples one
    mesh = read_obj('teapot.obj') # many triangles
    #mesh = read_obj('lamp.obj') # n-gons
    #mesh = read_obj('cessna.obj') # doesnt work..

    #renderer = Renderer(512, 512)
    renderer = Renderer(1024, 1024)

    camera_position = Point(3, 2, 5)

    print("Transforming points to screen pos..")

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

    for vertex in mesh.vertices:
        transform(vertex)

    print("Rendering..")

    # TODO: move those routines to mesh renderer class (?)
    i = 0
    for polygon in mesh.polygons:
        if np.dot(mesh.vertices[polygon.indices[0]].position - camera_position, polygon.normal) >= 0: continue
        vertices = list(map(lambda x: mesh.vertices[x], polygon.indices))
        renderer.depth_test = True
        #renderer.draw_fill_triangle(*vertices, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        #renderer.draw_fill_triangle(*vertices, (150, 50, 50))
        renderer.draw_fill_triangle(*vertices, ((polygon.normal.x + 1) / 2 * 255, (polygon.normal.y + 1) / 2 * 255, (polygon.normal.z + 1) / 2 * 255))
        #z = (vertices[0].tposition.z - 0.25) * 255 * 2
        #renderer.draw_fill_triangle(*vertices, (z, z, z))
        renderer.depth_test = False
        #renderer.draw_fill_triangle_lerp(*vertices, (200, 160, 100))
        #renderer.draw_wire_triangle(*vertices, (100, 160, 200))

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
