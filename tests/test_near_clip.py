# A floor that runs from far in front of the camera to behind it. Without
# near-plane clipping the vertices behind the camera project mirrored and the
# floor smears over the sky. Checks that the floor covers exactly the pixels a
# ray cast says it should, and that the interpolated world position is right
# (varyings survive clipping).
import numpy as np

from softrender.camera import project
from softrender.geometry import matrices
from softrender.geometry.point import Point
from softrender.geometry.polygon import Polygon
from softrender.geometry.vertex import Vertex
from softrender.raster.renderer import Renderer
from softrender.shaders import Shader


class PositionShader(Shader):
    def vertex(self, vertex, polygon):
        return {'position': vertex.position}

    def fragment(self, v):
        self.positions[self.pixel] = v['position']
        return (1, 1, 1)


def test_near_clip(size=128):
    camera = Point(0, 2, 5)
    renderer = Renderer(size, size)
    # Built here instead of camera.view_projection, so the ray cast below
    # can rely on this exact camera: 90 degree view, looking down -z
    transform_matrix = matrices.screen(size, size) * matrices.frustrum() * matrices.transpose(*-camera)

    corners = [(-40, -40), (40, -40), (40, 30), (-40, 30)]  # (x, z), camera is at z = 5
    vertices = [Vertex(Point(x, 0, z), Point(0, 1, 0)) for x, z in corners]
    for vertex in vertices:
        project(vertex, transform_matrix)

    shader = PositionShader()
    shader.positions = np.full((size, size, 3), np.nan)
    # Let the shader know which pixel it is shading
    triangle_pixels = renderer.triangle_pixels
    def tracking_pixels(*args):
        for x, y, z in triangle_pixels(*args):
            shader.pixel = (y, x)
            yield x, y, z
    renderer.triangle_pixels = tracking_pixels

    for indices in ((0, 2, 1), (0, 3, 2)):
        renderer.draw_triangle(*(vertices[i] for i in indices), shader, Polygon(indices))

    # Ray cast every pixel center against the floor. The camera looks down -z,
    # screen y points down, and the projection maps x/w and y/w to -1..1.
    ys, xs = np.mgrid[0:size, 0:size] + 0.5
    nx = xs / size * 2 - 1
    ny = ys / size * 2 - 1
    with np.errstate(divide='ignore'):
        t = np.where(ny > 0, camera.y / ny, np.inf)  # distance along -z
    hx, hz = camera.x + nx * t, camera.z - t
    expected = (ny > 0) & (hx > -40) & (hx < 40) & (hz > -40) & (hz < 30)

    drawn = renderer.color_buffer.data[:, :, 0] > 0
    wrong = (drawn != expected).sum()
    assert wrong <= size // 8, f"{wrong} pixels differ from the ray cast"  # slack for the far edge
    assert drawn[-1].all(), "floor right under the camera is missing"

    # Interpolated world position matches the ray hit point
    hit = np.stack([hx, np.zeros_like(hx), hz], axis=-1)
    error = np.abs(shader.positions - hit)[drawn & expected].max()
    assert error < 1e-4, f"interpolated position off by {error}"


test_near_clip()
print("ok")
