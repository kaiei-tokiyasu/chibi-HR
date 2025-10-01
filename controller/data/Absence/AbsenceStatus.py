from config import ConfigManager

class AbsenceStatus:
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
        self.recentWin = CM.config['data']["absence-recent-trend-M"]

        return

    def setStatusGrade(self, valid_grades, conditionType):
        grade_counts = {}
        for g in valid_grades:
            grade_counts[g] = grade_counts.get(g, 0) + 1

        perfectCon = conditionType['perfectCon']

        if not valid_grades:
            status = self.no_data_msg
        elif valid_grades and all(g == perfectCon for g in valid_grades):
            # print("Perfect condition matched")
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

    def StatusGradeCal(self, grades, gradeThreshold, conditionType):
        valid_grades = []
        for i, g in enumerate(grades):
            if isinstance(g, str):
                grade = g.strip().upper()
                if grade in gradeThreshold:
                    valid_grades.append(grade)
                else:
                    continue;
                    # print(f"Ignored invalid grade at index {i}: '{g}' normalized as '{grade}'")
            else:
                continue;
                # print(f"Ignored non-string grade at index {i}: {g}")

        # print(f"All input grades: {grades}")
        # print(f"Valid grades after filtering: {valid_grades}")
        # print(f"Distinct grades found: {set(valid_grades)}")

        # print(f"Grade counts: {grade_counts}")

        overall_status = self.setStatusGrade(valid_grades, conditionType)
        recent_grades = valid_grades[-self.recentWin:]
        recent_scores = [self.absence_grade_M[g] for g in recent_grades]
        # print(f"Recent grades (last {self.recentWin}): {recent_grades}")
        # print(f"Recent scores: {recent_scores}")

        if len(recent_scores) < 2:
            recent_trend = self.tr_stable_msg
        else:
            if recent_scores[-2] > recent_scores[-1]:
                recent_trend = self.tr_improve_msg
            elif recent_scores[-2] < recent_scores[-1]:
                recent_trend = self.tr_decline_msg
            else:
                recent_trend = self.tr_stable_msg

        # print(f"Final Status: {overall_status}, Trend: {recent_trend}")

        return {
            "overall_status_A": overall_status,
            "recent_trend_A": recent_trend
        }
