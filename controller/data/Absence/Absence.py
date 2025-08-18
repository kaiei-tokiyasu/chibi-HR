
import pathlib
import pandas as pd
import numpy as np
from utils.lib import lib
from config import ConfigManager
from controller.pathController import pathController
from utils.system import SystemController
from controller.data.Absence.AbsenceController import AbsenceController

class Absence:
    def __init__(self):
        
        #month config
        self.PivotIndexM = ['No.Absen', 'Nama', 'Bagian', 'tahun', 'branch']
        self.PivotColM = 'bulan'
        self.pivotTotalM = 'Total'
        self.pivotGradeM = 'Grade'
        self.PivotPrefixTotalM = 'Total_Absen_B'
        self.PivotPrefixGradeM = 'Nilai_Absen_B'
        self.groupbyM = ['No.Absen', 'Nama', 'branch']
        self.expected_columnsM = [
            'No.Absen', 'Nama', 'Bagian', 'branch', 'tahun', 'overall_status_A', 'recent_trend_A'
        ]
        self.dropDuplicateListM = [{'subset':'No.Absen', 'keep':'last'}]

        #annual config
        self.groupbyA = ['No.Absen', 'Nama', 'Bagian', 'tahun', 'branch']
        self.valTargetToCalA = 'Total'
        self.gradeValColnameA = 'annual_avg'
        self.gradeColnameA = 'nilai_tahunan'
        self.dropDuplicateListA = [{'subset':'No.Absen', 'keep':'last'}]
        self.expected_columnsA = [ 'No.Absen', 'Nama', 'Bagian', 'branch', 'tahun', self.gradeValColnameA, self.gradeColnameA]

        #semester config
        self.monthColtoConvertS = 'bulan'
        self.semesterColName = 'semester' 
        self.copyColS = ['No.Absen', 'Nama', 'Bagian', 'branch', 'tahun', 'bulan', 'Total']
        self.dropColS = 'bulan'
        # tempCol = self.copyColS
        # tempCol = tempCol[:-2]
        # tempCol.append(self.semesterColName)
        self.groupbyS = ['No.Absen', 'Nama', 'Bagian', 'branch', 'tahun', 'semester' ]
        

        self.valTargetToCalS = 'Total'
        self.totalValColnameS = 'total_absence'
        self.avgValColnameS = 'avg_semester'
        self.gradeValColnameS = 'nilai'

        self.fullSemesterColS = ['No.Absen', 'Nama', 'Bagian', 'tahun', 'branch']
        self.fullDataMergeColS = ['No.Absen', 'Nama', 'Bagian', 'tahun', 'branch', 'semester']
        # self.fullSemesterColS.append(self.semesterColName)

        self.fullDataFillS = [
            {
                'col': self.avgValColnameS,
                'val': '-'
            },
            {
                'col': self.gradeValColnameS,
                'val': '#'
            },
            {
                'col': self.totalValColnameS,
                'val': '#'
            }
        ]

        # self.PivotIndexS = ['No.Absen', 'Nama', 'Bagian', 'tahun', 'branch']
        self.PivotIndexS = ['No.Absen', 'Nama', 'Bagian', 'tahun', 'branch']
        self.PivotColS = 'semester'
        self.pivotTotalS = 'Total'
        self.pivotGradeS = 'Grade'
        self.PivotPrefixTotalS = 'Total_Absence_S'
        self.PivotPrefixAvgS = 'avg_S'
        self.PivotPrefixGradeS = 'Nilai_S'

        self.resultgroupbyS = ['No.Absen', 'Nama']
        self.dropDuplicateListS = [{'subset':'No.Absen', 'keep':'last'}]
        self.expected_columnsS = [
            'No.Absen', 'Nama', 'Bagian', 'tahun', 'branch',
            'avg_S1', 'Nilai_S1',
            'avg_S2', 'Nilai_S2',
            'Total_Absence_S1', 'Total_Absence_S2'
        ]



        self.paths = pathController().paths
        self.input_path = self.paths['input_path']
        self.absenceDir = pathlib.Path(self.input_path+"\\ABSENCE")



        CM = ConfigManager()

        self.perfectCon = CM.config['data']["absence-perfect-con-M"]
        self.dismissCon = CM.config['data']["absence-dismiss-threshold-M"]
        self.riskCon = CM.config['data']["absence-risk-threshold-M"]
        self.warnCon = CM.config['data']["absence-warn-threshold-M"]

        self.recentWin = CM.config['data']["absence-recent-trend-M"]

        self.absence_grade_M = CM.config['data']['absence-M']
        self.absence_grade_Q = CM.config['data']['absence-Q']
        self.absence_grade_S = CM.config['data']['absence-Semester']
        self.absence_grade_A = CM.config['data']['absence-Annual']
    
    def setGrade(self, avg, gradeType):
        
        if not isinstance(avg, (int, float)):
            return '?!'
        elif avg <= gradeType['A']:
            return 'A'
        elif avg <= gradeType['B']:
            return 'B'
        elif avg <= gradeType['C']:
            return 'C'
        elif avg <= gradeType['D']:
            return 'D'
        elif avg <= gradeType['E']:
            return 'E'
        else:
            return '?!'
    
    def gradeM(self, avg):
        grade = self.absence_grade_M
        return self.setGrade(avg=avg, gradeType=grade)

    def gradeQ(self, avg):
        grade = self.absence_grade_Q
        return self.setGrade(avg=avg, gradeType=grade)
        
    def gradeS(self, avg):
        grade = self.absence_grade_S
        return self.setGrade(avg=avg, gradeType=grade)

    def gradeA(self, avg):
        grade = self.absence_grade_A
        return self.setGrade(avg=avg, gradeType=grade)
    
    def StatusGradeCal(self, grades):
        valid_grades = []
        for i, g in enumerate(grades):
            if isinstance(g, str):
                grade = g.strip().upper()
                if grade in self.absence_grade_M:
                    valid_grades.append(grade)
                else:
                    continue;
                    # print(f"Ignored invalid grade at index {i}: '{g}' normalized as '{grade}'")
            else:
                continue;
                # print(f"Ignored non-string grade at index {i}: {g}")

        # print(f"All input grades: {grades}")
        # print(f"Valid grades after filtering: {valid_grades}")
        # print(f"Distinct grades found: {set(valid_grades)}")

        grade_counts = {}
        for g in valid_grades:
            grade_counts[g] = grade_counts.get(g, 0) + 1
        # print(f"Grade counts: {grade_counts}")

        if not valid_grades:
            overall_status = "no data"

        elif valid_grades and all(g in self.perfectCon for g in valid_grades):
            # print("Perfect condition matched")
            overall_status = "S Perfect Record"

        elif all(grade_counts.get(k, 0) >= v for k, v in self.dismissCon.items()):
            overall_status = "Recommended for Dismissal"

        elif all(grade_counts.get(k, 0) >= v for k, v in self.riskCon.items()):
            overall_status = "At Risk"

        elif all(grade_counts.get(k, 0) >= v for k, v in self.warnCon.items()):
            overall_status = "Needs Improvement"

        else:
            overall_status = "Good Record"

        recent_grades = valid_grades[-self.recentWin:]
        recent_scores = [self.absence_grade_M[g] for g in recent_grades]
        # print(f"Recent grades (last {self.recentWin}): {recent_grades}")
        # print(f"Recent scores: {recent_scores}")

        if len(recent_scores) < 2:
            recent_trend = "stable"
        else:
            if recent_scores[-2] > recent_scores[-1]:
                recent_trend = "improving"
            elif recent_scores[-2] < recent_scores[-1]:
                recent_trend = "declining"
            else:
                recent_trend = "stable"

        # print(f"Final Status: {overall_status}, Trend: {recent_trend}")

        return {
            "overall_status_A": overall_status,
            "recent_trend_A": recent_trend
        }

    def setStatus(self, data):
        grade_cols = [col for col in data.columns if col.startswith('Nilai_Absen_B')]
        
        data[['overall_status_A', 'recent_trend_A']] = data.apply(
            lambda row: pd.Series(
                self.StatusGradeCal([row[col] for col in grade_cols])
            ), axis=1)
        return data
    
    def MonthlySummary(self, dataframe):
        df = dataframe

        monthly_df = df.copy()
        monthly_df[self.pivotGradeM] = monthly_df[self.pivotTotalM].apply(self.gradeM)

        pivotCols = self.PivotColM
        total_pivot = monthly_df.pivot(index=self.PivotIndexM,
                                      columns=pivotCols,
                                      values=self.pivotTotalM).add_prefix(self.PivotPrefixTotalM)
        
        grade_pivot = monthly_df.pivot(index=self.PivotIndexM,
                                      columns=pivotCols,
                                      values=self.pivotGradeM).add_prefix(self.PivotPrefixGradeM)
        
        result = pd.concat([total_pivot, grade_pivot], axis=1)

        result = result.reset_index()

        result = ( 
            result.groupby(self.groupbyM, as_index=False)
                  .agg(lambda x: x.ffill().bfill().iloc[0]) )
        result = result.infer_objects(copy=False)

        for key in self.dropDuplicateListM:
            result = result.drop_duplicates(subset=key['subset'], keep=key['keep'])
        
        result = result.reset_index(drop=True)

        result = self.setStatus(result)
        
        expected_columns = self.expected_columnsM

        for i in range(1, 13):
            expected_columns.append(f'{self.PivotPrefixTotalM}{i}')
            expected_columns.append(f'{self.PivotPrefixGradeM}{i}')
        
        existing_columns = [col for col in expected_columns if col in result.columns]

        result = result[existing_columns]
        
        return result
    
    def getPRL(self, data):
        result = data[data['overall_status_A'].str.contains('perfect', case=False)]
        return result
    
    def getGRL(self, data):
        result = data[data['overall_status_A'].str.contains('good', case=False)]
        return result
    
    def getNIL(self, data):
        result = data[data['overall_status_A'].str.contains('needs', case=False)]
        return result
    
    def getARL(self, data):
        result = data[data['overall_status_A'].str.contains('risks', case=False)]
        return result
    
    def getRDL(self, data):
        result = data[data['overall_status_A'].str.contains('dismissal', case=False)]
        return result
    
    def getImporvingList(self, data):
        result = data[data['recent_trend_A'].str.contains('improving', case=False)]
        return result
    
    def getStableList(self, data):
        result = data[data['recent_trend_A'].str.contains('stable', case=False)]
        return result
    
    def getDecliningList(self, data):
        result = data[data['recent_trend_A'].str.contains('declining', case=False)]
        return result
    
    def AnnualSummary(self, dataframe):
        df = dataframe.copy()
        annual_avg = df.groupby(self.groupbyA)
        valColname = self.gradeValColnameA
        annual_avg[valColname] = annual_avg[self.valTargetToCalA].mean().reset_index()
        annual_avg[valColname] = annual_avg[valColname].round(2)

        annual_avg[self.gradeColnameA] = annual_avg[valColname].apply(self.gradeA)
        
        result = annual_avg
        
        for key in self.dropDuplicateListM:
            result = result.drop_duplicates(subset=key['subset'], keep=key['keep'])

        result = result[self.expected_columnsA]
        return result
        
    def SemesterSummary(self, dataframe):
        df = dataframe[self.copyColS].copy()

        df[self.semesterColName] = df[self.monthColtoConvertS].apply(lambda m: 1 if m <= 6 else 2)

        totalValColName = self.totalValColnameS
        avgValColName = self.avgValColnameS

        total_absence = df.copy().drop(self.dropColS, axis=1)
        

        semester_avg = df.copy().drop(self.dropColS, axis=1)
        
        total_absence[totalValColName] = (
            total_absence.groupby(self.groupbyS)[self.valTargetToCalS]
            .transform("sum")
            .astype(int)
        )
        
        semester_avg[avgValColName] = (
            semester_avg.groupby(self.groupbyS)[self.valTargetToCalS]
            .transform("mean")
            .astype(float)
        )
        semester_avg[self.gradeValColnameS] = (
            semester_avg.groupby(self.groupbyS)[self.valTargetToCalS]
            .transform("mean")
            .astype(float)
            .apply(self.gradeS)
        )
        
        full_semester = (
            df[self.fullSemesterColS]
            .drop_duplicates()
            .assign(dummy=1)
            .merge(pd.DataFrame({self.semesterColName: [1,2], 'dummy':1}), on='dummy')
            .drop(columns='dummy')
        )
        full_data = pd.merge(full_semester, semester_avg, on=self.fullDataMergeColS, how='left')

        full_data = pd.merge(full_data, total_absence, on=self.fullDataMergeColS, how='left')

        full_data[avgValColName] = full_data[avgValColName].round(2)

        for key in self.fullDataFillS:
            full_data[key['col']] = full_data[key['col']].fillna(key['val'])


        pivotIndex = self.PivotIndexS
        pivotCols = self.PivotColS

        total_pivot = full_data.pivot_table(index=pivotIndex,
                                      columns=pivotCols,
                                      values=totalValColName,
                                      aggfunc='max'
                                      ).add_prefix(self.PivotPrefixTotalS)
        
        avg_pivot = full_data.pivot_table(index=pivotIndex,
                                      columns=pivotCols,
                                      values=avgValColName,
                                      aggfunc='first'
                                      ).add_prefix(self.PivotPrefixAvgS)
        
        grade_pivot = full_data.pivot_table(index=pivotIndex,
                                      columns=pivotCols,
                                      values=self.gradeValColnameS,
                                      aggfunc='first'
                                      ).add_prefix(self.PivotPrefixGradeS)

        result = pd.concat([avg_pivot, grade_pivot, total_pivot], axis=1)
        result = result.reset_index()
        
        result = ( 
            result.groupby(self.resultgroupbyS, as_index=False)
                  .agg(lambda x: x.ffill().bfill().iloc[0]) )
        result = result.infer_objects(copy=False)

        for key in self.dropDuplicateListM:
            result = result.drop_duplicates(subset=key['subset'], keep=key['keep'])

        print(result)
        result = result[self.expected_columnsS]
        return result

    def QuarterSummary(self, dataframe):
        df = dataframe.copy()
        df['kuartal'] = ((df['bulan'] - 1) // 3) + 1

        total_absence = df.groupby(['No.Absen', 'Nama', 'Bagian', 'tahun', 'kuartal'])['Total'].sum().reset_index()
        print(total_absence)
        total_absence.rename(columns={'Total': 'total_absence'}, inplace=True)
        total_absence['total_absence'] = total_absence['total_absence']

        quarter_avg = df.groupby(['No.Absen', 'Nama', 'Bagian', 'tahun', 'kuartal'])['Total'].mean().reset_index()
        quarter_avg.rename(columns={'Total': 'avg_absence'}, inplace=True)
        
        quarter_avg['nilai'] = quarter_avg['avg_absence'].apply(self.gradeQ)
        
        full_quarters =(
            df[['No.Absen', 'Nama', 'Bagian', 'tahun']]
            .drop_duplicates()
            .assign(dummy=1)
            .merge(pd.DataFrame({'kuartal': [1,2,3,4], 'dummy':1}), on='dummy')
            .drop(columns='dummy')
        )

        full_data = pd.merge(full_quarters, quarter_avg, on=['No.Absen', 'Nama', 'Bagian', 'tahun', 'kuartal'], how='left')
        full_data = pd.merge(full_data, total_absence, on=['No.Absen', 'Nama', 'Bagian', 'tahun', 'kuartal'], how='left')        

        full_data['avg_absence'] = full_data['avg_absence'].round(2)
        full_data['avg_absence'] = full_data['avg_absence'].fillna('-')
        full_data['nilai'] = full_data['nilai'].fillna('#')

        
        full_data['total_absence'] = full_data['total_absence'].fillna('-')
        
        total_pivot = full_data.pivot(index=['No.Absen', 'Nama', 'Bagian', 'tahun'],
                                      columns='kuartal',
                                      values='total_absence').add_prefix('Total_Absen_Q')
        
        avg_pivot = full_data.pivot(index=['No.Absen', 'Nama', 'Bagian', 'tahun'],
                                      columns='kuartal',
                                      values='avg_absence').add_prefix('absen_avg_Q')
        
        grade_pivot = full_data.pivot(index=['No.Absen', 'Nama', 'Bagian', 'tahun'],
                                      columns='kuartal',
                                      values='nilai').add_prefix('nilai_absen_Q')
        

        result = pd.concat([avg_pivot, grade_pivot, total_pivot], axis=1)
        result = result.reset_index()

        result = ( 
            result.groupby(['No.Absen', 'Nama'], as_index=False)
                  .agg(lambda x: x.ffill().bfill().iloc[0]) )
        result = result.infer_objects(copy=False)
        
        result = result.drop_duplicates(subset='No.Absen', keep='last').reset_index(drop=True)
        
        result = result[[
            'No.Absen', 'Nama', 'Bagian', 'tahun',
            'absen_avg_Q1', 'nilai_absen_Q1',
            'absen_avg_Q2', 'nilai_absen_Q2',
            'absen_avg_Q3', 'nilai_absen_Q3',
            'absen_avg_Q4', 'nilai_absen_Q4',
            'Total_Absen_Q1', 'Total_Absen_Q2', 'Total_Absen_Q3', 'Total_Absen_Q4'
            ]]
        return result

    def sync(self):
        AbsController = AbsenceController()
        hasFilesA = AbsController.checkAbsenceFiles()
        
        if not hasFilesA:
            print()
            print("WARNING!")
            print("no data available. please insert files in directory below")
            print(self.absenceDir)
            print()
            SystemController.wait_for_keypress()
            return
        
        df = pd.DataFrame()
        df = AbsController.SetAbsenceDF()
        
        return df
    