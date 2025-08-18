from logging import config
import os
import pathlib
import json
from config import ConfigManager

from ui import ui

CONFIG_FILE = "config.json"

class pathController:
    def __init__(self):
        self.paths = self.load_paths()

    def set_path(self, key_name):
        label = key_name.replace("_", " ").capitalize()
        new_path = input(f"Enter {label}: ").strip()

        if os.path.exists(new_path):
            self.paths[key_name] = new_path
            ConfigManager().set("path",key_name, new_path)
        else:
            print("Invalid path. Please try again.")
    
    def show_paths(self):
        if not self.paths:
            print("No path set yet")
        else:
            title = "Save paths"
            ui.Header(title)

            for key, path in self.paths.items():
                label = key.replace("_", " ").capitalize()
                print(f"{label}: {path}")

    def load_paths(self):
        paths = {}
        paths['input_path'] = ConfigManager().get("path", "input_path")
        paths['output_path'] = ConfigManager().get("path", "output_path")
        return paths


