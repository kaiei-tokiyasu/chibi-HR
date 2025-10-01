import pathlib
from pathlib import Path
from numpy import dtype, extract
import os
import glob
import pandas as pd
from utils.lib import lib
from utils.system import SystemController

from controller.pathController import pathController

class AbsenceController:
    def __init__(self):
        self.sheetName = 0
        self.StartRowAt = 7
        self.pickColumns = [0,1,2,34,35,36,37]

        self.rename_columns = {
            "Unnamed: 0": "No.Absen",
            "Unnamed: 1": "Bagian",
            "Unnamed: 2": "Nama",
            "Unnamed: 34": "Sakit",
            "Unnamed: 35": "Izin",
            "Unnamed: 36": "A",
            "Unnamed: 37": "Total"
        }

        self.dtypes = {
            "No.Absen" : str,
            "Bagian" : str,
            "Nama" : str,
            "Sakit" : int,
            "Izin" : int,
            "A" : int,
            "Total" : int
        }

        self.dropnaList = ['No.Absen', 'Bagian', 'Total']
        self.dropExceptionList = [{'col':'Bagian', 'val':0}, {'col':'Bagian', 'val':'-'}]
        self.dropDuplicateList = [{'subset':'No.Absen', 'keep':'first'}]

        self.monthYearStartAtRow = 4
        self.monthYearCol = [34, 36]
        self.monthYearRenameCols = {
            "Unnamed: 34":"month", "Unnamed: 36":"year"
        }

        self.insertMonthAt = 4
        self.insertYearAt = 3
        self.yearColName = 'tahun'
        self.monthColName = 'bulan'

        #location/branch read by filename
        self.insertLocationAt = 5
        self.LocationColName= 'branch'
        self.location = ['kalisabi', 'sangiang']

        self.sortValuesBy = ['No.Absen','Bagian', 'bulan']

        self.cleanByColumnName = "Nama"


        self.paths = pathController().paths
        self.input_path = self.paths['input_path']
        self.output_path = self.paths['output_path']

        self.input_data_dir =  pathlib.Path(self.input_path)

        self.absenceDir = os.path.join(self.input_path, "ABSENCE")
        return

    def checkAbsenceFiles(self):
        files = glob.glob(os.path.join(self.absenceDir, '*.xlsx'))
        data_count_Absence_xls = len(files)
        if data_count_Absence_xls <= 0:
            return False
        return True

    def extract_data(self, filename):
        sheetname = self.sheetName
        atRows = self.StartRowAt
        columns=self.pickColumns

        df = pd.DataFrame()
        df = lib().extractToDF(df=df, filename=filename, sheetname=sheetname, atRows=atRows, columns=columns)

        rename_columns = self.rename_columns
        dtypes = self.dtypes

        df = df.rename(columns= rename_columns)

        for key in self.dropnaList:
            df = df.dropna(subset=[key], axis=0)

        for key in self.dropExceptionList:
            df = df[df[key['col']] != key['val']]

        df = df.astype(dtypes)

        for key in self.dropDuplicateList:
            df = df.drop_duplicates(subset=key['subset'], keep=key['keep'])

        df = df.reset_index(drop=True)

        return df

    def get_month_year(self, filename):
        dfdate = pd.DataFrame()
        dfdate = pd.read_excel(filename, sheet_name=0, usecols=self.monthYearCol,skiprows=self.monthYearStartAtRow, nrows=1)
        dfdate = dfdate.rename(columns=self.monthYearRenameCols)

        month = dfdate['month'][0]
        year = dfdate['year'][0]

        return month, year

    def cleanOldNames(self, raw_data):
        targetCol = self.cleanByColumnName
        yearCol = self.yearColName
        monthCol = self.monthColName

        max_year = raw_data[yearCol].max()
        max_month = raw_data.loc[raw_data[yearCol] == max_year, monthCol].max()

        result = raw_data[(raw_data[yearCol] == max_year) & (raw_data[monthCol] == max_month)][targetCol ].unique()

        result = raw_data[raw_data[targetCol].isin(result)]
        return result
    def SetAbsenceDF(self):
        list_Absence_xls = list(Path(self.absenceDir).glob('*.xlsx'))
        total_files = len(list_Absence_xls) + 1
        AbsenceDF = pd.DataFrame()
        for idx, val in enumerate(list_Absence_xls, 1):
            task_name = f"Processing {val}"
            SystemController().print_loading_bar(task_name, idx, total_files)
            df = self.extract_data(val)

            month, year = self.get_month_year(val)

            df.insert(self.insertYearAt, self.yearColName, year)
            df.insert(self.insertMonthAt, self.monthColName, month)

            loc = self.location

            setKey = 'unknown'
            for key in loc:
                if key in val.name.lower():
                    setKey = key

            df.insert(self.insertLocationAt, self.LocationColName, setKey)

            AbsenceDF = pd.concat([AbsenceDF, df], axis=0)

        SystemController().print_loading_bar(task_name=f"Load Succesfull", current=total_files, total=total_files)

        AbsenceDF = AbsenceDF.sort_values(self.sortValuesBy).reset_index(drop=True)

        AbsenceDF = self.cleanOldNames(AbsenceDF)

        # print(AbsenceDF)
        return AbsenceDF
