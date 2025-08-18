from menuList.data.EmployeePerformanceMenu import EmployeePerformanceMenu
from menuList.data.Etarget.targetmenu import TargetMenu
from menuList.data.absence.AbsenceMenu import AbsenceMenu
from credit import printCredit
from controller.climenu import CLImenu

class DataMenu:
    def __init__(self):
        self.title = "Data Menu"
        self.menuList = {
            "1": ("Absense", AbsenceMenu().run),
            "2": ("Target", TargetMenu().run),
            "3": ("Employee Performance", EmployeePerformanceMenu().run)
        }
    
    def run(self):
        title = self.title
        Menu = CLImenu(menuTitle=title) 
        MenuList = self.menuList
        for idx, (label, func) in MenuList.items():
            Menu.add_option(idx, label, func)

        Menu.run()
