"""Provides functions for geometric transformations."""

import numpy as np
from math import sin, cos

def translate(t_x, t_y, t_z):
    translate_matrix = np.identity(4)

    translate_matrix[0][3] = t_x
    translate_matrix[1][3] = t_y
    translate_matrix[2][3] = t_z

    return translate_matrix

def scale(s_x, s_y, s_z):
    scale_matrix = np.identity(4)

    scale_matrix[0][0] = s_x
    scale_matrix[1][1] = s_y
    scale_matrix[2][2] = s_z

    return scale_matrix

def rotate(a_x, a_y, a_z):
    z_sin = sin(a_z); z_cos = cos(a_z)
    x_sin = sin(a_x); x_cos = cos(a_x)
    y_sin = sin(a_y); y_cos = cos(a_y)

    rotate_matrix = np.identity(4)
    rotate_matrix[0][0] = (z_cos*y_cos)-(y_sin*z_sin*x_sin)
    rotate_matrix[0][1] = -(z_sin*x_cos)
    rotate_matrix[0][2] = (z_sin*x_sin*y_cos) + (y_sin*z_cos)
    rotate_matrix[1][0] = (z_sin*y_cos) + (y_sin*z_cos*x_sin)
    rotate_matrix[1][1] = (z_cos*x_cos)
    rotate_matrix[1][2] = (y_sin*z_sin) - (z_cos*x_sin*y_cos)
    rotate_matrix[2][0] = -(y_sin*x_cos)
    rotate_matrix[2][1] = x_sin
    rotate_matrix[2][2] = (x_cos*y_cos)

    return rotate_matrix
