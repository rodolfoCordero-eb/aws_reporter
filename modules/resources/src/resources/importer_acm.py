import boto3
from actions.importer import Importer

class ACMImporter(Importer):
    def description(self) -> str:
        return "Retrieve all ACM certificates for the given AWS account."

    def menu_name(self) -> str:
        return "ACM Certificates"

    def name(self) -> str:
        return "acm_certificates"

    def run(self, session: boto3.session.Session, acc_id: str, acc_name: str, region: str) -> None:
        print(f"Running ACMImporter for account {acc_name} ({acc_id}) in region {region}")
        acm_client = session.client("acm", region_name=region)
        paginator = acm_client.get_paginator("list_certificates")

        all_certs = []
        try:
            for page in paginator.paginate():
                certs = page.get("CertificateSummaryList", [])
                # Opcional: obtener detalles de cada certificado
                for c in certs:
                    cert_detail = acm_client.describe_certificate(CertificateArn=c["CertificateArn"])
                    all_certs.append(cert_detail.get("Certificate", {}))

            print(f"Found {len(all_certs)} ACM certificates in {region}")
            self.save(acc_id, acc_name, region, all_certs)
            self.write_resume(acc_name, acc_id, region, len(all_certs))
        except Exception as e:
            print(f"Error fetching ACM certificates for {acc_name} in {region}: {e}")
