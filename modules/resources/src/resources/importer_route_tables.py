import boto3
from actions.importer import Importer

class RouteTablesImporter(Importer):
    def description(self) -> str:
        return "Retrieve all Route Tables for the given AWS account and region."

    def menu_name(self) -> str:
        return "Route Tables"

    def name(self) -> str:
        return "route_tables"

    def run(self, session: boto3.session.Session, acc_id: str, acc_name: str, region: str) -> None:
        print(f"Running RouteTablesImporter for account {acc_name} ({acc_id}) in region {region}")
        ec2_client = session.client("ec2", region_name=region)
        paginator = ec2_client.get_paginator("describe_route_tables")

        all_rt = []
        try:
            for page in paginator.paginate():
                all_rt.extend(page.get("RouteTables", []))

            print(f"Found {len(all_rt)} Route Tables in {region}")
            self.save(acc_id, acc_name, region, all_rt)
            self.write_resume(acc_name, acc_id, region, len(all_rt))
        except Exception as e:
            print(f"Error fetching Route Tables for {acc_name} in {region}: {e}")
