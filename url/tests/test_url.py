# SWAMI KARUPPASWAMI THUNNAI

import unittest
from url.URL import URL

class URLTest(unittest.TestCase):
    """
    This class is used to test the URL class
    """

    def test_get_request(self):
        self.assertNotEqual(first=URL().get_request(url="https://www.kalasalingam.ac.in"), second=None)
        self.assertEqual(first=URL().get_request(url="https://www.kaladbfjsdwljgfjsalingam.ac.in"), second=None)
        self.assertNotEqual(first=URL().get_request(url="https://www.google.co.in"), second=None)

    def test_post_request(self):
        self.assertNotEqual(first=URL().
                            post_request("http://edu.kalasalingam.ac.in/sis/", data={'log':'9915004240', 'pwd':'07091998'}), second=None)
        status_code_for_corrent_auth = URL().post_request("http://edu.kalasalingam.ac.in/sis/", data={'log':'9915004240', 'pwd':'07091998'}).status_code
        self.assertEqual(first=status_code_for_corrent_auth, second=200, msg="Not properly logging in!")

    def test_file_name(self):
        self.assertEqual(URL().get_file_name("https://github.com/scikit-learn/scikit-learn"), None, "Not wokring for urls without file nanes")
        self.assertEqual(URL().get_file_name("https://github.com/scikit-learn/scikit-learn/index.html"), "index.html")
        self.assertEqual(URL().get_file_name("https://github.com"), None)
        self.assertEqual(URL().get_file_name("h"), None)
        self.assertEqual(URL().get_file_name("/a."), "a.")
        self.assertEqual(URL().get_file_name(None), None)

    def test_query_present(self):
        self.assertEqual(URL().is_query_present("https://github.com"), False)
        self.assertEqual(URL().is_query_present("https://github.com/kdfhh/index?id=1"), True)
        self.assertEqual(URL().is_query_present("https://github.com/kdfhh/"), False)

    def test_is_same_domain(self):
        self.assertEqual(URL().is_same_domain("https://github.com", "https://github.com"), True)
        self.assertEqual(URL().is_same_domain("https://github.com", ""), False)
        self.assertEqual(URL().is_same_domain(None, "https://github.com"), False)
        self.assertEqual(URL().is_same_domain("https://github.com", "https://github.com"), True)
        self.assertEqual(URL().is_same_domain("https://github.com", None), False)
        self.assertEqual(URL().is_same_domain(None, None), False)

    def test_if_query_present(self):
        self.assertEqual(URL().is_query_present("https://github.com"), False)
        self.assertEqual(URL().is_query_present("https://github.com/index.php?id=1"), True)


if __name__ == "__main__":
    unittest.main()