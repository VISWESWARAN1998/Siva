# SWAMI KARUPPASWAMI THUNNAI

import socket
from threading import Thread
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from information_gathering_phase1.database import InfoGatheringPhaseOneDatabase
from url.URL import URL
from user_agent import UserAgent


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
        # self.__domain is unused. consider remove it when testing is done.
        self.__domain = urlparse(url=url).netloc
        self.__domain = self.__domain.replace("www.", "")
        # Now we will load the information gathered from the phase-1 of IG
        self.__load_phase_one_info()
        if self.__programming_language_used == "None":
            get_prog_lang_thread = Thread(target=self.__check_programming_language, args=(url,))
            get_prog_lang_thread.start()
            get_prog_lang_thread.join()
        # If we cannot get the webserver name we will try this method
        if self.__firewall_name == "None":
            get_webserver_thread = Thread(target=self.__check_webserver_name)
            get_webserver_thread.start()
            get_webserver_thread.join()
        if self.__webserver_name is not None:
            if self.__server_os is None:
                if "Win" in self.__webserver_name:
                    self.__server_os = "Windows"
                elif "Uni" in self.__server_os:
                    self.__server_os = "Unix"
                elif "Lin" in self.__server_os:
                    self.__server_os = "Linux"
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

    def __check_webserver_name(self):
        self.__thread_semaphore.acquire()
        try:
            tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp_socket.connect((self.__ip, 80))  # connect to http port no 80
            tcp_socket.send("GET / HTTP/1.1\r\n\r\n".encode("utf-8"))
            result = tcp_socket.recv(4096)  # receive first 4096 bytes of information
            result = result.decode("utf-8")
            result = result.split("\r\n")
            for i in result:
                if "Server" in i:
                    i = i.replace("Server:", "")
                    i = i.strip()
                    self.__webserver_name = i  # we have obtained the server name
        except socket.error as e:
            print(e)
        except TypeError as e:
            print(e)
        except Exception as e:
            print(e)
        self.__thread_semaphore.release()