import pandas as pd
from controller.data.Absence.AbsenceGrading import AbsenceGrading

class AbsenceQuarter:
    def __init__(self):
        # quarter config
        self.monthColtoConvertQ = 'bulan'
        self.quaterColName = 'kuartal' 

        self.copyColQ = ['No.Absen', 'Nama', 'Bagian', 'branch', 'tahun', 'bulan', 'Total']
        self.dropColQ = 'bulan'

        tempCol = self.copyColQ
        tempCol = tempCol[:-2]
        tempCol = tempCol+[self.quaterColName]
        self.groupbyQ = tempCol

        self.valTargetToCalQ = 'Total'
        self.totalValColnameQ = 'total_absence'
        self.avgValColnameQ = 'avg_absence'
        self.gradeValColnameQ = 'nilai'

        self.fullQuarterColQ = ['No.Absen', 'Nama', 'Bagian', 'tahun', 'branch']
        self.fullDataMergeColQ = ['No.Absen', 'Nama', 'Bagian', 'tahun', 'branch', 'kuartal']

        self.fullDataFillQ = [
            {
                'col': self.avgValColnameQ,
                'val': '-'
            },
            {
                'col': self.gradeValColnameQ,
                'val': '#'
            },
            {
                'col': self.totalValColnameQ,
                'val': '-'
            }
        ]

        #pivot
        self.pivotIndexQ = self.fullQuarterColQ
        self.pivotColQ = self.quaterColName

        self.pivotTotalQ = self.totalValColnameQ
        self.pivotAvgQ = self.avgValColnameQ
        self.pivotGradeQ = self.gradeValColnameQ

        self.PivotPrefixTotalQ = 'Total_Absen_Q'
        self.PivotPrefixAvgQ = 'absen_avg_Q'
        self.PivotPrefixGradeQ = 'nilai_absen_Q'

        #result
        self.resultgroupbyQ = ['No.Absen', 'Nama']
        self.dropDuplicateListQ = [{'subset':'No.Absen', 'keep':'last'}]

        self.expected_columnsS = [
            'No.Absen', 'Nama', 'Bagian', 'tahun',
            'absen_avg_Q1', 'nilai_absen_Q1',
            'absen_avg_Q2', 'nilai_absen_Q2',
            'absen_avg_Q3', 'nilai_absen_Q3',
            'absen_avg_Q4', 'nilai_absen_Q4',
            'Total_Absen_Q1', 'Total_Absen_Q2', 'Total_Absen_Q3', 'Total_Absen_Q4'
            ]
        self.SETGRADE = AbsenceGrading().gradeQ
        return
    
    def GetSummary(self, dataframe):
        df = dataframe[self.copyColQ].copy()
        df[self.quaterColName] = ((df[self.monthColtoConvertQ] - 1) // 3) + 1

        total_absence = df.copy().drop(self.dropColQ, axis=1)
        quarter_avg = df.copy().drop(self.dropColQ, axis=1)

        totalValColName = self.totalValColnameQ
        avgValColName = self.avgValColnameQ
        gradeValColName = self.gradeValColnameQ

        total_absence[totalValColName] = (
            total_absence.groupby(self.groupbyQ)[self.valTargetToCalQ]
            .transform("sum")
            .astype(int)
        )
        quarter_avg[avgValColName] = (
            quarter_avg.groupby(self.groupbyQ)[self.valTargetToCalQ]
            .transform("mean")
            .astype(float)
        )
        quarter_avg[gradeValColName] = (
            quarter_avg.groupby(self.groupbyQ)[self.valTargetToCalQ]
            .transform("mean")
            .astype(float)
            .apply(self.SETGRADE)
        )
        
        full_quarters =(
            df[self.fullQuarterColQ]
            .drop_duplicates()
            .assign(dummy=1)
            .merge(pd.DataFrame({self.quaterColName: [1,2,3,4], 'dummy':1}), on='dummy')
            .drop(columns='dummy')
        )

        full_data = pd.merge(full_quarters, quarter_avg, on=self.fullDataMergeColQ, how='left')
        full_data = pd.merge(full_data, total_absence, on=self.fullDataMergeColQ, how='left')        

        full_data[avgValColName] = full_data[avgValColName].round(2)

        for key in self.fullDataFillQ:
            full_data[key['col']] = full_data[key['col']].fillna(key['val'])

        pivotIndex = self.pivotIndexQ
        pivotCols = self.pivotColQ

        total_pivot = full_data.pivot_table(index=pivotIndex,
                                      columns=pivotCols,
                                      values=self.pivotTotalQ,
                                      aggfunc='max'
                                      ).add_prefix(self.PivotPrefixTotalQ)
        
        avg_pivot = full_data.pivot_table(index=pivotIndex,
                                      columns=pivotCols,
                                      values= self.pivotAvgQ,
                                      aggfunc='first'
                                      ).add_prefix(self.PivotPrefixAvgQ)
        
        grade_pivot = full_data.pivot_table(index=pivotIndex,
                                      columns=pivotCols,
                                      values=self.pivotGradeQ,
                                      aggfunc='first'
                                      ).add_prefix(self.PivotPrefixGradeQ)
        

        result = pd.concat([avg_pivot, grade_pivot, total_pivot], axis=1)
        result = result.reset_index()

        result = ( 
            result.groupby(self.resultgroupbyQ, as_index=False)
                  .agg(lambda x: x.ffill().bfill().iloc[0]) )
        result = result.infer_objects(copy=False)

        for key in self.dropDuplicateListQ:
            result = result.drop_duplicates(subset=key['subset'], keep=key['keep'])
        
        result = result[self.expected_columnsS]
        return result
