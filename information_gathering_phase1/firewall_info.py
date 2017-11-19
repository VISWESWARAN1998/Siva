# SWAMI KARUPPASWAMI THUNNAI

from url.URL import URL
from bs4 import BeautifulSoup
from information_gathering_phase1.firewall_symptom import FirewallSymptom

class FirewallInformation:
    """
    Description:
    ============
    This class is used to check whether the
    website is using firewall or not. If yes, will provide some information
    about it!
    """
    __url = None
    __ip = None
    __firewall = None
    __ip_url = None

    def get_info(self, url, ip):
        """
        :param url: The url of the website
        :param ip: The ip address of the website
        :return: The firewall name if present else it will return None
        """
        self.__ip = ip
        self.__url = url
        self.__ip_url = "http://"+self.__ip
        ip_url_requests_object = URL().get_request(url=self.__ip_url, user_agent=None)
        url_requests_object = URL().get_request(url=self.__url, user_agent=None)
        #=======================   CLOUDFLARE PROTECTION ======================
        self.__firewall = "CLOUDFLARE" if \
            self.__is_firewall_present(ip_url_requests_object, FirewallSymptom().cloudflare_symptom) else None
        if self.__firewall is not None:
            return self.__firewall
        #===================== AMAZON CLOUDFRONT PROTECTION ===================
        self.__firewall = "AMAZON CLOUDFRONT" if \
            self.__is_firewall_present(ip_url_requests_object, FirewallSymptom().cloudfront_symptom) else None
        if self.__firewall is not None:
            return self.__firewall
        #=======================
        return self.__firewall

    def __is_firewall_present(self, r_object, rule):
        """
        Description:
        ============
        This method will return True if a specific firewall rule matches
        :param r_object: the requests object for the __ip_url (e.g: http://52.222.128.203/)
        :return: None if the firewall is not present
        """
        firewall_present = False
        total_symptoms = 0
        firewall_symptoms = 0
        try:
            r = r_object
            soup = BeautifulSoup(r.content, "html.parser")
            if r.status_code == rule["status_code"]:
                firewall_symptoms += 1
                total_symptoms+=1
            else:
                total_symptoms += 1
            if rule["title"] in soup.title.string:
                firewall_symptoms += 1
                total_symptoms += 1
            else:
                total_symptoms += 1
            for i in rule["soup_text"]:
                if i in soup.text:
                    firewall_symptoms += 1
                    total_symptoms += 1
                else:
                    total_symptoms += 1
            if (firewall_symptoms/total_symptoms) >= 0.5:
                firewall_present = True
        finally:
            return firewall_present

