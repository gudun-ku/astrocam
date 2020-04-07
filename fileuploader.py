import os
from os.path import basename
import logging
import requests
from requests.api import sessions
from requests.auth import HTTPBasicAuth
import time
import string
import random
from constants import SERVER, USERNAME, PASSWORD, ERROR


class FileUploader():

    def __init__(self, fileToUpload):
        self.username = USERNAME
        self.password = PASSWORD
        self.fileToUpload = fileToUpload

    def _random_string(self, length):
        return ''.join(random.choice(string.ascii_letters) for ii in range(length + 1))

    # for test test server
    def _getinfo(self, url):
        auth = HTTPBasicAuth(username, password)
        response = requests.get(
            url=url + "/test_is_protected", auth=auth)
        print(response.status_code)

    def _send_post(self, url, filepath, filesize):

        auth = HTTPBasicAuth(USERNAME, PASSWORD)

        # debug
        # print(filepath)

        file_ = {'file': (basename(filepath), open(
            filepath, 'rb'), 'application/x-rar-compressed')}
        #response = requests.post(url, files=file_, headers=headers, auth=auth)
        response = requests.post(url, files=file_, auth=auth)

        # debug
        #logging.debug('Code: %s %s', response.status, response.reason)
        # print(response)

        if response.ok:
            print("File uploaded to server: ", basename(filepath))
            return None
        else:
            return ERROR

    def uploadFile(self):
        return self._send_post(url=SERVER, filepath=self.fileToUpload,
                               filesize=os.path.getsize(self.fileToUpload))
