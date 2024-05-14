class flag_one_function:
    """Creates a on/off flag that executes a function.

    Instance attributes:
        off_values: list -- values passed when switching off
        on_values: list -- values passed when switching on
        function: function -- function executed on state change
        state: bool|None -- current state
    Instance methods:
        on -- switch on
        off -- switch off
        toggle -- toggle state (off if no current state)
    """

    def __init__(self, function, off_values, on_values):
        self.function = function
        self.off_values = off_values
        self.on_values = on_values
        self._state = None

    @property
    def state(self):
        return self._state

    def on(self):
        if self._state != True:
            self.function(*self.on_values)
            self._state = True

    def off(self):
        if self._state != False:
            self.function(*self.off_values)
            self._state = False

    def toggle(self):
        if self._state == False:
            self.on()
        else:
            self.off()

class flag_two_functions:
    """Creates a on/off flag that executes their respective functions.

    Instance attributes:
        values: list -- values passed to all functions
        function_off: function -- function executed when switching off
        function_on: function -- function executed when switching on
        state: bool|None -- current state
    Instance methods:
        on -- switch on
        off -- switch off
        toggle -- toggle state (off if no current state)
    """
    def __init__(self, function_off, function_on, values):
        self.function_off = function_off
        self.function_on = function_on
        self.values = values
        self._state = None

    @property
    def state(self):
        return self._state

    def on(self):
        if self._state != True:
            self.function_on(*self.values)
            self._state = True

    def off(self):
        if self._state != False:
            self.function_off(*self.values)
            self._state = False

    def toggle(self):
        if self._state == False:
            self.on()
        else:
            self.off()
