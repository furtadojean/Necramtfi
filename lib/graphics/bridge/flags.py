from ...util import flag_two_functions, flag_one_function
from OpenGL.GL import glEnable, glDisable, glPolygonMode
from OpenGL.GL import GL_DEPTH_TEST, GL_FRONT_AND_BACK, GL_FILL, GL_LINE


F_depth_test = flag_two_functions(glDisable, glEnable, [GL_DEPTH_TEST])

F_polygonal_mode = flag_one_function(glPolygonMode, [GL_FRONT_AND_BACK, GL_FILL], [GL_FRONT_AND_BACK, GL_LINE])
