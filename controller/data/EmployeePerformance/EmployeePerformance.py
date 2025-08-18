import pathlib
from openpyxl import load_workbook
from urllib.parse import urlparse
import subprocess

import pandas as pd
from config import ConfigManager
from controller.data.EmployeePerformance.EmployeePerformanceController import EmployeePerformanceController  as EPC 
from menuList.data.absence.summary import AbsenceSummaryMenu
from menuList.data.Etarget.summary import TargetSummaryMenu
from controller.data.ETarget.TargetController import TargetController
from utils.system import SystemController

from controller.pathController import pathController

class EmployeePerformance:
    def __init__(self):
        self.paths = pathController().paths
        self.output_path = self.paths['output_path']

        self.EPSummaryM = None
        self.EPSummaryMRaw = None

        CM = ConfigManager()

        self.cliLinkMode = CM.config['cli-link-mode']

        return
    
    def SetEPSummary(self, dataM):
        self.EPSummaryM = dataM

    
    def ProcessSummaryQuarter(self):
        ASummaryQ = self.AsummaryQ
        TDSummaryQ = self.TsummaryQ

        SummaryQ = pd.merge(
            ASummaryQ, 
            TDSummaryQ,
            on=['No.Absen', 'Nama', 'Bagian', 'tahun'],
            how='outer'
        )
        SummaryQ = ( 
            SummaryQ.groupby(['No.Absen'], as_index=False)
                .agg(lambda x: x.ffill().bfill().iloc[0]) )
        SummaryQ = SummaryQ.infer_objects(copy=False)
        SummaryQ = SummaryQ.drop_duplicates(subset='No.Absen', keep='last').reset_index(drop=True)
        columnQ = [
            'No.Absen', 'Nama', 'Bagian', 'tahun', 
            'absen_avg_Q1', 'nilai_absen_Q1', 'Total_Absen_Q1', 'target_avg_Q1', 'nilai_Target_Q1',
            'absen_avg_Q2', 'nilai_absen_Q2', 'Total_Absen_Q2', 'target_avg_Q2', 'nilai_Target_Q2',
            'absen_avg_Q3', 'nilai_absen_Q3', 'Total_Absen_Q3', 'target_avg_Q3', 'nilai_Target_Q3',
            'absen_avg_Q4', 'nilai_absen_Q4', 'Total_Absen_Q4', 'target_avg_Q4', 'nilai_Target_Q4',
        ]
        SummaryQ = SummaryQ[columnQ]
        return SummaryQ
        
    def checkSelfData(self):
        if self.EPSummaryM is None:
            AC = AbsenceSummaryMenu()
            AC.updateAll()

            TD = TargetSummaryMenu()
            TD.updateAll()

            self.EPSummaryMRaw = [
                AC.raw,
                AC.summaryM, 
                TD.raw,
                TD.summaryM,
            ]

            SummaryMonth = EPC.ProcessSummaryMonth(AC.summaryM, TD.summaryM)
            self.SetEPSummary(dataM=SummaryMonth)


    def exportGoodPerformance(self):
        self.checkSelfData()
        # SummaryMonth = self.EPSummaryM

        return
    
    def exportBadPerformance(self):
        self.checkSelfData()

        return
    
    def exportAllTEMP (self):
        total_Process = 7
        SC = SystemController()

        SC.print_loading_bar(task_name="Checking Data",current=1, total=total_Process)
        self.checkSelfData()
        
        # ASummaryS = self.AsummaryS
        # ASummaryA = self.AsummaryA
        # All_Absence = self.AsummaryM
        
        # TDSummaryS = self.TsummaryS
        # TDSummaryA = self.TsummaryA
        # All_Target = self.Tsummary

        SummaryM = self.EPSummaryM
        
        AbsenceSummary = self.EPSummaryMRaw[0]
        AbsenceSummaryM = self.EPSummaryMRaw[1]
        TargetSummary = self.EPSummaryMRaw[2]
        TargetSummaryM = self.EPSummaryMRaw[3]

        
        # SummaryQ = self.ProcessSummaryQuarter()
        
        outputAName = "\\Employee_Absence_Performance_Summary.xlsx"
        SummaryOutputPath = self.output_path+outputAName

        SC.print_loading_bar(task_name="Exporting",current=2, total=total_Process)

        with pd.ExcelWriter(SummaryOutputPath) as writer:
            SummaryM.to_excel(writer, sheet_name="Employee Performance", index=True)
            AbsenceSummary.to_excel(writer, sheet_name="Absence-Raw", index=True)
            AbsenceSummaryM.to_excel(writer, sheet_name="Absence", index=True)
            TargetSummary.to_excel(writer, sheet_name="Target-Raw", index=True)
            TargetSummaryM.to_excel(writer, sheet_name="Target", index=True)
            
            # SummaryQ.to_excel(writer, sheet_name="Quarter", index=True)
            
        SC.print_loading_bar(task_name="1/3 Conditional Formatting",current=4, total=total_Process)
        EPC().formatExcelMonth(w=SummaryOutputPath, sheetname="Employee Performance", data=SummaryM, type="combine")
        
        SC.print_loading_bar(task_name="2/3 Conditional Formatting",current=5, total=total_Process)
        EPC().formatExcelMonth(w=SummaryOutputPath, sheetname="Absence", data=AbsenceSummaryM, type="Absence")
        
        SC.print_loading_bar(task_name="3/3 Conditional Formatting",current=5, total=total_Process)
        EPC().formatExcelMonth(w=SummaryOutputPath, sheetname="Target", data=TargetSummaryM, type="Target")

        SC.print_loading_bar(task_name="Formatting",current=7, total=total_Process)

        # self.formatExcelQuarter(w=SummaryOutputPath, data=SummaryQ)
        
        if self.cliLinkMode == "UNC":
            folder_url = pathlib.Path(SummaryOutputPath).as_uri()
            parsed = urlparse(folder_url)
            path_fixed = parsed.path.replace('/', '\\')
            unc_path = rf"\\{parsed.netloc}{path_fixed}"
            print()
            print(f"✅ Excel saved! File is ready to open! Open this folder in your file explorer:\n🔗 {unc_path}")
            subprocess.run(['explorer', unc_path])
        else:
            print(f"\n✅ Excel saved! File is ready to open! Open this folder in your file explorer:\n📁 {SummaryOutputPath}")
            subprocess.run(['explorer', SummaryOutputPath])

        return
    

    def run(self):
        
        TarController = TargetController()
        
        hasFilesT = TarController.checkTargetFiles()

        if not hasFilesT:
            print()
            print("no data available. please insert files in directory below")
            print(self.targetDir)
            print()
            SystemController.wait_for_keypress()
            return 
        
        # AbsenceDF = AbsController.SetAbsenceDF()
        # outputAName = "\\absenceCleaned.xlsx"
        # AbsenceOutputPath = self.output_path+outputAName
        # AbsenceDF.to_excel(AbsenceOutputPath)

        # TargetDF = TarController.SetTargetDF()
        # outputTName = "\\targetCleaned.xlsx"
        # TargetOutputPath = self.output_path+outputTName
        # TargetDF.to_excel(TargetOutputPath)
   
        return