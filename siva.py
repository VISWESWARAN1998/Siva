# SWAMI KARUPPASWAMI THUNNAI

import sys
import pymysql
import threading
from information_gathering_phase1 import web_server_informtaion
from information_analysis.phase_one_analysis import PhaseOneAnalysis
from information_analysis.phase_two_analysis import PhaseTwoAnalysis
from siva_db import SivaDB
from url.URL import URL
import getpass
from information_gathering_phase1.database import InfoGatheringPhaseOneDatabase
from information_gathering_phase2.host_discovery import PortScan
from locals.directory import Directory
from information_gathering_phase3.info_gathering_phase_three import InfoGatheringPhasethree
from information_gathering_phase4.info_gathering_phase_four import InfoGatheringPhaseFour
from information_analysis.phase_three_analysis import PhaseThreeAnalysis


def check_for_vulnerabilities(connection, project_id, url):
    """First phase of Information gathering"""
    thread_semaphore = threading.Semaphore(100)
    database_semaphore = threading.Semaphore(100)

    # =========================== INFORMATION GATHERING PHASE - 1 =====================
    print("[*] Gathering PHASE-1 INFORMATION")
    information_gathering = web_server_informtaion.WebServerInformation(project_id=project_id, connection=connection,
                                                                        thread_semaphore=thread_semaphore,
                                                                        database_semaphore=database_semaphore, url=url)
    information_gathering.gather_information()
    SivaDB.update_result(connection=connection, project_id=project_id, phase_id="IG-PHASE-1")

    # =====================  INFORMATION ANALYSIS PHASE - 1 =============================
    PhaseOneAnalysis(project_id=project_id, url=url, thread_semaphore=thread_semaphore,
                                            database_semaphore=database_semaphore, connection=connection)
    SivaDB.update_result(connection=connection, project_id=project_id, phase_id="IA-PHASE-1")

    # =========================  IG PHASE - 2 HOST - DISCOVERY =================
    print("[+] INFORMATION GATHERING PHASE-2 HAS BEEN STARTED")
    result = InfoGatheringPhaseOneDatabase.get_info_gathering_phase_one(project_id=project_id,
                                                                        connection=connection)
    if result is not None:
        result = result[0]
        ip = result[2]
        firewall_name = result[6]
    if firewall_name == "None":
        port_scan = PortScan(project_id=project_id, ip=ip, connection=connection, thread_semaphore=thread_semaphore, database_semaphore=database_semaphore)
        port_scan.scan()
    SivaDB.update_result(connection=connection, project_id=project_id, phase_id="IG-PHASE-2")

    # =========================== INFORMATION GATHERING PHASE - 3 ============================
    print("[+] INFORMATION GATHERING PHASE-3 HAS BEEN STARTED")
    InfoGatheringPhasethree(project_id=project_id, url=url, thread_semaphore=thread_semaphore)
    SivaDB.update_result(connection=connection, project_id=project_id, phase_id="IG-PHASE-3")

    # ============================ INFORMATION ANALYSIS PHASE - 2 ===========================
    print("[+] INFORMATION ANALYSIS PHASE - 2 HAS BEEN STARTED")
    PhaseTwoAnalysis(project_id=project_id, url=url, thread_semaphore=thread_semaphore,
                     database_semaphore=database_semaphore, connection=connection)
    SivaDB.update_result(connection=connection, project_id=project_id, phase_id="IA-PHASE-2")

    # ============================ INFORMATION ANALYSIS PHASE - 3 ==========================
    print("[+] INFORMATION ANALYSIS PHASE - 3 HAS BEEN STARTED")
    info_result = InfoGatheringPhaseOneDatabase.get_info_gathering_phase_one(project_id=project_id,
                                                                        connection=connection)
    webserver_name = None  # At this stage we should have the name of the webserver
    programming_language = None # and also the name of the programming language
    info_result = info_result[0]
    if info_result is not None:
        webserver_name = info_result[3]
        programming_language = info_result[5]
    PhaseThreeAnalysis(project_id=project_id, webserver_name=webserver_name, programming_language=programming_language,
                       thread_semaphore=thread_semaphore, database_semaphore=database_semaphore)

    # ============================= INFORMATION GATHERING PHASE - 4 =========================
    print("[+] INFORMATION GATHERING PHASE - 4 HAS BEEN STARTED")
    InfoGatheringPhaseFour(project_id=project_id, url=url, thread_semaphore=thread_semaphore,
                           database_semaphore=database_semaphore, connection=connection)
    SivaDB.update_result(connection=connection, project_id=project_id, phase_id="IG-PHASE-4")





def main():
    print("Siva Vulnerability Scanner v1.0")
    user_name = input("USER NAME: ")
    password = getpass.getpass()
    try:
        connection = pymysql.connect(host="localhost", user=user_name, password=password,
                                     db="siva")
    except pymysql.err.OperationalError:
        print("[-] WRONG PASSWORD. EXITING...")
        sys.exit()
    project_id = int(input("Project ID: "))
    url = input("URL: ")
    scheme = URL().get_scheme(url)
    host_name = URL().get_host_name(url)
    project_url = scheme + "://" + host_name
    Directory.create_directory("projects")  # create projects for stroing files from remote host to your local PC
    Directory.create_directory("projects/project-" + str(project_id)) # and create a working directory for the project
    if SivaDB().create_project(connection=connection, project_id=project_id, url=project_url):
        check_for_vulnerabilities(connection, project_id, url)
    else:
        print("Cannot be scanned!")



if __name__ == "__main__":
    commands = sys.argv
    if len(commands) == 1:
        main()
    if len(commands) == 2:
        command = commands[1]
        if command == "install":
            SivaDB().install()

