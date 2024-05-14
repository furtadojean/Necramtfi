"""Provides functions to deal with coordinate buffers."""

from OpenGL.GL import ctypes, glBindBuffer, glBufferData, glEnableVertexAttribArray, glGetAttribLocation, glVertexAttribPointer, glGenBuffers
from OpenGL.GL import GL_ARRAY_BUFFER, GL_STATIC_DRAW, GL_FLOAT
import numpy as np


def coordinates_create(dimension=3):
    return _buffer(10000, dimension, GL_ARRAY_BUFFER, GL_STATIC_DRAW)


def coordinates_upload(coordinates, vector, replace=False):
    first_new_position = coordinates.size

    if replace:
        coordinates.capacity = len(vector)
        coordinates.vector = np.resize(coordinates.vector, coordinates.capacity)

        coordinates.vector["position"] = vector
        coordinates.size = coordinates.capacity
        first_new_position = 0

    # Concatenate
    else:
        new_size = coordinates.size + len(vector)
        if coordinates.capacity < new_size:
            coordinates.capacity = new_size
            coordinates.vector = np.resize(coordinates.vector, coordinates.capacity)

        coordinates.vector["position"][coordinates.size:new_size] = vector
        coordinates.size = new_size

    count = coordinates.size - first_new_position
    return (first_new_position, count)


def coordinates_link(program, attribute, coordinates):
    glBindBuffer(coordinates.target, coordinates.buffer)
    glBufferData(coordinates.target, coordinates.vector.nbytes, coordinates.vector, coordinates.usage)

    stride = coordinates.vector.strides[0]
    offset = ctypes.c_void_p(0)
    loc = glGetAttribLocation(program, attribute)
    glEnableVertexAttribArray(loc)
    glVertexAttribPointer(loc, coordinates.dimension, GL_FLOAT, False, stride, offset)






class _buffer():
    def __init__(self, capacity, dimension, target, usage):
        self.size = 0
        self.capacity = capacity
        self.dimension = dimension
        self.vector = np.zeros(capacity, [("position", np.float32, dimension)])

        self.buffer = glGenBuffers(1)
        self.target = target

        self.usage = usage
