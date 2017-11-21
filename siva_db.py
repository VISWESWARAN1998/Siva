# SWAMI KARUPPASWAMI THUNNAI

# ===============================================
# UNIT TEST THIS CLASS LIKE ANYTHING IN THE WORLD
# ===============================================

from url.URL import URL

class SivaDB:
    """
    This class will be the one and the only class which is used to perform database related operations
    """

    def install(self):
        """
        This method is used to install the database
        :return: True if the database has been installed successfully
        """
        pass

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
