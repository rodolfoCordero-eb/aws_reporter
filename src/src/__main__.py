import os
import sys
import resources    
import sessions 
from sessions import  OrgSession
from resources import VPCPeeringImporter

def print_importers(resources):
    importers = resources.get_importers()
    print("Available Importers:")
    for imp in importers:
        print(f"- {imp.menu_name()}")
def print_sessions(org_session):
    print("Available Sessions:")
    for acc in org_session.accounts:
        print(f"- {acc['Id']} ({acc['Name']})")


if __name__ == "__main__":
    resources_list=resources.get_importers("/db")
    #print_importers(resources)
    org_sess=OrgSession()
    #print_sessions(org_sess)
    sessions=org_sess.get_single_sessions()
    path = os.path.abspath("db")
    for session in sessions:
        print(session.get_account_info())
        session.run_importer(VPCPeeringImporter(path),region="us-west-2")
    