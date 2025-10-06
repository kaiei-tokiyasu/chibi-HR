from config import ConfigManager

class TargetStatus:
    def __init__(self):
        CM = ConfigManager()
        self.perfect_msg = CM.config['row-msg']['perfect-msg']
        self.good_msg = CM.config['row-msg']['good-msg']
        self.improve_msg = CM.config['row-msg']['improve-msg']
        self.risk_msg = CM.config['row-msg']['risk-msg']
        self.dismiss_msg = CM.config['row-msg']['dismiss-msg']
        self.no_data_msg =  CM.config['row-msg']['no-data']

        self.tr_improve_msg = CM.config['row-msg']['trend-improve-msg']
        self.tr_decline_msg = CM.config['row-msg']['trend-decline-msg']
        self.tr_stable_msg = CM.config['row-msg']['trend-stable-msg']

        self.absence_grade_M = CM.config['data']['absence-M']
        self.recentWin = CM.config['data']["target-recent-trend-M"]
        return

    def setStatusGrade(self, valid_grades, conditionType):
        grade_counts = {}
        for g in valid_grades:
            grade_counts[g] = grade_counts.get(g, 0) + 1

        perfectCon = conditionType['perfectCon']

        if not valid_grades:
            status = self.no_data_msg
        elif valid_grades and all(g ==  perfectCon for g in valid_grades):
            status = self.perfect_msg
        elif any(grade_counts.get(k, 0) >= v for k, v in conditionType['dismissCon'].items()):
            status = self.dismiss_msg
        elif any(grade_counts.get(k, 0) >= v for k, v in conditionType['riskCon'].items()):
            status = self.risk_msg
        elif any(grade_counts.get(k, 0) >= v for k, v in conditionType['warnCon'].items()):
            status = self.improve_msg
        else:
            status = self.good_msg
        return status

    def StatusGradeCal (self, grades, gradeThreshold, conditionType):
        grade_scale = gradeThreshold
        valid_grades = [g for g in grades if isinstance(g, str) and g in grade_scale and g != '#' and g != '-' and g != 'X']

        overall_status = self.setStatusGrade(valid_grades, conditionType)
        recent_grades = [grade_scale[g.upper()] for g in valid_grades[-self.recentWin:]]

        if len(recent_grades) < self.recentWin:
            recent_trend = self.tr_stable_msg
        elif recent_grades[-2] < recent_grades[-1]:
            recent_trend = self.tr_improve_msg
        elif recent_grades[-2] > recent_grades[-1]:
            recent_trend = self.tr_decline_msg
        else:
            recent_trend = self.tr_stable_msg

        return {
            "overall_status_T": overall_status,
            "recent_trend_T": recent_trend
        }
