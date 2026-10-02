import argparse
import os
import time

import numpy as np

from softrender.camera import frame, project, view_projection
from softrender.geometry.obj import read_obj
from softrender.raster.renderer import Renderer
from softrender.shaders import SHADERS

MODELS_DIR = os.path.join(os.path.dirname(__file__), 'assets', 'models')


def render_mesh(mesh_path, shader_name, size, out, aa=1):
    start = time.time_ns()
    print("Start")

    # polygons.obj - some flat polys, cube.obj - simplest one,
    # teapot.obj - many triangles, lamp.obj - n-gons, cessna.obj - big one
    if not os.path.exists(mesh_path):
        mesh_path = os.path.join(MODELS_DIR, mesh_path)
    mesh = read_obj(mesh_path)

    renderer = Renderer(size * aa, size * aa, aa=aa)

    camera_position, target = frame([v.position for v in mesh.vertices], renderer.width, renderer.height)
    shader = SHADERS[shader_name](camera_position)

    print("Transforming points to screen pos..")

    transform_matrix = view_projection(camera_position, target, renderer.width, renderer.height)
    for vertex in mesh.vertices:
        project(vertex, transform_matrix)

    print("Rendering..")

    i = 0
    for polygon in mesh.polygons:
        if np.dot(mesh.vertices[polygon.indices[0]].position - camera_position, polygon.normal) >= 0: continue
        vertices = list(map(lambda x: mesh.vertices[x], polygon.indices))
        renderer.draw_triangle(*vertices, shader, polygon)

        i += 1
        if i % 50 == 0: print(f"{i} polygons drawn")

    end = time.time_ns()
    print(f"{(end - start) / 1000000000} seconds ellapsed")

    if out:
        renderer.save(out)
    else:
        renderer.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('shader', nargs='?', default='phong', choices=SHADERS)
    parser.add_argument('--mesh', default='teapot.obj', help='path, or a file name in assets/models')
    parser.add_argument('--size', type=int, default=512)
    parser.add_argument('--aa', type=int, default=1, help='supersampling factor (1 = off), cost grows as aa^2')
    parser.add_argument('--out', help='save to a png instead of opening a window')
    args = parser.parse_args()
    render_mesh(args.mesh, args.shader, args.size, args.out, args.aa)


# Perspective projection
# https://en.wikipedia.org/wiki/3D_projection#Mathematical_formula
