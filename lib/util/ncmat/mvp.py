"""Provides functions to calculate model view projection matrices."""

from functools import reduce
import numpy as np
import math
from .transform import translate

def model(trans_n_values):
    return reduce(np.dot,
            [
                tv[0](*tv[1]) for tv in trans_n_values
            ]
    )

# Adapted from the class material and
# https://community.khronos.org/t/view-and-perspective-matrices/74154
def view(eye, target, up):
    n = eye - target
    n = n / np.linalg.norm(n)
    up = up / np.linalg.norm(up)
    u = np.cross(-n, up)
    v = np.cross(u, -n)
    R = np.identity(4)
    R[:3,:3] = np.vstack((u,v,n))
    T = np.array(translate(*-eye)).reshape(4,4)
    return np.matmul(R,T)

# Adapted from the class material and
# https://community.khronos.org/t/view-and-perspective-matrices/74154
def projection(fovy, aspect, near, far):
    cot_angle = 1.0/math.tan(math.radians(fovy)/2.0)
    sx = cot_angle / aspect
    sy =  cot_angle
    sz = (far+near)/(near-far)
    tw = 2*far*near/(near-far)

    return np.matrix([[sx,0,0,0],
                      [0,sy,0,0],
                      [0,0,sz,tw],
                      [0,0,-1,0]])

