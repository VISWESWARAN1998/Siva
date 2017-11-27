# SWAMI KARUPPASWAMI THUNNAI

import socket
from url.URL import URL
import requests
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from information_gathering_phase1.database import InfoGatheringPhaseOneDatabase
from user_agent import UserAgent


class WebServerInformation(InfoGatheringPhaseOneDatabase):
    """
    Description:
    =============
    This class is used to used to
    get some valuable information about the webserver
    Information gathered:
    =======================
    1. Web-Server Name, e.g Apache
    2. Remote Host Os, e.g Windows
    3. Programming Language Used, e.g PHP
    4. Presence of firewall like Cloudflare
    """
    __project_id = 0
    __connection = None
    __thread_semaphore = None
    __database_semaphore = None
    __url = None
    __ip = None
    __headers = None # request headers object
    __firewall = None
    __webserver_name = None
    __webserver_os = None
    __programming_language_used = None

    def __init__(self, project_id, connection, thread_semaphore, database_semaphore, url):
        """
        Paramters:
        ==========
        :param thread_semaphore: This semaphore is used to control the running threads
        :param database_semaphore: This semaphore is used to add control the threads which
        adds information to the database
        :param url: The url for which the information is to be gathered
        :param connection: MySQL database connection object
        :return: None
        """
        self.__project_id = project_id
        self.__connection = connection
        self.__thread_semaphore = thread_semaphore
        self.__database_semaphore = database_semaphore
        self.__url = url
        # get the ip address of the url
        with ThreadPoolExecutor(max_workers=1) as executor:
            ip = executor.submit(URL().get_ip, self.__url)
            self.__ip = ip.result()
        # we will get the headers of the request
        self.__headers = URL().get_head_request(url=self.__url, user_agent=UserAgent.get_user_agent()).headers

    def __check_for_firewall(self):
        """
        This method will check if any firewall is present or Not
        :return:
        """
        self.__thread_semaphore.acquire()
        try:
            file = open("firewall_names.txt", "r")
            firewall_names = file.readlines()
            if self.__headers is None:
                header_string = ""
            else:
                header_string = str(self.__headers)
            for firewall_name in firewall_names:
                firewall_name = firewall_name.replace("\n", "")
                if firewall_name in header_string.lower():
                    self.__firewall = firewall_name.upper()
                    break
            file.close()
        except IOError:
            print("[+] FILE CANNOT BE OPENED")
        except Exception as e:
            print("[-] FATAL EXCEPTION OCCURED")
            print(e)
        self.__thread_semaphore.release()

    def __get_webserver_name(self):
        """
        This method is used to get the server header by sending a
        request to the bad gateway
        :return:
        """
        self.__thread_semaphore.acquire()
        try:
            self.__webserver_name = self.__headers['Server']
        except KeyError:
            print("[-] SEVER INFORMATION NOT FOUND IN HEADERS")
            self.__webserver_name = None
        except Exception as e:
            print(e)
            self.__webserver_name = None
        self.__thread_semaphore.release()

    def __get_programming_language(self):
        """
        We will use to get the programming language from headers of the request
        :return: None
        """
        self.__thread_semaphore.acquire()
        try:
            self.__programming_language_used = self.__headers['X-Powered-By']
        except KeyError:
            self.__programming_language_used = None
        except Exception as e:
            print(e)
            self.__programming_language_used = None
        # If we didn't get the programming language we will try to get
        # it from the cookies
        if self.__programming_language_used is None:
            r = URL().get_request(url=self.__url, user_agent=UserAgent.get_user_agent())
            cookies = r.cookies if r is not None else ""
            session_id = requests.utils.dict_from_cookiejar(cookies)
            # session_id contains the session id of the targetted url
            if "PHPSESSID" in session_id:
                self.__programming_language_used = "PHP"
            elif "JSESSIONID" in session_id:
                self.__programming_language_used = "J2EE"
            elif "ASP.NET_SessionId" in session_id:
                self.__programming_language_used = "ASP.NET"
            elif "CFID & CFTOKEN" in session_id:
                self.__programming_language_used = "COLDFUSION"
            else:
                self.__programming_language_used = "None"
        self.__thread_semaphore.release()

    def gather_information(self):
        """
        This method is used to gather all the webserver information
        :return: None
        """
        # By now we have obtained the url and the I.P address of the website
        # Now scan for firewalls
        if self.__ip is not None:
            firewall_check = Thread(target=self.__check_for_firewall)
            firewall_check.start()
            firewall_check.join()
            # self.__firwall now has the name of the firewall if present
        """
        @ This stage we have acquired self.__url, self.__ip and self.__firewall
        """
        if self.__firewall is None:
            server_name = Thread(target=self.__get_webserver_name)
            server_name.start()
            server_name.join()
            # Now we have the web server name
        # Now get the web server os
        if self.__webserver_name is not None:
            if "Win" in self.__webserver_name:
                self.__webserver_os = "Windows"
            if "Uni" in self.__webserver_name:
                self.__webserver_os = "Unix"
            if "Lin" in self.__webserver_name:
                self.__webserver_os = "Linux"
        # Now get the programming language
        programming_lang = Thread(target=self.__get_programming_language)
        programming_lang.start()
        programming_lang.join()
        # Now let us see what we have got
        print("IP:       ", self.__ip)
        print("DOMAIN:   ", URL().get_host_name(self.__url))
        print("SERVER:   ", self.__webserver_name)
        print("OS:       ", self.__webserver_os)
        print("Firewall: ", self.__firewall)
        print("Language: ", self.__programming_language_used)
        if self.__ip is None:
            self.__ip = "None"
        if self.__webserver_name is None:
            self.__webserver_name = "None"
        if self.__webserver_os is None:
            self.__webserver_os = "None"
        if self.__programming_language_used is None:
            self.__programming_language_used = "None"
        if self.__firewall is None:
            self.__firewall = "None"
        # Now add the information to database
        query = "insert into info_gathering values(%s,%s,%s,%s,%s,%s,%s)"
        args = (self.__project_id, "PRELIMINARY", self.__ip, self.__webserver_name,
                              self.__webserver_os, self.__programming_language_used,
                              self.__firewall)
        # A thread to add the information to the database
        database_adding_thread = Thread(target=self.add_info_gathering_phase_one, args=(self.__database_semaphore, self.__connection, query, args))
        database_adding_thread.start()
        database_adding_thread.join()
