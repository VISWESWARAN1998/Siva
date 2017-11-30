# SWAMI KARUPPASWAMI THUNNAI

import pythonwhois


class WhoIs:
    """
    This calss is used to get the whois information of the I.P address
    """
    __domain = None  # The domain for which the who is information is need to be gathered

    def __init__(self, domain):
        self.__domain = domain

    def get_whois(self):
        try:
            whois = pythonwhois.get_whois(domain=self.__domain)
            return whois
        except Exception:
            return None
