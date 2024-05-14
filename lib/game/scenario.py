from ..io.bridge import LoopBreak
from ..graphics.bridge import textures_create, textures_load
from ..graphics.bridge import coordinates_create

class scenario:
    """Defines a world filled with objects.

    Instance attributes:
        objects: dict[str:object] -- direct access to named objects
        loop_break: str -- the name of the next scenario to switch to
    Instance methods:
        add_object -- adds an object to the scenario
        load -- loads coordinates and textures
        loop -- draws objects

    Subclassing interface:
        texture_bank: textures -- stores textures
        vcoordinates: buffer -- stores the vertex coordinates
        fcoordinates: buffer -- stores the fragment/texture coordinates
        ---
        draw -- draws the objects
        behavior -- executed before draw on every loop
    """

    def __init__(self):
        self.game = None
        self.objects = dict()

        self.texture_bank = textures_create(500)
        self.vcoordinates = coordinates_create(3)
        self.fcoordinates = coordinates_create(2)

        self.loop_break = ""

    def draw(self):
        for objects in self.objects:
            objects.draw()

    def behavior(self):
        pass

    def loop(self):
        if self.loop_break != "":
            text = self.loop_break
            self.loop_break = ""
            raise LoopBreak(text)
        self.behavior()
        self.draw()

    def add_object(self, name, object):
        self.objects[name] = object
        object.scenario = self

    def load(self):
        for object in self.objects:
            object = self.objects[object]
            if not object.skip_load:
                object.wavefront.offload(self.vcoordinates, self.fcoordinates)
                for material in object.wavefront.material_texture:
                    textures_load(self.texture_bank, material, object.wavefront.material_texture[material])
