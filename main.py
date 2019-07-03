from PIL import Image
import numpy as np
import math

def lerp(a, b, t):
    return a + (b - a) * t

class P:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, other):
        return math.sqrt(math.pow(self.x - other.x, 2) + 
                         math.pow(self.y - other.y, 2))


w, h = 512, 512

data = np.zeros((h, w, 3), dtype=np.uint8)

def shader(p):
    return (p.x * 255, p.y * 255, 0)

for x in range(w):
    for y in range(h):
        data[y, x] = shader(P(x/w, y/h))


def draw_rect(p1, p2, color):
    maxx = max(p1.x, p2.x)
    maxy = max(p1.y, p2.y)
    minx = min(p1.x, p2.x)
    miny = min(p1.y, p2.y)
    for cx in range(maxx - minx):
        for cy in range(maxy - miny):
            x = cx + minx
            y = cy + miny
            data[y, x] = color

def draw_line(p1, p2, color):
    # Some kind of Bresenhams line algorithm
    dx = abs(p2.x - p1.x)
    sx = 1 if p1.x < p2.x else -1
    dy = -abs(p2.y - p1.y)
    sy = 1 if p1.y < p2.y else -1
    err = dx + dy
    movex, movey = p1.x, p1.y
    while True:
        data[int(movey), int(movex)] = color
        if movex >= p2.x and movey >= p2.y: break
        erri = 2 * err
        if erri >= dy:
            err += dy
            movex += sx
        if erri <= dx:
            err += dx
            movey += sy

def draw_triangle(p1, p2, p3, color):
    # Edge Function
    def edge(a, b, c):
        return (c.x - a.x) * (b.y - a.y) - (c.y - a.y) * (b.x - a.x) >= 0

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
                data[y, x] = color
    

for i in range(0, 255, 15):
    draw_line(P(10, 10), P(w-10, h-10-i), (0, 0, 128))
for i in range(0, 255, 15):
    draw_line(P(w-10, 10), P(10, h-10-i), (0, 0, 128))
for i in range(0, w, 15):
    draw_line(P(i, 10), P(w/2, h-10), (0, 0, 128))
draw_triangle(P(15, 15), P(10, 100), P(50, 10), (0, 128, 0))
draw_rect(P(50, 50), P(100, 100), (128, 0, 0))

img = Image.fromarray(data, 'RGB')
img.show()
