"""Provides functions related to filepaths."""
from os import path
from pathlib import Path

get_full_path = lambda __file__: lambda relative_path: str(Path(path.abspath(__file__)).parent) + "/{}".format(relative_path)
