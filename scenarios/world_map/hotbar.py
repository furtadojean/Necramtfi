from template.game import object
from lib.util.ncmat import model, translate, rotate, scale
from lib.io.user_input import keycontrol
from lib.io.user_input import K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_PERIOD, K_COMMA, K_X, K_Y, K_Z
from template.io_accumulators import keycontrol_accumulator

import numpy as np
import math

# User should add both the hotbar and its selected_object to the scenario
class hotbar(object):
    """A one-line summary.

    Instance attributes:
        selected_object: object
        scenario: scenario -- scenario to add hotbar
    Instance methods:
        fill_shot -- adds an object to a free slot
        empty_slot -- removes an object from a slot

    Protected interface:
        slots: list -- all the slots
        fill_objs: list -- objects filling the slots
        free_huds: dict[int:bool] -- slot availability
    """

    def __init__(self, gfp):
        self.gfp = gfp
        self.slots = [slot(gfp("objects/hotbar.obj"), t=(x/4.0, -0.8, 0.0)) for x in range(-3,3)]
        self.fill_objs = [obj_on_slot(after_t=self.slots[_].t) for _ in range(len(self.slots))]
        for obj in self.fill_objs:
            obj.skip_draw = True
        self.free_huds = {i:True for i in range(len(self.slots))}
        super().__init__("", skip_load=True)
        self.skip_draw = True
        self._scenario = None
        self.selected_object = None

    @property
    def scenario(self):
        return self._scenario

    @scenario.setter
    def scenario(self, scenario):
        if scenario != None:
            self._scenario = scenario
            i = 0
            for hud in self.slots:
                scenario.add_object("hud"+str(i), hud)
                i += 1

    def fill_slot(self, object):
        self.free_huds_list = sorted(list(filter(lambda fh: self.free_huds[fh] == True, self.free_huds)))
        if len(self.free_huds_list) < 1:
            return False
        index = self.free_huds_list[0]
        self.free_huds[index] = False
        self.fill_objs[index].skip_draw = False
        self.fill_objs[index].wavefront = object.wavefront
        self.fill_objs[index].correct_for_misaligned_center()
        self.scenario.add_object("obj_on_slot"+str(index), self.fill_objs[index])
        return True

    def empty_slot(self, index):
        if index >= len(self.free_huds) or self.free_huds[index] == True:
            return
        self.scenario.objects.pop("obj_on_slot"+str(index))


# User should also add this keycontrol accumulator
class hotbar_keycontrol(keycontrol_accumulator):
    def __init__(self, hotbar, camera):
        self.selection_keycontrol = selection_keycontrol(hotbar)
        self.selected_keycontrol = selected_keycontrol(camera)
        hotbar.selected_object = self.selected_keycontrol.selected_object
        super().__init__({self.selection_keycontrol, self.selected_keycontrol})

    def call_on_draw(self):
        try:
            self.selected_keycontrol.currently_selected = self.selection_keycontrol.current_objs[1]
        except:
            pass
        super().call_on_draw()




# Class for the slots that appear on the bottom of the screen
class slot(object):
    def __init__(self, filepath, t=(0.0,0.0,0.0), s=(0.10,0.10,0.10), a=(0.0,0.0,0.0), aspect_dim=0, skip_load=False):
        super().__init__(filepath, t, s, a, skip_load=skip_load)
        self.aspect_dim = aspect_dim

    def draw(self):
        self.scenario.skip_view_and_projection()
        super().draw()

    def model_behavior(self):
        self.aspect = self.scenario.game.window.width / self.scenario.game.window.height
        self.width = self.scenario.game.window.width/800
        self.height = self.scenario.game.window.height/800

    def return_coordinate_scale(self, en):
        dim, value = en
        if dim == self.aspect_dim:
            return value/self.aspect*self.width
        return value*self.width

    def model(self):
        self.model_behavior()
        return model([[translate, [self.t[0], self.t[1]/self.height, self.t[2]]],
                      [rotate, self.a],
                      [scale, list(map(self.return_coordinate_scale, enumerate(self.s)))]])


