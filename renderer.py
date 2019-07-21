from buffer import Buffer
from point import Point

class Renderer():
    def __init__(self, width, height, depth_test=True):
        self.width = width
        self.height = height
        self.depth_test = depth_test
        self.color_buffer = Buffer(width, height, channels=3)
        self.depth_buffer = Buffer(width, height, channels=1, fill_value=1)
    
    def show(self):
        self.color_buffer.show()

    def draw_point(self, p, color):
        pint = p.integrated()

        # X and Y are flipped in buffer, so..
        if (0 <= pint.x < self.width and 0 <= pint.y < self.height):
            # TODO: color can be as class
            if (self.depth_test):
                if (self.depth_buffer[pint.y, pint.x] < p.z):
                    return
                self.depth_buffer[pint.y, pint.x] = p.z
            self.color_buffer[pint.y, pint.x] = color

    def draw_shader(self, shader):
        for x in range(self.width):
            for y in range(self.height):
                self.draw_point(Point(x, y), shader(Point(x/self.width, y/self.height)))

    def draw_rect(self, p1, p2, color):
        maxx = max(p1.x, p2.x)
        maxy = max(p1.y, p2.y)
        minx = min(p1.x, p2.x)
        miny = min(p1.y, p2.y)
        for cx in range(maxx - minx):
            for cy in range(maxy - miny):
                x = cx + minx
                y = cy + miny
                self.draw_point(Point(x, y), color)

    def draw_line(self, p1, p2, color):
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
        movex, movey = p1.x, p1.y

        while True:
            self.draw_point(Point(movex, movey, z), color)
            if movex == p2.x and movey == p2.y: break
            erri = err + err
            if erri >= dy:
                err += dy
                movex += sx
            if erri <= dx:
                err += dx
                movey += sy

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
        # TODO: iterpolate z-value
        z = sum([p1.z, p2.z, p3.z]) / 3

        for cx in range(int(maxx - minx)):
            for cy in range(int(maxy - miny)):
                x = cx + minx
                y = cy + miny
                point = Point(x, y)
                inside = True
                inside &= edge(p1, p2, point)
                inside &= edge(p2, p3, point)
                inside &= edge(p3, p1, point)
                if inside:
                    self.draw_point(Point(x, y, z), color)
