# SWAMI KARUPPASWAMI THUNNAI

import time
from url.URL import URL
from bs4 import BeautifulSoup
import queue as q
from user_agent import UserAgent
from simple_scan_engine.simple_scan import SimpleScan
from algorithms.ml.bob import BOB


class SimpleCrawler:
    """
    Description:
    -----------
    This class will quickly crawl all urls present in the website,
    as an anonymous user. and will get all the urls from the website
    """
    __project_id = None
    __base_url = None
    __thread_semaphore = None
    __database_semaphore = None
    __connection = None
    __poc_object = None
    __urls = q.PriorityQueue(
    )  # We will use the priority queue stroring and getting the further urls
    __crawled_urls = []  # Crawled urls
    __bob_object = None

    def __init__(self, project_id, base_url, thread_semaphore,
                 database_semaphore, connection, poc_oject):
        self.__project_id = project_id
        self.__base_url = base_url
        self.__thread_semaphore = thread_semaphore
        self.__database_semaphore = database_semaphore
        self.__connection = connection
        self.__poc_object = poc_oject
        # Initailize the Bot's Brain
        self.__bob_object = BOB(thread_semaphore=self.__thread_semaphore)
        self.crawl(base_url)

    def crawl(self, url):
        """
        Description:
        ------------
        This will crawl the urls completely
        :param url: The url to be crawled
        :return: None
        """
        start_time = time.time()
        r = URL().get_request(url=url, user_agent=UserAgent.get_user_agent())
        end_time = time.time()
        total_time = end_time - start_time
        self.__bob_object.predict(total_time)
        if r is not None:
            soup = BeautifulSoup(r.content, "html.parser")
            # At this stage we have got the beautiful soup objects
            #First find all the href links
            for i in soup.find_all("a"):
                try:
                    partial_url = i.get("href")
                    url_to_be_scanned = None  # we will scan this urls
                    # Check if the partial url is actually a partial url
                    if "http" in partial_url:
                        if URL.is_same_domain(self.__base_url, partial_url):
                            if partial_url not in self.__crawled_urls:
                                self.__urls.put(partial_url)
                                self.__crawled_urls.append(partial_url)
                                url_to_be_scanned = partial_url
                    else:
                        full_url = URL.join_urls(self.__base_url, partial_url)
                        if full_url not in self.__crawled_urls:
                            self.__urls.put(full_url)
                            self.__crawled_urls.append(full_url)
                            url_to_be_scanned = full_url
                    # run a simple scan in the url
                    if url_to_be_scanned is not None:
                        print("[i] CURRENTLY SCANNING [GET]: ",
                              url_to_be_scanned)
                        # Make the scanning as a new process
                        SimpleScan(
                            project_id=self.__project_id,
                            thread_semaphore=self.__thread_semaphore,
                            database_semaphore=self.__database_semaphore,
                            url=url_to_be_scanned,
                            connection=self.__connection,
                            poc_object=self.__poc_object)
                except Exception as e:
                    print("[-] EXCEPTION OCCURED ", e)
        while not self.__urls.empty():
            self.crawl(self.__urls.get())
