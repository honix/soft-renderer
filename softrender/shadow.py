"""Shadow mapping for one directional light.

Two passes, the way a GPU does it:

1. Depth pass: render the scene from the light with an orthographic camera
   (the light's rays are parallel) and keep only the depth buffer. Each
   texel holds the distance to the closest surface the light hits.
2. Lookup: while shading, a lit shader projects the pixel's world position
   into the same light space. If something in the depth map is closer to
   the light than the pixel, the pixel is in shadow.

A surface shadows itself a bit ("shadow acne") because of the limited
depth map resolution, so the lookup point is pushed off the surface along
the normal by about a texel. Edges are softened by averaging 3x3 lookups
(percentage closer filtering).
"""
import numpy as np

from .camera import project
from .geometry import matrices
from .raster.renderer import Renderer
from .shaders import normalize


class ShadowMap:
    def __init__(self, light_direction, positions, size=1024, normal_offset=1.5, bias=0.002):
        self.size = size
        self.normal_offset = normal_offset
        self.bias = bias

        # Fit the light's box around all the given positions
        light_direction = normalize(np.asarray(light_direction, dtype=float))
        positions = np.asarray(positions, dtype=float)
        center = (positions.min(axis=0) + positions.max(axis=0)) / 2
        radius = np.max(np.linalg.norm(positions - center, axis=1))
        view = matrices.look_at(center + light_direction * radius * 2, center)
        light_space = np.c_[positions, np.ones(len(positions))] @ np.asarray(view).T
        (left, bottom, _), (right, top, _) = light_space[:, :3].min(axis=0), light_space[:, :3].max(axis=0)
        # Square texels, so the normal offset is the same in x and y
        half = max(right - left, top - bottom) / 2
        mx, my = (left + right) / 2, (bottom + top) / 2
        near, far = -light_space[:, 2].max(), -light_space[:, 2].min()
        near, far = near - 0.01 * (far - near), far + 0.01 * (far - near)
        self.texel = 2 * half / size  # texel size in world units
        self.matrix = np.asarray(
            matrices.screen(size, size) *
            matrices.ortho(mx - half, mx + half, my + half, my - half, near, far) *
            view
        )
        self.depth = None

    def render(self, meshes):
        """Depth pass. Overwrites vertex.clip/tposition/w of the meshes, so
        run it before projecting them with the camera."""
        renderer = Renderer(self.size, self.size)
        for mesh in meshes:
            for vertex in mesh.vertices:
                project(vertex, self.matrix)
            # Only depth is needed, so no shader: plain fill with the depth test.
            # The light's box holds the whole scene, nothing to clip
            for polygon in mesh.polygons:
                renderer.draw_fill_triangle(*(mesh.vertices[i] for i in polygon.indices), 255)
        self.depth = renderer.depth_buffer.data

    def visibility(self, position, normal):
        """How much light reaches the position: 0 in shadow, 1 fully lit."""
        p = np.asarray(position, dtype=float) + normalize(np.asarray(normal, dtype=float)) * self.texel * self.normal_offset
        x, y, z = (self.matrix @ np.append(p, 1))[:3]  # orthographic, w stays 1
        x, y = int(x), int(y)
        if not (1 <= x < self.size - 1 and 1 <= y < self.size - 1): return 1
        return np.mean(self.depth[y - 1:y + 2, x - 1:x + 2] >= z - self.bias)
