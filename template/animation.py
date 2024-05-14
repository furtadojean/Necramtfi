class animation():
    """Supports animations through a finite-state machine.

    Instance methods:
        start: starts the animation
        end: ends the animation ahead of time

    Subclassing interface:
        lock: bool -- True if it has started and not ended
        state: int -- current state
        ---
        update_states -- algorithm for state changes
        Note: it needs to be wrapped with animation.on_lock
              and return a list
    """

    def __init__(self):
        self.lock = False
        self.state = 0

    def start(self):
        self.lock = True

    def end(self):
        self.lock = False
        self.state = 0

    def update_states(self, *args):
        pass

    @staticmethod
    def on_lock(func):
        def wrapper(self, *args):
            if self.lock == True:
                return func(self, *args)
            return [*args]
        return wrapper


# Jump animation to be used with the y coordinate
class jump_animation(animation):
    def __init__(self, initial_speed, gravity, height):
        super().__init__()
        self.speed = initial_speed
        self.gravity = gravity
        self.height = height

    @animation.on_lock
    def update_states(self, y):
        if self.state == 0:
            self.speed = 0.3
            self.gravity = -0.02
            self.state = 1
        elif self.state == 1:
            self.speed += self.gravity
            y += self.speed
            if y <= self.height:
                y = self.height
                self.state = 0
                self.end()
        return [y]

