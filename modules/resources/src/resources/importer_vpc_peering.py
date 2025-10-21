from actions.importer import Importer
from boto3 import session
import json
class VPCPeeringImporter(Importer):

    def __init__(self, path="/tmp/"):
        super().__init__(path)
        
    def name(self) -> str:
        return "vpc_peering"
    
    def description(self) -> str:
        return "Imports VPC Peering Connections"
    
    def menu_name(self) -> str:
        return "VPC Peering"

    def run(self, session: session, acc_id: str, acc_name: str, region: str) -> None:
        ec2_client = session.client('ec2', region_name=region)
        paginator = ec2_client.get_paginator('describe_vpc_peering_connections')
        print('--------------------------------------------------')
        page_iterator = paginator.paginate()
        vpc_peering_connections = []
        for page in page_iterator:
            vpc_peering_connections.extend(page.get('VpcPeeringConnections', []))  
        self.write_resume(acc_name=acc_name,acc_id=acc_id,region=region,content=[len(vpc_peering_connections)])
        json_content = json.dumps(vpc_peering_connections, indent=2, default=str)
        print(f"Found {len(vpc_peering_connections)} VPC Peering Connections in region {region}.")
        print('--------------------------------------------------')
        self.save(acc_id=acc_id, acc_name=acc_name,region=region,content=json_content) 
