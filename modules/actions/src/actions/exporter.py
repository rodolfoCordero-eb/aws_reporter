from abc import ABC,abstractmethod
from datetime import datetime

class Exporter(ABC):
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def run(self,importer_name:str,date:datetime):
        pass

    