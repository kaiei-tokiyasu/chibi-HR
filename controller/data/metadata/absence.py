import pandas as pd
from config import ConfigManager

class metadataAbsence:
    def __init__(self):
        CM = ConfigManager()

        self.perfectCon = CM.config['data']["absence-perfect-con-M"]
        self.dismissCon = CM.config['data']["absence-dismiss-threshold-M"]
        self.riskCon = CM.config['data']["absence-risk-threshold-M"]
        self.warnCon = CM.config['data']["absence-warn-threshold-M"]

        self.recentWin = CM.config['data']["absence-recent-trend-M"]

        self.absence_grade_M = CM.config['data']['absence-M']
        
        return
    def getMetaDataPD(self):
        absence_info = {
            'perfect_con': self.perfectCon,
            'dismiss_threshold': self.dismissCon,
            'risk_threshold': self.riskCon,
            'warn_threshold': self.warnCon,
            'recent_trend': self.recentWin,
            'scores': self.absence_grade_M
        }
        absence_df = pd.DataFrame(list(absence_info['scores'].items()), columns=['Grade', 'Count'])
        absence_df.insert(0, 'Category', 'Absence')
        absence_meta = pd.DataFrame({
            'Metric': ['Perfect Con', 'Dismiss Threshold', 'Risk Threshold', 'Warn Threshold', 'Recent Trend'],
            'Value': [
                    absence_info['perfect_con'],
                    str(absence_info['dismiss_threshold']),
                    str(absence_info['risk_threshold']),
                    str(absence_info['warn_threshold']),
                    absence_info['recent_trend']
                ]
        })
        return absence_df, absence_meta

    