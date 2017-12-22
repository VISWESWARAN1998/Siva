# SWAMI KARUPPASWAMI THUNNAI
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# =================================
# Author: Visweswaran Nagasivam
# Email: visweswaran.nagasivam98@gmail.com
# Copyright(C): 2017
# This class will make find the anomale present in the input tags.
# Reference: see references.txt about bypassing client side controls
# Note: These may not be the actual vulnerabilities, but it has greater risk
# of exploitation when it is not handled properly.
# ==================================

from siva_db import SivaDB

class InputAnomaly:
    __project_id = None
    __thread_semaphore = None
    __database_semaphore = None
    __connection = None
    __url = None
    __soup_object = None

    def __init__(self, project_id, thread_semaphore, database_semaphore, connection, url, soup_object):
        self.__project_id = project_id
        self.__thread_semaphore = thread_semaphore
        self.__database_semaphore = database_semaphore
        self.__connection = connection
        self.__url = url
        self.__soup_object = soup_object
        if self.__soup_object is not None:
            self.find_hidden_feilds()
            self.find_max_length()

    def find_hidden_feilds(self):
        """
        Description:
        ------------
        This method will check if the input value gets silently transmitted
        to the remote host.

        Example:
        --------
        <input type="hidden" name="amount" value="500">
        In the above code 500 gets transimitted from the client which is hidden to the user but could
        be bypassed.
        :return: None
        """
        self.__thread_semaphore.acquire(5)  # time out is set for five seconds
        for i in self.__soup_object.find_all("input"):
            try:
                if i["type"] == "hidden":
                    print("[+] HIDDEN VALUE IS SILENTLY TRANSMITTED")
                    SivaDB.update_analysis(connection=self.__connection, database_semaphore=self.__database_semaphore,
                                           method="GET", source=self.__url, project_id=self.__project_id,
                                           payload=str(i), description="HIDDEN VALUE TRANSMITTED")
            except KeyError:
                print()
            except Exception:
                print()
        self.__thread_semaphore.release()

    def find_max_length(self):
        """
        Description:
        ------------
        This method will check if the input value has maxlength tag, We can see what happens if the maximum
        length is exceeded which could be a vlunerablity.
        """
        self.__thread_semaphore.acquire(5)  # time out is set for five seconds
        for i in self.__soup_object.find_all("input"):
            try:
                if i["maxlength"]:
                    print("[+] There is a maximum length limit for this input tag!")
                    SivaDB.update_analysis(connection=self.__connection, database_semaphore=self.__database_semaphore,
                                           method="GET", source=self.__url, project_id=self.__project_id,
                                           payload=str(i), description="MAX LENGTH LIMIT FOUND")
            except Exception:
                print()
        self.__thread_semaphore.release()


