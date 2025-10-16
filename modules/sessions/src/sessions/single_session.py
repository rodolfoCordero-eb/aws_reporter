import boto3 
from actions.analycer import Analycer
from actions.importer import Importer
from actions.exporter import Exporter
from datetime import datetime

class SingleSession:
    def __init__(self,session:boto3.session, region:str="us-east-1"):
        self.session = session
        self.region = region
        self.set_caller_identity()

    def set_caller_identity(self):
        org = self.session.client('organizations')
        sts_client = self.session.client("sts")
        self.identity = sts_client.get_caller_identity()
        self.userId=self.identity["UserId"]
        self.account_id = self.identity["Account"]
        self.account_name = org.describe_account(AccountId=self.account_id).get('Account').get('Name')
        print(f"🔍 Scanning account {self.account_id}-({self.account_name}) {self.account_name}...!!")
        return self.identity
    
    def run_importer(self,importer:Importer,region:str=None):
        print(f"🚀 Running importer: {importer.name()} for account {self.account_id}-({self.account_name})...")
        importer.run(self.session,self.account_id,self.account_name,region)
        print(f"✅ Importer {importer.name()} completed for account {self.account_id}-({self.account_name}).")

    def run_analycer(self,analycer:Analycer,output_path:str):
        print(f"🚀 Running analycer: {analycer.name()} for account {self.account_id}-({self.account_name})...")
        analycer.run({
            'account_id': self.account_id,
            'account_name': self.account_name
        },analycer.name(),output_path)
        print(f"✅ Analycer {analycer.name()} completed for account {self.account_id}-({self.account_name}).")

    def run_exporter(self,exporter:Exporter):
        print(f"🚀 Running exporter: {exporter.name()} for account {self.account_id}-({self.account_name})...")
        exporter.run({
            'account_id': self.account_id,
            'account_name': self.account_name
        },exporter.name())
        print(f"✅ Exporter {exporter.name()} completed for account {self.account_id}-({self.account_name}).")

    def get_account_info(self):
        return {
            'account_id': self.account_id,
            'account_name': self.account_name,
            'user_id': self.userId
        }
    
    def get_regions(self):
        ec2 = self.session.client('ec2')
        regions = [region['RegionName'] for region in ec2.describe_regions()['Regions']]
        return regions
    
    def run_in_all_regions(self,importer:Importer):
        regions = self.get_regions()
        for region in regions:
            print(f"🌍 Switching to region: {region}") 
            self.run_importer(importer,region)
    
    
