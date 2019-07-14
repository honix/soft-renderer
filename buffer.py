from PIL import Image
import numpy as np

from point import P

class Buffer:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.data = np.zeros((h, w, 3), dtype=np.uint8)

    def show(self):
        img = Image.fromarray(self.data, 'RGB')
        img.show()

    def draw_pixel(self, x, y, color):
        x = int(x)
        y = int(y)
        # X and Y are flipped in buffer, so..
        if (0 <= x < self.w and 0 <= y < self.h):
            self.data[y, x] = color

    def draw_shader(self, shader):
        for x in range(self.w):
            for y in range(self.h):
                self.draw_pixel(x, y, shader(P(x/self.w, y/self.h)))

    def draw_rect(self, p1, p2, color):
        maxx = max(p1.x, p2.x)
        maxy = max(p1.y, p2.y)
        minx = min(p1.x, p2.x)
        miny = min(p1.y, p2.y)
        for cx in range(maxx - minx):
            for cy in range(maxy - miny):
                x = cx + minx
                y = cy + miny
                self.draw_pixel(x, y, color)

    def draw_line(self, p1, p2, color):
        p1.integrate()
        p2.integrate()

        # Some kind of Bresenhams line algorithm
        dx = abs(p2.x - p1.x)
        sx = 1 if p1.x < p2.x else -1
        dy = -abs(p2.y - p1.y)
        sy = 1 if p1.y < p2.y else -1
        err = dx + dy
        movex, movey = p1.x, p1.y

        i = 0
        while True:
            # TODO: oh i dont like infinity loops
            # i += 1
            # if i > 255 : 
            #     break

            self.draw_pixel(movex, movey, color)
            erri = err + err
            if erri >= dy:
                err += dy
                movex += sx
            if erri <= dx:
                err += dx
                movey += sy
            if movex == p2.x and movey == p2.y: break

    def draw_wire_triangle(self, p1, p2, p3, color):
        self.draw_line(p1, p2, color)
        self.draw_line(p2, p3, color)
        self.draw_line(p3, p1, color)

    def draw_fill_triangle(self, p1, p2, p3, color):
        # Edge Function
        def edge(a, b, c):
            return (c.x - a.x) * (b.y - a.y) - (c.y - a.y) * (b.x - a.x) >= 0

        # TODO: try span method https://www.joshbeam.com/articles/triangle_rasterization/
        minx = min(p1.x, p2.x, p3.x)
        miny = min(p1.y, p2.y, p3.y)
        maxx = max(p1.x, p2.x, p3.x)
        maxy = max(p1.y, p2.y, p3.y)
        for cx in range(int(maxx - minx)):
            for cy in range(int(maxy - miny)):
                x = cx + minx
                y = cy + miny
                point = P(x, y)
                inside = True
                inside &= edge(p1, p2, point)
                inside &= edge(p2, p3, point)
                inside &= edge(p3, p1, point)
                if inside:
                    self.draw_pixel(x, y, color)