# Class for the objects that appear on top of a filled slot
class obj_on_slot(slot):
    def __init__(self, after_t=(0, 0, 0), aspect_dim=0):
        super().__init__("", t=(0.0,0.0,0.0), a=(0.0, math.radians(90), 0.0), aspect_dim=aspect_dim, skip_load=True)
        self.after_t = after_t

    def correct_for_misaligned_center(self):
        self.t = -self.wavefront.diff_from_center
        self.s = np.array([0.15,0.15,1.0])/self.wavefront.physical_size

    def model(self):
        self.model_behavior()
        return model([[translate, [self.after_t[0], self.after_t[1]/self.height, self.after_t[2]]],
                      [scale, list(map(self.return_coordinate_scale, enumerate(self.s)))],
                      [rotate, self.a],
                      [translate, [1.0, self.t[1]/self.height, self.t[2]]]])


# Controls the selection of a slot
class selection_keycontrol(keycontrol):
    keys = [K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_0]
    def __init__(self, hotbar):
        super().__init__()
        self.hotbar = hotbar
        self.size = min(10, len(hotbar.slots))
        self.valid_keys = [selection_keycontrol.keys[i] for i in range(self.size)]
        self.add_keys(self.valid_keys)
        self.key_to_objs = {self.valid_keys[i]:[hotbar.slots[i], hotbar.fill_objs[i]] for i in range(self.size)}
        self.current_objs = None


    def on_press_function(self, window, key, scancode, action, mods):
        if self.current_objs != None:
            self._revert_current_objs()
        if key in self.valid_keys:
            objs = self.key_to_objs[key]
            self.current_objs = objs
            objs[0].wavefront.change_material[0] = (0, "hotbar_selected")

    def _revert_current_objs(self):
        self.current_objs[0].wavefront.change_material[0] = (0, "hotbar_unselected")

# Controls the rotation and scaling of the selected object
class selected_keycontrol(keycontrol):
    def __init__(self, camera):
        super().__init__()
        self.currently_selected = None
        self.previously_selected = None
        self.selected_object = selected_object()
        self.camera = camera
        self.add_keys([
            K_X,
            K_Y,
            K_Z,
            K_COMMA,
            K_PERIOD,
        ])

    def on_press_function(self, window, key, scancode, action, mods):
        if key == K_X:
            self.selected_object.a[0] += 0.2
        elif key == K_Y:
            self.selected_object.a[1] += 0.2
        elif key == K_Z:
            self.selected_object.a[2] += 0.2
        elif key == K_COMMA:
            self.selected_object.s -= np.array([0.05, 0.05, 0.05])
        elif key == K_PERIOD:
            self.selected_object.s += np.array([0.05, 0.05, 0.05])

    def call_on_draw(self):
        self.selected_object.update_target_n_offset(self.camera.t, self.camera.front)
        if self.currently_selected != self.previously_selected:
            self.previously_selected = self.currently_selected
            self._setup()

    def _setup(self):
        self.selected_object.update_object(self.currently_selected)

# Class for the shared object that represents the currently selected one
class selected_object(object):
    def __init__(self, target=(0.0,0.0,0.0), offset=(0.0,0.0,0.0)):
        super().__init__("", skip_load=True)
        self.target = np.array(target)
        self.offset = np.array(offset)
        self.skip_draw = True
        self.after_t = self.t

    def update_target_n_offset(self, target, offset):
        self.target = np.array(target)
        self.offset = np.array(offset)

    def update_object(self, object):
        if not hasattr(object, "wavefront"):
            return
        self.object = object
        self.wavefront = object.wavefront
        self._setup()
        self.skip_draw = False

    def _setup(self):
        self.t = -self.wavefront.diff_from_center
        self.s = np.array([1.0,1.0,1.0])/self.wavefront.physical_size
        self.a = np.array([0.0,0.0,0.0])
        self.after_t = self.target + self.offset

    def model(self):
        return model([[translate, self.after_t],
                      [scale, self.s],
                      [rotate, self.a],
                      [translate, self.t]])
