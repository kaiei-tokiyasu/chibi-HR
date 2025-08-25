import numpy as np
from config import ConfigManager
from controller.data.ETarget.TargetGrading import TargetGrading


class TargetQuarter:
    def __init__(self):
        self.yearColname = 'tahun'
        self.targetColname = "target_avg_Q"
        self.gradeColname = "nilai_Target_Q"
        self.quarters = {
            '1': ['1', '2', '3'],
            '2': ['4', '5', '6'],
            '3': ['7', '8', '9'],
            '4': ['10', '11', '12']
        }
        self.expected_columns = [
            'No.Absen', 'Nama', 'Bagian', 'tahun', 
            'target_avg_Q1', 'nilai_Target_Q1',
            'target_avg_Q2', 'nilai_Target_Q2',
            'target_avg_Q3', 'nilai_Target_Q3',
            'target_avg_Q4', 'nilai_Target_Q4'
        ]

        CM = ConfigManager()
        self.target_grade_Q = CM.config['data']['target-Q']

        self.SETGRADE = TargetGrading().gradeQ

        
        return
    
    def GetSummary(self, dataframe):
        df = dataframe
        grade_map = self.target_grade_Q

        month_cols = [str(i) for i in range(1, 13)]
        quarter_avg = df.copy()
        quarter_avg[self.yearColname] = quarter_avg[self.yearColname].astype(np.int64)
        quarter_avg[month_cols] = quarter_avg[month_cols].apply(lambda col: col.map(grade_map))

        for q, months in self.quarters.items():
            avg_col = f'{self.targetColname}{q}'
            grade_col = f'{self.gradeColname}{q}'
            
            quarter_avg[avg_col] = quarter_avg[months].mean(axis=1).round(2)
            quarter_avg[grade_col] = quarter_avg[avg_col].apply(self.SETGRADE)

        quarter_avg = quarter_avg.fillna('-')

        result = quarter_avg[self.expected_columns]

        return result