# SWAMI KARUPPASWAMI THUNNAI

import socket
from threading import Thread
from information_gathering_phase2.database import PortScanDatabase
from tqdm import tqdm


class PortScan(PortScanDatabase):
    """
    This class will port scan the ip address of the remote host
    if the firewall is not present.
    """
    __project_id = 0
    __ip = None
    __connection = None
    __thread_semaphore = None
    __database_semaphore = None

    def __init__(self, project_id, ip, connection, thread_semaphore,
                 database_semaphore):
        self.__project_id = project_id
        self.__ip = ip
        self.__connection = connection
        self.__thread_semaphore = thread_semaphore
        self.__database_semaphore = database_semaphore

    def scan(self):
        """
        This method is used for scanning the ports on the remote host
        :return:
        """
        ports = [20, 21, 80, 1521, 2483, 2484,
                 3360]  # added few ports based upon OWASP-CM-002
        for port_no in tqdm(ports, ncols=70, desc="[+] SCANNING PORTS"):
            self.__thread_semaphore.acquire(timeout=10)
            add_port = Thread(target=self.add_if_port_open, args=(port_no, ))
            add_port.start()
            add_port.join()

    def add_if_port_open(self, port_no):
        """
        Description:
        ============
        This method will add the information to the database if the port is opened
        :param port_no: the port_no to be added
        :return: None
        """
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((self.__ip, port_no))
            self.add_port_to_database(self.__project_id, self.__connection,
                                      port_no)
        except Exception:
            pass
        self.__thread_semaphore.release()
