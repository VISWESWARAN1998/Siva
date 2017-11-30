# SWAMI KARUPPASWAMI THUNNAI
"""
This .py file is soley used to test the Directory class
"""

from locals.directory import Directory
import unittest


class TestDirectory(unittest.TestCase):
    def test_directory_create(self):
        """
        This class is used to test create directory method of Directory class
        :return:
        """
        self.assertEqual(Directory.create_directory("E:\KT"), True)
        self.assertEqual(
            Directory.create_directory("C:\Program Files\siva"), False)
