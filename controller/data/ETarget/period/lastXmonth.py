from datetime import datetime
from config import ConfigManager
from controller.data.ETarget.TargetStatus import TargetStatus

class TargetXMonth:
    def __init__(self):
        self.expected_columns =  [
            'No.Absen', 'Nama', 'Bagian', 'tahun', 'recent_status_T', 'recent_trend_T', 'Keterangan'
        ] 

        CM = ConfigManager()

        self.perfectCon = CM.config['data']["target-perfect-con-M"]
        self.dismissCon = CM.config['data']["target-dismiss-threshold-M"]
        self.riskCon = CM.config['data']["target-risk-threshold-M"]
        self.warnCon = CM.config['data']["target-warn-threshold-M"]

        self.recentWin = CM.config['data']["target-recent-trend-M"]
        self.XMonth = CM.config['data']["target-X-M"]
        
        self.SETSTATUSGRADE = TargetStatus().setStatusGrade
        return
    
    def getLastXMonthData(self,data):
        df = data.copy()

        current_month = datetime.now().month

        grade_cols = list(range(1, current_month + 1))
        grade_cols = grade_cols[-self.XMonth:]
        grade_cols = [str(col) for col in grade_cols]
        grade_cols = [col for col in grade_cols if col in df.columns]
        conditionType= {
            'perfectCon': self.perfectCon,
            'dismissCon': self.dismissCon,
            'riskCon': self.riskCon,
            'warnCon': self.warnCon,
        }
        df['recent_status_T'] = df[grade_cols].apply(lambda row: self.SETSTATUSGRADE(row.dropna().tolist(), conditionType), axis=1)
        
        result = df[self.expected_columns+grade_cols]
        return result
    