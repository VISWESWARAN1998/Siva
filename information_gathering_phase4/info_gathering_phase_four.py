# SWAMI KARUPPASWAMI THUNNAI

from locals.file import File
from tqdm import tqdm
from url.URL import URL
from user_agent import UserAgent
from threading import Thread
from information_gathering_phase4.database import AdminPageDatabase

class InfoGatheringPhaseFour(AdminPageDatabase):
    """
    Aim:
    ----
    Will find the administrator page of the website
    Description:
    ------------
    A typical web-application has three types of users,
    1.	Anonymous Users: These users just surf the website without any logging in mechanisms. They reveal less information to the remote host. They have the least privilege.
    2.	Authenticated Users: These users are logged into the website. They reveal great information about themselves to the remote host. They have greater privilege to anonymous users.
    3.	Administrators: They are higher level users in the hierarchy of web-application; they could be the site-owners and system administrators.

    If we are performing a vulnerability scan with anonymous user privilege we will miss the privilege of authenticated and administrators. Since authenticated and administrators will have more additional web content, pages, permissions, accesses levels etc.
    Both anonymous, authenticated are hot hidden to the users, whereas admin pages don’t have any links to access. So, in this phase we will find the administrator’s authentication phase by brute-forcing (trying all combinations) of the URL like this,
    https://abc.com/admin  => 404 not Found
    https://abc.com/site-owner => 200 Found\
    Note: This approach may or may not find the admin page.
    """
    __project_id = None
    __url = None
    __thread_semaphore = None
    __database_semaphore = None
    __connection = None
    __admin_pages = []  # This will contain the list of admin pages
    __threads = []

    def __init__(self, project_id, url, thread_semaphore, database_semaphore, connection):
        """
        :param project_id: The id of the project
        :param url: The website for which the administrator page is to be found
        :param thread_semaphore:
        :param database_semaphore:
        """
        self.__project_id = project_id
        self.__url = url
        self.__thread_semaphore = thread_semaphore
        self.__database_semaphore = database_semaphore
        self.__connection = connection
        admin_contents = File.read_to_list("admin.txt")
        for admin_page in tqdm(admin_contents, ncols=100):
            self.__thread_semaphore.acquire()
            admin_url = URL.join_urls(self.__url, admin_page)
            t = Thread(target=self.add_if_page_found, args=(admin_url, ))
            t.start()
        print("[+] WAITING FOR THE THREADS TO COMPLETE THEIR TASKS")
        for thread in self.__threads:
            if thread.is_alive():
                thread.join()
        # Now display and add the admin pages in database table named "admin_table"
        for admin_page in self.__admin_pages:
            print("[+] ADMIN PAGE: ", admin_page)
            self.update_admin_page(project_id=project_id, url=admin_page,
                                   connection=self.__connection, database_semaphore=self.__database_semaphore)


    def add_if_page_found(self, url):
        """
        Description:
        ------------
        This will add the information to the database if admin page is found
        :param url: The url to be added to the database
        :return: None
        """
        r = URL().get_head_request(url=url, user_agent=UserAgent.get_user_agent())
        try:
            if r.status_code == 200:
                if url not in self.__admin_pages:
                    self.__admin_pages.append(url)
        except AttributeError:
            pass
        self.__thread_semaphore.release()