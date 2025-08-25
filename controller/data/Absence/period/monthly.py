import pandas as pd
from config import ConfigManager

from controller.data.Absence.AbsenceGrading import AbsenceGrading
from controller.data.Absence.AbsenceStatus import AbsenceStatus

class AbsenceMonthly:
    def __init__(self):
        #montly config
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
        
        self.SETGRADE = AbsenceGrading().gradeM
        self.SETSTATUSGRADECAL = AbsenceStatus().StatusGradeCal

        CM = ConfigManager()
        self.perfectConA = CM.config['data']["absence-perfect-con-A"]
        self.dismissConA = CM.config['data']["absence-dismiss-threshold-A"]
        self.riskConA = CM.config['data']["absence-risk-threshold-A"]
        self.warnConA = CM.config['data']["absence-warn-threshold-A"]
        
        self.absence_grade_M = CM.config['data']['absence-M']
        return
    def setStatus(self, data):
        grade_cols = [col for col in data.columns if col.startswith('Nilai_Absen_B')]
        conditionType= {
            'perfectCon': self.perfectConA,
            'dismissCon': self.dismissConA,
            'riskCon': self.riskConA,
            'warnCon': self.warnConA
        }
        data[['overall_status_A', 'recent_trend_A']] = data.apply(
            lambda row: pd.Series(
                self.SETSTATUSGRADECAL([row[col] for col in grade_cols], gradeThreshold=self.absence_grade_M, conditionType=conditionType)
            ), axis=1)
        return data
    
    def GetSummary(self, dataframe):
        df = dataframe

        monthly_df = df.copy()
        monthly_df[self.pivotGradeM] = monthly_df[self.pivotTotalM].apply(self.SETGRADE)

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

    