# Scene graph: a child's world transform is its parent's times its own, and
# meshes are moved into world space with normals that still point outwards.
import numpy as np

from softrender.scene import Node, plane, rotate_y, scale, translate


def test_child_inherits_parent_transform():
    child = Node('child', transform=translate(0, 1, 0))
    root = Node('root', transform=translate(5, 0, 0) @ rotate_y(90)).add(
        Node('middle', transform=scale(2)).add(child))

    world = dict((node.name, matrix) for node, matrix in root.walk())
    origin = world['child'] @ np.array([0, 0, 0, 1])
    assert np.allclose(origin[:3], (5, 2, 0)), origin
    # rotate_y(90) turns +x into -z
    x_axis = world['child'] @ np.array([1, 0, 0, 0])
    assert np.allclose(x_axis[:3], (0, 0, -2)), x_axis


def test_world_meshes_move_vertices_and_normals():
    root = Node('root', transform=translate(0, 3, 0)).add(
        Node('floor', plane(2, cells=2), translate(1, 0, 0) @ scale(1, 1, 4)),
        Node('empty'))

    meshes = list(root.world_meshes())
    assert [node.name for node, _ in meshes] == ['floor']
    mesh = meshes[0][1]
    positions = np.array([v.position for v in mesh.vertices])
    assert np.allclose(positions.min(axis=0), (0, 3, -4))
    assert np.allclose(positions.max(axis=0), (2, 3, 4))
    for polygon in mesh.polygons:
        assert np.allclose(polygon.normal, (0, 1, 0))
    # The node's own mesh is left untouched
    assert np.allclose(root.children[0].mesh.vertices[0].position, (-1, 0, -1))


if __name__ == '__main__':
    test_child_inherits_parent_transform()
    test_world_meshes_move_vertices_and_normals()
    print("ok")
