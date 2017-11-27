# SWAMI KARUPPASWAMI THUNNAI

class PortScanDatabase:
    """
    This class is used to add/remove ports to the port table
    present in the siva database.
    """

    def add_port_to_database(self, project_id, connection, port_no):
        """
        Description:
        ============
        This method is used to add the port no to the port table present in the siva database
        Parameters:
        ===========
        :param project_id: The id of the project
        :param connection: pymysql connection object
        :param port_no: The port No to be added
        :return: None
        """
        try:
            cursor = connection.cursor()
            query = "insert into port values(%s,%s)"
            cursor.execute(query,(project_id, port_no))
            connection.commit()
        except Exception as e:
            print("[-] CANNOT ADD TO DATBASE ",e)

    def remove_port_from_database(self, project_id, connection, port_no):
        """
        Description:
        ============
        This method is used to remove the port no to the port table present in the siva database
        [Note]: This method is not used right now and may be used in future of this project
        Parameters:
        ===========
        :param project_id: The id of the project
        :param connection: pymysql connection object
        :param port_no: The port No to be added
        :return: None
        """
        pass