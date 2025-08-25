import pandas as pd
from controller.data.Absence.period.annual import AbsenceAnnual
from controller.data.Absence.period.lastXmonth import AbsenceXMonth
from controller.data.Absence.period.monthly import AbsenceMonthly
from controller.data.Absence.period.quarter import AbsenceQuarter
from controller.data.Absence.period.semester import AbsenceSemester
from controller.pathController import pathController
from utils.system import SystemController
from utils.lib import lib
from config import ConfigManager
from controller.data.Absence.Absence import Absence
from credit import printCredit
from controller.climenu import CLImenu

class AbsenceSummaryMenu:
    def __init__(self):
        self.paths = pathController().paths
        self.output_path = self.paths['output_path']
        self.title = "Absence Summary Menu"
        CM = ConfigManager()
        self.XMonth = CM.config['data']["absence-X-M"]
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
            # "11": ("all raw summary", self.getSummary),
            # "12": ("export all raw summary data", self.exportAllSummary),
            "14": ("update/sync data", self.updateAll),
        }
        self.raw = None
        self.summaryM =None
        self.summaryXM =None
        self.summaryQ =None
        self.summaryS =None
        self.summaryA =None

        self.dfSummary = None

        self.perfectCon = CM.config['data']["absence-perfect-con-M"]
        self.dismissCon = CM.config['data']["absence-dismiss-threshold-M"]
        self.riskCon = CM.config['data']["absence-risk-threshold-M"]
        self.warnCon = CM.config['data']["absence-warn-threshold-M"]
        self.recentWin = CM.config['data']["absence-recent-trend-M"]
    
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
    
    def setAbsence(self, type):
        if self.raw is None:
            raw = self.loadRaw()
            if raw is None:
                return
            self.setRaw(raw)

        data = self.raw
        if type == 'M':
            summaryM = AbsenceMonthly().GetSummary(dataframe=data)
            self.setSummaryM(summaryM)
            return 
        elif type == 'XM':
            summaryXM = AbsenceXMonth().getLastXMonthData(data=self.summaryM)
            self.setSummaryXM(summaryXM)
            return 
        elif type == 'Q':
            summaryQ = AbsenceQuarter().GetSummary(dataframe=data)
            self.setSummaryQ(summaryQ)
            return 
        elif type =='S':
            summaryS = AbsenceSemester().GetSummary(dataframe=data)
            self.setSummaryS(summaryS)
            return
        elif type == 'A':
            summaryA = AbsenceAnnual().GetSummary(dataframe=data)
            self.setSummaryA(summaryA)
            return
        return None
    
    def loadRaw(self):
        AC = Absence()
        AC = AC.sync()
        return AC
    
    def getSummaryM(self):
        if self.summaryM is None:
            self.setAbsence(type='M')
        
        libS = lib()
        libS.show_df_page(self.summaryM)
    
    def getSummaryQ(self):
        if self.summaryQ is None:
            self.setAbsence(type='Q')
        
        libS = lib()
        libS.show_df_page(self.summaryQ)
    
    def getSummaryS(self):
        if self.summaryS is None:
            self.setAbsence(type='S')
        
        libS = lib()
        libS.show_df_page(self.summaryS)
    
    def getSummaryA(self):
        if self.summaryA is None:
            self.setAbsence(type='A')
        
        libS = lib()
        libS.show_df_page(self.summaryA)
        
    def getSummary(self):
        if self.dfSummary is None:
            if self.raw is None:
                return
             
            if self.summaryM is None:
                self.setAbsence(type='M')
            
            if self.summaryQ is None:
                self.setAbsence(type='Q')
            
            if self.summaryS is None:
                self.setAbsence(type='S')
            if self.summaryA is None:
                self.setAbsence(type='A')
            
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
                self.setAbsence(type='M')
            self.setAbsence(type='XM')
        
        libS = lib()
        libS.show_df_page(self.summaryXM)

    def updateAll(self):
        raw = self.loadRaw()
        if raw is None:
            return
        
        total_Process = 8
        SC = SystemController()
        self.setRaw(raw)
        data = self.raw

        SC.print_loading_bar(task_name="Processing Monthly",current=1, total=total_Process)
        summaryM = AbsenceMonthly().GetSummary(dataframe=data)
        self.setSummaryM(summaryM)

        SC.print_loading_bar(task_name=f"Processing last {self.XMonth} Month",current=2, total=total_Process)
        summaryXM = AbsenceXMonth().getLastXMonthData(data=summaryM)
        self.setSummaryXM(summaryXM)

        SC.print_loading_bar(task_name="Processing Quarter",current=3, total=total_Process)
        summaryQ = AbsenceQuarter().GetSummary(dataframe=data)
        self.setSummaryQ(summaryQ)

        SC.print_loading_bar(task_name="Processing Semester",current=4, total=total_Process)
        summaryS = AbsenceSemester().GetSummary(dataframe=data)        
        self.setSummaryS(summaryS)

        SC.print_loading_bar(task_name="Processing Annual",current=5, total=total_Process)
        summaryA = AbsenceAnnual().GetSummary(dataframe=data)
        self.setSummaryA(summaryA)

        SC.print_loading_bar(task_name="Combining . . .",current=6, total=total_Process)
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
        SC.print_loading_bar(task_name="Finishing",current=7, total=total_Process)
        self.setDF(finalSummary)

        SC.print_loading_bar(task_name="Completed",current=8, total=total_Process)

        print()
        # SystemController.wait_for_keypress()
        return
    
    def exportAllSummary(self):
        if self.dfSummary is None:
            self.updateAll()
        
        summaryM = self.summaryM
        summaryQ = self.summaryQ
        summaryS = self.summaryS
        summaryA = self.summaryA

        All = self.dfSummary
        outputAName = "\\absenceRawSummary.xlsx"
        AbsenceOutputPath = self.output_path+outputAName

        with pd.ExcelWriter(AbsenceOutputPath) as writer:
            summaryM.to_excel(writer, sheet_name="Monthly", index=True)
            summaryQ.to_excel(writer, sheet_name="Quarter", index=True)
            summaryS.to_excel(writer, sheet_name="Semester", index=True)
            summaryA.to_excel(writer, sheet_name="Annual", index=True)
            All.to_excel(writer, sheet_name="All", index=True)
        
        return
    
    def getPerfectListM(self):
        if self.summaryM is None:
            self.setAbsence(type='M')
        
        df_clean = Absence().getPRL(data=self.summaryM)
        libS = lib()
        libS.show_df_page(df_clean)

    def getGoodListM(self):
        if self.summaryM is None:
            self.setAbsence(type='M')
        
        df_clean = Absence().getGRL(data=self.summaryM)
        libS = lib()
        libS.show_df_page(df_clean)

    def getWarnListM(self):
        if self.summaryM is None:
            self.setAbsence(type='M')
        
        df_clean = Absence().getNIL(data=self.summaryM)
        libS = lib()
        libS.show_df_page(df_clean)
    
    def getCallListM(self):
        if self.summaryM is None:
            self.setAbsence(type='M')
        
        df_clean = Absence().getARL(data=self.summaryM)
        libS = lib()
        libS.show_df_page(df_clean)

    def getDismissListM(self):
        if self.summaryM is None:
            self.setAbsence(type='M')
        
        df_clean = Absence().getRDL(data=self.summaryM)
        libS = lib()
        libS.show_df_page(df_clean)
    
    def getImprovingListM(self):
        if self.summaryM is None:
            self.setAbsence(type='M')
        
        df_clean = Absence().getImporvingList(data=self.summaryM)
        libS = lib()
        libS.show_df_page(df_clean)

    def getStableListM(self):
        if self.summaryM is None:
            self.setAbsence(type='M')
        
        df_clean = Absence().getStableList(data=self.summaryM)
        libS = lib()
        libS.show_df_page(df_clean)

    def getDecliningListM(self):
        if self.summaryM is None:
            self.setAbsence(type='M')
        
        df_clean = Absence().getDecliningList(data=self.summaryM)
        libS = lib()
        libS.show_df_page(df_clean)
        
    def run(self):
        title = self.title

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
