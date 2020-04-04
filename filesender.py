import os
import threading
import logging
import requests
from requests.api import sessions
from requests.auth import HTTPBasicAuth
import time
import string
import random


username = "nmv"
password = "v5589sgr"


def random_string(length):
    return ''.join(random.choice(string.ascii_letters) for ii in range(length + 1))


def send_post(url, filepath, filesize):

    auth = HTTPBasicAuth(username, password)
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Content-Type": "application/rar",
        "Content-Size": str(filesize)
    }

    with open(filepath, 'rb') as f:
        response = requests.post(
            url, {'files': f}, headers=headers, auth=auth)

    # debug
    logging.debug('Code: %s %s', response.status, response.reason)

    if response.status == 200:
        return True
    else:
        return False


def getinfo(url):
    auth = HTTPBasicAuth(username, password)
    response = requests.get(
        url=url + "/test_is_protected", auth=auth)
    print(response.status_code)


class FileUploader(threading.Thread):

    def __init__(self, function_that_works):
        threading.Thread.__init__(self)
        self.runnable = send_post
        self.daemon = True

    def run(self):
        self.runnable()
