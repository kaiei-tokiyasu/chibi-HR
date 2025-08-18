from menuList.data.DataMenu import DataMenu
from credit import printCredit

from controller.climenu import CLImenu

from menuList.MenuConfig import MenuConfig

class MenuMain:
    def __init__(self):
        self.title = "Main Menu"
        self.menuList = {
            "1": ("Data", DataMenu().run),
            "99": ("Config", MenuConfig().run),
            "100": ("Credit", printCredit)
        }
    
    def run(self):
        title = self.title
        Menu = CLImenu(menuTitle=title) 
        MenuList = self.menuList
        for idx, (label, func) in MenuList.items():
            Menu.add_option(idx, label, func)

        Menu.run()
