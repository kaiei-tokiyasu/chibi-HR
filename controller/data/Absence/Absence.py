import pathlib
import pandas as pd
from config import ConfigManager
from controller.data.Absence.AbsenceStatus import AbsenceStatus
from controller.pathController import pathController
from utils.system import SystemController
from controller.data.Absence.AbsenceController import AbsenceController

class Absence:
    def __init__(self):
        self.paths = pathController().paths
        self.input_path = self.paths['input_path']
        self.absenceDir = pathlib.Path(self.input_path+"\\ABSENCE")

    def getPRL(self, data):
        result = data[data['overall_status_A'].str.contains('perfect', case=False)]
        return result
    
    def getGRL(self, data):
        result = data[data['overall_status_A'].str.contains('good', case=False)]
        return result
    
    def getNIL(self, data):
        result = data[data['overall_status_A'].str.contains('needs', case=False)]
        return result
    
    def getARL(self, data):
        result = data[data['overall_status_A'].str.contains('risks', case=False)]
        return result
    
    def getRDL(self, data):
        result = data[data['overall_status_A'].str.contains('dismissal', case=False)]
        return result
    
    def getImporvingList(self, data):
        result = data[data['recent_trend_A'].str.contains('improving', case=False)]
        return result
    
    def getStableList(self, data):
        result = data[data['recent_trend_A'].str.contains('stable', case=False)]
        return result
    
    def getDecliningList(self, data):
        result = data[data['recent_trend_A'].str.contains('declining', case=False)]
        return result
    
    def sync(self):
        AbsController = AbsenceController()
        hasFilesA = AbsController.checkAbsenceFiles()
        
        if not hasFilesA:
            print()
            print("WARNING!")
            print("no data available. please insert files in directory below")
            print(self.absenceDir)
            print()
            SystemController.wait_for_keypress()
            return
        
        df = pd.DataFrame()
        df = AbsController.SetAbsenceDF()
        
        return df
    