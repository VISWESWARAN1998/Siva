# SWAMI KARUPPASWAMI THUNNAI

import socket
import pymysql
import threading
from information_gathering_phase1 import web_server_informtaion
from siva_db import SivaDB
from url.URL import URL


def check_for_vulnerabilities(connection, project_id, url):
    """First phase of Information gathering"""
    thread_semaphore = threading.Semaphore(100)
    database_semaphore = threading.Semaphore(100)
    information_gathering = web_server_informtaion.WebServerInformation(project_id=project_id, connection=connection,
                                                                        thread_semaphore=thread_semaphore,
                                                                        database_semaphore=database_semaphore, url=url)
    information_gathering.gather_information()

def scan(project_id, url):
    connection = pymysql.connect(host="localhost", user="root", password="YOUR PASSWORD HERE",
                                 db="siva")
    project_id = project_id
    url = url
    scheme = URL().get_scheme(url)
    host_name = URL().get_host_name(url)
    project_url = scheme + "://" + host_name
    if SivaDB().create_project(connection=connection, project_id=project_id, url=project_url):
        check_for_vulnerabilities(connection, project_id, url)
    else:
        print("Cannot be scanned!")

def main():
    print("Siva Vulnerability Scanner v0.1")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = int(input("Enter the port: "))
    server.bind(("127.0.0.1", port))
    server.listen(5)
    while True:
        client, address = server.accept()
        message = client.recv(4000)
        parameters = message.decode("utf-8")
        parameters = parameters.split(" ")
        project_id = parameters[0]
        url = parameters[1]
        scan(project_id, url)
        server.close()
        break



if __name__ == "__main__":
    main()

