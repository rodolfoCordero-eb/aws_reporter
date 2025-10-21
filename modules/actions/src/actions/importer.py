from abc import ABC,abstractmethod
import boto3.session
from pathlib import Path
import os
import json
from datetime import datetime
class Importer(ABC):
    def __init__(self,path="/tmp/"):
        self.path = Path(path)

    def set_path(self,path:str)->None:
        self.path = Path(path)

    @abstractmethod
    def description(self)->str:
        pass

    @abstractmethod
    def menu_name(self)->str:
        pass

    @abstractmethod
    def name(self)->str:
        pass

    @abstractmethod
    def run(self,session:boto3.session,acc_id:str, acc_name:str, region:str) ->None:
        pass
    
    def save(self,acc_id:str, acc_name:str,region:str,content: json)->None:
        now = datetime.now()
        full_path = f'{self.path}/{acc_name}_{acc_id}/json/{region}/{self.name()}/{now.strftime("%Y-%m-%d")}/'
        self.write_to_file(full_path,content)


    def write_to_file(self,full_path:str,content:json)->None:
        filename = self.name()+".json"
        if not os.path.exists(full_path):
            print(f"Creating directory: {full_path}")
            os.makedirs(full_path, exist_ok=True)
        print(f"Writing to file: {full_path+filename}")
        with open(full_path+filename,'w') as f:
            f.write(json.dumps(content))
        print(f"File {filename} written successfully.")

    def list_states(self,acc_id:str, acc_name:str)->list:
        full_path = f'{self.path}/{acc_name}_{acc_id}/json/{self.name()}/'
        elements = os.listdir(full_path) if os.path.exists(full_path) else []
        dirs =  [d for d in elements if os.path.isdir(os.path.join(full_path, d))]
        dirs.sort(reverse=True)
        return dirs
    
    def write_resume(self,acc_name:str,acc_id:str,region:str,content:list)->None:
        now = datetime.now()
        full_path = f'{self.path}/resumes/{region}/'

        filename = f'resume_{self.name()}_{region}.csv'
        if not os.path.exists(full_path):
            print(f"Creating directory: {full_path}")
            os.makedirs(full_path, exist_ok=True)
        print(f"Writing to file: {full_path+filename}")
        content = [self.name(),acc_id,acc_name, now.strftime("%Y-%m-%d %H:%M:%S"), content]
        with open(full_path+filename,'a') as f:
            content_str = ','.join(map(str, content))
            f.write(content_str + '\n')
        print(f"File {filename} written successfully.")