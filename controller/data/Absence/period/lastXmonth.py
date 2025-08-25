from datetime import datetime
from config import ConfigManager

from controller.data.Absence.AbsenceStatus import AbsenceStatus

class AbsenceXMonth:
    def __init__(self):
        self.gradeCols = 'Nilai_Absen_B'
        self.expected_columns = [
            'No.Absen', 'Nama', 'Bagian', 'branch', 'tahun', 'recent_status_A', 'recent_trend_A'
        ]

        CM = ConfigManager()

        self.perfectCon = CM.config['data']["absence-perfect-con-M"]
        self.dismissCon = CM.config['data']["absence-dismiss-threshold-M"]
        self.riskCon = CM.config['data']["absence-risk-threshold-M"]
        self.warnCon = CM.config['data']["absence-warn-threshold-M"]
        
        self.XMonth = CM.config['data']["absence-X-M"]
        
        self.SETSTATUSGRADE = AbsenceStatus().setStatusGrade
        return
    
    def getLastXMonthData(self,data):
        df = data.copy()
        
        current_month = datetime.now().month
        recent_n = self.XMonth
        grade_cols = [col for col in df.columns if col.startswith(self.gradeCols)]
        cols_with_months = [(col, int(col.split('B')[-1])) for col in grade_cols]
        last_n_months = [
            (col, m) for col, m in cols_with_months
            if 0 <= (current_month - m) < recent_n
        ]
        last_n_months_sorted = sorted(last_n_months, key=lambda x: x[1])
        grade_cols = [col for col, _ in last_n_months_sorted]
                
        conditionType= {
            'perfectCon': self.perfectCon,
            'dismissCon': self.dismissCon,
            'riskCon': self.riskCon,
            'warnCon': self.warnCon,
        }

        df['recent_status_A'] = df[grade_cols].apply(lambda row: self.SETSTATUSGRADE(row.dropna().tolist(), conditionType), axis=1)
        
        result = df[self.expected_columns+grade_cols]
        return result