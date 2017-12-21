# SWAMI KARUPPASWAMI THUNNAI
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ===================================
# COPYRIGHT (C), 2017 TO VISWESWARAN NAGASIVAM
# THIS CLASS WILL HELP TO GENERATE A RESULT OF THE PROJECT
# WITH A STATIC HTML FILE
# ==============================================

import sys
import pymysql
from siva_database.database import Database


class ResultGenerator:
    """
    This class is used to generate the HTML string
    which is saved as index.html in the project directory.
    """
    __result_string = """
    <html>
    <head>
    <title>Siva Results</title>
    </head>
    <body>
    <centre>
    <h3>Siva Web Vulnerability Scanner v0.4 Results</h3>
    </centre>
    
    """
    __connection = None

    def __init__(self, connection):
        self.__connection = connection

    def generate_result(self, project_id):
        """
        Description:
        -------------
        This one long method will generate the HTML result with the project id
        :param project_id: The project id for which the result is to be generated.
        :return: None
        """
        project_details = Database(
            self.__connection).get_project_details(project_id=project_id)
        if project_details is None:
            print("[+] INVALID PROJECT")
            sys.exit(-1)


"""
if __name__ == "__main__":
    username = "visweswaran"
    password = "12345"
    connection = pymysql.connect(
        host="localhost", user=username, password=password, db="siva")
    gen = ResultGenerator(connection).generate_result(-1)
"""
