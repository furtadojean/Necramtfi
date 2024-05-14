"""Provides functions for dealing with a window class."""

import glfw
import time

# Keeping associated functions instead of methods for consistency
def window_create(width, height, title):
    return window(width, height, title)

def window_set_key_callback(window, func):
    glfw.set_key_callback(window.window, func)

def window_set_click_callback(window, func):
    glfw.set_mouse_button_callback(window.window, func)

def window_set_mouse_callback(window, func):
    glfw.set_cursor_pos_callback(window.window, func)

def window_set_focus_callback(window, func):
    glfw.set_window_focus_callback(window.window, func)

def window_set_resize_callback(window, func):
    glfw.set_window_size_callback(window.window, func)

def window_ready(window):
        glfw.show_window(window.window)

def window_loop(window, func, max_fps=0):
    while not glfw.window_should_close(window.window):
        expected_delay_time = 1.0/(max_fps+1)
        start_time = time.perf_counter()

        glfw.poll_events()
        func()
        glfw.swap_buffers(window.window)

        end = start_time+expected_delay_time
        if max_fps != 0:
            while(left := end-time.perf_counter()) > 0:
                    time.sleep(min(10/1000,left*0.5))
    glfw.terminate()


class window:
    """Stores information about a window.

    Instance attributes:
        width: int -- width when created
        height: int -- height when created
        title: str -- title when created
    Instance methods:
        ready -- makes window visible
    """
    
    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.title = title
        self.window = None

        self._create()

    def _create(self):
        glfw.init()
        glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
        glfw.window_hint(glfw.SAMPLES, 4)
        self.window = glfw.create_window(self.width, self.height, self.title, None, None)
        glfw.make_context_current(self.window)
