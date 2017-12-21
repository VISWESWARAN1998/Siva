# SWAMI KARUPPASWAMI THUNNAI
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# =================================
# Author: Visweswaran Nagasivam
# Email: visweswaran.nagasivam98@gmail.com
# Copyright(C): 2017
# This class will make find if there is any hidden transmission of
# data via input tag with type hidden
# Reference: see references.txt about bypassing client side controls
# ==================================

from siva_db import SivaDB


class HiddenFieldFinder:
    __project_id = None
    __thread_semaphore = None
    __database_semaphore = None
    __connection = None
    __url = None
    __soup_object = None

    def __init__(self, project_id, thread_semaphore, database_semaphore,
                 connection, url, soup_object):
        self.__project_id = project_id
        self.__thread_semaphore = thread_semaphore
        self.__database_semaphore = database_semaphore
        self.__connection = connection
        self.__url = url
        self.__soup_object = soup_object

    def find_hidden_feilds(self):
        self.__thread_semaphore.acquire(5)
        for i in self.__soup_object.find_all("input"):
            try:
                if i["type"] == "hidden":
                    print("[+] HIDDEN VALUE IS SILENTLY TRANSMITTED")
                    SivaDB.update_analysis(
                        connection=self.__connection,
                        database_semaphore=self.__database_semaphore,
                        method="GET",
                        source=self.__url,
                        project_id=self.__project_id,
                        payload=str(i),
                        description="HIDDEN VALUE TRANSMITTED")
            except KeyError:
                print()
        self.__thread_semaphore.release()
