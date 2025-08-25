from config import ConfigManager

class AbsenceGrading:
    def __init__(self):
        CM = ConfigManager()
        self.absence_grade_M = CM.config['data']['absence-M']
        self.absence_grade_Q = CM.config['data']['absence-Q']
        self.absence_grade_S = CM.config['data']['absence-Semester']
        self.absence_grade_A = CM.config['data']['absence-Annual']
        return
    
    def setGrade(self, avg, gradeType): 
        if not isinstance(avg, (int, float)):
            return '?!'
        elif avg <= gradeType['A']:
            return 'A'
        elif avg <= gradeType['B']:
            return 'B'
        elif avg <= gradeType['C']:
            return 'C'
        elif avg <= gradeType['D']:
            return 'D'
        elif avg <= gradeType['E']:
            return 'E'
        else:
            return '?!'
        
    def gradeM(self, avg):
        grade = self.absence_grade_M
        return self.setGrade(avg=avg, gradeType=grade)
    
    def gradeQ(self, avg):
        grade = self.absence_grade_Q
        return self.setGrade(avg=avg, gradeType=grade)
    
    def gradeS(self, avg):
        grade = self.absence_grade_S
        return self.setGrade(avg=avg, gradeType=grade)
    
    def gradeA(self, avg):
        grade = self.absence_grade_A
        return self.setGrade(avg=avg, gradeType=grade)
