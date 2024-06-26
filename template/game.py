import glob
from os import path

import numpy as np

from lib.game import game, scenario, object
from lib.graphics.bridge import C_TRIANGLES
from lib.graphics.bridge import FC_set_uniform_mat4, FC_clear, FC_clear_color
from lib.graphics.bridge.functions import FC_set_uniform_float, FC_set_uniform_vec3
from lib.io.user_input import empty_function
from lib.util import get_full_path
from lib.util.ncmat import model, translate, rotate, scale
from .camera import camera
from .lighting import light_source, light_source_controller

# Adds program and window information to the game
# Scenarios and objects can follow the hierarchy up to get this information
class game(game):
    def __init__(self, program, window):
        super().__init__()
        self.program = program
        self.window = window


# Overrides the draw function to follow mvp conventions
# Adds a function to add all objects from a folder,
# a function for temporarily disabling the view and projection matrices
# and a function to add a light source to all objects with a certain tag
class scenario(scenario):
    def __init__(self, game, filepath):
        super().__init__()
        self.game = game

        self.camera = camera(self.game.window)

        self.keycontrol = empty_function
        self.mousecontrol = empty_function
        self.clickcontrol = empty_function

        self.use = lambda: None
        self.filepath = filepath

        self.scene_lights = []
        self.light_source_controller = light_source_controller(self.game.program)
        self.n_scene_lights = len(self.scene_lights)

        self.ambient_source = light_source(color=[1.0,0.98,0.92], intensity=1.0)

    def draw(self):
        FC_clear()
        FC_clear_color()
        self.light_source_controller.send()
        FC_set_uniform_vec3(self.game.program, "viewer_position", self.camera.t)
        for obj in self.objects:
            obj = self.objects[obj]
            FC_set_uniform_mat4(self.game.program, "model", obj.model())
            FC_set_uniform_mat4(self.game.program, "view", self.camera.view())
            FC_set_uniform_mat4(self.game.program, "projection", self.camera.projection())

            obj.draw()
            self.light_source_controller.trunc(self.n_scene_lights)

    def add_objects_from_folder(self, folder_name, local=True):
        filepath = folder_name
        if local:
            filepath = get_full_path(__file__)(filepath) + "/"

        for file in glob.glob(filepath+"*.obj"):
            obj = object(file)
            self.add_object(path.basename(file)[:-4], obj)

    def skip_view_and_projection(self):
        FC_set_uniform_mat4(self.game.program, "view", np.identity(4))
        FC_set_uniform_mat4(self.game.program, "projection", np.identity(4))

    def add_light_to_objects(self, light, tags):
        tmp_tags = tags - set()
        if "all" in tmp_tags:
            self.scene_lights.append(light)
            self.n_scene_lights += 1
            tmp_tags.remove("all")
        affected_objects = filter(lambda obj: any([tag in obj.tags for tag in tmp_tags]), self.objects.values())
        for obj in affected_objects:
            obj.active_lights.append(light)

    def load(self):
        super().load()
        for luminous_obj in filter(lambda obj: "luminous" in obj.tags, self.objects.values()):
            self.add_light_to_objects(luminous_obj.light_source, luminous_obj.affected_tags)
        self.light_source_controller.add(self.scene_lights)
        self.light_source_controller.ambient_source = self.ambient_source



# Adds a function to return the model matrix
# Overrides _on_change_material in order to set the lighting coefficients
class object(object):
    def __init__(self, filepath, t=(0.0,0.0,0.0), s=(1.0,1.0,1.0), a=(0.0,0.0,0.0), mode=C_TRIANGLES, skip_load=False, tags=set()):
        super().__init__(filepath, t, s, a, mode, skip_load, tags)
        self.active_lights = list()

    def model(self):
        return model([[translate,self.t],[rotate,self.a],[scale,self.s]])

    def behavior(self):
        super().behavior()
        if len(self.active_lights) > 0:
            self.scenario.light_source_controller.add(self.active_lights)
        self.scenario.light_source_controller.send()

    def _on_change_material(self, material_name):
        try:
            FC_set_uniform_vec3(self.scenario.game.program, "ka", self.wavefront.materials[material_name].ka)
            FC_set_uniform_vec3(self.scenario.game.program, "kd", self.wavefront.materials[material_name].kd)
            FC_set_uniform_vec3(self.scenario.game.program, "ks", self.wavefront.materials[material_name].ks)
            FC_set_uniform_float(self.scenario.game.program, "ns", self.wavefront.materials[material_name].ns)
        except:
            pass

# Represents an object that acts as a light source
class luminous_object(object):
    def __init__(self, filepath, color, intensity=1.0, affected_tags={"all"}, t=(0.0,0.0,0.0), s=(1.0,1.0,1.0), a=(0.0,0.0,0.0), mode=C_TRIANGLES, skip_load=False, tags=set()):
        super().__init__(filepath, t, s, a, mode, skip_load, tags)

        self.color = color
        self.intensity = intensity
        self.light_source = light_source(self.t, self.color, self.intensity)
        self.y_size = self.get_y_size()

        self.tags.add("luminous")

        self.affected_tags = affected_tags

    def get_y_size(self):
        return (self.wavefront._physical_size_pc[1][1] - self.wavefront._physical_size_pc[1][0])/2 + 1

    def behavior(self):
        super().behavior()
        self.light_source._offset[1] = np.array(self.y_size) * self.s[1]
