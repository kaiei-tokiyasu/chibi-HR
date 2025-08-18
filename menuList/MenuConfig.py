from menuList.data.Etarget.configMenu import TargetConfigMenu
from menuList.data.absence.ConfigMenu import AbsenceConfigMenu
from config import ConfigManager
from controller.climenu import CLImenu
from controller.pathController import pathController

class MenuConfig:
    def __init__(self):
        self.title = "Configuration"
        self.paths = pathController()
        self.menuList = {
            "1":("Show Configurations", lambda: ConfigManager().printConfig()),
            "2": ("Set Input Path", lambda: self.paths.set_path(key_name="input_path")),
            "3": ("Set Output Path",  lambda: self.paths.set_path(key_name="output_path")),
            "4": ("Set page size", lambda: self.setPageSize()),
            "5": ("Absence Grade", AbsenceConfigMenu().run),
            "6": ("Target Grade", TargetConfigMenu().run)
        }
    
    def setPageSize(self):
        u_input = input("Enter Page Size: ")

        try:
            u_input = int(u_input)
            if u_input <= 0:
                print("Invalid Page size cannot be 0 or negative")
            else:
                ConfigManager().set("settings", "default_page_size", u_input)
        except ValueError:
            print("❌ Not a valid integer.")
    
    def run(self):
        title = self.title
        Menu = CLImenu(menuTitle=title)
        menuList = self.menuList
        for idx, (label, func) in menuList.items():
            Menu.add_option(idx, label, func)
        
        Menu.run()
