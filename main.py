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

def test_persp_render():
    color_buffer = Buffer(1024, 512)

    def persp(p):

        proj = matrices.frustrum()

        trans = np.matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, -3],
            [0, 0, 0, 1]
        ])

        # TODO: clean up usage of matrices
        o = proj * trans * np.matrix([[p.x], [p.y], [p.z], [1]])
        o /= o[3]

        return P(o[0] + color_buffer.w / color_buffer.h, o[1] + 1)

    for p in cube_points:
        op = persp(p)
        color_buffer.draw_pixel(
            op.x * color_buffer.h / 2, 
            op.y * color_buffer.h / 2, 
            (255, 255, 255))

    color_buffer.show()

test_persp_render()




# Perspective projection
# https://en.wikipedia.org/wiki/3D_projection#Mathematical_formula