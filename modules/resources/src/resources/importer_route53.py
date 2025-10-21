import boto3
from actions.importer import Importer

class Route53Importer(Importer):
    def description(self) -> str:
        return "Retrieve all Route53 Hosted Zones for the given AWS account."

    def menu_name(self) -> str:
        return "Route53"

    def name(self) -> str:
        return "route53"

    def run(self, session: boto3.session.Session, acc_id: str, acc_name: str, region: str = "us-east-1") -> None:
        # Route53 es global, region no es relevante
        print(f"Running Route53Importer for account {acc_name} ({acc_id})")
        r53_client = session.client("route53")

        paginator = r53_client.get_paginator("list_hosted_zones")
        all_zones = []
        try:
            for page in paginator.paginate():
                all_zones.extend(page.get("HostedZones", []))

            print(f"Found {len(all_zones)} Hosted Zones")
            self.save(acc_id, acc_name, "global", all_zones)
            self.write_resume(acc_name, acc_id, "global", len(all_zones))
        except Exception as e:
            print(f"Error fetching Route53 Hosted Zones for {acc_name}: {e}")
