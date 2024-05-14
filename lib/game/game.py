class game:
    """Stores scenarios, with one being the current.

    Instance attributes:
        scenarios: dict[str:scenario] -- direct access to named scenarios
    Instance methods:
        add_scenario -- adds a scenario to the game
        set_scenario -- sets the current scenario
        get_scenario -- gets the current scenario
    """

    def __init__(self):
        self.scenarios = dict()
        self._current_scenario = None

    def set_scenario(self, name):
        if name in self.scenarios:
            self._current_scenario = name
            self.scenarios[name].load()
            return True
        return False

    def get_scenario(self):
        if self._current_scenario != None:
            return self.scenarios[self._current_scenario]

    def add_scenario(self, name, scenario):
        self.scenarios[name] = scenario
