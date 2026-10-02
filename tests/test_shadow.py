# Shadow map: a small square floating above a floor, lit from straight above.
# The floor under the square must be in shadow, the floor around it and the
# square's own top lit (no shadow acne), and edges partly lit (PCF).
from softrender.scene import Node, plane, translate
from softrender.shadow import ShadowMap

UP = (0, 1, 0)


def make_shadow_map():
    scene = Node('scene').add(
        Node('floor', plane(10, cells=4)),
        Node('blocker', plane(2, cells=1), translate(0, 2, 0)),
    )
    meshes = [mesh for _, mesh in scene.world_meshes()]
    positions = [v.position for mesh in meshes for v in mesh.vertices]
    shadow = ShadowMap(UP, positions, size=128)
    shadow.render(meshes)
    return shadow


def test_shadow_under_blocker():
    shadow = make_shadow_map()
    assert shadow.visibility((0, 0, 0), UP) == 0
    assert shadow.visibility((0.5, 0, -0.5), UP) == 0


def test_lit_outside_and_no_acne():
    shadow = make_shadow_map()
    assert shadow.visibility((3, 0, 3), UP) == 1
    assert shadow.visibility((-4, 0, 2), UP) == 1
    # Surfaces facing the light don't shadow themselves
    assert shadow.visibility((0.3, 2, 0.2), UP) == 1
    assert shadow.visibility((2.5, 0, -1.7), UP) == 1


def test_soft_edge():
    shadow = make_shadow_map()
    # Right at the blocker's edge the 3x3 filter sees both sides
    edge = shadow.visibility((1, 0, 0), UP)
    assert 0 < edge < 1, edge


if __name__ == '__main__':
    test_shadow_under_blocker()
    test_lit_outside_and_no_acne()
    test_soft_edge()
    print("ok")
