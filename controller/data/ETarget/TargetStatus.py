from config import ConfigManager

class TargetStatus:
    def __init__(self):
        self.perfect_msg = "S Perfect Record"
        self.good_msg = "Good Record"
        self.improve_msg = "Needs Improvement"
        self.risk_msg = "At Risk"
        self.dismiss_msg = "Recommended for Dismissal"
        self.no_data_msg =  "no data"

        self.tr_improve_msg = "improving"
        self.tr_decline_msg = "declining"
        self.tr_stable_msg = "stable"

        CM = ConfigManager()
        self.absence_grade_M = CM.config['data']['absence-M']
        self.recentWin = CM.config['data']["target-recent-trend-M"]
        return

    def setStatusGrade(self, valid_grades, conditionType):
        grade_counts = {}
        for g in valid_grades:
            grade_counts[g] = grade_counts.get(g, 0) + 1

        perfectCon = conditionType['perfectCon']

        if not valid_grades:
            status = "no data"
        elif valid_grades and all(g ==  perfectCon for g in valid_grades):
            status = self.perfect_msg
        elif all(grade_counts.get(k, 0) >= v for k, v in conditionType['dismissCon'].items()):
            status = self.dismiss_msg
        elif all(grade_counts.get(k, 0) >= v for k, v in conditionType['riskCon'].items()):
            status = self.risk_msg
        elif all(grade_counts.get(k, 0) >= v for k, v in conditionType['warnCon'].items()):
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
            recent_trend = "stable"  # Not enough data
        elif recent_grades[-2] < recent_grades[-1]:
            recent_trend = "improving"
        elif recent_grades[-2] > recent_grades[-1]:
            recent_trend = "declining"
        else:
            recent_trend = "stable"

        return {
            "overall_status_T": overall_status,
            "recent_trend_T": recent_trend
        }
