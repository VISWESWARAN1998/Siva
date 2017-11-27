# SWAMI KARUPPASWAMI THUNNAI

import os
from threading import Thread
from siva_db import SivaDB
from url.URL import URL

class PhaseTwoAnalysis:
    """
    Description:
    -------------
    This class is used to perform phase two analysis
    Steps Taken By This class:
    ---------------------------

    Note:
    -----
    All This is done in one single looping
    Result:
    ------
    You will get a preprocessed robots.txt file
    """
    __project_id = None
    __url = None
    __thread_semaphore = None
    __database_semaphore = None
    __connection = None
    __rep_list = None  # Robots Exclusion Protocol List
    __robots_path = None  # This will be the path to the robots.txt file
    __robots_preprocessed_file = None

    def __init__(self, project_id, url, thread_semaphore, database_semaphore, connection):
        self.__project_id = project_id
        self.__url = url
        self.__thread_semaphore = thread_semaphore
        self.__database_semaphore = database_semaphore
        self.__connection = connection
        self.__robots_path = "projects/project-"+str(project_id)+"/robots.txt"
        if os.path.exists(self.__robots_path):
            self.__robots_preprocessed_file = open("projects/project-"+str(project_id)+"/robots-preprocessed.txt", "w")
            preprocess_thread = Thread(target=self.__preprocess())
            preprocess_thread.start()
            preprocess_thread.join()
            self.__robots_preprocessed_file.close()
        else:
            print("[-] ROBOTS.TXT - NOT FOUND")


    def __preprocess(self):
        print("[+] PRE-PROCESSING ROBOTS.TXT")
        self.__thread_semaphore.acquire(timeout=10)
        robots_file = open(self.__robots_path, "r")
        robots_file_contents = robots_file.readlines()
        for content in robots_file_contents:
            content = content.replace("\n", "")
            content = content.strip()
            try:
                # If it is a comment
                if content[0] == "#":
                    SivaDB.update_raw_info(connection=self.__connection, project_id=self.__project_id,
                                           info_source="robots.txt", information=content,
                                           database_semaphore=self.__database_semaphore)
                else:
                    if "U" in content[0]:
                        self.__robots_preprocessed_file.write(content+"\n")
                    else:
                        if "D" in content[0]:
                            content = content.replace("Disallow:", "")
                            content = content.strip()
                            full_url = URL.join_urls(self.__url, content)
                            full_content = "Disallow: "+ full_url
                        elif "U" in content[0]:
                            content = content.replace("Allow:", "")
                            content = content.strip()
                            full_url = URL.join_urls(self.__url, content)
                            full_content = "Allow: "+full_url
                        self.__robots_preprocessed_file.write(full_content + "\n")
            except IndexError:
                self.__robots_preprocessed_file.write("\n")
        self.__thread_semaphore.release()
