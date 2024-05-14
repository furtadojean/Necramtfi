from lib.io.user_input import keycontrol
from lib.io.user_input import A_PRESS, A_RELEASE, A_REPEAT

class keycontrol_accumulator(keycontrol):
    """Composite keycontrol.

    Instance methods:
        add_keycontrol -- adds a keycontrol to the accumulator
        call_on_draw -- function that acts on on_hold keys and other behaviors
        __call__ -- key callback

    Subclassing interface:
        keycontrols: set[keycontrol] -- all keycontrols added
    """

    def __init__(self, keycontrols=None):
        super().__init__()
        if keycontrols != None:
            self.keycontrols = keycontrols
            self.keys_being_used = {i for k in keycontrols for i in k.keys_being_used }
        else:
            self.keycontrols = set()

    def __call__(self, window, key, scancode, action, mods):
        for k in self.keycontrols:
            k(window, key, scancode, action, mods)

    def add_keycontrol(self, keycontrol):
        self.add_keys(keycontrol.keys_being_used)
        self.keycontrols.add(keycontrol)

    def call_on_draw(self):
        for k in self.keycontrols:
            k.call_on_draw()
