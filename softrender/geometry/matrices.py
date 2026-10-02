import numpy as np
from math import pi, cos, sin

# https://en.wikipedia.org/wiki/Camera_matrix
# https://www.brainvoyager.com/bv/doc/UsersGuide/CoordsAndTransforms/SpatialTransformationMatrices.html
# https://www.youtube.com/watch?v=mpTl003EXCY&list=LLa6zoMLQWrtFEn4pp0W2Tzg

# TODO: ortho

# https://gitlab.freedesktop.org/mesa/mesa/blob/master/src/mesa/math/m_matrix.c#L982
def frustrum(left = -1, right = 1,
             bottom = 1, top = -1,
             near = 1, far = 1000):

    x = (2 * near) / (right - left)
    y = (2 * near) / (top - bottom)
    a = (right + left) / (right - left)
    b = (top + bottom) / (top - bottom)
    c = -(far + near) / (far - near)
    d = -(2 * far * near) / (far - near)

    return np.matrix([
        [x,  0,  a,  0],
        [0,  y,  b,  0],
        [0,  0,  c,  d],
        [0,  0, -1,  0],
    ])

def transpose(x, y, z):
    return np.matrix([
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1],
    ])

def look_at(eye, target, up=(0, 1, 0)):
    """World to camera space: camera at eye, looking down -z towards target."""
    eye = np.asarray(eye, dtype=float)
    forward = np.asarray(target, dtype=float) - eye
    forward /= np.linalg.norm(forward)
    right = np.cross(forward, up)
    right /= np.linalg.norm(right)
    true_up = np.cross(right, forward)

    return np.matrix([
        [*right,    -np.dot(right, eye)],
        [*true_up,  -np.dot(true_up, eye)],
        [*-forward,  np.dot(forward, eye)],
        [0, 0, 0, 1],
    ])

def rotate_y(t):
    return np.matrix([
        [ cos(t),      0, sin(t), 0],
        [      0,      1,      0, 0],
        [-sin(t),      0, cos(t), 0],
        [      0,      0,      0, 1],
    ])

def screen(width, height):
    return np.matrix([
        [height/2,        0, 0, 0],
        [       0, height/2, 0, 0],
        [       0,        0, 1, 0],
        [       0,        0, 0, 1],
    ]) * transpose(width / height, 1, 0)
