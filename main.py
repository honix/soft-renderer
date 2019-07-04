from PIL import Image
import numpy as np
import math

def lerp(a, b, t):
    return a + (b - a) * t

class P:
    def __init__(self, x, y, z = 0):
        self.x = x
        self.y = y
        self.z = z

    def distance(self, other):
        return math.sqrt(math.pow(self.x - other.x, 2) + 
                         math.pow(self.y - other.y, 2))


w, h = 512, 512

color_buffer = np.zeros((h, w, 3), dtype=np.uint8)

def draw_pixel(x, y, color):
    # X and Y are flipped in buffer, so..
    try:
        color_buffer[y, x] = color
    except Exception as ex:
        print(ex)

def shader(p):
    return (p.x * 255, p.y * 255, 128)

for x in range(w):
    for y in range(h):
        draw_pixel(x, y, shader(P(x/w, y/h)))


def draw_rect(p1, p2, color):
    maxx = max(p1.x, p2.x)
    maxy = max(p1.y, p2.y)
    minx = min(p1.x, p2.x)
    miny = min(p1.y, p2.y)
    for cx in range(maxx - minx):
        for cy in range(maxy - miny):
            x = cx + minx
            y = cy + miny
            draw_pixel(x, y, color)

def draw_line(p1, p2, color):
    # Some kind of Bresenhams line algorithm
    dx = abs(p2.x - p1.x)
    sx = 1 if p1.x < p2.x else -1
    dy = -abs(p2.y - p1.y)
    sy = 1 if p1.y < p2.y else -1
    err = dx + dy
    movex, movey = p1.x, p1.y
    while True:
        draw_pixel(int(movex), int(movey), color)
        erri = err + err
        if erri >= dy:
            err += dy
            movex += sx
        if erri <= dx:
            err += dx
            movey += sy
        if movex == p2.x and movey == p2.y: break

def draw_wire_triangle(p1, p2, p3, color):
    draw_line(p1, p2, color)
    draw_line(p2, p3, color)
    draw_line(p3, p1, color)

def draw_fill_triangle(p1, p2, p3, color):
    # Edge Function
    def edge(a, b, c):
        return (c.x - a.x) * (b.y - a.y) - (c.y - a.y) * (b.x - a.x) >= 0

    # TODO: try span method https://www.joshbeam.com/articles/triangle_rasterization/
    minx = min(p1.x, p2.x, p3.x)
    miny = min(p1.y, p2.y, p3.y)
    maxx = max(p1.x, p2.x, p3.x)
    maxy = max(p1.y, p2.y, p3.y)
    for cx in range(maxx - minx):
        for cy in range(maxy - miny):
            x = cx + minx
            y = cy + miny
            point = P(x, y)
            inside = True
            inside &= edge(p1, p2, point)
            inside &= edge(p2, p3, point)
            inside &= edge(p3, p1, point)
            if inside:
                draw_pixel(x, y, color)
    
def test_2d_render():
    for i in range(0, 255, 15):
        draw_line(P(10, 10), P(w-10, h-10-i), (0, 0, 128))
    for i in range(0, 255, 15):
        draw_line(P(w-10, 10), P(10, h-10-i), (0, 0, 128))
    for i in range(0, w, 15):
        draw_line(P(i, 10), P(w/2, h-10), (0, 0, 128))
    draw_fill_triangle(P(15, 15), P(10, 100), P(50, 10), (0, 128, 0))
    draw_wire_triangle(P(15, 15), P(10, 100), P(50, 10), (0, 0, 0))
    draw_rect(P(50, 50), P(100, 100), (128, 0, 0))
    draw_pixel(255, 255, (255, 255, 255))

    img = Image.fromarray(color_buffer, 'RGB')
    img.show()

test_2d_render()

# Orthographic projection
# https://en.wikipedia.org/wiki/3D_projection#Orthographic_projection
cube_points = [
    P(-1, -1,  1),
    P( 1, -1,  1),
    P( 1,  1,  1),
    P(-1,  1,  1),

    P(-1, -1, -1),
    P( 1, -1, -1),
    P( 1,  1, -1),
    P(-1,  1, -1),
]


# Perspective projection
# https://en.wikipedia.org/wiki/3D_projection#Mathematical_formula