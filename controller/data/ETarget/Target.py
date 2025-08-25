import pathlib

import pandas as pd
from utils.system import SystemController
from controller.data.ETarget.TargetController import TargetController
from config import ConfigManager
from controller.pathController import pathController

class Target:
    def __init__(self):
        self.paths = pathController().paths
        self.input_path = self.paths['input_path']
        self.targetDir = pathlib.Path(self.input_path+"\\TARGET")
        
    def getPRL(self, data):
        result = data[data['overall_status_T'].str.contains('perfect', case=False)]
        return result
    
    def getGRL(self, data):
        result = data[data['overall_status_T'].str.contains('good', case=False)]
        return result
    
    def getNIL(self, data):
        result = data[data['overall_status_T'].str.contains('needs', case=False)]
        return result
    
    def getARL(self, data):
        result = data[data['overall_status_T'].str.contains('risks', case=False)]
        return result
    
    def getRDL(self, data):
        result = data[data['overall_status_T'].str.contains('dismissal', case=False)]
        return result
    
    def getImporvingList(self, data):
        result = data[data['recent_trend_T'].str.contains('improving', case=False)]
        return result
    def getStableList(self, data):
        result = data[data['recent_trend_T'].str.contains('stable', case=False)]
        return result
    def getDecliningList(self, data):
        result = data[data['recent_trend_T'].str.contains('declining', case=False)]
        return result
    
    def sync(self):
        TarController = TargetController()
        hasFilesA = TarController.checkTargetFiles()
        
        if not hasFilesA:
            print()
            print("WARNING!")
            print("no data available. please insert files in directory below")
            print(self.targetDir)
            print()
            SystemController.wait_for_keypress()
            return
        
        df = pd.DataFrame()
        df =TarController.SetTargetDF()
        return df