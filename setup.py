import subprocess
import pymysql
import os
import siva
import sys


def is_service_running(name):
    with open(os.devnull, 'wb') as hide_output:
        exit_code = subprocess.Popen(['service', name, 'status'], stdout=hide_output, stderr=hide_output).wait()
        return exit_code == 0


def setup_linux():
    """This method is used to create the necessary workspace for the first run in Linux Operating System
    """
    if not is_service_running('mysql'):
        print('[+] Mysql is not Running')
        print('[+] Please start the MySql service and Try Again ! Eg.[service mysql start]')

    else:
        print("[+] Mysql is Running ")
        connection = pymysql.connect(host="127.0.0.1", user=str(input("[+] Enter the MySql username : ")),
                                     password=str(input("[+] Enter the MySql password : ")))
        cursor = connection.cursor()
        try:
            cursor.execute('create database siva;')
            cursor.execute('use siva;')
            cursor.execute('create table project (project_id int(10) primary key, domain varchar(100));')
            cursor.execute('create table info_gathering(project_id int(10) primary key,status varchar(100),'
                           'ip varchar(50),webserver_name  varchar (150), server_os varchar (100), '
                           'programming_language varchar(150), firewall_name varchar (150));')
            print("""[+] Successfully Created the Database... ! 
                     [+] Happy Hacking :)
            
            """)
            siva.main()

        except pymysql.err.ProgrammingError:
            print("Database exists already !")
            print("""[+] Opening the Source file... {siva.py}
                     [+] Happy Hacking :)
            
            """)
            siva.main()


if __name__ == "__main__":
    if sys.platform == "linux":
        setup_linux()
    else:
        pass
