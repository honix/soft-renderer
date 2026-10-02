# Draws a few 2D primitives straight in screen space and checks pixels.
# Lines and triangles take vertices and read vertex.tposition, so screen
# points are wrapped in a Vertex.
from softrender.raster.renderer import Renderer
from softrender.geometry.point import Point
from softrender.geometry.vertex import Vertex


def v(x, y):
    return Vertex(Point(x, y, 0))


def test_2d_render(show=False):
    renderer = Renderer(512, 512)
    width, height = renderer.width, renderer.height

    def shader(p):
        return (p.x * 255, p.y * 255, 128)

    renderer.draw_shader(shader)
    assert tuple(renderer.color_buffer[0, 0]) == (0, 0, 128)
    assert tuple(renderer.color_buffer[256, 128]) == (63, 127, 128)

    for i in range(0, 255, 15):
        renderer.draw_line(v(10, 10), v(width-10, height-10-i), (0, 0, 128))
    for i in range(0, 255, 15):
        renderer.draw_line(v(width-10, 10), v(10, height-10-i), (0, 0, 128))
    for i in range(0, width, 15):
        renderer.draw_line(v(i, 10), v(width/2, height-10), (0, 0, 128))
    # Both ends of a line are drawn
    assert tuple(renderer.color_buffer[10, 10]) == (0, 0, 128)
    assert tuple(renderer.color_buffer[height-10, width-10]) == (0, 0, 128)

    renderer.draw_fill_triangle(v(15, 15), v(10, 100), v(50, 10), (0, 128, 0))
    assert tuple(renderer.color_buffer[30, 25]) == (0, 128, 0)
    renderer.draw_wire_triangle(v(15, 15), v(10, 100), v(50, 10), (0, 0, 0))
    assert tuple(renderer.color_buffer[100, 10]) == (0, 0, 0)

    renderer.draw_fill_triangle(v(255, 15), v(270, 100), v(240, 10), (0, 128, 0))
    renderer.draw_wire_triangle(v(255, 15), v(270, 100), v(240, 10), (0, 128, 0))
    assert tuple(renderer.color_buffer[40, 258]) == (0, 128, 0)

    renderer.draw_rect(Point(50, 50), Point(100, 100), (128, 0, 0))
    assert tuple(renderer.color_buffer[75, 75]) == (128, 0, 0)

    renderer.draw_pixel(255, 255, 0, (255, 255, 255))
    assert tuple(renderer.color_buffer[255, 255]) == (255, 255, 255)

    renderer.draw_fill_trapezoid(v(260, 255), v(250, 300), v(280, 300), v(270, 255), (255, 255, 255))
    assert tuple(renderer.color_buffer[280, 265]) == (255, 255, 255)
    assert tuple(renderer.color_buffer[280, 245]) != (255, 255, 255)

    if show:
        renderer.show()


if __name__ == '__main__':
    test_2d_render(show=True)
    print("ok")
