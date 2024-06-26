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
        ncoordinates: coordinates -- normal coordinates
        attribute_name: type -- description
    Instance methods:
        ready -- must be called once coordinates are ready
    """

    def __init__(self, title):
        self.window = window_create(800, 800, title)
        self.max_light_sources = 10;
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
        self._setup_lighting()

        self.pipeline.vertex_shader(self.vertex_glsl)
        self.pipeline.fragment_shader(self.fragment_glsl)
        self.pipeline.ready()


        self.vcoordinates = None
        self.fcoordinates = None
        self.ncoordinates = None

        F_depth_test.on()

    def ready(self):
        if self.vcoordinates == None or self.fcoordinates == None:
            return
        coordinates_link(self.pipeline.program, "position", self.vcoordinates)
        coordinates_link(self.pipeline.program, "texture_position", self.fcoordinates)
        coordinates_link(self.pipeline.program, "normal_vector", self.ncoordinates)



    def _setup_vertices(self):
        self.vertex_glsl.add_to_global(
            """
            attribute vec3 position;
            varying vec3 out_position;
            """
        )
        self.vertex_glsl.add_to_function("void main()",
            """
            gl_Position = projection * view * model * vec4(position, 1.0);
            out_position = vec3(model * vec4(position, 1.0));
            """
        )

        self.fragment_glsl.add_to_global(
            """
            varying vec3 out_position;
            """
        )

    def _setup_lighting(self):
        self.vertex_glsl.add_to_global(
            """
            attribute vec3 normal_vector;
            attribute vec3 viewer_position;
            varying vec3 out_normal;
            varying vec3 out_viewer_position;
            """
        )
        self.vertex_glsl.add_to_function("void main()",
            """
            mat4 model_rot = model;
            model_rot[3] = vec4(0.0, 0.0, 0.0, 1.0);

            out_normal = vec3(model_rot * vec4(normal_vector, 1.0));
            out_viewer_position = vec3(viewer_position);
            """
        )

        self.fragment_glsl.add_to_global(
            """
            varying vec3 out_normal;
            varying vec3 out_viewer_position;

            uniform vec3 ka;
            uniform vec3 kd;
            uniform vec3 ks;
            uniform float ns;

            struct LightSource {{
                vec3 position;
                vec3 color;
                float intensity;
            }};

            uniform LightSource light_sources[{0}];
            uniform int n_light_sources;
            uniform vec3 ambient_color;
            //vec3 ambient_color = vec3(1.0, 1.0, 1.0);
            """.format(self.max_light_sources)
        )

        self.fragment_glsl.add_to_function("void main()",
            """
            vec3 ambient = ka * ambient_color * 2.0;
            vec3 normal = normalize(out_normal);
            gl_FragColor *= vec4(ambient, 1.0);

            vec3 result = vec3(1.0,1.0,1.0);
            for(int i = 0; i < min(n_light_sources, {0}); ++i) {{
                vec3 light_vector = (light_sources[i].position - out_position);
                light_vector = normalize(light_vector) / length(light_vector);

                float cos_L_N = max(dot(normal, light_vector), 0.0);

                vec3 normalized_color = normalize(light_sources[i].color) * light_sources[i].intensity;

                vec3 diffuse = kd * cos_L_N * normalized_color;

                if(ns != 0.0) {{
                    vec3 viewer_vector = (out_viewer_position - out_position);
                    viewer_vector = normalize(viewer_vector) / length(viewer_vector);
                    vec3 H = normalize(light_vector + viewer_vector);

                    float cos_N_H = pow(max(dot(normal, viewer_vector), 0.0), ns);

                    vec3 specular = ks * cos_N_H * normalized_color;
                    result += vec3(specular);
                }}

                result += vec3(diffuse);
            }}

            gl_FragColor = (gl_FragColor*((vec4(1.0, 1.0, 1.0, 1.0) * vec4(result, 1.0)) - vec4(1.0, 1.0, 1.0, 1.0)) + gl_FragColor*vec4(result, 1.0))/2.0;
            """.format(self.max_light_sources)
        )

    def _setup_textures(self):
        self.vertex_glsl.add_to_global(
            """
            attribute vec2 texture_position;
            varying vec2 out_texture;
            """
        )
        self.vertex_glsl.add_to_function("void main()",
            """
            out_texture = vec2(texture_position);
            """
        )

        self.fragment_glsl.add_to_global(
            """
            varying vec2 out_texture;
            uniform sampler2D samplerTexture;
            """
        )
        self.fragment_glsl.add_to_function("void main()",
            """
            vec4 my_tex = texture2D(samplerTexture, out_texture);
            if(my_tex.a < 0.1)
                discard;
            gl_FragColor = my_tex;
            """
        )

    def _setup_mvp(self):
        self.vertex_glsl.add_to_global(
            """
            uniform mat4 model;
            uniform mat4 view;
            uniform mat4 projection;
            """
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
