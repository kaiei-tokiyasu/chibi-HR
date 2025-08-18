from typing import Self
from openpyxl import load_workbook
from openpyxl.styles import Border, Side, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import FormulaRule
from openpyxl.worksheet.table import Table, TableStyleInfo

import pandas as pd

class EmployeePerformanceController:
    def __init__(self):

        self.status_fills = {
            'S Perfect Record': PatternFill(start_color='A7C7E7', end_color='A7C7E7', fill_type='solid'), 
            'Good Record': PatternFill(start_color='C6DBF0', end_color='C6DBF0', fill_type='solid'),    
            'Needs Improvement': PatternFill(start_color='FFF2A6', end_color='FFF2A6', fill_type='solid'),  
            'At Risk': PatternFill(start_color='FFCC99', end_color='FFCC99', fill_type='solid'),     
            'Recommended for Dismissal': PatternFill(start_color='F4A6A6', end_color='F4A6A6', fill_type='solid'),  
            'no data': PatternFill(start_color='D9D9D9', end_color='D9D9D9', fill_type='solid'),          
        }

        self.trend_fills = {
                'improving': PatternFill(start_color='A8E6CF', end_color='A8E6CF', fill_type='solid'),
                'declining': PatternFill(start_color='F7A1C4', end_color='F7A1C4', fill_type='solid'),
                'stable':    PatternFill(start_color='D9D9D9', end_color='D9D9D9', fill_type='solid'),
        }
        self.red_fill = PatternFill(start_color='FADBD8', end_color='FADBD8', fill_type='solid')
        self.yellow_fill = PatternFill(start_color='FFF9CC', end_color='FFF9CC', fill_type='solid')  

        self.odd_fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
        self.even_fill = PatternFill(start_color='F0F0F0', end_color='F0F0F0', fill_type='solid')
        
        return
    
    def ProcessSummaryMonth(AbsenData, TargetData):
        SummaryM = pd.merge(
            AbsenData, 
            TargetData,
            on=['No.Absen', 'Nama', 'Bagian', 'tahun'],
            how='outer'
        )

        Column_M = [
            'No.Absen', 'Nama', 'Bagian', 'tahun', 'branch', 'overall_status_A', 'overall_status_T', 'recent_trend_A',  'recent_trend_T'
        ]

        for i in range(1, 13):
            Column_M.append(f'Total_Absen_B{i}')
            Column_M.append(f'Nilai_Absen_B{i}')
            Column_M.append(f'{i}')
        
        Column_M =  [col for col in Column_M if col in SummaryM.columns]
        Column_M.append('Keterangan')
        
        SummaryM = SummaryM[Column_M]
        SummaryM = ( 
            SummaryM.groupby(['No.Absen'], as_index=False)
                  .agg(lambda x: x.ffill().bfill().iloc[0]) )
        SummaryM = SummaryM.infer_objects(copy=False)
        SummaryM = SummaryM.drop_duplicates(subset='No.Absen', keep='last').reset_index(drop=True)

        # top down
        record = []
        for _, row in SummaryM.iterrows():
            absence = {
                'No.Absen': row['No.Absen'],
                'Nama': row['Nama'],
                'Bagian': row['Bagian'],
                'tahun': row['tahun'],
                'branch': row['branch'],
                '#': 'absence',
                'overall_status': row['overall_status_A'],
                'recent_trend': row['recent_trend_A']
            }
            target = {
                'No.Absen': row['No.Absen'],
                'Nama': row['Nama'],
                'Bagian': row['Bagian'],
                'tahun': row['tahun'],
                'branch': row['branch'],
                '#': 'target',
                'overall_status': row['overall_status_T'],
                'recent_trend': row['recent_trend_T']
            }

            for i in range(1, 13):
                absence[f'T{i}'] = row.get(f'Total_Absen_B{i}', '-')
                absence[f'm{i}'] = row.get(f'Nilai_Absen_B{i}', '-')

                target[f'T{i}'] = '-'
                target[f'm{i}'] = row.get(str(i), '-')
            
            absence['Keterangan'] = row.get('Keterangan', '')
            target['Keterangan'] = row.get('Keterangan', '')
            record.append(absence)
            record.append(target)

        result = pd.DataFrame(record)

        return result
    
    def SortData(data):
        
        return 
    
    def setGradeColour(self, ws, Column_M, dataCols, start_row, end_row, colCondition):
        grade_columns = [col for col in Column_M if col.startswith(colCondition)]
        for col_name in grade_columns:
            col_index = dataCols.get_loc(col_name) + 2
            col_letter = get_column_letter(col_index)
            cell_range = f'{col_letter}{start_row}:{col_letter}{end_row}'

            formula_e = f'${col_letter}{start_row}="E"'
            formula_d = f'${col_letter}{start_row}="D"'
            
            ws.conditional_formatting.add(cell_range, FormulaRule(formula=[formula_e], fill=self.red_fill))
            ws.conditional_formatting.add(cell_range, FormulaRule(formula=[formula_d], fill=self.yellow_fill))
        return
    
    def setOverallStatus(self, ws, dataCols, start_row, end_row):
        normalized_cols = dataCols.str.replace("_", " ", regex=False)
        found = any("overall status" in col for col in normalized_cols)
        if found:
            loc =  next(
                (dataCols[i] for i, col in enumerate(normalized_cols) if col.startswith("overall status")),
                ""
            )
            status_index = dataCols.get_loc(loc) + 2
            status_col = get_column_letter(status_index)
            status_range = f'{status_col}{start_row}:{status_col}{end_row}'

            for status, fill in self.status_fills.items():
                formula = f'${status_col}{start_row}="{status}"'
                ws.conditional_formatting.add(status_range, FormulaRule(formula=[formula], fill=fill))
        return 

    def setRecentTrend(self, ws, dataCols, start_row, end_row):
        normalized_cols = dataCols.str.replace("_", " ", regex=False)
        found = any("recent trend" in col for col in normalized_cols)
        if found:
            loc =  next(
                (dataCols[i] for i, col in enumerate(normalized_cols) if col.startswith("recent trend")),
                ""
            )
            trend_index = dataCols.get_loc(loc) + 2
            trend_col = get_column_letter(trend_index)
            trend_range = f'{trend_col}{start_row}:{trend_col}{end_row}'

            for trend, fill in self.trend_fills.items():
                formula = f'${trend_col}{start_row}="{trend}"'
                ws.conditional_formatting.add(trend_range, FormulaRule(formula=[formula], fill=fill))

        return
    
    
    def setAlternatingFill(self, ws):
        thin_border = Border(
            left=Side(style='none'),
            right=Side(style='none'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
        for row in ws.iter_rows(min_row=1, max_row=ws.max_row):
            row_idx = row[0].row
            for cell in row:
                # Apply border
                cell.border = thin_border
                
                # Fill even or odd row
                if row_idx % 2 == 0:
                    cell.fill = self.even_fill
                else:
                    cell.fill = self.odd_fill
        return
    def formatExcelMonth(self, w, sheetname, data, type):
        wb = load_workbook(w)
        ws = wb[sheetname]

        ws.row_dimensions[1].height = 30
        ws.auto_filter.ref = ws.dimensions

        Column_M = []
        colCondition = ''
        if type == "combine":
            Column_M = [
                'No.Absen', 'Nama', 'Bagian', 'tahun', 'branch', 'overall_status', 'recent_trend'
            ]
            colCondition = 'm'
        elif type == 'Absence':
            Column_M = [
                'No.Absen', 'Nama', 'Bagian', 'branch',  'tahun',  'overall_status_A', 'recent_trend_A'
            ]
            colCondition = 'Nilai_Absen_B'
        elif type == 'Target':
            Column_M = [
                'No.Absen', 'Nama', 'Bagian', 'tahun',  'overall_status_T', 'recent_trend_T'
            ]
            colCondition = ''
        

        dataCols = data.columns
        for i in range(1, 13):
            if type == 'combine':
                Column_M.append(f'T{i}')
                Column_M.append(f'm{i}')
            elif type == 'Absence':
                Column_M.append(f'Total_Absen_B{i}')
                Column_M.append(f'Nilai_Absen_B{i}')
            elif type == 'Target':
                Column_M.append(f'{i}')
        
        
        Column_M = [col for col in Column_M if col in dataCols]
        Column_M.append('Keterangan')

        start_row = 2
        end_row = ws.max_row
        
        self.setGradeColour(ws, Column_M, dataCols, start_row, end_row, colCondition)
        self.setOverallStatus(ws, dataCols, start_row, end_row)
        self.setRecentTrend(ws, dataCols, start_row, end_row)
        self.setAlternatingFill(ws)
        # max_row = ws.max_row
        # max_col = ws.max_column

        # ref = f"A1:{get_column_letter(max_col)}{max_row}"
        # table = Table(displayName="MyDynamicTable", ref=ref)

        # ws.add_table(table)

        

        wb.save(w)
        return


       

      