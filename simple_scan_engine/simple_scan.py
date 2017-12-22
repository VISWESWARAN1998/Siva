# SWAMI KARUPPASWAMI THUNNAI

from threading import Thread
from url.URL import URL
from user_agent import UserAgent
from bs4 import BeautifulSoup
from client_side_bypass.input import InputAnomaly
from data_stores.sql.sql_injection import GetBasedSQLInjection


class SimpleScan:
    """
    Description:
    ------------
    This class is used the url for individual vulnerabilities. This class will not find complex loop holes.
    """
    __project_id = None
    __thread_sempahore = None
    __database_semaphore = None
    __connection = None
    __url = None
    __requests_object = None
    __soup_object = None
    __poc_object = None
    __banned_extensions = [".exe", ".jpg", ".png", ".mp4", ".pdf", ".mp3", ".zip"]

    __banned_names = ["drop", "delete", "erase", "reset", "remove", "clear"]

    def __init__(self, project_id, thread_semaphore, database_semaphore, url,
                 connection, poc_object):
        self.__project_id = project_id
        self.__thread_sempahore = thread_semaphore
        self.__database_semaphore = database_semaphore
        self.__connection = connection
        self.__url = url
        self.__poc_object = poc_object
        if self.is_url_banned(self.__url) == False:
            self.run()

    def run(self):
        self.__requests_object = URL().get_request(
            url=self.__url, user_agent=UserAgent.get_user_agent())
        self.__soup_object = BeautifulSoup(self.__requests_object.content,
                                           "html.parser")
        # By now we have got the requests object and soup object
        #================== SQL Injection Test ====================
        sqli_thread = Thread(target=self.check_sql_injection)
        sqli_thread.start()
        # ================= HTML VULNERABILITIES ============
        self.check_html_vulnerabilities()

    def is_url_banned(self, url):
        """
        Description:
        ------------
        This method will check whether the URL is banned ot not.
        Note: Soon this method will be ported to some other class
        -----
        :param url: the URL which is about to be checked
        :return: True if the url is banned
        """
        for banned_name in self.__banned_names:
            if banned_name in self.__url:
                print("[*] This name is banned, So wont proceed to check")
                return True
        for banned_extension in self.__banned_extensions:
            if banned_extension in self.__url:
                print("[i] ", banned_extension.upper(), " is banned")
                return True
        return False

    def check_sql_injection(self):
        """
        Description:
        ------------
        This method is used to check the SQL injection
        :return:
        """
        GetBasedSQLInjection(
            project_id=self.__project_id,
            thread_semaphore=self.__thread_sempahore,
            database_semaphore=self.__database_semaphore,
            soup_object=self.__soup_object,
            url=self.__url,
            connection=self.__connection,
            poc_object=self.__poc_object)

    def check_html_vulnerabilities(self):
        InputAnomaly(project_id=self.__project_id, thread_semaphore=self.__thread_sempahore, database_semaphore=self.__database_semaphore,
                     connection=self.__connection, soup_object=self.__soup_object, url=self.__url)
