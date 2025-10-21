from .importer_route_tables import RouteTablesImporter
from .importer_vpc_peering import VPCPeeringImporter
from .importer_vpc import VpcsImporter
from .importer_ig import IGImporter
from .importer_route53 import Route53Importer
from .importer_acm import ACMImporter
from .importer_cloudfront import CloudFrontImporter
from .import_subnets import SubnetsImporter


def get_importers(path="/tmp")->list:
    importers =[VPCPeeringImporter(path),IGImporter(path),
                RouteTablesImporter(path),VpcsImporter(path),
                CloudFrontImporter(path),ACMImporter(path),
                Route53Importer(path),SubnetsImporter(path)]
    return importers

def get_analycers()->list:
    analycers =[]
    return analycers

def get_exporters()->list:
    exporters =[]
    return exporters