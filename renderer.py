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

    def draw_fill_trapezoid(self, v1, v2, v3, v4, color):
        p1 = v1.tposition
        p2 = v2.tposition
        p3 = v3.tposition
        p4 = v4.tposition

        #if look_up:
        #    z_anchor_x = p3.x
        #    z_anchor_z = z3
        #    z_base_x = p2.x
        #else:
        #    z_anchor_x = p4.x
        #    z_anchor_z = z4
        #    z_base_x = p1.x

        dy = p2.y - p1.y
        if dy == 0: return

        #dx = z_anchor_x - z_base_x
        #if dx == 0: return

        dxleft, dxright = p2.x - p1.x, p3.x - p4.x
        xleft_step, xright_step = dxleft / dy, dxright / dy

        dzleft, dzright = p2.z - p1.z, p3.z - p4.z
        zleft_step, zright_step = dzleft / dy, dzright / dy

        xleft, xright = p1.x, p4.x
        zleft, zright = p1.z, p4.z
        for y in range(round(p1.y), round(p2.y)):
            dz = zright - zleft
            dx = xright - xleft
            if dx == 0: 
                z_step = 0
            else:
                z_step = dz / dx
            z = zleft
            # for x in range(floor(xleft), floor(xright)):
            #     if x == floor(xleft) and y == floor(p1.y):
            #         self.draw_pixel(x, y, z, (0, 255, 0))
            #     elif x == floor(xleft):
            #         self.draw_pixel(x, y, z, (255, 0, 0))
            #     elif x == floor(xright) - 1:
            #         self.draw_pixel(x, y, z, (0, 0, 255))
            #     else:
            #         self.draw_pixel(x, y, z, z * 255 * 1) # draw z
            #         #self.draw_pixel(x, y, z, color)
            #     z += z_step
            for x in range(round(xleft), round(xright)):
                self.draw_pixel(x, y, z, color)
                z += z_step
            # TODO: Can we do without float? nope
            xleft += xleft_step
            xright += xright_step
            zleft += zleft_step
            zright += zright_step

    def draw_fill_triangle(self, v1, v2, v3, color):
        [top, middle, bottom] = sorted([v1, v2, v3], key=lambda v: v.tposition.y)

        t = (top.tposition.y - middle.tposition.y) / (top.tposition.y - bottom.tposition.y)

        middle_oposit = Vertex.lerp(top, bottom, t)

        [left, right] = sorted([middle, middle_oposit], key=lambda v: v.tposition.x)

        self.draw_fill_trapezoid(top, left, right, top, color)
        self.draw_fill_trapezoid(left, bottom, bottom, right, color)

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
