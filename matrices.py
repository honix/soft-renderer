import numpy as np
import math

# https://en.wikipedia.org/wiki/Camera_matrix
# https://www.youtube.com/watch?v=mpTl003EXCY&list=LLa6zoMLQWrtFEn4pp0W2Tzg

# TODO: ortho
# TODO: look-at

# https://gitlab.freedesktop.org/mesa/mesa/blob/master/src/mesa/math/m_matrix.c#L982
def frustrum(left = -2, right = 2,
             bottom = 2, top = -2,
             near = 1, far = 5):

    x = (2 * near) / (right - left);
    y = (2 * near) / (top - bottom);
    a = (right + left) / (right - left);
    b = (top + bottom) / (top - bottom);
    c = -(far + near) / (far - near);
    d = -(2 * far * near) / (far - near);

    return np.matrix([
        [x,  0,  a,  0],
        [0,  y,  b,  0],
        [0,  0,  c,  d],
        [0,  0, -1,  0],
    ])
