from ..bridge import window_set_key_callback, window_set_mouse_callback, window_set_click_callback
from .actions import A_PRESS, A_RELEASE, A_REPEAT

empty_function = lambda *args, **kwargs: None

class io_controller:
    """Controls all user input and output.

    Instance attributes:
        keycontrol: function -- a key callback
        mousecontrol: function -- a mouse callback
        clickcontrol: function -- a click callback
    """

    def __init__(self, window):
        self.window = window

        self.keycontrol = empty_function
        self.mousecontrol = empty_function
        self.clickcontrol = empty_function

        window_set_key_callback(window, self._on_key)
        window_set_click_callback(window, self._on_click)
        window_set_mouse_callback(window, self._on_mouse)

    def _on_key(self, *args, **kwargs):
        self.keycontrol(*args, **kwargs)

    def _on_click(self, *args, **kwargs):
        self.clickcontrol(*args, **kwargs)

    def _on_mouse(self, *args, **kwargs):
        self.mousecontrol(*args, **kwargs)

class keycontrol:
    """Acts as a key callback function.

    Instance attributes:
        self.keys_being_used: set[const] -- keys being tracked
        self.on_hold: dict[const:bool] -- if key has not yet been released
    Instance methods:
        add_keys -- adds keys to be tracked
        __call__ -- key callback

    Subclassing interface:
        on_press_function -- key callback for press action
        on_release_function -- key callback for release function
        on_repeat_function -- key callback for repeat function
        call_on_draw -- function that acts on on_hold keys and other behaviors
    """

    def __init__(self):
        self.keys_being_used = set()

        self.on_hold = dict()

    def on_press_function(*args, **kwargs):
        pass

    def on_release_function(*args, **kwargs):
        pass

    def on_repeat_function(*args, **kwargs):
        pass

    def call_on_draw(self):
        pass

    def add_keys(self, keys):
        for key in keys:
            self.keys_being_used.add(key)
            self.on_hold[key] = False

    def __call__(self, window, key, scancode, action, mods):
        if key in self.keys_being_used:
            if action==A_PRESS:
                self.on_hold[key] = True
                self.on_press_function(window, key, scancode, action, mods)
            elif action==A_RELEASE:
                self.on_hold[key] = False
                self.on_release_function(window, key, scancode, action, mods)
            elif action==A_REPEAT:
                self.on_repeat_function(window, key, scancode, action, mods)



class mousecontrol:
    """Acts as a mouse callback function.

    Instance attributes:
        self.x: int -- x coordinate of mouse
        self.y: int -- y coordinate of mouse
    Instance methods:
        __call__ -- mouse callback
    """

    def __init__(self):
        self.x = 0
        self.y = 0

    def __call__(self, window, xpos, ypos):
        self.x = xpos
        self.y = ypos
