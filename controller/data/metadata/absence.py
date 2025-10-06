import pandas as pd
from config import ConfigManager

class metadataAbsence:
    def __init__(self):
        CM = ConfigManager()

        self.perfect_msg = CM.config['row-msg']['perfect-msg']
        self.good_msg = CM.config['row-msg']['good-msg']
        self.improve_msg = CM.config['row-msg']['improve-msg']
        self.risk_msg = CM.config['row-msg']['risk-msg']
        self.dismiss_msg = CM.config['row-msg']['dismiss-msg']
        self.no_data_msg =  CM.config['row-msg']['no-data']

        self.perfectCon = CM.config['data']["absence-perfect-con-M"]
        self.dismissCon = CM.config['data']["absence-dismiss-threshold-M"]
        self.riskCon = CM.config['data']["absence-risk-threshold-M"]
        self.warnCon = CM.config['data']["absence-warn-threshold-M"]

        self.recentWin = CM.config['data']["absence-recent-trend-M"]

        self.absence_grade_M = CM.config['data']['absence-M']

        return
    def getMetaDataPD(self):
        absence_info = {
            self.perfect_msg : self.perfectCon,
            self.dismiss_msg  : self.dismissCon,
            self.risk_msg: self.riskCon,
            self.improve_msg : self.warnCon,
            'recent_trend': self.recentWin,
            'scores': self.absence_grade_M
        }
        absence_df = pd.DataFrame(list(absence_info['scores'].items()), columns=['Grade', 'Count'])
        absence_df.insert(0, 'Category', 'Absence')
        absence_meta = pd.DataFrame({
            'Metric': [self.perfect_msg, self.dismiss_msg , self.risk_msg, self.improve_msg, 'Recent Trend'],
            'Value': [
                    absence_info[self.perfect_msg],
                    str(absence_info[self.dismiss_msg]),
                    str(absence_info[self.risk_msg]),
                    str(absence_info[self.improve_msg]),
                    absence_info['recent_trend']
                ]
        })
        return absence_df, absence_meta
