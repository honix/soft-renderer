# Tiles a rectangle with jittered triangles and checks that every pixel inside
# is drawn exactly once: no holes (cracks) and no double drawing on shared edges.
import random
import numpy as np

from softrender.raster.renderer import Renderer
from softrender.geometry.vertex import Vertex
from softrender.geometry.point import Point

def test_watertight(seed, snap=False, size=256, cells=9):
    random.seed(seed)
    renderer = Renderer(size, size, depth_test=False)
    hits = np.zeros((size, size), int)

    draw_pixel = renderer.draw_pixel
    def counting_draw_pixel(x, y, z, color):
        hits[int(y), int(x)] += 1
        draw_pixel(x, y, z, color)
    renderer.draw_pixel = counting_draw_pixel

    x0, y0, x1, y1 = 20.3, 17.7, 235.6, 238.2
    grid = [[None] * (cells + 1) for _ in range(cells + 1)]
    for j in range(cells + 1):
        for i in range(cells + 1):
            x = x0 + (x1 - x0) * i / cells
            y = y0 + (y1 - y0) * j / cells
            if 0 < i < cells: x += random.uniform(-9, 9)
            if 0 < j < cells: y += random.uniform(-9, 9)
            # Snapping to half pixels puts edges exactly through pixel centers
            if snap and 0 < i < cells: x = round(x * 2) / 2
            if snap and 0 < j < cells: y = round(y * 2) / 2
            vertex = Vertex(Point(0, 0, 0), Point(0, 0, 0))
            vertex.tposition = Point(x, y, 0.5)
            grid[j][i] = vertex

    def area(a, b, c):
        a, b, c = a.tposition, b.tposition, c.tposition
        return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)

    for j in range(cells):
        for i in range(cells):
            a, b, c, d = grid[j][i], grid[j][i+1], grid[j+1][i+1], grid[j+1][i]
            triangles = ((a, b, c), (a, c, d))
            # Pick the diagonal that doesn't fold the quad over itself
            if min(area(*t) for t in triangles) <= 0:
                triangles = ((a, b, d), (b, c, d))
            for triangle in triangles:
                renderer.draw_fill_triangle(*triangle, (255, 255, 255))

    ys, xs = np.mgrid[0:size, 0:size] + 0.5
    inside = (xs > x0) & (xs < x1) & (ys > y0) & (ys < y1)
    holes = (inside & (hits == 0)).sum()
    overdraw = (hits > 1).sum()
    assert holes == 0 and overdraw == 0, f"seed {seed}: {holes} holes, {overdraw} pixels drawn twice"

for seed in range(20):
    test_watertight(seed)
    test_watertight(seed, snap=True)
print("ok")
