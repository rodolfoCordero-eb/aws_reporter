from abc import ABC,abstractmethod
from datetime import datetime
import os
from pathlib import Path

class Analycer(ABC):
    @abstractmethod
    def __init__(self,path="/tmp/"):
        self.path = Path(path)
    def name(self):
        pass

    @abstractmethod
    def run(self,items:dict,importer_name:str,output_path:str):
        pass
    

    def get_files(self,items:dict,importer_name:str)->list:
        """
        items: lista de dicts con keys 'acc' y 'date', example:
        [{'acc': 'account1_123', 'date': '2025-10-09'}, ...]
        """
        results = []
        for item in items:
            account_id = item['account_id']
            account_name = item["account_name"]
            date = item['date']
            file_path = f"{self.path}/{account_name}_{account_id}/json/{importer_name}/{date}/{importer_name}.json"
            if os.path.exists(file_path):
                results.append(file_path)
        return results