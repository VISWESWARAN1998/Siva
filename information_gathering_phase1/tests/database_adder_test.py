# SWAMI KARUPPASWAMI THUNNAI
import pymysql
import threading
from information_gathering_phase1.web_server_informtaion import WebServerInformation
connection = pymysql.connect(host="localhost", user="root", password="",
                                 db="siva")

w = WebServerInformation(3, connection, threading.Semaphore(10), threading.Semaphore(10), "http://121.200.55.239/admin/")
w.add_info_to_database()