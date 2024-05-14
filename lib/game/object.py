import numpy as np
from ..graphics.bridge import FC_draw_arrays, C_TRIANGLES
from .wavefront import wavefront
from ..graphics.bridge import textures_use

class object:
    """Represents an object in the scenario.

    Instance attributes:
        scenario: scenario -- the scenario the object is in
        skip_draw -- if True, object is not drawn on screen, but behavior is executed
        skip_load -- if True, wavefront is not created
        skip_behavior -- if True, behavior is not executed
    Instance methods:
        draw -- draws object after executing behavior

    Subclassing interface:
        behavior -- executes every time the object is drawn
    """

    def __init__(self, filepath, t=(0,0,0), s=(1,1,1), a=(0,0,0), mode=C_TRIANGLES, skip_load=False):
        if not skip_load:
            self.wavefront = wavefront(filepath)
        self._mode = mode

        self._assign_model_info(t, s, a)

        self.scenario = None

        self.skip_draw = False
        self.skip_load = skip_load
        self.skip_behavior = False


    def behavior(self):
        pass

    def _assign_model_info(self, t, s, a):
        self.t = np.array(t)
        self.s = np.array(s)
        self.a = np.array(a)

    def draw(self):
        if not self.skip_behavior:
            self.behavior()
        if not self.skip_draw:
            drawn_vertices = 0
            textures_use(self.scenario.texture_bank, self.wavefront.change_material[0][1])
            for (vertice, material) in self.wavefront.change_material[1:]:
                FC_draw_arrays(self._mode, self.wavefront.first+drawn_vertices, vertice-drawn_vertices)
                textures_use(self.scenario.texture_bank, material)
                drawn_vertices = vertice
            FC_draw_arrays(self._mode, self.wavefront.first+drawn_vertices, self.wavefront.count-drawn_vertices)
