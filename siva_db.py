# SWAMI KARUPPASWAMI THUNNAI

# ===============================================
# UNIT TEST THIS CLASS LIKE ANYTHING IN THE WORLD
# ===============================================

from url.URL import URL

class SivaDB:
    """
    This class will be the one and the only class which is used to perform database related operations
    """

    def create_project(self, connection, project_id, url):
        """
        Description:
        =============
        This method is used to create the project, and the project id
        :param connection: The database connection object
        :param project_id: The id of the project
        :param url: The url of the project
        :return: True if the process is competed else false
        """
        try:
            cursor = connection.cursor()
            cursor.execute("insert into project values(%s, %s)", (project_id, URL().get_host_name(url)))
            connection.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def add_info_gathering_phase_one(self, database_semaphore, connection, query, arguments):
        """
        :param connection: The mysql connection object
        :param query: the sql query
        :param arguments: parameters for the sql query
        :return:
        """
        database_semaphore.acquire()
        try:
            cursor = connection.cursor()
            cursor.execute(query, arguments)
            connection.commit()
            print("[*] ADDED INFORMATION SUCCESSFULLY")
        finally:
            database_semaphore.release()  # No matter what happens release the semaphore
