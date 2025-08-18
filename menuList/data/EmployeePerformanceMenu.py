import pandas as pd
from menuList.data.Etarget.summary import TargetSummaryMenu
from menuList.data.absence.summary import AbsenceSummaryMenu
from controller.data.EmployeePerformance.EmployeePerformance import EmployeePerformance
from controller.climenu import CLImenu
from controller.pathController import pathController

def validate():
    print("hello")
class EmployeePerformanceMenu:
    def __init__(self):

        self.title = "Merge Data to summary"
        self.paths = pathController()
        self.menuList = {
            # "97": ("export sort by good performance", lambda: EmployeePerformance().exportGoodPerformance()),
            # "98": ("export sort by bad performance", lambda: EmployeePerformance().exportBadPerformance()),
            "99": ("Export ALL to FILE", lambda: EmployeePerformance().exportAllTEMP()),
        }
    
    
    def run(self):
        title = self.title
        Menu = CLImenu(menuTitle=title)
        menuList = self.menuList
        for idx, (label, func) in menuList.items():
            Menu.add_option(idx, label, func)
        
        Menu.run()
