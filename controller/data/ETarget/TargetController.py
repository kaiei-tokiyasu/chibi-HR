from csv import excel
import pathlib
from numpy import dtype

import datetime

import pandas as pd
from utils.lib import lib
from utils.system import SystemController

from controller.pathController import pathController

class TargetController:
    def __init__(self):
        self.paths = pathController().paths
        self.input_path = self.paths['input_path']
        self.output_path = self.paths['output_path']
        self.input_data_dir =  pathlib.Path(self.input_path)

        self.targetDir = pathlib.Path(self.input_path+"\\TARGET")

        #config
        self.rename_columns = {
            "NO ABSEN ": "No.Absen",
            "NAMA  " : "Nama",
            "DEVISI " : "Bagian",
            "Unnamed: 16": "Rata-Rata",
            "Unnamed: 17": "Keterangan",
            
            "Unnamed: 19": "m-1",
            "Unnamed: 20": "m-2",
            "Unnamed: 21": "m-3",
            "Unnamed: 22": "m-4",
            "Unnamed: 23": "m-5",
            "Unnamed: 24": "m-6",
            "Unnamed: 25": "m-7",
            "Unnamed: 26": "m-8",
            "Unnamed: 27": "m-9",
            "Unnamed: 28": "m-10",
            "Unnamed: 29": "m-11",
            "Unnamed: 30": "m-12",

            "JAN": "m-1",
            "FEB": "m-2",
            "MAR": "m-3",
            "APR": "m-4",
            "APR ": "m-4",
            "MEY ": "m-5",
            "JUNI": "m-6",
            "JULI ": "m-7",
            "AGUS ": "m-8",
            "SEPT ": "m-9",
            "OKT ": "m-10",
            "NOV ": "m-11",
            "DES": "m-12",
        }

        self.dropnaList = ['No.Absen', 'Nama']

        self.dfFill = [
            {
                'col': 'Keterangan',
                'val': '-'
            }
        ]
        self.dfFillOther = "#"

        return
    
    def checkTargetFiles(self):
        data_count_Target_xls = len(list(self.targetDir.glob('*.xlsx')))
        if data_count_Target_xls <= 0:
            return False
        return True
    
    def extract_data(self, filename):

        sheetname = 0
        atRows = 2
        columns= None
        df = pd.DataFrame()
        df = lib().extractToDF(df=df, filename=filename, sheetname=sheetname, atRows=atRows, columns=columns)
        
        
        for col in df.columns:
            if isinstance(col, datetime.datetime):
                self.rename_columns[col] = str(col.month)
        
        df = df.rename(columns= self.rename_columns)
        df = df.loc[:, ~df.columns.str.startswith("Unnamed")]

        for key in self.dropnaList:
            df = df.dropna(subset=[key], axis=0)

        for key in self.dfFill:
            df[key['col']] = df[key['col']].fillna(key['val'])

        df = df.fillna(self.dfFillOther, axis=1)

        # dtypes = {
        #     "No.Absen" : str,

        # }
        # df = df.astype(dtypes)
        df = df.reset_index(drop=True)

        return df
    
    def SetTargetDF(self):
        list_Target_xls = list(self.targetDir.glob('*.xlsx'))
        total_files = len(list_Target_xls) + 1
        TargetDF = pd.DataFrame()

        for idx, val in enumerate(list_Target_xls, 1):
            task_name = f"Processing {val}"
            SystemController().print_loading_bar(task_name, idx, total_files)
            df = self.extract_data(val)
            
            sheetname = pd.ExcelFile(val).sheet_names[0]
            year = sheetname[-4:]
            df.insert(3, 'tahun', year)
            
            TargetDF = pd.concat([TargetDF, df], axis=0)
        SystemController().print_loading_bar(task_name=f"Load Succesfull", current=total_files, total=total_files)
        
        TargetDF = TargetDF.reset_index(drop=True)
        return TargetDF