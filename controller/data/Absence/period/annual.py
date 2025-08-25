from controller.data.Absence.AbsenceGrading import AbsenceGrading

class AbsenceAnnual:
    def __init__(self):
        # annual Config
        self.groupbyA = ['No.Absen', 'Nama', 'Bagian', 'tahun', 'branch']
        self.valTargetToCalA = 'Total'
        self.gradeValColnameA = 'annual_avg'
        self.gradeColnameA = 'nilai_tahunan'
        self.dropDuplicateListA = [{'subset':'No.Absen', 'keep':'last'}]
        self.expected_columnsA = [ 'No.Absen', 'Nama', 'Bagian', 'branch', 'tahun', self.gradeValColnameA, self.gradeColnameA]

        self.SETGRADE = AbsenceGrading().gradeA
        return
    
    def GetSummary(self, dataframe):
        df = dataframe.copy()
        valColname = self.gradeValColnameA
        
        annual_avg = df.copy()
        annual_avg[valColname] = (
            df.groupby(self.groupbyA)[self.valTargetToCalA]
            .transform("mean")
            .round(2)
        )

        annual_avg[self.gradeColnameA] = annual_avg[valColname].apply(self.SETGRADE)
        
        result = annual_avg
        
        for key in self.dropDuplicateListA:
            result = result.drop_duplicates(subset=key['subset'], keep=key['keep'])

        result = result[self.expected_columnsA]
        return result
       