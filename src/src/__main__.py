import os
import sys
import resources    
import sessions 
from sessions import  OrgSession
import resources

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
    resources_list=resources.get_importers()
    org_sess=OrgSession()
    sessions=org_sess.get_single_sessions()
    path = os.path.abspath("db")
    for session in sessions:
        print(session.get_account_info())
        for importer_instance in resources_list:
            importer_name = importer_instance.menu_name()
            print(f"Running importer: {importer_name} for account {session.account_id}-({session.account_name})...")
            session.run_importer(importer_instance,region="us-west-2")
            print(f"Completed importer: {importer_name} for account {session.account_id}-({session.account_name}).")
    