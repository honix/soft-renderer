import argparse
import os
import time

import numpy as np

from softrender.camera import frame, project, view_projection
from softrender.geometry.obj import read_obj
from softrender.raster.renderer import Renderer
from softrender.scene import Node, plane, rotate_y, scale, translate
from softrender.shaders import LIGHT_DIRECTION, SHADERS
from softrender.shadow import ShadowMap

MODELS_DIR = os.path.join(os.path.dirname(__file__), 'assets', 'models')


def load_mesh(mesh_path):
    # polygons.obj - some flat polys, cube.obj - simplest one,
    # teapot.obj - many triangles, lamp.obj - n-gons, cessna.obj - big one
    if not os.path.exists(mesh_path):
        mesh_path = os.path.join(MODELS_DIR, mesh_path)
    return read_obj(mesh_path)


# Low and from the left, so the teapots throw long shadows towards the right
TEAPOTS_LIGHT = (-1.0, 0.9, 0.5)


def teapots_scene():
    """A ground plane with a few teapots. The small teapot is a child of the
    blue one, so it rides on its lid wherever the blue one goes."""
    teapot = load_mesh('teapot.obj')
    small = Node('small teapot', teapot, translate(0, 3.15, 0) @ rotate_y(-60) @ scale(0.35),
                 material={'albedo': (0.9, 0.75, 0.2)})
    return Node('scene').add(
        Node('ground', plane(18), material={'albedo': (0.7, 0.7, 0.65), 'specular': 0.1}),
        Node('teapots', transform=rotate_y(15)).add(
            Node('red teapot', teapot, translate(-4.5, 0, 1.5) @ rotate_y(30)),
            Node('blue teapot', teapot, translate(4, 0, -1) @ rotate_y(-20) @ scale(1.2),
                 material={'albedo': (0.2, 0.4, 0.8)}).add(small),
            Node('green teapot', teapot, translate(0.5, 0, 5) @ rotate_y(160) @ scale(0.7),
                 material={'albedo': (0.25, 0.65, 0.3)}),
        ),
    )


def render(scene, shader_name, size, out, aa=1, shadows=True, light=LIGHT_DIRECTION):
    start = time.time_ns()
    print("Start")

    meshes = list(scene.world_meshes())
    renderer = Renderer(size * aa, size * aa, aa=aa)

    positions = [v.position for _, mesh in meshes for v in mesh.vertices]
    camera_position, target = frame(positions, renderer.width, renderer.height)

    shadow = None
    if shadows:
        print("Rendering shadow map..")
        shadow = ShadowMap(light, positions)
        shadow.render([mesh for _, mesh in meshes])

    print("Transforming points to screen pos..")

    transform_matrix = view_projection(camera_position, target, renderer.width, renderer.height)
    for _, mesh in meshes:
        for vertex in mesh.vertices:
            project(vertex, transform_matrix)

    print("Rendering..")

    i = 0
    for node, mesh in meshes:
        shader = SHADERS[shader_name](camera_position, light_direction=light, shadow=shadow, **node.material)
        for polygon in mesh.polygons:
            if np.dot(mesh.vertices[polygon.indices[0]].position - camera_position, polygon.normal) >= 0: continue
            vertices = list(map(lambda x: mesh.vertices[x], polygon.indices))
            renderer.draw_triangle(*vertices, shader, polygon)

            i += 1
            if i % 500 == 0: print(f"{i} polygons drawn")

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
    parser.add_argument('--scene', choices=['teapots'], help='render a demo scene instead of --mesh')
    parser.add_argument('--no-shadows', action='store_true')
    parser.add_argument('--out', help='save to a png instead of opening a window')
    args = parser.parse_args()
    scene = teapots_scene() if args.scene == 'teapots' else Node('scene', load_mesh(args.mesh))
    light = TEAPOTS_LIGHT if args.scene == 'teapots' else LIGHT_DIRECTION
    render(scene, args.shader, args.size, args.out, args.aa, not args.no_shadows, light)


# Perspective projection
# https://en.wikipedia.org/wiki/3D_projection#Mathematical_formula
