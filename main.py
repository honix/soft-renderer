import numpy as np

import matrices
from buffer import Buffer
from point import P

def lerp(a, b, t):
    return a + (b - a) * t


# TODO: move test to sep file
def test_2d_render():
    color_buffer = Buffer(512, 512)
    def shader(p):
        return (p.x * 255, p.y * 255, 128)
    color_buffer.draw_shader(shader)
    for i in range(0, 255, 15):
        color_buffer.draw_line(P(10, 10), P(color_buffer.w-10, color_buffer.h-10-i), (0, 0, 128))
    for i in range(0, 255, 15):
        color_buffer.draw_line(P(color_buffer.w-10, 10), P(10, color_buffer.h-10-i), (0, 0, 128))
    for i in range(0, color_buffer.w, 15):
        color_buffer.draw_line(P(i, 10), P(color_buffer.w/2, color_buffer.h-10), (0, 0, 128))
    color_buffer.draw_fill_triangle(P(15, 15), P(10, 100), P(50, 10), (0, 128, 0))
    color_buffer.draw_wire_triangle(P(15, 15), P(10, 100), P(50, 10), (0, 0, 0))
    color_buffer.draw_rect(P(50, 50), P(100, 100), (128, 0, 0))
    color_buffer.draw_pixel(255, 255, (255, 255, 255))

    color_buffer.show()

#test_2d_render()

cube_points = [
    P(-1, -1,  1),
    P( 1, -1,  1),
    P( 1,  1,  1),
    P(-1,  1,  1),

    P(-1, -1,  -1),
    P( 1, -1,  -1),
    P( 1,  1,  -1),
    P(-1,  1,  -1),

    P(0,  -1,   0),
]

# TODO: mesh will be a class
cube_mesh = {
    'vertices': [
        P(-1, -1,  2), # 0
        P( 1, -1,  2), # 1
        P( 1,  1,  2), # 2
        P(-1,  1,  2), # 3

        P(-1, -1,  1), # 4
        P( 1, -1,  1), # 5
        P( 1,  1,  1), # 6
        P(-1,  1,  1), # 7
    ],
    'triangles': [
        # TODO: will be triangle a class? (normal calculation, etc)
        # anti clock-wice
        [0, 2, 1],
        [0, 3, 2],

        [4, 6, 5],
        [4, 7, 6],
    ]
}

def test_persp_render():
    color_buffer = Buffer(1024, 512)

    def persp(p):

        proj = matrices.frustrum()

        trans = np.matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, -4],
            [0, 0, 0, 1]
        ])

        # TODO: clean up usage of matrices
        o = proj * trans * np.matrix([[p.x], [p.y], [p.z], [1]])
        o /= o[3]

        return P(o.item(0) + color_buffer.w / color_buffer.h, o.item(1) + 1)

    def screen(p):
        return P(
            p.x * color_buffer.h / 2, 
            p.y * color_buffer.h / 2,
            p.z
        )

    def trans(p):
        return screen(persp(p))

    screen_vertices = list(map(trans, cube_mesh['vertices']))

    for triangle in cube_mesh['triangles']:
        vertices = list(map(lambda x: screen_vertices[x], triangle))
        color_buffer.draw_fill_triangle(*vertices, (25, 25, 25))
        color_buffer.draw_wire_triangle(*vertices, (25, 25, 255))
        for vertex in vertices:
            color_buffer.draw_pixel(
                vertex.x,
                vertex.y,
                (255, 25, 25))

    color_buffer.show()

test_persp_render()




# Perspective projection
# https://en.wikipedia.org/wiki/3D_projection#Mathematical_formula