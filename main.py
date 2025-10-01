# log-1
# from creator / solo developer notes:
# sorry for what comes next
#
# for converting to .exe run it in CLI (for production)
# pyinstaller --onefile --version-file=version.txt --name chibi-HR main.py
# pyinstaller chibi-HR.spec
#
# this code starts on 2 July 2025
#
# please enable warnings before production thank you

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

import pandas as pd
pd.set_option('future.no_silent_downcasting', True)

import os.path
from config import ConfigManager
from menuList.MainMenu import MenuMain

from utils.system import SystemController

def closeProgramMessage():
    SystemController.clear_screen()
    print("exiting program . . .")
    print("Thank you for using this program.")
    SystemController.wait_for_keypress()

def checkDir():
    total_Process = 4
    CM = ConfigManager()
    SC = SystemController()
    try:
        SC.print_loading_bar(task_name="Initializing",current=1, total=total_Process)
        current_path = os.getcwd()

        config = CM.path
        input_path = os.path.join(current_path, "DATASET", "INPUT")
        output_path = os.path.join(current_path, "DATASET", "OUTPUT")

        SC.print_loading_bar(task_name="Checking Config",current=2, total=total_Process)
        if not os.path.exists(config):
            ConfigManager().initConfig()

        # print(f"{config} ok")

        SC.print_loading_bar(task_name="Checking Path",current=3, total=total_Process)
        if not os.path.exists(input_path) or os.path.exists(output_path):
            absencePath = os.path.join(input_path, "ABSENCE")
            targetPath = os.path.join(input_path, "TARGET")

            os.makedirs(input_path, exist_ok=True)
            os.makedirs(absencePath, exist_ok=True)
            os.makedirs(targetPath, exist_ok=True)

            os.makedirs(output_path, exist_ok=True)
            # print()
            # print("directories created")

        # print(f"{input_path} ok")
        # print(f"{output_path} ok")
        SC.print_loading_bar(task_name="Initiation",current=4, total=total_Process)
    except ValueError:
        print("Initiation Error")
        print(ValueError)
    print()
    isSkip = CM.config['skip-init-loader']
    if not isSkip:
        SystemController.wait_for_keypress()

    return

def main():
    MenuMain().run()

    closeProgramMessage()

    return

if __name__ == "__main__":
    SystemController.clear_screen()
    checkDir()
    SystemController.clear_screen()
    try:
        main()
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting gracefully.")
        closeProgramMessage()
