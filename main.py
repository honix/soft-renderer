import numpy as np
import math
import random

import matrices
from renderer import Renderer
from point import Point
from mesh import Mesh

def lerp(a, b, t):
    return a + (b - a) * t

# cube.png
cube = Mesh(
    vertices = [
        Point(-1, -1,  1), # 0
        Point( 1, -1,  1), # 1
        Point( 1,  1,  1), # 2
        Point(-1,  1,  1), # 3

        Point(-1, -1, -1), # 4
        Point( 1, -1, -1), # 5
        Point( 1,  1, -1), # 6
        Point(-1,  1, -1), # 7

        Point( 0, -1,  0), # 8
    ],
    triangles = [
        # TODO: will be triangle a class? (normal calculation, etc)
        # anti clock-wice
        [0, 2, 1], # back face
        [0, 3, 2],

        [4, 6, 5], # front face
        [4, 7, 6],

        [4, 1, 5], # up face
        [4, 0, 1],

        [7, 2, 6], # down face
        [7, 3, 2],

        [4, 3, 0], # left face
        [4, 7, 3],

        [1, 6, 5], # right face
        [1, 2, 6],
    ]
)

def test_persp_render():
    renderer = Renderer(1024, 512)

    # TODO: split camera/world transform and object transform
    def transform(p):
        transform = (matrices.screen(renderer.width, renderer.height) *
                     matrices.frustrum() *
                     matrices.transpose(0, 0 , -3) *
                     matrices.rotate_y(-1/6 * math.pi))

        point = transform * np.matrix([[p.x], [p.y], [p.z], [1]])
        point /= point[3]
        
        # TODO: Point will contain numpy array
        return Point(point.item(0), point.item(1), point.item(2))

    screen_vertices = list(map(transform, cube.vertices))

    # TODO: move those routines to mesh class (?)
    for triangle in cube.triangles:
        vertices = list(map(lambda x: screen_vertices[x], triangle))
        renderer.draw_fill_triangle(*vertices, (25, 25, random.randint(25, 125)))
        renderer.draw_wire_triangle(*vertices, (25, 25, 125))
        
    for vertex in screen_vertices:
        renderer.draw_point(vertex, (255, 25, 25))

    renderer.show()

test_persp_render()




# Perspective projection
# https://en.wikipedia.org/wiki/3D_projection#Mathematical_formula