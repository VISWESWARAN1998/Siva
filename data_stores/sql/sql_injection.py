# SWAMI KARUPPASWAMI THUNNAI

from url.query import Query
from url.URL import URL

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
    __session = None  # This will be our requests session
    __url = None
    __thread_semaphore = None
    __database_semaphore = None
    __soup_object = None  # If BeautifulSoup object is present it would be nice
    __sqli_vuln_urls = []  # This will be the list of lists

    def __init__(self, project_id, session, url, thread_semaphore, database_semaphore, soup_object):
        self.__project_id = project_id
        self.__session = session
        self.__url = url
        self.__thread_semaphore = thread_semaphore
        self.__database_semaphore = database_semaphore
        self.__soup_object = soup_object

    def check_escape_sequence_vulnerability(self):
        """
        Description:
        ------------
        We will append a single quote (') to check if the sql vulnerability is happended or not
        :return:
        """
        # We will append ' to all the individual parameters and store it to payloaded urls
        self.__thread_semaphore.acquire()
        print("[+] CHECKING ESCAPE SEQUENCE VULNERABILITY")
        payloaded_urls = Query().append_payload_to_all_queries(url=self.__url, payload="'")
        for payloaded_url in payloaded_urls:
            print(payloaded_url)
        self.__thread_semaphore.release()


