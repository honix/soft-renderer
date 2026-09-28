from buffer import Buffer
from point import Point
from vertex import Vertex
from utils import lerp
from math import floor, ceil

import numpy as np

class Renderer:
    def __init__(self, width, height, depth_test=True):
        self.width = width
        self.height = height
        self.depth_test = depth_test
        self.color_buffer = Buffer(width, height, channels=3)
        self.depth_buffer = Buffer(width, height, channels=1, fill_value=1, dtype=np.float)
    
    def show(self):
        self.color_buffer.show()

    def draw_pixel(self, x, y, z, color):
        x = int(x)
        y = int(y)

        # X and Y are flipped in buffer, so..
        if 0 <= x < self.width and 0 <= y < self.height:
            # TODO: color can be as class
            if self.depth_test:
                if self.depth_buffer[y, x] < z:
                    return
                self.depth_buffer[y, x] = z
            self.color_buffer[y, x] = color

    def draw_shader(self, shader):
        for x in range(self.width):
            for y in range(self.height):
                self.draw_pixel(x, y, 0, shader(Point(x/self.width, y/self.height)))

    def draw_rect(self, p1, p2, color):
        maxx = max(p1.x, p2.x)
        maxy = max(p1.y, p2.y)
        minx = min(p1.x, p2.x)
        miny = min(p1.y, p2.y)

        for cx in range(maxx - minx):
            for cy in range(maxy - miny):
                x = cx + minx
                y = cy + miny
                self.draw_pixel(x, y, 0, color)

    def draw_line(self, p1, p2, color):
        p1 = p1.tposition
        p2 = p2.tposition

        # TODO: iterpolate z-value
        z = sum([p1.z, p2.z]) / 2

        p1 = p1.integrated()
        p2 = p2.integrated()

        # Some kind of Bresenhams line algorithm
        dx = abs(p2.x - p1.x)
        sx = 1 if p1.x < p2.x else -1
        dy = -abs(p2.y - p1.y)
        sy = 1 if p1.y < p2.y else -1
        err = dx + dy
        x, y = p1.x, p1.y

        while True:
            self.draw_pixel(x, y, z, color)
            if x == p2.x and y == p2.y: break
            double_err = err + err
            if double_err >= dy:
                err += dy
                x += sx
            if double_err <= dx:
                err += dx
                y += sy

    def draw_wire_triangle(self, p1, p2, p3, color):
        self.draw_line(p1, p2, color)
        self.draw_line(p2, p3, color)
        self.draw_line(p3, p1, color)

    def draw_fill_trapezoid(self, v1, v2, v3, v4, color, y_top=None, y_bottom=None):
        # Left edge is v1 -> v2, right edge is v4 -> v3 (both going down).
        # Rows between y_top and y_bottom are filled, by default the span
        # where both edges exist.
        p1 = v1.tposition
        p2 = v2.tposition
        p3 = v3.tposition
        p4 = v4.tposition

        if y_top is None: y_top = max(p1.y, p4.y)
        if y_bottom is None: y_bottom = min(p2.y, p3.y)

        # Sample coverage at pixel centers (x + 0.5, y + 0.5) with a top-left
        # fill rule: a pixel is drawn if its center is in [top, bottom) and
        # [left, right). Two triangles sharing an edge then compute the exact
        # same edge position, so every pixel goes to exactly one of them:
        # no holes and no double drawing.
        for y in range(ceil(y_top - 0.5), ceil(y_bottom - 0.5)):
            yc = y + 0.5
            xleft, zleft = edge_at(p1, p2, yc)
            xright, zright = edge_at(p4, p3, yc)

            dx = xright - xleft
            z_step = (zright - zleft) / dx if dx > 0 else 0

            x_start = ceil(xleft - 0.5)
            # Depth is sampled at the pixel center too, not at the edge
            z = zleft + (x_start + 0.5 - xleft) * z_step
            for x in range(x_start, ceil(xright - 0.5)):
                self.draw_pixel(x, y, z, color)
                z += z_step

    def draw_fill_triangle(self, v1, v2, v3, color):
        [top, middle, bottom] = sorted([v1, v2, v3], key=lambda v: v.tposition.y)
        t, m, b = top.tposition, middle.tposition, bottom.tposition

        # Which side of the long edge (top -> bottom) the middle vertex is on
        cross = (m.x - t.x) * (b.y - t.y) - (m.y - t.y) * (b.x - t.x)
        if cross == 0: return  # degenerate, zero area

        # Always pass the real edge endpoints (never a lerped split point),
        # so a shared edge is evaluated identically by both triangles
        if cross < 0:  # middle is on the left
            self.draw_fill_trapezoid(top, middle, bottom, top, color, t.y, m.y)
            self.draw_fill_trapezoid(middle, bottom, bottom, top, color, m.y, b.y)
        else:
            self.draw_fill_trapezoid(top, bottom, middle, top, color, t.y, m.y)
            self.draw_fill_trapezoid(top, bottom, bottom, middle, color, m.y, b.y)

    def draw_fill_triangle_lerp(self, v1, v2, v3, color):
        for i in range(0, 8):
            vu = Vertex.lerp(v1, v2, i/8)
            for j in range(0, 8):
                v = Vertex.lerp(vu, v3, j/8)
                p = v.tposition
                self.draw_pixel(p.x, p.y, p.z, color)

    def draw_fill_triangle_check_edge(self, p1, p2, p3, color):
        # Edge Function
        def edge(a, b, x, y):
            return (x - a.tposition.x) * (b.tposition.y - a.tposition.y) - (y - a.tposition.y) * (b.tposition.x - a.tposition.x) >= 0

        # TODO: try span method https://www.joshbeam.com/articles/triangle_rasterization/
        minx = min(p1.tposition.x, p2.tposition.x, p3.tposition.x)
        miny = min(p1.tposition.y, p2.tposition.y, p3.tposition.y)
        maxx = max(p1.tposition.x, p2.tposition.x, p3.tposition.x)
        maxy = max(p1.tposition.y, p2.tposition.y, p3.tposition.y)
        # TODO: iterpolate z-value
        z = sum([p1.tposition.z, p2.tposition.z, p3.tposition.z]) / 3

        for x in range(floor(minx), floor(maxx)):
            for y in range(floor(miny), floor(maxy)):
                inside = True
                inside &= edge(p1, p2, x, y)
                inside &= edge(p2, p3, x, y)
                inside &= edge(p3, p1, x, y)
                if inside:
                    self.draw_pixel(x, y, z, color)


def edge_at(a, b, y):
    # X and Z of the edge a -> b at height y. Always computed from the edge's
    # own endpoints with the same formula, so it is bit-identical for every
    # triangle that shares this edge.
    t = (y - a.y) / (b.y - a.y)
    return lerp(a.x, b.x, t), lerp(a.z, b.z, t)
