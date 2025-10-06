import pandas as pd
from config import ConfigManager

class metadataEmployeeId:
    def __init__(self):
        self.col_id = "id"
        self.col_desc = "deskripsi"
        CM = ConfigManager()
        self.metadata = CM.config['row-id-metadata']

        return
    def getMetaDataPD(self):
        metadata_info = self.metadata
        col_id = self.col_id
        col_desc = self.col_desc

        employee_id_df = pd.DataFrame(list(metadata_info.items()), columns=[col_id, col_desc])

        return employee_id_df
