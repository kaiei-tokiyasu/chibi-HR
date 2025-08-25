import pandas as pd
from config import ConfigManager
from menuList.data.Etarget.summary import TargetSummaryMenu
from menuList.data.absence.summary import AbsenceSummaryMenu
from controller.data.EmployeePerformance.EmployeePerformance import EmployeePerformance
from controller.climenu import CLImenu
from controller.pathController import pathController

def validate():
    print("hello")
class EmployeePerformanceMenu:
    def __init__(self):
        CM = ConfigManager()
        self.XMonthAbsence = CM.config['data']["absence-X-M"]
        self.XMonthTarget = CM.config['data']["target-X-M"]

        self.title = "Merge Data to summary"
        self.paths = pathController()
        self.menuList = {

            # "97": (f"Export Absence last {self.XMonthAbsence} month to FILE", lambda: EmployeePerformance().exportAllTEMP()),
            # "98": (f"Export Target last {self.XMonthTarget} month to FILE", lambda: EmployeePerformance().exportAllTEMP()),
            "99": ("Export ALL to FILE", lambda: EmployeePerformance().exportAllTEMP()),
        }
    
    
    def run(self):
        title = self.title
        Menu = CLImenu(menuTitle=title)
        menuList = self.menuList
        for idx, (label, func) in menuList.items():
            Menu.add_option(idx, label, func)
        
        Menu.run()
