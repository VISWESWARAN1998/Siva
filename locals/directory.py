# SWAMI KARUPPASWAMI THUNNAI

import os


class Directory:
    """
    Description:
    ------------
    This class is used to handle any directories related activities.
    """

    @staticmethod
    def create_directory(directory_location):
        """
        Description:
        ------------
        This method is used to create
        :param directory_location:
        :return: True if creatd false
        """
        if os.path.exists(directory_location):
            return True
        else:
            try:
                os.mkdir(directory_location)
                return True
            except FileNotFoundError:
                return False
            except PermissionError:
                print(
                    "[-] WARNING UNABLE TO CREATE THE DIRECTORY DUE TO MISSING PERMISSION"
                )
                return False
        return False
