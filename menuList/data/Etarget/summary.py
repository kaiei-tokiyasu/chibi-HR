import pandas as pd
from controller.data.ETarget.period.annual import TargetAnnual
from controller.data.ETarget.period.lastXmonth import TargetXMonth
from controller.data.ETarget.period.monthly import TargetMonthly
from controller.data.ETarget.period.quarter import TargetQuarter
from controller.data.ETarget.period.semester import TargetSemester
from utils.system import SystemController
from controller.data.ETarget.Target import Target
from utils.lib import lib
from config import ConfigManager
from controller.data.Absence.Absence import Absence
from credit import printCredit
from controller.climenu import CLImenu

class TargetSummaryMenu:
    def __init__(self):
        self.title = "Absence Summary Menu"
        CM = ConfigManager()
        
        self.XMonth = CM.config['data']["target-X-M"]
        self.menuList = {
            "1": ("Montly data", self.getSummaryM),
            "2": (f"Show Last {self.XMonth} month", self.getXmonth),
            "3": ("List Perfect Record", self.getPerfectListM),
            "4": ("List Good Record", self.getGoodListM),
            "5": ("List to warn", self.getWarnListM),
            "6": ("List to call for improvement", self.getCallListM),
            "7": ("List to dismiss", self.getDismissListM),
            "8": ("List Improving", self.getImprovingListM),
            "9": ("List Stable", self.getStableListM),
            "10": ("List Declining", self.getDecliningListM),
            "11": ("Quarter data", self.getSummaryQ),
            "12": ("Semester data", self.getSummaryS),
            "13": ("Annual data", self.getSummaryA),
            "14": ("update/sync data", self.updateAll),
        }
        self.raw = None

        self.summaryM =None
        self.summaryXM =None
        self.summaryQ =None
        self.summaryS =None
        self.summaryA =None

        self.dfSummary = None

       

        self.perfectCon = CM.config['data']["target-perfect-con-M"]
        self.dismissCon = CM.config['data']["target-dismiss-threshold-M"]
        self.riskCon = CM.config['data']["target-risk-threshold-M"]
        self.warnCon = CM.config['data']["target-warn-threshold-M"]
        self.recentWin = CM.config['data']["target-recent-trend-M"]

    
    def dummy(self):
        print('not yet')
        return
    
    def setRaw(self, data):
        self.raw = data
    
    def setSummaryM(self, data):
        self.summaryM = data

    def setSummaryXM(self, data):
        self.summaryXM = data

    def setSummaryQ(self, data):
        self.summaryQ = data

    def setSummaryS(self, data):
        self.summaryS = data

    def setSummaryA(self, data):
        self.summaryA = data

    def setDF(self, data):
        self.dfSummary = data

    def setTarget(self, type):
        if self.raw is None:
            raw = self.loadRaw()
            if raw is None:
                return
            self.setRaw(raw)

        data = self.raw
        if type == 'M':
            summaryM = TargetMonthly().GetSummary(dataframe=data)
            self.setSummaryM(summaryM)
            return 
        elif type == 'XM':
            summaryM = TargetXMonth().getLastXMonthData(data=self.summaryM)
            self.setSummaryXM(summaryM)
            return 
        elif type == 'Q':
            summaryQ = TargetQuarter().GetSummary(dataframe=data)
            self.setSummaryQ(summaryQ)
            return 
        elif type =='S':
            summaryS = TargetSemester().GetSummary(dataframe=data)
            self.setSummaryS(summaryS)
            return
        elif type == 'A':
            summaryA = TargetAnnual().GetSummary(dataframe=data)
            self.setSummaryA(summaryA)
            return
        return None
   
    def loadRaw(self):
        TD = Target()
        TD = TD.sync()
        return TD
   
    def getSummaryM(self):
        if self.summaryM is None:
            self.setTarget(type='M')
        
        libS = lib()
        libS.show_df_page(self.summaryM)
    
    def getSummaryQ(self):
        if self.summaryQ is None:
            self.setTarget(type='Q')
        
        libS = lib()
        libS.show_df_page(self.summaryQ)
    
    def getSummaryS(self):
        if self.summaryS is None:
            self.setTarget(type='S')
        
        libS = lib()
        libS.show_df_page(self.summaryS)
    
    def getSummaryA(self):
        if self.summaryA is None:
            self.setTarget(type='A')
        
        libS = lib()
        libS.show_df_page(self.summaryA)
        
    def getSummary(self):
        if self.dfSummary is None:
            if self.summaryM is None:
                self.setTarget(type='M')
            
            if self.raw is None:
                return
            
            if self.summaryQ is None:
                self.setTarget(type='Q')
            if self.summaryS is None:
                self.setTarget(type='S')
            if self.summaryA is None:
                self.setTarget(type='A')
            
            summaryM = self.summaryM
            summaryQ = self.summaryQ
            summaryS = self.summaryS
            summaryA = self.summaryA

            finalSummary = pd.merge(
                summaryM,
                summaryQ,
                on=['No.Absen', 'Nama', 'Bagian', 'tahun'],
                how='outer'
            )

            finalSummary = pd.merge(
                finalSummary,
                summaryS,
                on=['No.Absen', 'Nama', 'Bagian', 'tahun'],
                how='outer'
            )
            finalSummary = pd.merge(
                finalSummary,
                summaryA,
                on=['No.Absen', 'Nama', 'Bagian', 'tahun'],
                how='outer'
            )
            self.setDF(finalSummary)
            
            libS = lib()
            libS.show_df_page(self.dfSummary)

            return
    def getXmonth(self):
        if self.summaryXM is None:
            if self.summaryM is None:
                self.setTarget(type='M')
            self.setTarget(type='XM')
        
        libS = lib()
        libS.show_df_page(self.summaryXM)
        
    def getPerfectListM(self):
        if self.summaryM is None:
            self.setTarget(type='M')
        
        df_clean = Target().getPRL(data=self.summaryM)
        libS = lib()
        libS.show_df_page(df_clean)

    def getGoodListM(self):
        if self.summaryM is None:
            self.setTarget(type='M')
        
        df_clean = Target().getGRL(data=self.summaryM)
        libS = lib()
        libS.show_df_page(df_clean)

    def getWarnListM(self):
        if self.summaryM is None:
            self.setTarget(type='M')
        
        df_clean = Target().getNIL(data=self.summaryM)
        libS = lib()
        libS.show_df_page(df_clean)
    
    def getCallListM(self):
        if self.summaryM is None:
            self.setTarget(type='M')
        
        df_clean = Target().getARL(data=self.summaryM)
        libS = lib()
        libS.show_df_page(df_clean)

    def getDismissListM(self):
        if self.summaryM is None:
            self.setTarget(type='M')
        
        df_clean = Target().getRDL(data=self.summaryM)
        libS = lib()
        libS.show_df_page(df_clean)
    
    def getImprovingListM(self):
        if self.summaryM is None:
            self.setTarget(type='M')
        
        df_clean = Target().getImporvingList(data=self.summaryM)
        libS = lib()
        libS.show_df_page(df_clean)

    def getStableListM(self):
        if self.summaryM is None:
            self.setTarget(type='M')
        
        df_clean = Target().getStableList(data=self.summaryM)
        libS = lib()
        libS.show_df_page(df_clean)

    def getDecliningListM(self):
        if self.summaryM is None:
            self.setTarget(type='M')
        
        df_clean = Target().getDecliningList(data=self.summaryM)
        libS = lib()
        libS.show_df_page(df_clean)
    
    
    def updateAll(self):
        raw = self.loadRaw()
        if raw is None:
            return
        
        total_Process = 8
        SC = SystemController()
        self.setRaw(raw)
        data = self.raw

        SC.print_loading_bar(task_name="Processing Monthly",current=1, total=total_Process)
        summaryM = TargetMonthly().GetSummary(dataframe=data)
        self.setSummaryM(summaryM)

        SC.print_loading_bar(task_name=f"Processing {self.XMonth} Monthly",current=2, total=total_Process)
        summaryXM = TargetXMonth().getLastXMonthData(data=summaryM)
        self.setSummaryXM(summaryXM)

        SC.print_loading_bar(task_name="Processing Quarter",current=3, total=total_Process)
        summaryQ = TargetQuarter().GetSummary(dataframe=data)
        self.setSummaryQ(summaryQ)

        SC.print_loading_bar(task_name="Processing Semester",current=4, total=total_Process)
        summaryS = TargetSemester().GetSummary(dataframe=data)        
        self.setSummaryS(summaryS)

        SC.print_loading_bar(task_name="Processing Annual",current=5, total=total_Process)
        summaryA = TargetAnnual().GetSummary(dataframe=data)
        self.setSummaryA(summaryA)

        SC.print_loading_bar(task_name="Combining . . .",current=6, total=total_Process)
        finalSummary = pd.merge(
            summaryQ,
            summaryS,
            on=['No.Absen', 'Nama', 'Bagian', 'tahun'],
            how='outer'
        )
        finalSummary = pd.merge(
            finalSummary,
            summaryA,
            on=['No.Absen', 'Nama', 'Bagian', 'tahun'],
            how='outer'
        )

        SC.print_loading_bar(task_name="Finishing",current=7, total=total_Process)
        self.setDF(finalSummary)

        SC.print_loading_bar(task_name="Completed",current=8, total=total_Process)

        print()
        # SystemController.wait_for_keypress()
        return
     
    def run(self):
        title = self.title
        # desc1 = f"=> Passing Grade Quarter: {passing_gradeQ}\n"
        # desc2 = f"=> Passing Grade Semester: {passing_gradeS}\n"
        # desc3 = f"=> Passing Grade Annual: {passing_gradeA}\n"

        desc1 = f"=> Absence perfect Condition in 1 year: {self.perfectCon}\n"
        desc2 = f"=> recent trend window in month: {self.recentWin}\n"
        desc3 = f"=> warn threshold: {self.warnCon}\n"
        desc4 = f"=> risk threshold: {self.riskCon}\n"
        desc5 = f"=> dismiss threshold: {self.dismissCon}\n"
        # desc6 = f"=> Passing Grade Quarter: {passing_gradeQ}\n"
        # desc7 = f"=> Passing Grade Semester: {passing_gradeS}\n"
        # desc8 = f"=> Passing Grade Annual: {passing_gradeA}\n"
        
        desc = desc1+desc2+desc3+desc4+desc5
        Menu = CLImenu(menuTitle=title, menuDesc=desc)

        MenuList = self.menuList
        for idx, (label, func) in MenuList.items():
            Menu.add_option(idx, label, func)

        Menu.run()
