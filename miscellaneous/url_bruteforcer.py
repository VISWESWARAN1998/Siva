# SWAMI KARUPPASWAMI THUNNAI
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
Some sites will behave different, like if the url is not found
it will be redirected to the home page this bruteforcer will hopefully solve that kinds of problem
"""

import time
from locals.static import Static
from url.URL import URL
from selenium import webdriver


class URLBruteforcer:
    __website = None
    __keywords = []
    __browser = None  # This will be the phantomjs object

    def __init__(self):
        self.__website = input("Website Name: ")
        file_location = input("Enter the keywords file location: ")
        file = open(file_location, "r")
        keywords = file.readlines()
        for key in keywords:
            key = key.replace("\n", "")
            self.__keywords.append(key)
        print("[+] Total Keywords: ", len(self.__keywords))

    def brutforce(self):
        self.__browser = webdriver.PhantomJS(Static.phantomjs)
        for partial_url in self.__keywords:
            new_url = URL.join_urls(self.__website, partial_url)
            self.__browser.get(new_url)
            print(self.__browser.current_url)
            print(self.__browser.get_log("har"))
        self.__browser.quit()

