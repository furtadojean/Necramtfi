from glfw import set_window_should_close, get_window_size

def window_close(window):
    set_window_should_close(window.window, True)

def window_get_size(window):
    return get_window_size(window.window)
