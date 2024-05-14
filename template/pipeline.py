from lib.graphics.bridge import *

class pipeline:
    """Simplifies the programmable pipeline.

    Instance attributes:
        program: program -- program created
        v_shader: shader -- vertex shader
        f_shader: shader -- fragment shader
    Instance methods:
        vertex_shader -- sets up vertex shader
        fragment_shader -- sets up fragment shader
        ready -- must be called once shaders are ready
    """
    
    def __init__(self):
        self.program = program_create()
        self.v_shader = shader_vertex_create()
        self.f_shader = shader_fragment_create()

    def vertex_shader(self, glsl):
        shader_set_source(self.v_shader, glsl)
        shader_compile(self.v_shader)
        shader_attach(self.program, self.v_shader)

    def fragment_shader(self, glsl):
        shader_set_source(self.f_shader, glsl)
        shader_compile(self.f_shader)
        shader_attach(self.program, self.f_shader)

    def ready(self):
        program_link(self.program)
        program_use(self.program)
