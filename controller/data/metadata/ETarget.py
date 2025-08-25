import pandas as pd
from config import ConfigManager

class metadataTarget:
    def __init__(self):
        CM = ConfigManager()

        self.perfectCon = CM.config['data']["target-perfect-con-M"]
        self.dismissCon = CM.config['data']["target-dismiss-threshold-M"]
        self.riskCon = CM.config['data']["target-risk-threshold-M"]
        self.warnCon = CM.config['data']["target-warn-threshold-M"]

        self.recentWin = CM.config['data']["target-recent-trend-M"]

        self.target_grade_M = CM.config['data']['target-M']
        
        return
    def getMetaDataPD(self):
        target_info = {
            'perfect_con': self.perfectCon,
            'dismiss_threshold': self.dismissCon,
            'risk_threshold': self.riskCon,
            'warn_threshold': self.warnCon,
            'recent_trend': self.recentWin,
            'scores': self.target_grade_M
        }
        target_df = pd.DataFrame(list(target_info['scores'].items()), columns=['Grade', 'Count'])
        target_df.insert(0, 'Category', 'Target')
        target_meta = pd.DataFrame({
            'Metric': ['Perfect Con', 'Dismiss Threshold', 'Risk Threshold', 'Warn Threshold', 'Recent Trend'],
            'Value': [
                    target_info['perfect_con'],
                    str(target_info['dismiss_threshold']),
                    str(target_info['risk_threshold']),
                    str(target_info['warn_threshold']),
                    target_info['recent_trend']
                ]
        })
        return target_df, target_meta

    