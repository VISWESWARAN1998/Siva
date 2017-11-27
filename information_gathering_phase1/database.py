# SWAMI KARUPPASWAMI THUNNAI

"""
This class is the one and the only class which has the access to information gathering table
"""

import pymysql


class InfoGatheringPhaseOneDatabase:
    """
    This class is used to add information and retrieve information from the info gathering
    table
    """

    @staticmethod
    def add_info_gathering_phase_one(database_semaphore, connection, query, arguments):
        """
        :param connection: The mysql connection object
        :param query: the sql query
        :param arguments: parameters for the sql query
        :param database_semaphore: a semaphore to control the threads
        :return:
        """
        database_semaphore.acquire()
        try:
            cursor = connection.cursor()
            cursor.execute(query, arguments)
            connection.commit()
            print("[+] ADDED INFORMATION SUCCESSFULLY")
        except Exception as e:
            print("[-] CANNOT ADD THE INFORMATION TO THE DATABASE")
        finally:
            database_semaphore.release()  # No matter what happens release the semaphore

    @staticmethod
    def get_info_gathering_phase_one(project_id, connection):
        """
        This method is used to get all the information from phase 1
        :param project_id:
        :param connection:
        :return:
        """
        try:
           cursor = connection.cursor()
           query = "select * from info_gathering where project_id=%s limit 1"
           cursor.execute(query, (project_id,))
           result = cursor.fetchall()
           if len(result) == 0:
               return None
           return result
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def update_status(database_semaphore, connection, project_id, status):
        """
        Used to update the ip address in the info gathering database
        :param database_semaphore:
        :param connection:
        :param project_id:
        :param status:
        :return: None
        """
        database_semaphore.acquire()
        try:
           cursor = connection.cursor()
           query = "update info_gathering set status=%s where project_id=%s"
           cursor.execute(query, (status, project_id))
           connection.commit()
           print("[+] STATUS HAS BEEN UPDATED SUCCESSFULLY")
        except Exception as e:
            print(e)
        database_semaphore.release()

    @staticmethod
    def update_ip(database_semaphore, connection, project_id, new_ip):
        """
        Used to update the ip address in the info gathering database
        :param database_semaphore:
        :param connection:
        :param project_id:
        :param new_ip:
        :return: None
        """
        database_semaphore.acquire()
        try:
           cursor = connection.cursor()
           query = "update info_gathering set ip=%s where project_id=%s"
           cursor.execute(query, (new_ip, project_id))
           connection.commit()
           print("[+] I.P ADDRESS HAS BEEN UPDATED SUCCESSFULLY")
        except Exception as e:
            print(e)
        database_semaphore.release()

    @staticmethod
    def update_webserver_name(database_semaphore, connection, project_id, new_webserver_name):
        """
        Used to update the ip address in the info gathering database
        :param database_semaphore:
        :param connection:
        :param project_id:
        :param new_webserver_name:
        :return: None
        """
        database_semaphore.acquire()
        try:
           cursor = connection.cursor()
           query = "update info_gathering set webserver_name=%s where project_id=%s"
           cursor.execute(query, (new_webserver_name, project_id))
           connection.commit()
           print("[+]WEBSERVER NAME HAS BEEN UPDATED SUCCESSFULLY")
        except Exception as e:
            print(e)
        database_semaphore.release()

    @staticmethod
    def update_server_os(database_semaphore, connection, project_id, server_os):
        """
        Used to update the ip address in the info gathering database
        :param database_semaphore:
        :param connection:
        :param project_id:
        :param server_os:
        :return: None
        """
        database_semaphore.acquire()
        try:
           cursor = connection.cursor()
           query = "update info_gathering set server_os=%s where project_id=%s"
           cursor.execute(query, (server_os, project_id))
           connection.commit()
           print("[+] SERVER OS HAS BEEN UPDATED SUCCESSFULLY")
        except Exception as e:
            print(e)
        database_semaphore.release()

    @staticmethod
    def update_programming_language(database_semaphore, connection, project_id, programming_language):
        """
        Used to update the ip address in the info gathering database
        :param database_semaphore:
        :param connection:
        :param project_id:
        :param programming_language:
        :return: None
        """
        database_semaphore.acquire()
        try:
           cursor = connection.cursor()
           query = "update info_gathering set programming_language=%s where project_id=%s"
           cursor.execute(query, (programming_language, project_id))
           connection.commit()
           print("[+] PROGRAMMING LANGUAGE HAS BEEN UPDATED SUCCESSFULLY")
        except Exception as e:
            print("Exception: ")
            print(e)
        database_semaphore.release()

    @staticmethod
    def update_firewall(database_semaphore, connection, project_id, firewall_name):
        """
        Used to update the ip address in the info gathering database
        :param database_semaphore:
        :param connection:
        :param project_id:
        :param firewall_name:
        :return: None
        """
        database_semaphore.acquire()
        try:
           cursor = connection.cursor()
           query = "update info_gathering set firewall_name=%s where project_id=%s"
           cursor.execute(query, (firewall_name, project_id))
           connection.commit()
           print("[+] FIREWALL HAS BEEN UPDATED SUCCESSFULLY")
        except Exception as e:
            print(e)
        database_semaphore.release()