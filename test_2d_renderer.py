from renderer import Renderer
from point import Point

def test_2d_render():
    color_buffer = Renderer(512, 512)

    def shader(p):
        return (p.x * 255, p.y * 255, 128)

    #color_buffer.draw_shader(shader)

    for i in range(0, 255, 15):
        color_buffer.draw_line(Point(10, 10), Point(color_buffer.width-10, color_buffer.height-10-i), (0, 0, 128))
    for i in range(0, 255, 15):
        color_buffer.draw_line(Point(color_buffer.width-10, 10), Point(10, color_buffer.height-10-i), (0, 0, 128))
    for i in range(0, color_buffer.width, 15):
        color_buffer.draw_line(Point(i, 10), Point(color_buffer.width/2, color_buffer.height-10), (0, 0, 128))
    color_buffer.draw_fill_triangle(Point(15, 15), Point(10, 100), Point(50, 10), (0, 128, 0))
    color_buffer.draw_wire_triangle(Point(15, 15), Point(10, 100), Point(50, 10), (0, 0, 0))
    color_buffer.draw_fill_triangle(Point(255, 15), Point(270, 100), Point(240, 10), (0, 128, 0))
    color_buffer.draw_rect(Point(50, 50), Point(100, 100), (128, 0, 0))
    color_buffer.draw_pixel(255, 255, 0, (255, 255, 255))
    color_buffer.draw_fill_trapezoid(Point(260, 255), Point(250, 300), Point(280, 300), Point(270, 255), (255, 255, 255))


    color_buffer.show()

test_2d_render()