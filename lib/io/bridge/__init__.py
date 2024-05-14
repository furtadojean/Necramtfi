"""Abstracts the window manager."""

from .window import window_create, window_set_click_callback, window_set_focus_callback, window_set_key_callback, window_set_mouse_callback, window_set_resize_callback, window_ready, window_loop

from .exceptions import LoopBreak

from .flags import F_cursor, F_full_screen

from .functions import window_close, window_get_size
