# SWAMI KARUPPASWAMI THUNNAI

import socket
import requests
from urllib.parse import urlparse
from urllib.parse import urljoin

class URL:
    """
    Description:
    ------------
    This class is used to perform any URL related operations
    """

    def get_request(self, url, user_agent=None):
        """
        Description:
        ------------
        This method will try its level best to get the requests object(as GET request) else,
        This method will return None. This method is considered to be safest
        since all exceptions are sanitized properly.
        Parameters:
        -----------
        :param url: The url for which the requests object is to be returned
        :param user_agent: The user_agent to be used
        Returns:
        ---------
        :return: Will return the requests object if possible else it will return None
        """
        try:
            r = requests.get(url=url, headers=user_agent)
            return r
        except requests.ConnectionError:
            self.get_request(url=url, user_agent=user_agent)
        except requests.exceptions.MissingSchema:
            return None
        except requests.exceptions.InvalidURL:
            return None
        except:
            return None

    def post_request(self, url, data, user_agent=None):
        """
        Description:
        ------------
        This method will try its level best to get the requests object(as POST request) else,
        This method will return None. This method is considered to be safest
        since all exceptions are sanitized properly.
        Parameters:
        -----------
        :param url: The url for which the requests object is to be returned
        :param user_agent: The user_agent to be used
        :param data: The data to be posted
        Returns:
        ---------
        :return: Will return the requests object if possible else it will return None
        """
        try:
            r = requests.post(url=url, headers=user_agent, data=data)
            return r
        except requests.ConnectionError:
            self.get_request(url=url, user_agent=user_agent)
        except requests.exceptions.MissingSchema:
            return None
        except requests.exceptions.InvalidURL:
            return None

    def get_file_name(self, url):
        """
        Description:
        ------------
        This method is used to get the file name from url
        Parameters:
        -----------
        :param url: The url for which the file name is to be returned
        Returns:
        --------
        :return: The filename will be returned if it is present
        else None will be returned
        """
        if url is None:
            return None
        url_path = urlparse(url=url)
        file_name = url_path.path.split("/")[-1]
        file_name = file_name.strip() if "." in file_name else None
        return file_name

    def is_same_domain(self, url1, url2):
        """
        Description:
        -------------
        This method is used to check whether the two urls belong to the same domain
        Parameters:
        ------------
        :param url1: frst url
        :param url2: sencond url
        Returns:
        --------
        :return: True if they belong to same domain
        """
        if url1 is None or url2 is None:
            return False
        domain1 = urlparse(url=url1)
        domain2 = urlparse(url=url2)
        if domain1.netloc == domain2.netloc:
            return True
        return False

    def is_query_present(self, url):
        """
        Description:
        ------------
        This method is used to check the query present in the url
        :param url: The url for which the query is to be checked
        :return: True if the query is present else false
        """
        query = urlparse(url=url)
        if len(query.query) > 0:
            return True
        return False

    def join_urls(self, url1, url2):
        """
        Description:
        ------------
        This method is used to join two urls
        Parameters:
        -----------
        :param url1: first url
        :param url2: second url
        :return: joined url
        """
        return urljoin(url1, url2)

    def get_ip(self, url):
        """
        This method will return the I.P address for the url provied

        Parameters:
        -----------
        url : The url for which the I.P address is needed
        :return: The I.P address of the remote host
        """
        try:
            ip = socket.gethostbyname(self.get_host_name(url))
        except socket.gaierror:
            ip = None
        return ip

    def get_host_name(self, url):
        """
        This method is used to get the host name for the url

        Parameters:
        ------------
        url : The url in which the host name can be acquired

        Returns:
        -------
        will return the host name
        Example:
        https://www.google.com will return www.google.com
        """
        return urlparse(url).hostname

    def get_scheme(self, url):
        """
        :param url: The url for which the scheme is to be returned
        :return: None
        """
        return urlparse(url).scheme

