from abc import ABC,abstractmethod

class Exporter(ABC):
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def save(self,):
        pass