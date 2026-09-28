import argparse
import time

import numpy as np

import matrices
from renderer import Renderer
from point import Point
from shaders import SHADERS


def test_persp_render(mesh_path, shader_name, size, out):
    start = time.time_ns()
    print("Start")

    from obj import read_obj

    # polygons.obj - some flat polys, cube.obj - simplest one,
    # teapot.obj - many triangles, lamp.obj - n-gons, cessna.obj - doesnt work..
    mesh = read_obj(mesh_path)

    renderer = Renderer(size, size)

    camera_position = Point(0, 2, 5)
    shader = SHADERS[shader_name](camera_position)

    print("Transforming points to screen pos..")

    # TODO: split camera/world transform and object transform
    transform_matrix = (
        matrices.screen(renderer.width, renderer.height) *
        matrices.frustrum() *
        #matrices.rotate_y(-1/6 * math.pi) *
        matrices.transpose(*-camera_position)
    )

    def transform(vertex):
        vertex_project = np.concatenate((vertex.position, [1]))[:,None]
        vertex_transformed = transform_matrix @ vertex_project
        vertex.w = float(vertex_transformed[3])
        vertex_transformed /= vertex_transformed[3]
        vertex_unproject = np.asarray(vertex_transformed).flatten()[:3]

        vertex.tposition = vertex_unproject.view(Point)

    for vertex in mesh.vertices:
        transform(vertex)

    print("Rendering..")

    # TODO: move those routines to mesh renderer class (?)
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
    parser.add_argument('--mesh', default='teapot.obj')
    parser.add_argument('--size', type=int, default=512)
    parser.add_argument('--out', help='save to a png instead of opening a window')
    args = parser.parse_args()
    test_persp_render(args.mesh, args.shader, args.size, args.out)


# Perspective projection
# https://en.wikipedia.org/wiki/3D_projection#Mathematical_formula
