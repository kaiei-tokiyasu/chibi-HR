
from menuList.data.absence.report import AbsenceReportMenu
from utils.lib import lib
from controller.data.Absence.Absence import Absence
from menuList.data.absence.summary import AbsenceSummaryMenu
from credit import printCredit
from controller.climenu import CLImenu

def overview():
    print('coming soon')
def generateReport():
    print('generate')


class AbsenceMenu:
    def __init__(self):
        self.title = "Absence Menu"
        
        self.menuList = {
            # "1": ("overview", overview),
            "2": ("show raw data", lambda: self.showData()), 
            "3": ("summary", AbsenceSummaryMenu().run),
            # "4": ("generate report", AbsenceReportMenu().run), 
        }

        self.df = None

    def setDF(self, data):
        self.df = data

    def showData(self):
        if self.df is None:
            AC = Absence()
            AC = AC.sync()
            if AC is None:
                return
            data = AC
            self.setDF(data=data)
        
        libS = lib()
        libS.show_df_page(self.df)

    def run(self):
        title = self.title
        absenceMenu = CLImenu(menuTitle=title) 
        absenceMenuList = self.menuList
        for idx, (label, func) in absenceMenuList.items():
            absenceMenu.add_option(idx, label, func)

        absenceMenu.run()
