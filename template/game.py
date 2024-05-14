import glob
from os import path

import numpy as np

from lib.game import game, scenario, object
from lib.graphics.bridge import C_TRIANGLES
from lib.graphics.bridge import FC_set_uniform_mat4, FC_clear, FC_clear_color
from lib.io.user_input import empty_function
from lib.util import get_full_path
from lib.util.ncmat import model, translate, rotate, scale
from .camera import camera

# Adds program and window information to the game
# Scenarios and objects can follow the hierarchy up to get this information
class game(game):
    def __init__(self, program, window):
        super().__init__()
        self.program = program
        self.window = window


# Overrides the draw function to follow mvp conventions
# Adds a function to add all objects from a folder and
# a function for temporarily disabling the view and projection matrices
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

    def draw(self):
        FC_clear()
        FC_clear_color()
        for obj in self.objects:
            obj = self.objects[obj]
            FC_set_uniform_mat4(self.game.program, "model", obj.model())
            FC_set_uniform_mat4(self.game.program, "view", self.camera.view())
            FC_set_uniform_mat4(self.game.program, "projection", self.camera.projection())

            obj.draw()

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



# Adds a function to return the model matrix
class object(object):
    def __init__(self, filepath, t=(0.0,0.0,0.0), s=(1.0,1.0,1.0), a=(0.0,0.0,0.0), mode=C_TRIANGLES, skip_load=False):
        super().__init__(filepath, t, s, a, mode, skip_load)
    def model(self):
        return model([[translate,self.t],[rotate,self.a],[scale,self.s]])
