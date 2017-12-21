# SWAMI KARUPPASWAMI THUNNAI

from url.query import Query
from url.URL import URL
from user_agent import UserAgent
from bs4 import BeautifulSoup
from data_stores.sql.error_identifier import SQLErrorIdentifier
from siva_db import SivaDB


class GetBasedSQLInjection:
    """
    Description:
    ------------
    This class is used to check if the web url is vulnarable is Vulnerable to SQL injection or not.
    This class mostly covers the vulnerability on the get request.
    Reference on what is SQL injection:
    -----------------------------------
    https://en.wikipedia.org/wiki/SQL_injection
    """
    __project_id = None
    __url = None
    __thread_semaphore = None
    __database_semaphore = None
    __connection = None
    __soup_object = None  # If BeautifulSoup object is present it would be nice
    __poc_object = None
    __sqli_vuln_urls = []  # This will be the list of lists

    def __init__(self, project_id, url, thread_semaphore, database_semaphore,
                 soup_object, connection, poc_object):
        self.__project_id = project_id
        self.__url = url
        self.__thread_semaphore = thread_semaphore
        self.__database_semaphore = database_semaphore
        self.__connection = connection
        self.__poc_object = poc_object
        # NOTE: self.__soup_object is the original unaltered BeautifulSoup object
        if soup_object is not None:
            self.__soup_object = soup_object
        else:
            r = URL().get_request(
                url=self.__url, user_agent=UserAgent.get_user_agent())
            self.__soup_object = BeautifulSoup(r.content, "html.parser")
        if URL.is_query_present(self.__url):
            self.__check_escape_sequence_vulnerability()
            self.__check_numerical_vulnerability()

    def __check_escape_sequence_vulnerability(self):
        """
        Description:
        ------------
        We will append a single quote (') to check if the sql vulnerability is happended or not
        :return:
        """
        # We will append ' to all the individual parameters and store it to payloaded urls
        self.__thread_semaphore.acquire()
        payloaded_urls = Query().append_payload_to_all_queries(
            url=self.__url, payload="'")
        for payloaded_url in payloaded_urls:
            print(payloaded_url)
            r = URL().get_request(
                url=payloaded_url, user_agent=UserAgent.get_user_agent())
            if r is not None:
                new_soup_object = BeautifulSoup(r.content, "html.parser")
                # Now compare bot soup objects
                SQLErrorIdentifier(
                    project_id=self.__project_id,
                    thread_semaphore=self.__thread_semaphore,
                    database_semaphore=self.__database_semaphore,
                    original_soup_object=self.__soup_object,
                    payloaded_soup_object=new_soup_object,
                    original_url=self.__url,
                    payloaded_url=payloaded_url,
                    connection=self.__connection,
                    poc_object=self.__poc_object)
        self.__thread_semaphore.release()

    def __check_numerical_vulnerability(self):
        """
        Description:
        -----------
        This method is used to check the numerical SQL vulnerability in the give url.
        See:
        -----
        Numerical Vulnerability in references.txt
        :return: None
        """
        self.__thread_semaphore.acquire()
        payloaded_urls = Query.add_one(self.__url)
        for payloaded_url in payloaded_urls:
            r = URL().get_request(
                url=payloaded_url, user_agent=UserAgent.get_user_agent())
            if r is not None:
                new_soup_object = BeautifulSoup(r.content, "html.parser")
                if self.__soup_object == new_soup_object:
                    print("[+] NUMERICAL VULNERABILITY FOUND IN THE DATABASE")
                    print("[+] PAYLOAD: ", payloaded_url)
                    SivaDB.update_analysis(
                        connection=self.__connection,
                        database_semaphore=self.__database_semaphore,
                        project_id=self.__project_id,
                        method="GET",
                        source=self.__url,
                        payload=payloaded_url,
                        description="NUMERICAL VULNERABILITY")
        self.__thread_semaphore.release()
