# SWAMI KARUPPASWAMI THUNNAI
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
Author: VISWESWARAN NAGASIVAM
Email: visweswaran.nagasivam98@gmail.com
Copyright (C): 2017 to Visweswaran Nagasivam
BOB a.k.a Brain Of Bot Helps your multi-threaded bot to learn,
think and act upon websites so that your bot will able make decisions
at a difficult situations like preventing DOS attack from your bot.
It holds the resources when the website is suffering from your bot thereby
stopping your bot at right situation and it will release the resources when
the website can handle.
It will help your bot to think efficently thereby
making your bot a website friendly crawling/scraping!
"""

import time
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from url.URL import URL
from user_agent import UserAgent
from locals.static import Static


class BOB:
    __thread_semaphore = None
    __fastest_website = "https://www.google.com"
    __response_time_of_fastest_website = 0.0
    __sleep_time = 0.1
    __regressor = None  # This will be our logistic regression class object

    def __init__(self, thread_semaphore):
        """
        This constructor is used to initialize the parameters
        """
        self.__thread_semaphore = thread_semaphore
        print("[+] LEARNING! PLEASE WAIT...")
        # set the response time of the fastest website
        self.__set_response_time_of_fastest_website()
        # load the ml algorithm
        self.__set_logistic_regressor_object()

    def __set_response_time_of_fastest_website(self):
        """
        Description:
        ------------
        This method will calculate the response time of the fastest website
        :return:
        """
        start_time = time.time()
        r = URL().get_request(
            url=self.__fastest_website, user_agent=UserAgent.get_user_agent())
        end_time = time.time()
        if r is not None:
            self.__response_time_of_fastest_website = end_time - start_time

    def __set_logistic_regressor_object(self):
        data_frame = pd.read_csv(filepath_or_buffer=Static.bob_file)
        # Independent Variable
        X = data_frame.iloc[:, :-1].values  # All rows except the 3rd column
        # Create a dependent Variable
        y = data_frame.iloc[:, 2].values  # All rows and 3rd column only
        self.__regressor = LogisticRegression()
        self.__regressor.fit(X, y)

    def predict(self, response_time):
        print("Fastest Response Time: ",
              self.__response_time_of_fastest_website)
        print("Target Response Time: ", response_time)
        prediction = np.array(
            [[self.__response_time_of_fastest_website, response_time]])
        predict = self.__regressor.predict(prediction)
        if predict[0] == 1:
            print("WEBSITE IS SLOWING DOWN. DELAYING A SECOND")
            for i in range(100):
                self.__thread_semaphore.acquire(timeout=0.1)
