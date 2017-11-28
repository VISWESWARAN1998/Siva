# SWAMI KARUPPASWAMI THUNNAI

import codecs
from locals.file import File

class PhaseThreeAnalysis:
    """
    Description:
    ------------
    Exploit Database, is a huge database of exploits found on the operating system, http servers, programming language etc. [Note: This is a third party open-source project by offensive security]
    We will use this database to see whether any exploits are available for the websites to exploit.
    First of all get the exploit database as a csv file from here: https://github.com/offensive-security/exploit-database
    And download the files.csv so that perform an offline analysis.
    """
    __project_id = None
    __thread_semaphore = None
    __database_semaphore = None
    __webserver_name = None
    __programming_language = None
    __exploits = []

    def __init__(self, project_id, thread_semaphore, database_semaphore, webserver_name, programming_language):
        """
        :param project_id: The id for the project
        :param thread_semaphore: The semaphore for the no of threads used for the project
        :param webserver_name: The name of the webserver
        :param programming_language: The programming language itself
        :param database_semaphore: The semaphore for the count of the threads.
        """
        print("[+] PHASE - 3 ANALYSIS HAS BEEN STARTED")
        self.__project_id = project_id
        self.__thread_semaphore = thread_semaphore
        self.__database_semaphore = database_semaphore
        self.__webserver_name = webserver_name
        self.__programming_language = programming_language
        # Now get the exploits
        self.__get_info_from_exploit_db()
        # and store the local copy of the exploits
        print("[+] SAVING A LOCAL COPY OF EXPLOITS PRESENT IN THE WEBSITE")
        exploit_copy_loc = "projects/project-"+str(project_id)+"/exploits.txt"
        File.write_to_list(exploit_copy_loc, self.__exploits)


    def __get_info_from_exploit_db(self):
        """
        Dexscription:
        -------------
        This method is used to get the information from the exploit db
        :return:
        """
        with codecs.open("exploit_db.csv", encoding="utf-8") as exploit_db:
            for exploit in exploit_db:
                if self.__programming_language is not None:
                    if self.__programming_language in exploit:
                        self.__exploits.append(exploit)
                if self.__webserver_name is not None:
                    if self.__webserver_name in exploit:
                        self.__exploits.append(exploit)
        print("[+] TOTAL EXPLOITS FOUND: ", len(self.__exploits))
        # Now we will print the exploits to user
        for exploit in self.__exploits:
            try:
                print("[+]", exploit)
            except UnicodeEncodeError:
                print("[-] CANNOT DISPLAY, DUE TO UNICODE PROBLEM")
            except UnicodeDecodeError:
                print("[-] UNICODE DECODING PROBLEM OCCURED, CANNOT DISPLAY")