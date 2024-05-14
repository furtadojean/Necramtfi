from lib.graphics.bridge import *
from lib.io.bridge import *
from lib.io.user_input import io_controller

from .pipeline import pipeline

class template:
    """Aggregates components and sets up application.

    Instance attributes:
        io_controller: io_controler -- allows adding callbacks for key, mouse and click actions
        cursor: flag -- controls cursor visibility
        vertex_glsl: glsl
        fragment_glsl: glsl
        pipeline: pipeline -- allows access to the program and shaders
        vcoordinates: coordinates -- vertex coordinates
        fcoordinates: coordinates -- fragment/texture coordinates
        attribute_name: type -- description
    Instance methods:
        ready -- must be called once coordinates are ready
    """

    def __init__(self, title):
        self.window = window_create(800, 800, title)
        self.io_controller = io_controller(self.window)
        self.cursor = F_cursor(self.window)
        self.cursor.off()

        self._setup_focus()
        self._setup_resize()

        self.vertex_glsl = GLSL()
        self.fragment_glsl = GLSL()

        self.pipeline = pipeline()

        self._setup_vertices()
        self._setup_textures()
        self._setup_mvp()

        self.pipeline.vertex_shader(self.vertex_glsl)
        self.pipeline.fragment_shader(self.fragment_glsl)
        self.pipeline.ready()


        self.vcoordinates = None
        self.fcoordinates = None

        F_depth_test.on()

    def ready(self):
        if self.vcoordinates == None or self.fcoordinates == None:
            return
        coordinates_link(self.pipeline.program, "vertex_position", self.vcoordinates)
        coordinates_link(self.pipeline.program, "texture_position", self.fcoordinates)



    def _setup_vertices(self):
        self.vertex_glsl.add_to_global(
            vec3
            .get_declaration(var.SQualifier.attribute, "vertex_position")
        )
        self.vertex_glsl.add_to_function("void main()",
            "gl_Position = projection * view * model * "
             +
             vec4.get_new("vertex_position, 1.0")
             +
             ";"
        )

    def _setup_textures(self):
        self.vertex_glsl.add_to_global(
            vec2
            .get_declaration(var.SQualifier.attribute, "texture_position")
        )
        self.vertex_glsl.add_to_global(
            vec2
            .get_declaration(var.SQualifier.varying, "out_texture")
        )
        self.vertex_glsl.add_to_function("void main()",
            "out_texture = "
            +
            vec2.get_new("texture_position")
             +
             ";"
        )

        self.fragment_glsl.add_to_global(
            vec2
            .get_declaration(var.SQualifier.varying, "out_texture")
        )
        self.fragment_glsl.add_to_global(
            var(var.DType.sampler2D)
            .get_declaration(var.SQualifier.uniform, "samplerTexture")
        )
        self.fragment_glsl.add_to_function("void main()", """
            vec4 my_tex = texture2D(samplerTexture, out_texture);
            if(my_tex.a < 0.1)
                discard;
            gl_FragColor = my_tex;
            """
        )

    def _setup_mvp(self):
        self.vertex_glsl.add_to_global(
            mat4
            .get_declaration(var.SQualifier.uniform, "model")
        )
        self.vertex_glsl.add_to_global(
            mat4
            .get_declaration(var.SQualifier.uniform, "view")
        )
        self.vertex_glsl.add_to_global(
            mat4
            .get_declaration(var.SQualifier.uniform, "projection")
        )


    def _setup_focus(self):
        def callback(window, focused):
            if focused:
                if self.cursor.state:
                    self.cursor.off()
            else:
                self.cursor.on()
        window_set_focus_callback(self.window, callback)

    def _setup_resize(self):
        def callback(window, width, height):
            self.window.width = width
            self.window.height = height
            FC_resize_viewport(0, 0, width, height)
        window_set_resize_callback(self.window, callback)
