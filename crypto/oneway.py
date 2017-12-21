# SWAMI KARUPPASWAMI THUNNAI
#~~~~~~~~~~~~~~~~~~~~~~~~~~~
# =============================================
# Siva Vulnerability Scanner v0.4
# Copyright 2017, Visweswaran Nagasivam
# Date: 02.12.201
# Author: Visweswaran Nagasivam
# email: visweswaran.nagasivam98@gmail.com
# This class is a wrapper class for python 3's hashlib.
# I have reduced it so that it can be done in a
# line on other parts of program. which will avoid the
# duplication of the code.
#==============================================
import hashlib


class Hash:
    @staticmethod
    def get_md5(string):
        md5 = hashlib.md5(string.encode("utf-8")).hexdigest()
        return md5

    @staticmethod
    def get_sha2(string):
        sha2 = hashlib.sha256(string.encode("utf-8")).hexdigest()
        return sha2
