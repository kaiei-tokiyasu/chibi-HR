from ui import ui
from utils.system import SystemController

class CLImenu:
    def __init__(self, menuTitle, menuDesc = None):
        self.menuTitle = menuTitle
        self.menuDesc = menuDesc
        self.menu = {}
        self.running = True

    def add_option(self, key: str, label: str, function):
        self.menu[key] = (label, function)

    def display_Menu (self):
        # print("\n")
        uiPrint = ui()
        uiPrint.setUi(title=self.menuTitle, desc=self.menuDesc)
        uiPrint.print_title()
        uiPrint.print_body()
        for key, (label, _) in sorted(self.menu.items(), key=lambda x: int(x[0])):
            print(f"{key}. {label}")
        print("0. Exit menu")

    def run(self):
        while self.running:
            self.display_Menu()
            choice = input("Select menu Item: ")
            SystemController.clear_screen()
            if choice == "0":
                self.running = False
                
            elif choice in self.menu:
                _, func = self.menu[choice]
                func()
                print()
            else:
                print("Invalid selection. Please try again.")
    
    
