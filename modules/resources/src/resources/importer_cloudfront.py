import boto3
from actions.importer import Importer

class CloudFrontImporter(Importer):
    def description(self) -> str:
        return "Retrieve all CloudFront distributions (CDN) for the given AWS account."

    def menu_name(self) -> str:
        return "CloudFront"

    def name(self) -> str:
        return "cloudfront"

    def run(self, session: boto3.session.Session, acc_id: str, acc_name: str, region: str = "us-east-1") -> None:
        # CloudFront es global, region no es relevante
        print(f"Running CloudFrontImporter for account {acc_name} ({acc_id})")
        cf_client = session.client("cloudfront")

        paginator = cf_client.get_paginator("list_distributions")
        all_distributions = []
        try:
            for page in paginator.paginate():
                items = page.get("DistributionList", {}).get("Items", [])
                all_distributions.extend(items)

            print(f"Found {len(all_distributions)} CloudFront distributions")
            self.save(acc_id, acc_name, "global", all_distributions)
            self.write_resume(acc_name, acc_id, "global", len(all_distributions))
        except Exception as e:
            print(f"Error fetching CloudFront distributions for {acc_name}: {e}")
