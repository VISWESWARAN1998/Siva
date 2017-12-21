# SWAMI KARUPPASWAMI THUNNAI
#~~~~~~~~~~~~~~~~~~~~~~~~~~~
# =============================================
# Siva Vulnerability Scanner v0.4
# Copyright 2017, Visweswaran Nagasivam
# Date: 02.12.2017
# Author: Visweswaran Nagasivam
# email: visweswaran.nagasivam98@gmail.com
# POCMaker a.k.a Proof Of Concept Maker which will help
# you to get the live snapshot of the payloaded url with the help
# of phantomjs. This class is very helpful in automating the report
# of penetration testing.
# ==============================================

from sys import platform
from selenium import webdriver
from threading import RLock


class POCMaker:
    __project_id = None
    __url = None
    __file_name = None
    __browser = None
    __lock = RLock()

    def create_object(self):
        """
        Description:
        ------------
        This method is used to configure webdriver object to various locations.
        Make this method as daemon, which is completely ditached to the main thread
        """
        if platform == "win32":
            self.__browser = webdriver.PhantomJS("binaries/phantomjs.exe")
        else:
            self.__browser = webdriver.PhantomJS(
            )  # for other platform install phatomjs and make it in path
        print("[+] POC DAEMON STARTED SUCCESSFULLY")

    def set_project_id(self, project_id):
        with self.__lock:
            self.__project_id = project_id

    def set_file_name(self, file_name):
        with self.__lock:
            self.__file_name = file_name

    def set_url(self, url):
        with self.__lock:
            self.__url = url

    def simple_snapshot(self):
        """
        Description:
        ------------
        This class is used to get the snapshot of the url
        :return:
        """
        with self.__lock:
            try:
                self.__browser.get(self.__url)
                file_location = "projects/project-" + str(
                    self.__project_id) + "/images/" + self.__file_name + ".png"
                self.__browser.save_screenshot(file_location)
                print("[+] SNAPSHOT TAKEN!")
                print("[+] SAVED TO: ", file_location)
            except Exception:
                print("[-] CANNOT GET THE SNAPSHOT")
