import pathlib
from unittest import result
import numpy as np
import pandas as pd
from utils.system import SystemController
from controller.data.ETarget.TargetController import TargetController
from config import ConfigManager
from controller.pathController import pathController

class Target:
    def __init__(self):
        self.paths = pathController().paths
        self.input_path = self.paths['input_path']
        self.targetDir = pathlib.Path(self.input_path+"\\TARGET")
        CM = ConfigManager()

        self.perfectCon = CM.config['data']["target-perfect-con-M"]
        self.dismissCon = CM.config['data']["target-dismiss-threshold-M"]
        self.riskCon = CM.config['data']["target-risk-threshold-M"]
        self.warnCon = CM.config['data']["target-warn-threshold-M"]

        self.recentWin = CM.config['data']["target-recent-trend-M"]

        self.target_grade_M = CM.config['data']['target-M']
        self.target_grade_Q = CM.config['data']['target-Q']
        self.target_grade_S = CM.config['data']['target-Semester']
        self.target_grade_A = CM.config['data']['target-Annual']

    def setGrade(self, avg, gradeType):
        if avg >= gradeType['A']:
            return 'A'
        elif avg >= gradeType['B'] and avg < gradeType['A']:
            return 'B'
        elif avg >= gradeType['C'] and avg < gradeType['B']:
            return 'C'
        elif avg >= gradeType['D'] and avg < gradeType['C']:
            return 'D'
        elif avg >= gradeType['E'] and avg < gradeType['D']:
            return 'E'
        elif avg >= gradeType['F'] and avg < gradeType['E']:
            return 'F'
        else:
            return '#'

    def gradeQ(self, avg):
        grade = self.target_grade_Q
        return self.setGrade(avg=avg, gradeType=grade)
    
    def gradeS(self, avg):
        grade = self.target_grade_S
        return self.setGrade(avg=avg, gradeType=grade)
    
    def gradeA(self, avg):
        grade = self.target_grade_A
        return self.setGrade(avg=avg, gradeType=grade)
    
    def StatusGradeCal (self, grades):
        grade_scale = self.target_grade_M
        valid_grades = [g for g in grades if isinstance(g, str) and g in grade_scale and g != '#' and g != '-' and g != 'X']

        grade_counts = {}
        for g in valid_grades:
            grade_counts[g] = grade_counts.get(g, 0) + 1

        if not valid_grades:
            overall_status = "no data"

        elif valid_grades and all(g in self.perfectCon for g in valid_grades):
                overall_status = "S Perfect Record"
        elif all(grade_counts.get(k, 0) >= v for k, v in self.dismissCon.items()):
            overall_status = "Recommended for Dismissal"
        elif all(grade_counts.get(k, 0) >= v for k, v in self.riskCon.items()):
            overall_status = "At Risk"
        elif all(grade_counts.get(k, 0) >= v for k, v in self.warnCon.items()):
            overall_status = "Needs Improvement"
        else:
            overall_status = "Good Record"

        recent_grades = [grade_scale[g.upper()] for g in valid_grades[-self.recentWin:]]

        if len(recent_grades) < self.recentWin:
            recent_trend = "stable"  # Not enough data
        elif recent_grades[-2] < recent_grades[-1]:
            recent_trend = "improving"
        elif recent_grades[-2] > recent_grades[-1]:
            recent_trend = "declining"
        else:
            recent_trend = "stable"
        
        return {
            "overall_status_T": overall_status,
            "recent_trend_T": recent_trend
        }
    
    def setStatus(self, data):
        grade_cols = [col for col in data.columns if col.isdigit() and 1 <= int(col) <= 12]

        data[['overall_status_T', 'recent_trend_T']] = data.apply(
            lambda row: pd.Series(
                self.StatusGradeCal([row[col] for col in grade_cols])
            ), axis=1)
        return data
    
    def MonthlySummary(self, dataframe):
        df = dataframe
        
        monthly = df.copy()
        monthly['tahun'] = monthly['tahun'].astype(np.int64)
        monthly =  self.setStatus(monthly)

        result = monthly[['No.Absen', 'Nama', 'Bagian', 'tahun', 'overall_status_T', 'recent_trend_T',
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
            'Keterangan']]

        return result
    
    def getPRL(self, data):
        result = data[data['overall_status_T'].str.contains('perfect', case=False)]
        return result
    
    def getGRL(self, data):
        result = data[data['overall_status_T'].str.contains('good', case=False)]
        return result
    
    def getNIL(self, data):
        result = data[data['overall_status_T'].str.contains('needs', case=False)]
        return result
    
    def getARL(self, data):
        result = data[data['overall_status_T'].str.contains('risks', case=False)]
        return result
    
    def getRDL(self, data):
        result = data[data['overall_status_T'].str.contains('dismissal', case=False)]
        return result
    
    def getImporvingList(self, data):
        result = data[data['recent_trend_T'].str.contains('improving', case=False)]
        return result
    def getStableList(self, data):
        result = data[data['recent_trend_T'].str.contains('stable', case=False)]
        return result
    def getDecliningList(self, data):
        result = data[data['recent_trend_T'].str.contains('declining', case=False)]
        return result
    
    def AnnualSummary(self, dataframe):
        df = dataframe
        grade_map = self.target_grade_A

        month_cols = [str(i) for i in range(1, 13)]
        annual_avg = df.copy()
        annual_avg['tahun'] = annual_avg['tahun'].astype(np.int64)
        annual_avg[month_cols] = annual_avg[month_cols].apply(lambda col: col.map(grade_map))

        annual_avg['Year_avg'] = annual_avg[['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']].mean(axis=1)
        annual_avg.loc[:, 'nilai_tahunan'] = annual_avg['Year_avg'].apply(self.gradeA)

        annual_avg = annual_avg.fillna('-').round(2)

        result = annual_avg[[
            'No.Absen', 'Nama', 'Bagian', 'tahun',
            'Year_avg', 'nilai_tahunan'
        ]]

        return result


    def SemesterSummary(self, dataframe):
        df = dataframe
        grade_map = self.target_grade_S

        month_cols = [str(i) for i in range(1, 13)]
        semester_avg = df.copy()
        semester_avg['tahun'] = semester_avg['tahun'].astype(np.int64)
        semester_avg[month_cols] = semester_avg[month_cols].apply(lambda col: col.map(grade_map))

        semester_avg['S1_avg'] = semester_avg[['1', '2', '3', '4', '5', '6']].mean(axis=1)
        semester_avg['S2_avg'] = semester_avg[['7', '8', '9', '10', '11', '12']].mean(axis=1)


        semester_avg.loc[:, 'nilai_S1'] = semester_avg['S1_avg'].apply(self.gradeS)
        semester_avg.loc[:, 'nilai_S2'] = semester_avg['S2_avg'].apply(self.gradeS)


        semester_avg = semester_avg.fillna('-').round(2)

        result = semester_avg[[
            'No.Absen', 'Nama', 'Bagian', 'tahun', 
            'S1_avg', 'nilai_S1',
            'S2_avg', 'nilai_S2'
        ]]

        return result

    def QuarterSummary(self, dataframe):
        df = dataframe
        grade_map = self.target_grade_Q

        month_cols = [str(i) for i in range(1, 13)]
        quarter_avg = df.copy()
        quarter_avg['tahun'] = quarter_avg['tahun'].astype(np.int64)
        quarter_avg[month_cols] = quarter_avg[month_cols].apply(lambda col: col.map(grade_map))

        quarter_avg['target_avg_Q1'] = quarter_avg[['1', '2', '3']].mean(axis=1).round(2)
        quarter_avg['target_avg_Q2'] = quarter_avg[['4', '5', '6']].mean(axis=1).round(2)
        quarter_avg['target_avg_Q3'] = quarter_avg[['7', '8', '9']].mean(axis=1).round(2)
        quarter_avg['target_avg_Q4'] = quarter_avg[['10', '11', '12']].mean(axis=1).round(2)

        quarter_avg.loc[:, 'nilai_Target_Q1'] = quarter_avg['target_avg_Q1'].apply(self.gradeQ)
        quarter_avg.loc[:, 'nilai_Target_Q2'] = quarter_avg['target_avg_Q2'].apply(self.gradeQ)
        quarter_avg.loc[:, 'nilai_Target_Q3'] = quarter_avg['target_avg_Q3'].apply(self.gradeQ)
        quarter_avg.loc[:, 'nilai_Target_Q4'] = quarter_avg['target_avg_Q4'].apply(self.gradeQ)

        quarter_avg = quarter_avg.fillna('-')

        result = quarter_avg[[
            'No.Absen', 'Nama', 'Bagian', 'tahun', 
            'target_avg_Q1', 'nilai_Target_Q1',
            'target_avg_Q2', 'nilai_Target_Q2',
            'target_avg_Q3', 'nilai_Target_Q3',
            'target_avg_Q4', 'nilai_Target_Q4'
        ]]

        return result

    def sync(self):
        TarController = TargetController()
        hasFilesA = TarController.checkTargetFiles()
        
        if not hasFilesA:
            print()
            print("WARNING!")
            print("no data available. please insert files in directory below")
            print(self.targetDir)
            print()
            SystemController.wait_for_keypress()
            return
        
        df = pd.DataFrame()
        df =TarController.SetTargetDF()
        return df