# SWAMI KARUPPASWAMI THUNNAI

import sys
import pymysql
import threading
from information_gathering_phase1 import web_server_informtaion
from information_analysis.phase_one_analysis import PhaseOneAnalysis
from siva_db import SivaDB
from url.URL import URL
import getpass

def check_for_vulnerabilities(connection, project_id, url):
    """First phase of Information gathering"""
    thread_semaphore = threading.Semaphore(100)
    database_semaphore = threading.Semaphore(100)
    print("[*] Gathering PHASE-1 INFORMATION")
    information_gathering = web_server_informtaion.WebServerInformation(project_id=project_id, connection=connection,
                                                                        thread_semaphore=thread_semaphore,
                                                                        database_semaphore=database_semaphore, url=url)
    information_gathering.gather_information()
    # INFORMATION ANALYSIS
    PhaseOneAnalysis(project_id=project_id, url=url, thread_semaphore=thread_semaphore,
                                            database_semaphore=database_semaphore, connection=connection)


def main():
    print("Siva Vulnerability Scanner v1.0")
    password = getpass.getpass()
    try:
        connection = pymysql.connect(host="localhost", user="root", password=password,
                                     db="siva")
    except pymysql.err.OperationalError:
        print("[-] WRONG PASSWORD. EXITING...")
        sys.exit()
    project_id = int(input("Project ID: "))
    url = input("URL: ")
    scheme = URL().get_scheme(url)
    host_name = URL().get_host_name(url)
    project_url = scheme + "://" + host_name
    if SivaDB().create_project(connection=connection, project_id=project_id, url=project_url):
        check_for_vulnerabilities(connection, project_id, url)
    else:
        print("Cannot be scanned!")



if __name__ == "__main__":
    main()

