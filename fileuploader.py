import os
from os.path import basename
import logging
import requests
from multiprocessing import Queue
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
        filename = basename(filepath)

        # debug
        # print(filepath)
        # print(filename)

        # print("Login to server... ")
        # response = requests.get(url, auth=auth)
        # debug
        # print("Server response is: ", response.status_code, response.reason, response.text)
        # print("Server response headers are: ", response.headers)
        # if not response.ok:
        #     print("Can't login to server: ", url)
        #     return None
        #
        # debug
        # print("Login ok!")

        file = {'file': open(filepath, 'rb')}
        # debug
        print("Posting file to server: ", basename(filepath))
        response = requests.post(url, files=file, auth=auth)

        # debug
        # print("Server response is: ", response.status_code, response.reason, response.text)
        # print("Server response headers are: ", response.headers)

        if response.ok:
            print("File uploaded to server: ", basename(filepath))
            return None
        else:
            # debug
            print("Server response is: ", response.status_code, response.reason, response.text)
            print("Server response headers are: ", response.headers)
            print("Error in response: ", response)
            return ERROR

    def uploadFile(self):
        return self._send_post(url=self.server, filepath=self.fileToUpload,
                               filesize=os.path.getsize(self.fileToUpload))
