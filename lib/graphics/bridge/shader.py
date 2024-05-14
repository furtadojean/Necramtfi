"""Provides functions to deal with shaders."""

from OpenGL.GL import glCreateShader, glShaderSource, glCompileShader, glAttachShader, glGetShaderiv, glGetShaderInfoLog, GL_VERTEX_SHADER, GL_FRAGMENT_SHADER, GL_COMPILE_STATUS

def shader_vertex_create():
    return glCreateShader(GL_VERTEX_SHADER)

def shader_fragment_create():
    return glCreateShader(GL_FRAGMENT_SHADER)

def shader_set_source(shader, glsl):
    glShaderSource(shader, glsl.code)

def shader_compile(shader):
    glCompileShader(shader)
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(shader).decode()
        print(error)
        raise RuntimeError("Erro de compilacao do shader")

def shader_attach(program, shader):
    glAttachShader(program, shader)
