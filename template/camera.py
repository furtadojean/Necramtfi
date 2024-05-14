from lib.io.bridge.flags import F_full_screen
from lib.util import ncmat
from lib.util.ncmat import rotate
from lib.io.user_input import *
from lib.io.bridge import window_get_size, window_close
from lib.graphics.bridge import F_polygonal_mode
from template.animation import jump_animation

import numpy as np
import math

class camera:
    """A 3D camera.

    Instance attributes:
        t: array[float] -- position
        front: array[float] -- direction relative to t
        up: array[float] -- view-up
        fovy: float -- field-of-vision angle in degrees
        near: float -- cut-off point (near camera)
        far: float -- cut-off point (far from camera)
    Instance methods:
        view -- returns view matrix
        projection -- returns projection matrix
    """

    def __init__(self, window):
        self.t = np.array([0.0, 4.0, 0.0])
        self.front = np.array([1.0, 1.0, 1.0])
        self.up = np.array([0.0, 1.0, 0.0])

        self.window = window
        self.fovy = 45.0
        self.near = 0.1
        self.far = 100.0

    def view(self):
        return ncmat.view(self.t, self.front+self.t, self.up)

    def projection(self):
        return ncmat.projection(self.fovy,
                                self.window.width/self.window.height,
                                self.near, self.far)


# Controls the camera's key callback
class camera_3d_keycontrol(keycontrol):
    def __init__(self, camera):
        super().__init__()
        self.camera = camera
        self.add_keys([
            K_P,
            K_W,
            K_A,
            K_S,
            K_D,
            K_SPACE,
            K_LEFT_SHIFT,
            K_F,
            K_Q,
        ])
        self.movement_vector = np.array([0.0,0.0,0.0])
        self.basespeed = 1.0
        self.speed = 1.0

        self.jump_animation = jump_animation(0.3, -0.02, 4)

        self.polygonal = F_polygonal_mode
        self.polygonal.off()

        self.full_screen = F_full_screen(self.camera.window)
        self.full_screen.off()

    def on_press_function(self, window, key, scancode, action, mods):
        # Polygonal mode
        if key == K_P:
            F_polygonal_mode.toggle()

        # Close window
        elif key == K_Q:
            window_close(self.camera.window)

        # Jump
        elif key == K_SPACE:
            self.jump_animation.start()

        # Full screen
        elif key == K_F:
            self.full_screen.toggle()


    def call_on_draw(self):
        cameraFront_locked = np.copy(self.camera.front)
        cameraFront_locked[1] = 0

        front_vector = cameraFront_locked

        movement_vector = np.array([0.0,0.0,0.0])
        speed = self.speed

        # Sprint
        if self.on_hold[K_LEFT_SHIFT]:
            speed = speed*3

        # Forward
        if self.on_hold[K_W]:
            movement_vector += front_vector

        # Back
        if self.on_hold[K_S]:
            movement_vector -= front_vector

        # Left
        if self.on_hold[K_A]:
            movement_vector += np.resize(
                    np.matmul(
                        np.resize(rotate(0,math.radians(90),0),(4,4)),
                        np.resize(front_vector, 4)
                    ),
            3)

        # Right
        if self.on_hold[K_D]:
            movement_vector += np.resize(
                    np.matmul(
                        np.resize(rotate(0,math.radians(-90),0),(4,4)),
                        np.resize(front_vector, 4)
                    ),
            3)

        self.movement_vector = movement_vector
        self._tmp_speed = speed

        self._update_camera()

    def _update_camera(self):
        norm = np.linalg.norm(self.movement_vector)
        if norm == 0: norm = 1
        self.camera.t += self._tmp_speed*(self.movement_vector*(self.basespeed/10) / norm)

        self.camera.t[1] = self.jump_animation.update_states(self.camera.t[1])[0]



# Controls the camera's mouse callback
class camera_3d_mousecontrol(mousecontrol):
        def __init__(self, camera):
            super().__init__()
            self.camera = camera
            self.angle = 0
            self.speed_x = 1
            self.speed_y = 1

        def __call__(self, window, xpos, ypos):
            super().__call__(window, xpos, ypos)
            (width, height) = window_get_size(self.camera.window)
            width = self.camera.window.width
            height = self.camera.window.height
            self.speed_x = width / 1500.0
            self.speed_y = height / 1500.0

            self.x = (xpos-width/2)/(width/2)
            self.y = -(ypos-height/2)/(height/2)

            self.angle = self.x * math.pi * self.speed_x
            self._update_camera()

        def _update_camera(self):
            self.camera.front[0] = math.cos(self.angle)
            self.camera.front[2] = math.sin(self.angle)
            self.camera.front[1] = self.y * self.speed_y
