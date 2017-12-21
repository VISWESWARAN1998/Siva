# SWAMI KARUPPASWAMI THUNNAI
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# =====================================
# Author: Visweswaran Nagasivam
# Email: visweswaran.nagasivam98@gmail.com
# Date: 05.12.2017
# Copyright(C): 2017
# =====================================

from information_gathering_phase1.database import InfoGatheringPhaseOneDatabase


class Database:
    __connection = None

    def __init__(self, connection):
        self.__connection = connection

    def get_project_details(self, project_id):
        query = "select * from project where project_id=%s limit 1"
        result = self.get_result_from_query(project_id, query)
        return result

    def get_info_gathering_details(self, project_id):
        result = InfoGatheringPhaseOneDatabase.get_info_gathering_phase_one(
            project_id=project_id, connection=self.__connection)
        return result

    def get_port_details(self, project_id):
        query = "select * from port where project_id=%s"
        result = self.get_result_from_query(project_id, query)
        return result

    def get_analysis_details(self, project_id):
        query = "select * from analysis where project_id=%s"
        result = self.get_result_from_query(project_id, query)
        return result

    def get_result_from_query(self, project_id, query):
        try:
            cursor = self.__connection.cursor()
            cursor.execute(query, (project_id, ))
            result = cursor.fetchall()
            if len(result) == 0:
                return None
            return result
        except Exception as e:
            print(e)
            return None

