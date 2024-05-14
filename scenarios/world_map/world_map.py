from template.game import scenario, object
from template.camera import camera_3d_keycontrol, camera_3d_mousecontrol
from template.io_accumulators import keycontrol_accumulator

from lib.util import get_full_path

from .cat import cat
from .hotbar import hotbar
from .hotbar import hotbar_keycontrol

import math
import numpy as np

class world_map(scenario):
    def __init__(self, game):
        super().__init__(game, __file__)

        # Camera initial position
        self.camera.t = np.array([11.0, 4.0, 12.0])

        # Function to insert the current directory before relative paths
        self.gfp = get_full_path(__file__)

        # Key callback
        self.keycontrol = keycontrol_accumulator({camera_3d_keycontrol(self.camera)})

        # Mouse position callback
        self.mousecontrol = camera_3d_mousecontrol(self.camera)


    def behavior(self):
        # Inserts some objects in the hotbar
        self.hotbar.fill_slot(self.pistol)
        self.hotbar.fill_slot(self.cat)
        self.hotbar.fill_slot(self.mini_castle)
        self.hotbar.fill_slot(self.skybox)
        super().behavior()

        # Restricts the camera to the map boundaries
        camera_pos_copy = np.copy(self.camera.t)
        self.keycontrol.call_on_draw()
        cp = self.camera.t
        if cp[0] < -10.8 or cp[0] > 64.5 \
                or cp[1] < 4.0 or cp[1] > 12.0 \
                or cp[2] < -16.7 or cp[2] > 72.8:
                    self.camera.t = camera_pos_copy

        # Day/Night cycle
        self.skybox.a[0] += math.radians(0.05)

        # Ender dragon flying
        self.enderdragon.a[0] += math.radians(0.5)
        self.enderdragon.a[2] += math.radians(0.1)

    def load(self):
        gfp = self.gfp

        # Map
        self.map = object(gfp("objects/gravity_falls.obj"),
                          t=(-21.0,-21.0,-21.0),
                          s=(0.4,0.4,0.4))
        self.add_object("map", self.map)

        # Cat
        self.cat = cat(gfp, self.camera)
        self.add_object("cat", self.cat)

        # Hotbar
        self.hotbar = hotbar(gfp)
        self.add_object("hotbar", self.hotbar)
        self.hotbar_keycontrol = hotbar_keycontrol(self.hotbar, self.camera)
        self.keycontrol.add_keycontrol(self.hotbar_keycontrol)
        self.add_object("selected_object", self.hotbar.selected_object)

        # Pistol
        self.pistol = object(gfp("objects/pistol.obj"),
                             s=(0.1,0.1,0.1))
        self.pistol.skip_draw = True
        self.add_object("pistol", self.pistol)

        # Skybox
        self.skybox = object(gfp("objects/skybox.obj"),
                             s=(4.0,4.0,4.0))
        self.camera.far = 1000
        self.skybox.t = -self.map.t
        self.skybox.t[1] *= 0
        self.add_object("skybox", self.skybox)

        # Ender Dragon
        self.enderdragon = object(gfp("objects/enderdragon.obj"))
        self.enderdragon.t -= self.map.t
        self.enderdragon.t[1] *= 0.2
        self.enderdragon.t[2] += 10
        self.add_object("enderdragon", self.enderdragon)

        # Book
        self.book = object(gfp("objects/book.obj"),
                           t=(2.0,-0.35,1.3),
                           s=(0.5,0.5,0.5),
                           a=(0.0,math.radians(90),0.0))
        self.book.t += self.camera.t
        self.add_object("book", self.book)

        # Miniature Castle
        self.mini_castle = object(gfp("objects/mine_castle.obj"),
                                  t=(3.6,-0.4,0.0),
                                  a=(0.0,math.radians(180),0.0),
                                  s=(0.1,0.1,0.1))
        self.mini_castle.t += self.camera.t
        self.add_object("mini_castle", self.mini_castle)

        # Tv
        self.tv = object(gfp("objects/tv_icmc.obj"),
                         t=(1.0,-0.4,-1.7),
                         a=(0.0,math.radians(270),0.0),
                         s=(0.5,0.5,0.5))
        self.tv.t += self.camera.t
        self.add_object("tv_icmc", self.tv)

        # Creeper
        self.creeper = object(gfp("objects/creeper.obj"),
                              t=(-4.0,-0.15,-1.5),
                              a=(0.0,0.0,0.0),
                              s=(2.0,2.0,2.0))
        self.creeper.t += self.camera.t
        self.add_object("creeper", self.creeper)



        super().load()
