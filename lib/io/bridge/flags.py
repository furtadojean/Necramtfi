from ...util import flag_one_function
import glfw

F_cursor = lambda window: flag_one_function(
        glfw.set_input_mode,
        [window.window, glfw.CURSOR, glfw.CURSOR_DISABLED],
        [window.window, glfw.CURSOR, glfw.CURSOR_NORMAL]
)

F_full_screen = lambda window: (lambda pm: flag_one_function(
        glfw.set_window_monitor,
        [window.window, None, *glfw.get_monitor_workarea(pm), glfw.get_video_mode(pm).refresh_rate],
        [window.window, pm, *glfw.get_monitor_workarea(pm), glfw.get_video_mode(pm).refresh_rate],
        ))(glfw.get_primary_monitor())
