from menuList.data.Etarget.summary import TargetSummaryMenu
from controller.data.ETarget.Target import Target
from utils.lib import lib
from config import ConfigManager
from controller.climenu import CLImenu

def overview():
    print('coming soon')
def generateReport():
    print('generate')

class TargetMenu:
    def __init__(self):
        self.title = "Target Config Menu"
        
        self.menuList = {
            # "1": ("overview", overview),
            "2": ("show raw data", lambda: self.showData()), 
            "3": ("summary", TargetSummaryMenu().run),
            # "4": ("generate report", TargetReportMenu().run), 
        }
        
        self.df = None

    def setDF(self, data):
        self.df = data

    def showData(self):
        if self.df is None:
            TD = Target()
            TD = TD.sync()
            if TD is None:
                return
            data = TD
            self.setDF(data=data)


        libS = lib()
        libS.show_df_page(self.df)
        return
    
    def run(self):
        title = self.title
        Menu = CLImenu(menuTitle=title) 
        MenuList = self.menuList
        for idx, (label, func) in MenuList.items():
            Menu.add_option(idx, label, func)

        Menu.run()
