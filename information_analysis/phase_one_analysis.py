# SWAMI KARUPPASWAMI THUNNAI

from urllib.parse import urlparse
from information_gathering_phase1.database import InfoGatheringPhaseOneDatabase
from information_analysis.whois import WhoIs
from url.URL import URL
from user_agent import UserAgent
from bs4 import BeautifulSoup
from threading import Thread

class PhaseOneAnalysis:
    """
    Description:
    ============
    This class is used to analyse the information of the phase one analysis.
    Wiki:
    =====
    1. It check once again for firewalls if it is missing
    2. It will try to get the programming language if the language is missing
    """
    __project_id = None
    __domain = None
    __thread_semaphore = None
    __database_semaphore = None
    __connection = None
    __ip = None
    __webserver_name = None
    __server_os = None
    __programming_language_used = None
    __firewall_name = None

    def __init__(self, project_id, url, thread_semaphore, database_semaphore, connection):
        """
        :param project_id: The id of the project
        :param thread_semaphore: The semaphore of the project
        :param database_semaphore: The semaphore of the database
        :param connection:
        """
        print("[+] ANALYSIS OF PHASE ONE HAS BEEN STARTED")
        self.__project_id = project_id
        self.__url = url
        self.__thread_semaphore = thread_semaphore
        self.__database_semaphore = database_semaphore
        self.__connection = connection
        self.__domain = urlparse(url=url).netloc
        self.__domain = self.__domain.replace("www.", "")
        # Now we will load the information gathered from the phase-1 of IG
        self.__load_phase_one_info()
        if self.__firewall_name == "None":
            self.__check_firewalls()
        if self.__programming_language_used == "None":
            get_prog_lang_thread = Thread(target=self.__check_programming_language, args=(url,))
            get_prog_lang_thread.start()
            get_prog_lang_thread.join()
        print("[*] ANALYSIS RESULT")
        print("Firewall: ", self.__firewall_name)
        print("Language: ", self.__programming_language_used)


    def __load_phase_one_info(self):
        """
        Description:
        ============
        This method is used to load the information from the phase one
        to the respective attributes
        :return:
        """
        result = InfoGatheringPhaseOneDatabase.get_info_gathering_phase_one(project_id=self.__project_id, connection=self.__connection)
        if result is not None:
            result = result[0] # result will deliver tuple of tuples so we need only the first one since we used limit 1
            # e.g (project_id, status, ip, webserver_name, server_os, programming_language, firewall)
            self.__ip = result[2]
            self.__webserver_name =  result[3]
            self.__server_os = result[4]
            self.__programming_language_used = result[5]
            self.__firewall_name = result[6]
        else:
            print("[-] CANNOT ADD THE INFORMATION. PLEASE CHECK YOUR DATABASE")

    def __check_firewalls(self):
        """
        Description:
        ============
        This method will try its level best to try to get the name of the firewall
        for the remote host
        :return:
        """
        print("[+] Checking for firewalls...")
        firewall_list = []  # This will contain the list of firewall
        file = open("firewall_names.txt", "r")
        firewall_names = file.readlines()
        for firewall in firewall_names:
            firewall = firewall.replace("\n", "")
            if firewall[0] is not "#":
                firewall_list.append(firewall.strip())
        # Now we will get the whois information
        whois_info = WhoIs(domain=self.__domain).get_whois()
        if whois_info is not None:
            for firewall in firewall_list:
                if firewall in str(whois_info).lower():
                    self.__firewall_name = firewall.upper()
                    update_info = Thread(target=InfoGatheringPhaseOneDatabase.update_firewall,
                                         args=(
                                             self.__database_semaphore,
                                             self.__connection,
                                             self.__project_id,
                                             self.__firewall_name
                                         ))
                    update_info.start()
                    break
                if firewall in str(whois_info).lower():
                    break
        print("[+] Process completed for checking firewalls...")

    def __check_programming_language(self, url):
        """
        Description:
        ============
        This method will try its level best to get the name of the programming
        language used to build the website.
        Notes:
        ======
        This method will heavily used URL class from url package
        :return:
        """
        self.__thread_semaphore.acquire()
        print("[+] ANALYSING PROGRAMMING LANGUAGE")
        # These are the popular programming languages used for designing websites
        language_names = {
            ".php" : "PHP",
            ".jsp" : "JSP",
            ".asp" : "ASP",
            ".aspx": "ASPX",
            ".py"  : "PYTHON",
            ".pl"  : "PERL"
        }
        user_agent = UserAgent.get_user_agent()
        r = URL().get_request(url=url, user_agent=user_agent)
        if r is not None:
            soup = BeautifulSoup(r.content, "html.parser")
            for i in soup.find_all("a"):
                try:
                    partial_url = i.get("href")
                    if "http" not in partial_url:
                        new_url = URL.join_urls(url, partial_url)
                    else:
                        new_url = partial_url if URL.is_same_domain(url, new_url) else ""
                    file_name = URL.get_file_name(new_url)
                    for i in language_names:
                        if i in file_name:
                            self.__programming_language_used = language_names[i]
                            # Now we will update the programming language used into the database
                            InfoGatheringPhaseOneDatabase.update_programming_language(
                                                    self.__database_semaphore,
                                                    self.__connection,
                                                    self.__project_id,
                                                    self.__programming_language_used
                                                    )
                            break
                        if i in file_name:
                            break
                except Exception:
                    pass
        self.__thread_semaphore.release()