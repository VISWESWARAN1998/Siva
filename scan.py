# SWAMI KARUPPASWAMI THUNNAI

import pymysql
import threading
from information_gathering_phase1 import web_server_informtaion
from siva_db import SivaDB
from url.URL import URL


def check_for_vulnerabilities(connection, project_id, url):
    """First phase of Information gathering"""
    thread_semaphore = threading.Semaphore(100)
    database_semaphore = threading.Semaphore(100)
    print("[*] Gathering PHASE-1 INFORMATION")
    information_gathering = web_server_informtaion.WebServerInformation(project_id=project_id, connection=connection,
                                                                        thread_semaphore=thread_semaphore,
                                                                        database_semaphore=database_semaphore, url=url)
    information_gathering.gather_information()


def main():
    print("Siva Vulnerability Scanner v0.1")
    password = input("Enter the password: ")
    connection = pymysql.connect(host="localhost", user="root", password=password,
                                 db="siva")
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

