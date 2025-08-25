import numpy as np
import pandas as pd

from config import ConfigManager
from controller.data.ETarget.TargetStatus import TargetStatus

class TargetMonthly:
    def __init__(self):
        #month config
        self.yearColname = 'tahun'
        self.expected_columns = ['No.Absen', 'Nama', 'Bagian', 'tahun', 'overall_status_T', 'recent_trend_T',
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
            'Keterangan']
        
        self.SETSTATUSGRADECAL = TargetStatus().StatusGradeCal

        CM = ConfigManager()

        self.perfectConA= CM.config['data']["target-perfect-con-A"]
        self.dismissConA = CM.config['data']["target-dismiss-threshold-A"]
        self.riskConA = CM.config['data']["target-risk-threshold-A"]
        self.warnConA = CM.config['data']["target-warn-threshold-A"]

        self.target_grade_M = CM.config['data']['target-M']
        return
    
    def setStatus(self, data):
        grade_cols = [col for col in data.columns if col.isdigit() and 1 <= int(col) <= 12]
        conditionType= {
            'perfectCon': self.perfectConA,
            'dismissCon': self.dismissConA,
            'riskCon': self.riskConA,
            'warnCon': self.warnConA
        }
        data[['overall_status_T', 'recent_trend_T']] = data.apply(
            lambda row: pd.Series(
                self.SETSTATUSGRADECAL([row[col] for col in grade_cols], gradeThreshold=self.target_grade_M, conditionType=conditionType)
            ), axis=1)
        return data
    
    def GetSummary(self, dataframe):
        df = dataframe
        
        monthly = df.copy()
        monthly[self.yearColname] = monthly[self.yearColname].astype(np.int64)
        monthly =  self.setStatus(monthly)

        result = monthly[self.expected_columns]

        return result
