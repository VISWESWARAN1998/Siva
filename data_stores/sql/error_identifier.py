# SWAMI KARUPPASWAMI THUNNAI
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# =============================================
# Siva Vulnerability Scanner v0.4
# Copyright 2017, Visweswaran Nagasivam
# Date: 02.12.201
# Author: Visweswaran Nagasivam
# email: visweswaran.nagasivam98@gmail.com
# This class is used to comapare two beautifulsoup
# objects and it will tell whether the resulting page contains sql SQL
# errors. This is the actual class which is going to inform
# SQL vulnerability in the url and going to update in the database
# =============================================

from siva_db import SivaDB
from crypto.oneway import Hash
from data_stores.sql.database import SQLInjectionDatabase


class SQLErrorIdentifier:
    __project_id = None
    __original_url = None
    __payloaded_url = None
    __original_soup_object = None
    __payloaded_soup_object = None
    __thread_semaphore = None
    __database_semaphore = None
    __connection = None
    __is_exception_present = False
    __description = ""
    __poc_object = None
    # These are the individual unique mysql error strinsg which are collecyed upon the reseach of
    # quiet good vulnerable websites.
    __mysql_errors = [
        "mysql_select_db()", "mysql_close()",
        "supplied argument is not a valid MySQL-Link resource",
        "mysql_fetch_assoc()", "mysql_free_result()", "mysql_query()",
        "mysql_result()", "mysql_close()", "mysql_connect()",
        "mysql_select_db()", "mysql_fetch_object()", "mysql_fetch_array()",
        "Access denied for user",
        "Can't connect to local MySQL server through socket",
        "expects parameter 1 to be resource",
        "You have an error in your SQL syntax", "mysql_num_rows()",
        "supplied argument is not a valid MySQL result"
    ]

    __mariadb_errors = [
        "You have an error in your SQL syntax", "MariaDB server version"
    ]

    __mssql_errors = [
        "Server Error in '/' Application", "CloseConnection()",
        "Unclosed quotation mark after the character string",
        "System.Data.SqlClient.SqlConnection.OnError", "SqlException",
        "System.Data.SqlClient", "System.Data.Common.DbCommand",
        "System.Data.Common.DbDataAdapter", "SqlDataReader", "SqlCommand"
    ]

    def __init__(self, project_id, thread_semaphore, database_semaphore,
                 original_url, payloaded_url, original_soup_object,
                 payloaded_soup_object, connection, poc_object):
        self.__project_id = project_id
        self.__thread_semaphore = thread_semaphore
        self.__database_semaphore = database_semaphore
        self.__original_url = original_url
        self.__payloaded_url = payloaded_url
        self.__original_soup_object = original_soup_object
        self.__payloaded_soup_object = payloaded_soup_object
        self.__connection = connection
        self.__poc_object = poc_object
        # Now check for the vulnerability
        self.__check_vulnerability()

    def __check_vulnerability(self):
        """
        This method is used to check for the SQL vulnerability by comparing two soup objects
        :return: None
        """
        for original_soup_object, payloaded_soup_object in zip(
                self.__original_soup_object, self.__payloaded_soup_object):
            try:
                if str(original_soup_object) != str(payloaded_soup_object):
                    if self.__is_mysql_error(payloaded_soup_object):
                        print("[+] SQL VULNERABILITY IN MYSQL DATABASE")
                        print("[+] PAYLOAD: ", self.__payloaded_url)
                        self.__is_exception_present = True
                        self.__description = "MYSQL SQL VULNERABILITY"
                    elif self.__is_mariadb_error(payloaded_soup_object):
                        print("[+] SQL VULNERABILITY IN MARIADB DATABASE")
                        print("[+] PAYLOAD: ", self.__payloaded_url)
                        self.__is_exception_present = True
                        self.__description = "MARIADB SQL VULNERABILITY"
                    elif self.__is_mssql_error(payloaded_soup_object):
                        print("[+] SQL VULNERABILITY IN MSSQL DATABASE")
                        print("[+] PAYLOAD: ", self.__payloaded_url)
                        self.__is_exception_present = True
                        self.__description = "MSSQL SQL VULNERABILITY"
            except Exception as e:
                print(
                    "[+] EXCEPTION HAS OCCURED WHICH HAS BEEN SAFETLY HANDLED")
        if self.__is_exception_present:
            # ================ ADD THE INFO TO THE DATABASE ===============
            SivaDB.update_analysis(
                connection=self.__connection,
                database_semaphore=self.__database_semaphore,
                project_id=self.__project_id,
                method="GET",
                source=self.__original_url,
                payload=self.__payloaded_url,
                description=self.__description)
            # ================= CREATE PROOF OF CONCEPT ===================
            self.__poc_object.set_file_name(
                Hash.get_sha2(self.__payloaded_url)
            )  # save the file name as the sha2 of the payloaded url for the local copy
            self.__poc_object.set_project_id(self.__project_id)
            self.__poc_object.set_url(self.__payloaded_url)
            self.__poc_object.simple_snapshot()
            # ================= SET THE NAME OF THE DATABASE ==============
            if "MYSQL" in self.__description:
                SQLInjectionDatabase.data_base_name = "MYSQL"
            elif "MARIADB" in self.__description:
                SQLInjectionDatabase.data_base_name = "MARIADB"
            elif "MSSQL" in self.__description:
                SQLInjectionDatabase.data_base_name = "MSSQL"

    def __is_mysql_error(self, error_message):
        """
        Description:
        -------------
        This method will check if the errror is mysql error
        Parameters:
        -----------
        :param error_message: The error message to be checked
        :return: Will return true if the error message is a valid mysql error message
        """
        error_message = str(error_message)
        for mysql_error in self.__mysql_errors:
            if mysql_error in error_message:
                return True
        return False

    def __is_mariadb_error(self, error_message):
        """
        Description:
        -------------
        This method will check if the errror is mariadb error
        Parameters:
        -----------
        :param error_message: The error message to be checked
        :return: Will return true if the error message is a valid mysql error message
        """
        error_message = str(error_message)
        for mariadb_error in self.__mariadb_errors:
            if mariadb_error in error_message:
                return True
        return False

    def __is_mssql_error(self, error_message):
        """
        Description:
        -------------
        This method will check if the errror is mssql error
        Parameters:
        -----------
        :param error_message: The error message to be checked
        :return: Will return true if the error message is a valid mysql error message
        """
        error_message = str(error_message)
        for mssql_error in self.__mssql_errors:
            if mssql_error in error_message:
                return True
        return False
