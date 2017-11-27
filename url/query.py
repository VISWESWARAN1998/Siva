# SWAMI KARUPPASWAMI THUNNAI

from urllib.parse import urlparse
from urllib.parse import parse_qs

class Query:
    """
    Description:
    ------------
    This class is used to interact with all the query related operations
    in the URL
    """

    @staticmethod
    def subtract_one(url):
        """REFERENCE: NUMERICAL SQL VULNERABILITY"""
        final_urls = []  # This will contain the list of urls with paylaod
        url_parsed = urlparse(url)
        queries = parse_qs(url_parsed.query)
        for query in queries:
            value = queries[query]
            if len(value) > 0:
                try:
                    check_for_integer = int(value[0])
                    # Increase the value by so that we can decrement and check it
                    check_for_integer+=1
                    payloaded_query = str(check_for_integer)+"-1"
                    final_payload = {query: payloaded_query}
                    partial_url = url_parsed.scheme + "://" + url_parsed.netloc + url_parsed.path + "?"
                    for new_query in queries:
                        if new_query in final_payload:
                            new_url = new_query + "=" + final_payload[new_query]
                            partial_url+=new_url
                            partial_url+="&"
                        else:
                            values = queries[new_query]
                            if len(values) > 0:
                                new_url = new_query + "=" + values[0]
                            else:
                                new_url = new_query + "="
                            partial_url += new_url
                            partial_url += "&"
                    final_url = partial_url[:-1]
                    if final_url not in final_urls:
                        final_urls.append(final_url)
                    # Now we will append the urls
                except ValueError:
                    pass
        # final_urls is a python list which contains payloaded urls
        return final_urls

    @staticmethod
    def add_one(url):
        """REFERENCE: NUMERICAL SQL VULNERABILITY"""
        final_urls = []  # This will contain the list of urls with paylaod
        url_parsed = urlparse(url)
        queries = parse_qs(url_parsed.query)
        for query in queries:
            value = queries[query]
            if len(value) > 0:
                try:
                    check_for_integer = int(value[0])
                    # Decrese the value by  1 so that we can increment and check it
                    check_for_integer-=1
                    payloaded_query = str(check_for_integer)+"%2b1"  # In url encoding + is used for whitespaces where as %2b is a + operator
                    final_payload = {query: payloaded_query}
                    partial_url = url_parsed.scheme + "://" + url_parsed.netloc + url_parsed.path + "?"
                    for new_query in queries:
                        if new_query in final_payload:
                            new_url = new_query + "=" + final_payload[new_query]
                            partial_url+=new_url
                            partial_url+="&"
                        else:
                            values = queries[new_query]
                            if len(values) > 0:
                                new_url = new_query + "=" + values[0]
                            else:
                                new_url = new_query + "="
                            partial_url += new_url
                            partial_url += "&"
                    final_url = partial_url[:-1]
                    if final_url not in final_urls:
                        final_urls.append(final_url)
                    # Now we will append the urls
                except ValueError:
                    pass
        # final_urls is a python list which contains payloaded urls
        return final_urls

    def append_payload_to_all_queries(self, url, payload):
        """
        This method will add the payload to all the queries
        """
        payload = self.encode_payload(payload)
        final_urls = []  # This will contain the list of urls with paylaod
        url_parsed = urlparse(url)
        queries = parse_qs(url_parsed.query)
        for query in queries:
            value = queries[query]
            if len(value) > 0:
                try:
                    value = int(value[0])
                    payloaded_query = str(value)+payload  # add the payload here
                    final_payload = {query: payloaded_query}
                    partial_url = url_parsed.scheme + "://" + url_parsed.netloc + url_parsed.path + "?"
                    for new_query in queries:
                        if new_query in final_payload:
                            new_url = new_query + "=" + final_payload[new_query]
                            partial_url+=new_url
                            partial_url+="&"
                        else:
                            values = queries[new_query]
                            if len(values) > 0:
                                new_url = new_query + "=" + values[0]
                            else:
                                new_url = new_query + "="
                            partial_url += new_url
                            partial_url += "&"
                    final_url = partial_url[:-1]
                    if final_url not in final_urls:
                        final_urls.append(final_url)
                    # Now we will append the urls
                except ValueError:
                    pass
        # final_urls is a python list which contains payloaded urls
        return final_urls
    
    def replace_payload_to_all_queries(self, url, payload):
        """
        This method will add the payload to all the queries
        """
        payload = self.encode_payload(payload)
        final_urls = []  # This will contain the list of urls with paylaod
        url_parsed = urlparse(url)
        queries = parse_qs(url_parsed.query)
        for query in queries:
            value = queries[query]
            if len(value) > 0:
                try:
                    value = int(value[0])
                    payloaded_query = payload  # replace the payload here
                    final_payload = {query: payloaded_query}
                    partial_url = url_parsed.scheme + "://" + url_parsed.netloc + url_parsed.path + "?"
                    for new_query in queries:
                        if new_query in final_payload:
                            new_url = new_query + "=" + final_payload[new_query]
                            partial_url+=new_url
                            partial_url+="&"
                        else:
                            values = queries[new_query]
                            if len(values) > 0:
                                new_url = new_query + "=" + values[0]
                            else:
                                new_url = new_query + "="
                            partial_url += new_url
                            partial_url += "&"
                    final_url = partial_url[:-1]
                    if final_url not in final_urls:
                        final_urls.append(final_url)
                    # Now we will append the urls
                except ValueError:
                    pass
        # final_urls is a python list which contains payloaded urls
        return final_urls    

    def encode_payload(self, payload):
        """
        :param payload: The payload which is to be encoded
        :return: return the encoded payload
        """
        # I know this can be looped, but why should I waste ecx?
        payload = payload.replace(" ","%20")
        payload = payload.replace("!","%21")
        payload = payload.replace("#","%23")
        payload = payload.replace("$","%24")
        payload = payload.replace("&","%26")
        payload = payload.replace("'","%27")
        payload = payload.replace("(","%28")
        payload = payload.replace(")","%29")
        payload = payload.replace("*","%2A")
        payload = payload.replace("+","%2B")
        payload = payload.replace(",","%2C")
        payload = payload.replace("/","%2F")
        payload = payload.replace(":","%3A")
        payload = payload.replace(";","%3B")
        payload = payload.replace("=","%3D")
        payload = payload.replace("?","%3F")
        payload = payload.replace("@","%40")
        payload = payload.replace("[","%5B")
        payload = payload.replace("]","%5D")
        # Now we have the encoded payload
        return payload
    
        
