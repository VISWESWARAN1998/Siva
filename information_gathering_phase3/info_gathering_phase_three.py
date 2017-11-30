# SWAMI KARUPPASWAMI THUNNAI

from urllib.parse import urlparse
from information_gathering_phase3.whois import WhoIs
from locals.file import File
from url.URL import URL
from user_agent import UserAgent
from threading import Thread


class InfoGatheringPhasethree:
    """
    Description:
    ------------
    This class will get the robots.txt and whois into the projects/project-project_id folder
    """
    __project_id = 0
    __url = None
    __domain = None
    __thread_semaphore = None

    def __init__(self, project_id, url, thread_semaphore):
        """
        Description:
        ------------
        This phase only needs to url of the website to get it's who-is and robots.txt
        :param project_id: is used to identify which project we are getting
        :param url: The url of the website for which this information is to be analysed
        """
        self.__project_id = project_id
        self.__url = url
        self.__thread_semaphore = thread_semaphore
        self.__domain = urlparse(url=url).netloc
        self.__domain = self.__domain.replace("www.", "")
        # Create a thread to create Who-Is information
        whois_thread = Thread(target=self.__get_whois)
        robots_thread = Thread(target=self.__get_robots)
        whois_thread.start()
        robots_thread.start()
        whois_thread.join()
        robots_thread.join()

    def __get_whois(self):
        """
        Description:
        ------------
        This method is used to get the who-is information of the remote server
        :return: None
        """
        self.__thread_semaphore.acquire()
        print("[+] GETTING WHO-IS")
        whois = WhoIs(domain=self.__domain).get_whois()
        if whois is not None:
            file_location = "projects/project-" + str(
                self.__project_id) + "/whois.json"
            File.write(file_location=file_location, content=whois)
        self.__thread_semaphore.release()

    def __get_robots(self):
        """
        Description:
        ------------
        This method is used to get the robots.txt file from the remote server
        :return:
        """
        self.__thread_semaphore.acquire()
        robots_url = URL.join_urls(self.__url, "/robots.txt")
        print("[+] GETTING ROBOTS.TXT AT ", robots_url)
        r = URL().get_head_request(
            url=self.__url, user_agent=UserAgent.get_user_agent())
        if r is not None:
            if r.status_code == 200:
                robots_file_location = "projects/project-" + str(
                    self.__project_id) + "/robots.txt"
                File.download_file(
                    local_file_location=robots_file_location,
                    remote_file_location=robots_url)
            else:
                print("[-] NO robots.txt FOUND IN THE SERVER")
        self.__thread_semaphore.release()
