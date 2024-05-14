# Jean Michel Furtado M'Peko - 5271916

from template import template as tpl
from template import game as gm
from lib.io.bridge import window_loop, window_ready, LoopBreak


# 1. Setup
from scenarios.world_map import world_map

template = tpl("Necramtfi")
game = gm(template.pipeline.program, template.window)
game.add_scenario("world_map",
    # Some objects may take some time to load
    world_map(game)
)

def change_scenario(scenario_name):
    if game.set_scenario(scenario_name):
        sc = game.get_scenario()
        # Updates the io_controller to reflect the callbacks
        # defined in the scenario
        template.io_controller.keycontrol = sc.keycontrol
        template.io_controller.mousecontrol = sc.mousecontrol
        template.io_controller.clickcontrol = sc.clickcontrol
        # Also updates the vertex and fragment/texture coordinate buffers
        template.vcoordinates = sc.vcoordinates
        template.fcoordinates = sc.fcoordinates

        template.ready()


# 2. Initial scenario
change_scenario("world_map")


# 3. Loop
def loop():
    try:
        game.get_scenario().loop()
    except LoopBreak as new_scenario_name:
        if new_scenario_name != "":
            print(new_scenario_name)
            change_scenario(str(new_scenario_name))
window_ready(template.window)
# Sets the window to use the above loop at a maximum of 60 fps
window_loop(template.window, loop, 60)
