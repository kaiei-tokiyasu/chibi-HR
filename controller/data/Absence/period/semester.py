import pandas as pd
from controller.data.Absence.AbsenceGrading import AbsenceGrading


class AbsenceSemester:
    def __init__(self):
        #semester config
        self.monthColtoConvertS = 'bulan'
        self.semesterColName = 'semester' 
        self.copyColS = ['No.Absen', 'Nama', 'Bagian', 'branch', 'tahun', 'bulan', 'Total']
        self.dropColS = 'bulan'
        tempCol = self.copyColS
        tempCol = tempCol[:-2]
        tempCol = tempCol+[self.semesterColName]
        self.groupbyS = tempCol
        # self.groupbyS = ['No.Absen', 'Nama', 'Bagian', 'branch', 'tahun', 'semester' ]
        
        self.valTargetToCalS = 'Total'
        self.totalValColnameS = 'total_absence'
        self.avgValColnameS = 'avg_semester'
        self.gradeValColnameS = 'nilai'

        self.fullSemesterColS = ['No.Absen', 'Nama', 'Bagian', 'tahun', 'branch']
        self.fullDataMergeColS = ['No.Absen', 'Nama', 'Bagian', 'tahun', 'branch', 'semester']
        # self.fullSemesterColS.append(self.semesterColName)

        self.fullDataFillS = [
            {
                'col': self.avgValColnameS,
                'val': '-'
            },
            {
                'col': self.gradeValColnameS,
                'val': '#'
            },
            {
                'col': self.totalValColnameS,
                'val': '#'
            }
        ]

        #pivot
        # self.PivotIndexS = ['No.Absen', 'Nama', 'Bagian', 'tahun', 'branch']
        self.PivotIndexS = self.fullSemesterColS
        self.PivotColS = self.semesterColName
        self.pivotTotalS = self.valTargetToCalS
        self.pivotGradeS = self.gradeValColnameS

        self.PivotPrefixTotalS = 'Total_Absence_S'
        self.PivotPrefixAvgS = 'avg_S'
        self.PivotPrefixGradeS = 'Nilai_S'

        #result
        self.resultgroupbyS = ['No.Absen', 'Nama']
        self.dropDuplicateListS = [{'subset':'No.Absen', 'keep':'last'}]
        self.expected_columnsS = [
            'No.Absen', 'Nama', 'Bagian', 'tahun', 'branch',
            'avg_S1', 'Nilai_S1',
            'avg_S2', 'Nilai_S2',
            'Total_Absence_S1', 'Total_Absence_S2'
        ]
        self.SETGRADE = AbsenceGrading().gradeS
        return
    
    def GetSummary(self, dataframe):
        df = dataframe[self.copyColS].copy()

        df[self.semesterColName] = df[self.monthColtoConvertS].apply(lambda m: 1 if m <= 6 else 2)

        total_absence = df.copy().drop(self.dropColS, axis=1)
        semester_avg = df.copy().drop(self.dropColS, axis=1)
        
        totalValColName = self.totalValColnameS
        avgValColName = self.avgValColnameS


        total_absence[totalValColName] = (
            total_absence.groupby(self.groupbyS)[self.valTargetToCalS]
            .transform("sum")
            .astype(int)
        )
        
        semester_avg[avgValColName] = (
            semester_avg.groupby(self.groupbyS)[self.valTargetToCalS]
            .transform("mean")
            .astype(float)
        )
        semester_avg[self.gradeValColnameS] = (
            semester_avg.groupby(self.groupbyS)[self.valTargetToCalS]
            .transform("mean")
            .astype(float)
            .apply(self.SETGRADE)
        )
        
        full_semester = (
            df[self.fullSemesterColS]
            .drop_duplicates()
            .assign(dummy=1)
            .merge(pd.DataFrame({self.semesterColName: [1,2], 'dummy':1}), on='dummy')
            .drop(columns='dummy')
        )
        full_data = pd.merge(full_semester, semester_avg, on=self.fullDataMergeColS, how='left')
        full_data = pd.merge(full_data, total_absence, on=self.fullDataMergeColS, how='left')

        full_data[avgValColName] = full_data[avgValColName].round(2)
        
        for key in self.fullDataFillS:
            full_data[key['col']] = full_data[key['col']].fillna(key['val'])


        pivotIndex = self.PivotIndexS
        pivotCols = self.PivotColS

        total_pivot = full_data.pivot_table(index=pivotIndex,
                                      columns=pivotCols,
                                      values=totalValColName,
                                      aggfunc='max'
                                      ).add_prefix(self.PivotPrefixTotalS)
        
        avg_pivot = full_data.pivot_table(index=pivotIndex,
                                      columns=pivotCols,
                                      values=avgValColName,
                                      aggfunc='first'
                                      ).add_prefix(self.PivotPrefixAvgS)
        
        grade_pivot = full_data.pivot_table(index=pivotIndex,
                                      columns=pivotCols,
                                      values=self.gradeValColnameS,
                                      aggfunc='first'
                                      ).add_prefix(self.PivotPrefixGradeS)

        result = pd.concat([avg_pivot, grade_pivot, total_pivot], axis=1)
        result = result.reset_index()
        
        result = ( 
            result.groupby(self.resultgroupbyS, as_index=False)
                  .agg(lambda x: x.ffill().bfill().iloc[0]) )
        result = result.infer_objects(copy=False)

        for key in self.dropDuplicateListS:
            result = result.drop_duplicates(subset=key['subset'], keep=key['keep'])

        # print(result)
        result = result[self.expected_columnsS]
        return result
