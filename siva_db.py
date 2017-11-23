# SWAMI KARUPPASWAMI THUNNAI

# ===============================================
# UNIT TEST THIS CLASS LIKE ANYTHING IN THE WORLD
# ===============================================

from url.URL import URL

class SivaDB:
    """
    This class will be the one and the only class which is used to perform database related operations
    """

    def install(self, connection):
        """
        This method is used to install the database
        :return: True if the database has been installed successfully
        """
        cursor = connection.cursor()
        ports_table = "create table if not exists ports(project_id int(10), port_no int(6))"
        print("[+] CREATING ports TABLE")
        self.execute_query(cursor, ports_table)


    def execute_query(self, cursor, query):
        """
        Dexcription:
        ============
        This method will blindly execute the sql query so use it carefully.
        Parameters:
        ===========
        :param cursor: pymysql cursor object
        :param query: the query to be executed
        :return:
        """
        cursor.execute(query)
        cursor.commit()
        print("[+] QUERY EXECUTED SUCCESSFULLY.")

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
