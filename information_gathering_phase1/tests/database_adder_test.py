# SWAMI KARUPPASWAMI THUNNAI
import pymysql
import unittest
from information_gathering_phase1.database import InfoGatheringPhaseOneDatabase
import threading


class DatabaseTest(unittest.TestCase):
    password = input("Enter the password: ")
    connection = pymysql.connect(
        host="localhost", user="root", password=password, db="siva")
    semaphore = threading.Semaphore(10)

    def test_firewall(self):
        self.assertEqual(
            InfoGatheringPhaseOneDatabase.update_firewall(
                database_semaphore=self.semaphore,
                connection=self.connection,
                project_id=800,
                firewall_name="Hower\""), None)
