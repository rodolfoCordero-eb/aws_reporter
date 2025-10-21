import boto3
from actions.importer import Importer

class SubnetsImporter(Importer):
    def description(self) -> str:
        return "Retrieve all Subnets for the given AWS account and region."

    def menu_name(self) -> str:
        return "Subnets"

    def name(self) -> str:
        return "subnets"

    def run(self, session: boto3.session.Session, acc_id: str, acc_name: str, region: str) -> None:
        print(f"Running SubnetsImporter for account {acc_name} ({acc_id}) in region {region}")
        ec2_client = session.client("ec2", region_name=region)
        paginator = ec2_client.get_paginator("describe_subnets")

        all_subnets = []
        try:
            for page in paginator.paginate():
                all_subnets.extend(page.get("Subnets", []))

            print(f"Found {len(all_subnets)} subnets in {region}")
            self.save(acc_id, acc_name, region, all_subnets)
            self.write_resume(acc_name, acc_id, region, len(all_subnets))
        except Exception as e:
            print(f"Error fetching Subnets for {acc_name} in {region}: {e}")
