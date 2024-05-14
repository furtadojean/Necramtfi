"""Provides functions to deal with a program."""

from OpenGL.GL import glCreateProgram, glLinkProgram, glUseProgram, glGetProgramiv, glGetProgramInfoLog, GL_LINK_STATUS


def program_create():
    return glCreateProgram()


def program_link(program):
    glLinkProgram(program)
    if not glGetProgramiv(program, GL_LINK_STATUS):
        print(glGetProgramInfoLog(program))
        raise RuntimeError('Linking error')

def program_use(program):
    glUseProgram(program)
