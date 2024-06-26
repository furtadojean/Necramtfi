import numpy as np
from lib.graphics.bridge import FC_set_uniform_vec3, FC_set_uniform_float, FC_set_uniform_int

class light_source:
    """Represents a light source.

    Instance attributes:
        position: array[float] -- position
        color: array[float] -- RGB color
        intensity: float -- intensity

    Subclassing interface:
        _offset: array[float] -- position offset
    """

    def __init__(self, position=[0.0,0.0,0.0], color=[1.0,1.0,1.0], intensity=1.0):
        self.position = position
        self._offset = [0.0,0.0,0.0]
        self.color = color
        self.intensity = intensity

class light_source_controller:
    """Controls the active light sources when drawing an object.

    Instance attributes:
        program: program -- program created
        ambient_source: light_source -- ambient light source to be used
    Instance methods:
        add - adds a light_source to the list
        trunc - truncates the list to the first n sources
        send - sends the list to the shaders
    """
    
    def __init__(self, program):
        self.ambient_source = None
        self.program = program
        self._light_sources = list()
        self._n = 0

    def add(self, light_source):
        if type(light_source) != list:
            light_source = [light_source]
        self._light_sources[self._n:] = light_source
        self._n = len(self._light_sources)

    def trunc(self, n):
        if n < self._n:
            self._n = n

    def send(self):
        if self.ambient_source != None:
            FC_set_uniform_vec3(self.program, "ambient_color", np.array(self.ambient_source.color)*self.ambient_source.intensity)
        FC_set_uniform_int(self.program, "n_light_sources", self._n)
        for i in range(self._n):
            base = "light_sources[{}]".format(i)
            FC_set_uniform_vec3(self.program, base+".position", np.array(self._light_sources[i].position)+self._light_sources[i]._offset)
            FC_set_uniform_vec3(self.program, base+".color", self._light_sources[i].color)
            FC_set_uniform_float(self.program, base+".intensity", self._light_sources[i].intensity)
