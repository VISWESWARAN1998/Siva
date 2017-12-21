# SWAMI KARUPPASWAMI THUNNAI

import codecs
import urllib.request


class File:
    """
    This class is used to handle everything with files in your local PC
    """

    @staticmethod
    def write(file_location, content, mode="w"):
        """
        :param file_location: The location of the file
        :param content: The content to be written to the file
        :param mode: The mode of the file
        :return: None
        """
        try:
            file = codecs.open(
                filename=file_location, encoding="utf-8", mode=mode)
            file.write(str(content))
            file.close()
        except FileNotFoundError:
            print("[-] CANNOT WRITE TO FILE. LOCATION INVALID")
        except PermissionError:
            print("[-] MISSING PERMISSIONS CANNOT WRITE INTO THE FILE")

    @staticmethod
    def write_to_list(file_location, contents):
        """
        Description:
        -------------
        This method will write the content of the list to the local file
        :param file_location: The location of the file
        :param content: the python list to be written
        :return:
        """
        try:
            file = codecs.open(
                filename=file_location, encoding="utf-8")
            for content in contents:
                try:
                    file.write(str(content))
                except:
                    pass
            file.close()
        except FileNotFoundError:
            print("[-] CANNOT WRITE TO FILE. LOCATION INVALID")
        except PermissionError:
            print("[-] MISSING PERMISSIONS CANNOT WRITE INTO THE FILE")

    @staticmethod
    def read_to_list(file_location):
        """
        Description:
        ------------
        This will read the contents of the file to a python list.
        \n will be replaced
        :param file_location: The location of the file
        :return: list[] of contents present in the file
        """
        try:
            file = open(file_location, "r")
            file_contents = []
            for i in file.readlines():
                i = i.replace("\n", "")
                file_contents.append(i)
            return file_contents
        except FileNotFoundError:
            print(
                "[-] CANNOT OPEN THE FILE LOCATION. PLEASE CHECK THE LOCATION")
            return None
        except Exception:
            return None

    @staticmethod
    def download_file(local_file_location, remote_file_location):
        """
        This method is used to download the file from the remote server
        :param local_file_location: The location in your P.C
        :param remote_file_location: The location of the remote host i.e, url
        :return:
        """
        try:
            urllib.request.urlretrieve(
                url=remote_file_location, filename=local_file_location)
        except Exception as e:
            print("[-] CANNOT DOWNLOAD THE FILE")
            print(e)
