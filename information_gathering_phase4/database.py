# SWAMI KARUPPASWAMI THUNNAI

class AdminPageDatabase:
    """
    Description:
    ------------
    This class is used to add the admin page to the database table if found
    """

    def update_admin_page(self, project_id, url, database_semaphore, connection):
        database_semaphore.acquire()
        try:
            cursor = connection.cursor()
            cursor.execute("insert into admin_page values(%s,%s)", (project_id, url))
            connection.commit()
            return True
        except Exception:
            return False
        database_semaphore.release()