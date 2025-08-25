import numpy as np
from config import ConfigManager
from controller.data.ETarget.TargetGrading import TargetGrading


class TargetSemester:
    def __init__ (self):
        self.yearColname = 'tahun'
        self.s1AvgColname = 'S1_avg'
        self.s2AvgColname = 'S2_avg'
        self.s1Months = ['1', '2', '3', '4', '5', '6']
        self.s2Months =['7', '8', '9', '10', '11', '12']

        self.s1GradeColname = 'nilai_S1'
        self.s2GradeColname = 'nilai_S2'

        self.expected_columns = [
            'No.Absen', 'Nama', 'Bagian', 'tahun', 
            'S1_avg', 'nilai_S1',
            'S2_avg', 'nilai_S2'
        ]
        CM = ConfigManager()
        self.target_grade_S = CM.config['data']['target-Semester']
        
        self.SETGRADE = TargetGrading().gradeS
        return
    
    def GetSummary(self, dataframe):
        df = dataframe
        grade_map = self.target_grade_S

        month_cols = [str(i) for i in range(1, 13)]
        semester_avg = df.copy()
        semester_avg[self.yearColname] = semester_avg[self.yearColname].astype(np.int64)
        semester_avg[month_cols] = semester_avg[month_cols].apply(lambda col: col.map(grade_map))

        semester_avg[self.s1AvgColname] = semester_avg[self.s1Months].mean(axis=1)
        semester_avg[self.s2AvgColname] = semester_avg[self.s2Months].mean(axis=1)


        semester_avg.loc[:, self.s1GradeColname] = semester_avg[self.s1AvgColname].apply(self.SETGRADE)
        semester_avg.loc[:, self.s2GradeColname] = semester_avg[self.s2AvgColname].apply(self.SETGRADE)

        semester_avg = semester_avg.fillna('-').round(2)

        result = semester_avg[self.expected_columns]

        return result
