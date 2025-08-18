from credit import printCredit
from controller.climenu import CLImenu

def generateReport():
    print('add Generate Report feature')

class AbsenceReportMenu:
    def __init__(self):
        self.title = "Generate Report Menu"
        self.menuList = {
            "1": ("Q I", generateReport),
            "2": ("Q II", generateReport),
            "3": ("Q III", generateReport),
            "4": ("Q IV", generateReport),

            "5": ("Semester I", generateReport),
            "6": ("Semester II", generateReport),
        }
    
    def run(self):
        title = self.title
        Menu = CLImenu(menuTitle=title) 
        MenuList = self.menuList
        for idx, (label, func) in MenuList.items():
            Menu.add_option(idx, label, func)
        Menu.run()
