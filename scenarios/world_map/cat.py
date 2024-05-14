from template.game import object
from template.animation import animation
import math
from random import random

# A cat that walks around while keeping itself close to a target
class cat(object):
    def __init__(self, gfp, target):
        super().__init__(gfp("objects/cat.obj"),
                         t=(0.0,3.2,0.0),
                         s=(0.15,0.15,0.15))

        self.target = target
        self.animation = walk_around_animation(self.t, 10)
        self.animation.start()

    def behavior(self):
        super().behavior()
        (new_x, new_z, y_angle) = self.animation.update_states(self.target.t)
        self.t[0] = new_x
        self.t[2] = new_z
        self.a[1] = y_angle

class walk_around_animation(animation):
    def __init__(self, initial_pos, radius=3):
        super().__init__()
        self.max = math.sqrt(math.pow(radius,2)/2)

        self.goal_x = 0
        self.goal_z = 0

        self.x = initial_pos[0]
        self.y = initial_pos[1]
        self.z = initial_pos[2]

        self.y_angle = 0

    def _get_random_pos(self, target_pos):
            neg_x = -1 if random() < 0.5 -1 else 1
            neg_y = -1 if random() < 0.5 -1 else 1
            return (target_pos[0] + random()*self.max * neg_x,
                    target_pos[2] + random()*self.max * neg_y)

    def _update_info(self):
            sign_x = -1 if self.goal_x < self.x else 1
            sign_z = -1 if self.goal_z < self.z else 1
            self.x += min(0.1, math.fabs(self.goal_x-self.x)/30) * sign_x
            self.z += min(0.1, math.fabs(self.goal_z-self.z)/30) * sign_z

            self.y_angle = math.atan2(self.x-self.goal_x, self.z-self.goal_z)


    @animation.on_lock
    def update_states(self, target_pos):
        # Chooses a new target_position
        if self.state == 0:
            self.goal_x, self.goal_z = self._get_random_pos(target_pos)
            self.state = 1

            return [self.x, self.z, self.y_angle]

        # Walks up to that target_position
        elif self.state == 1:
            # If distance is too large -> 3
            if math.fabs(target_pos[0]-self.x) > self.max:
                self.state = 3

            self._update_info()

            # When target is reached -> 0
            if math.fabs(self.x-self.goal_x) <= 0.01:
                self.state = 0

            return [self.x, self.z, self.y_angle]

        # Walks in the direction of the target until close enough
        elif self.state == 3:
            # When close enough -> 0
            if math.fabs(target_pos[0]-self.x) < self.max:
                self.state = 0

            self.goal_x = target_pos[0]
            self.goal_z = target_pos[2]
            self._update_info()

            return [self.x, self.z, self.y_angle]


