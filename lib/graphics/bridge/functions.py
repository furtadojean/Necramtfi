from OpenGL.GL import glViewport, glClearColor, glClear, glDrawArrays, glGetUniformLocation, glUniformMatrix4fv
from OpenGL.GL import GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_TRUE

def FC_resize_viewport(x, y, width, height):
    glViewport(x, y, width, height)

def FC_clear_color(red=1.0, green=1.0, blue=1.0, alpha=1.0):
    glClearColor(red, green, blue, alpha)

def FC_clear():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

def FC_draw_arrays(mode, first, count):
    glDrawArrays(mode, first, count)

def FC_set_uniform_mat4(program, name, value):
    loc = glGetUniformLocation(program, name)
    glUniformMatrix4fv(loc, 1, GL_TRUE, value)