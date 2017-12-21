# SWAMI KARUPPASWAMI THUNNAI
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ===================================
# Author: Visweswaran Nagasaivam
# Email: visweswaran.nagasivam98@gmail.com
# Copyright(C) : 2017
# This class will supply the data for the bob library to learn
# This class will update the bob.csv dataframe so that
# we can apply machine learning algoritm to increase
# the intelligence of the bot. Unlike other classes,
# This class requires user-interaction completely
# ====================================

import sys
import time
from url.URL import URL
from user_agent import UserAgent
from locals.file import File


class BobLearn:
    __fastest_website = "https://www.facebook.com"
    __speed_of_fastest_website = 0.0
    __speed_of_target_website = 0.0
    __average_count = 5
    __is_website_slower = 0

    def __init__(self):
        print("[+] CALCULATING THE SPEED OF THE FASTEST WEBSITE")
        self.__speed_of_fastest_website = self.get_speed_of_website(url=self.__fastest_website)
        print("SPEED: ", self.__speed_of_fastest_website)
        if self.__speed_of_fastest_website is None:
            print("ERROR IN CALCULATING THE VALUES, EXITTING...")
            sys.exit(-1)

    def set_target_website_speed(self, target_url):
        print("[+] CALCULATING THE SPEED OF THE TARGET WEBSITE ", target_url)
        self.__speed_of_target_website = self.get_speed_of_website(url=target_url)
        print("SPEED: ", self.__speed_of_target_website)
        if self.__speed_of_target_website is None:
            print("ERROR IN CALCULATING THE VALUES, EXITTING...")
            sys.exit(-1)


    def get_speed_of_website(self, url):
        start_time = time.time()
        r = URL().get_request(url=url, user_agent=UserAgent.get_user_agent())
        end_time = time.time()
        if r is None:
            return None
        total_time = end_time - start_time
        return total_time

    def update(self):
        result = input("[+] Question: Is this website slower? [y/n]")
        if result.lower() == "y":
            self.__is_website_slower = 1
        # Now update the information to the file
        details = "{},{},{}\n".format(self.__speed_of_fastest_website,
                                      self.__speed_of_target_website,
                                      self.__is_website_slower)
        File.write(file_location="data_frames/bob.csv", content=details, mode="a")
        print("[+] RESULT UPDATED! THANK YOU FOR TEACHING")
