import numpy as np
from config import ConfigManager
from controller.data.ETarget.TargetGrading import TargetGrading

from controller.data.ETarget.TargetStatus import TargetStatus

class TargetAnnual:
    def __init__(self):
        # annual config
        self.yearColname = 'tahun'
        self.yearAvgColname = 'Year_avg'
        self.meanColTarget = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
        self.yearGradeColname = 'nilai_tahunan' 

        self.expected_columns = [
            'No.Absen', 'Nama', 'Bagian', 'tahun',
            'Year_avg', 'nilai_tahunan'
        ]

        CM = ConfigManager()
        self.target_grade_A = CM.config['data']['target-Annual']
        
        self.SETGRADE = TargetGrading().gradeA

        return
    
    def GetSummary(self, dataframe):
        df = dataframe
        grade_map = self.target_grade_A

        month_cols = [str(i) for i in range(1, 13)]
        annual_avg = df.copy()
        annual_avg[self.yearColname] = annual_avg[self.yearColname].astype(np.int64)
        annual_avg[month_cols] = annual_avg[month_cols].apply(lambda col: col.map(grade_map))

        annual_avg[self.yearAvgColname] = annual_avg[self.meanColTarget].mean(axis=1)
        annual_avg.loc[:, self.yearGradeColname] = annual_avg[self.yearAvgColname].apply(self.SETGRADE)

        annual_avg = annual_avg.fillna('-').round(2)

        result = annual_avg[self.expected_columns]

        return result
