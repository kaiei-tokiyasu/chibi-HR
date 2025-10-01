import json
from logging import config
import os
import platform


class ConfigManager:
    def __init__(self, path="config.json"):
        self.path = path
        self.config = self.load_config()

    def get_path_type(self):
        path = os.path.normpath(os.getcwd())
        system = platform.system()
        if system == 'Windows':
            # UNC paths on Windows start with double backslashes
            if path.startswith(r'\\'):
                return "UNC"
            else:
                return "local"
        else:
            # On Unix-like systems, check common SMB mount points
            smb_mount_prefixes = ['/mnt/smb', '/Volumes', '/media', '/run/user']
            if any(path.startswith(mount) for mount in smb_mount_prefixes):
                return "UNC"
            else:
                return "local"


    def default_config(self):
        current_path = os.getcwd()

        input_path = os.path.join(current_path, "DATASET", "INPUT")
        output_path = os.path.join(current_path, "DATASET", "OUTPUT")

        cliLinkMode = self.get_path_type()
        configs = {
            "cli-link-mode": cliLinkMode,
            "skip-init-loader": False,
            "path":{
                "input_path": input_path,
                "output_path": output_path
            },
            "settings":{
                "default_page_size": 30
            },
            "data":{
                "absence-perfect-con-M": "A",
                "absence-dismiss-threshold-M": {"E": 2},
                "absence-risk-threshold-M": {"E": 1, "D": 2},
                "absence-warn-threshold-M": {"D": 1, "C": 2},
                "absence-recent-trend-M": 3,
                "absence-X-M": 4,

                "absence-perfect-con-A": "A",
                "absence-dismiss-threshold-A": {"E": 2},
                "absence-risk-threshold-A": {"E": 1, "D": 2},
                "absence-warn-threshold-A": {"D": 1, "C": 2},

                # "absence-passing-grade-M": "C",
                # "absence-passing-grade-Q": "D",
                # "absence-passing-grade-S": "D",
                # "absence-passing-grade-A": "D",

                "target-perfect-con-M": "A",
                "target-dismiss-threshold-M": {"E": 2},
                "target-risk-threshold-M": {"E": 1, "D": 2},
                "target-warn-threshold-M": {"D": 1, "C": 2},
                "target-recent-trend-M": 3,
                "target-X-M": 4,

                "target-perfect-con-A": "A",
                "target-dismiss-threshold-A": {"E": 2},
                "target-risk-threshold-A": {"E": 1, "D": 2},
                "target-warn-threshold-A": {"D": 1, "C": 2},
                # "target-passing-grade-M": "C",
                # "target-passing-grade-Q": "D",
                # "target-passing-grade-S": "D",
                # "target-passing-grade-A": "D",

                "absence-M":{
                    "A": 0,
                    "B": 2,
                    "C": 3,
                    "D": 4,
                    "E": 30
                },
                "absence-Q":{
                    "A": 0,
                    "B": 6,
                    "C": 9,
                    "D": 16,
                    "E": 90
                },
                "absence-Semester":{
                    "A": 0,
                    "B": 12,
                    "C": 18,
                    "D": 24,
                    "E": 183
                },
                "absence-Annual": {
                    "A": 2,
                    "B": 24,
                    "C": 36,
                    "D": 48,
                    "E": 365
                },
                "target-M":{
                    "A": 5,
                    "B": 4,
                    "C": 3,
                    "D": 2,
                    "E": 1,
                    "F" : 0
                },
                "target-Q":{
                    "A": 5,
                    "B": 4,
                    "C": 3,
                    "D": 2,
                    "E": 1,
                    "F" : 0
                },
                "target-Semester":{
                    "A": 5,
                    "B": 4,
                    "C": 3,
                    "D": 2,
                    "E": 1,
                    "F" : 0
                },
                "target-Annual": {
                    "A": 5,
                    "B": 4,
                    "C": 3,
                    "D": 2,
                    "E": 1,
                    "F" : 0
                }

            }
        }
        return configs

    def printConfig(self):
        print("\n🔧Current Configuration:")
        print("📁 Paths:")
        for key, val in self.config.get("path", {}).items():
            print(f"  - {key}: {val or '[empty]'}")

        print("\n Settings:")
        for key, val in self.config.get("settings", {}).items():
            print(f"  - {key}: {val}")

        print("\n data:")
        for key, val in self.config.get("data", {}).items():
            print(f"  - {key}: {val}")


    def initConfig(self):
        configs = self.default_config()
        with open(self.path, "w") as f:
            json.dump(configs, f, indent=4)

    def load_config(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                return json.load(f)
        else:
            return self.default_config()

    def save_config(self):
        with open(self.path, "w") as f:
            json.dump(self.config, f, indent=4)

        print(f"\n✅ Config saved to '{self.path}'")

    def get(self, section, key, default=None):
        return self.config.get(section, {}).get(key, default)

    def set(self, section, key, value):
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value
        self.save_config()
