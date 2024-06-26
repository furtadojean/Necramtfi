"""Abstracts the graphical library to facilitate change"""

from .glsl import GLSL

from .program import program_create, program_link, program_use

from .shader import shader_vertex_create, shader_fragment_create, shader_set_source, shader_compile, shader_attach

from .flags import F_depth_test, F_polygonal_mode
from .functions import FC_resize_viewport, FC_clear, FC_clear_color, FC_draw_arrays, FC_set_uniform_mat4, FC_set_uniform_vec3, FC_set_uniform_float, FC_set_uniform_int

from .coordinates import coordinates_create, coordinates_upload, coordinates_link

from .textures import textures_create, textures_load, textures_use

from .constants import C_TRIANGLES
