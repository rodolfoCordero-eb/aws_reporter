from actions.importer import Importer
from boto3 import session   
import json

class IGImporter(Importer):
    def description(self) -> str:
        return "Retrieve all Internet Gateways for the given AWS account and region."

    def menu_name(self) -> str:
        return "Internet Gateways"

    def name(self) -> str:
        return "internet_gateways"

    def run(self, session: session.Session, acc_id: str, acc_name: str, region: str) -> None:
        print(f"Running IGImporter for account {acc_name} ({acc_id}) in region {region}")
        ec2_client = session.client("ec2", region_name=region)
        paginator = ec2_client.get_paginator("describe_internet_gateways")

        all_igs = []
        try:
            for page in paginator.paginate():
                all_igs.extend(page.get("InternetGateways", []))

            print(f"Found {len(all_igs)} Internet Gateways in {region}")
            self.save(acc_id, acc_name, region, all_igs)
            self.write_resume(acc_name, acc_id, region, len(all_igs))
        except Exception as e:
            print(f"Error fetching Internet Gateways for {acc_name} in {region}: {e}")
