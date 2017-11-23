# SWAMI KARUPPASWAMM THUNNAI

class PortScan:
    """
    This class will port scan the ip address of the remote host
    if the firewall is not present.
    """
    __project_id = 0
    __ip = None
    __connection = None
    __database_semaphore = None

    def __init__(self, project_id, ip, connection, database_semaphore):
        self.__project_id = project_id
        self.__ip = ip
        self.__connection = connection
        self.__database_semaphore = database_semaphore

    def scan(self):
        """
        This method is used in scanning the ports on the remote host
        :return:
        """
        pass
