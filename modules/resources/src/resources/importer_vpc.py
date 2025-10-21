import boto3
from actions.importer import Importer

class VpcsImporter(Importer):
    def description(self) -> str:
        return "Retrieve all VPCs for the given AWS account and region."

    def menu_name(self) -> str:
        return "VPCs"

    def name(self) -> str:
        return "vpcs"

    def run(self, session: boto3.session.Session, acc_id: str, acc_name: str, region: str) -> None:
        print(f"Running VpcsImporter for account {acc_name} ({acc_id}) in region {region}")
        ec2_client = session.client("ec2", region_name=region)
        paginator = ec2_client.get_paginator("describe_vpcs")

        all_vpcs = []
        try:
            for page in paginator.paginate():
                all_vpcs.extend(page.get("Vpcs", []))

            print(f"Found {len(all_vpcs)} VPCs in {region}")
            self.save(acc_id, acc_name, region, all_vpcs)
            self.write_resume(acc_name, acc_id, region, len(all_vpcs))
        except Exception as e:
            print(f"Error fetching VPCs for {acc_name} in {region}: {e}")
