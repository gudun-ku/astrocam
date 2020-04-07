import os
from os.path import basename
import logging
import requests
from requests.api import sessions
from requests.auth import HTTPBasicAuth
import time
import string
import random
from constants import ERROR
from environ import Environ


class FileUploader():

    def __init__(self, fileToUpload):
        ENV = Environ().get()
        try:
            # debug
            # print(ENV)
            self.username = ENV.get('SAI_USERNAME', '')
            self.password = ENV.get('SAI_PASSWORD', '')
            self.server = ENV.get('SAI_SERVER', '')

        except Exception as e:
            print('Error: config.env has wrong format!')

        self.fileToUpload = fileToUpload

        # debug
        # print("server: ", self.server)
        # print("username: ", self.username)
        # print("password: ", self.password)

    def _random_string(self, length):
        return ''.join(random.choice(string.ascii_letters) for ii in range(length + 1))

    # for test test server
    def _getinfo(self, url):
        auth = HTTPBasicAuth(self.username, self.password)
        response = requests.get(
            url=url + "/test_is_protected", auth=auth)
        print(response.status_code)

    def _send_post(self, url, filepath, filesize):

        auth = HTTPBasicAuth(self.username, self.password)

        # debug
        # print(filepath)

        file_ = {'file': (basename(filepath), open(
            filepath, 'rb'), 'application/x-rar-compressed')}
        #response = requests.post(url, files=file_, headers=headers, auth=auth)
        response = requests.post(url, files=file_, auth=auth)

        # debug
        #logging.debug('Code: %s %s', response.status, response.reason)

        if response.ok:
            print("File uploaded to server: ", basename(filepath))
            return None
        else:
            print("Error in response: ", response)
            return ERROR

    def uploadFile(self):
        return self._send_post(url=self.server, filepath=self.fileToUpload,
                               filesize=os.path.getsize(self.fileToUpload))
