from config import ConfigManager

class TargetGrading:
    def __init__(self):
        CM = ConfigManager()

        self.target_grade_M = CM.config['data']['target-M']
        self.target_grade_Q = CM.config['data']['target-Q']
        self.target_grade_S = CM.config['data']['target-Semester']
        self.target_grade_A = CM.config['data']['target-Annual']
        return
    
    def setGrade(self, avg, gradeType):
        if avg >= gradeType['A']:
            return 'A'
        elif avg >= gradeType['B'] and avg < gradeType['A']:
            return 'B'
        elif avg >= gradeType['C'] and avg < gradeType['B']:
            return 'C'
        elif avg >= gradeType['D'] and avg < gradeType['C']:
            return 'D'
        elif avg >= gradeType['E'] and avg < gradeType['D']:
            return 'E'
        elif avg >= gradeType['F'] and avg < gradeType['E']:
            return 'F'
        else:
            return '?!no-data'
        
    def gradeQ(self, avg):
        grade = self.target_grade_Q
        return self.setGrade(avg=avg, gradeType=grade)
    
    def gradeS(self, avg):
        grade = self.target_grade_S
        return self.setGrade(avg=avg, gradeType=grade)
    
    def gradeA(self, avg):
        grade = self.target_grade_A
        return self.setGrade(avg=avg, gradeType=grade)