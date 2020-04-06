# file monitoring classes to check every time interval for new files

import sys
import os
import getopt
import threading
import time
import signal
from constants import EMPTY, ERROR

from datetime import timedelta
from imagepacker import ImagePacker
from fileuploader import FileUploader

MIN_INTERVAL = 15


def prepareAreas():
    areasFile = open('areas.txt', 'r')
    areasSet = set(areasFile.read().splitlines())
    areasFile.close()
    return areasSet


def deleteFile(file):
    try:
        os.remove(file)
        return None
    except OSError:
        print(f"Error deleting file: {file}")
        return ERROR


class ProgramKilled(Exception):
    pass
# main loop for execution


def makeJobForArea(imagesDirectory, area):
    packer = ImagePacker(imagesDirectory, area)
    archiveFile = packer.packImagesForArea(area)
    if archiveFile == ERROR:
        print("Error in archiving files!")
        return

    if archiveFile == EMPTY:
        # debug
        # print("No new files, skipping... ")
        return

    # debug
    print(archiveFile)

    uploader = FileUploader(archiveFile)
    res = uploader.uploadFile()
    if res != None:
        print(f"Error uploading file: {res}!")
        return

    res = deleteFile(archiveFile)
    if res != None:
        print(f"Error deleting file after uploading: {res}!")


def programLoop(imagesDirectory, areas):
    print("Checking camera folder ... ", time.ctime())
    for area in areas:
        # debug
        # print(area)
        makeJobForArea(imagesDirectory, area)


def signal_handler(signum, frame):
    raise ProgramKilled


class Job(threading.Thread):
    def __init__(self, interval, execute, *args, **kwargs):
        threading.Thread.__init__(self)
        self.daemon = False
        self.stopped = threading.Event()
        self.interval = interval
        self.execute = execute
        self.args = args
        self.kwargs = kwargs

    def stop(self):
        self.stopped.set()
        self.join()

    def run(self):
        while not self.stopped.wait(self.interval.total_seconds()):
            self.execute(*self.args, **self.kwargs)


def main(argv):
    interval = 180  # seconds
    count = 3  # count in series
    directory = ''  # camera directory

    try:
        opts, args = getopt.getopt(
            argv, "hi:c:d:", ["interval=", "count=", "directory="])
    except getopt.GetoptError:
        print('astrocam.py -i <interval> -c <countInSeries> -d <photoDirectory>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('astrocam.py -i <interval> -c <countInSeries> -d <photoDirectory>')
            sys.exit()
        elif opt in ("-i", "--interval"):
            interval = int(arg)
        elif opt in ("-c", "--count"):
            count = int(arg)
        elif opt in ("-d", "--directory"):
            directory = arg

    print('================================== BEGIN TO WORK =====================================')
    print('interval is :"', interval)
    print('count is :"', count)
    print('camera directory is :"', directory)

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    scanInterval = interval if interval >= MIN_INTERVAL else MIN_INTERVAL

    job = Job(interval=timedelta(seconds=scanInterval),
              execute=programLoop, imagesDirectory=directory, areas=prepareAreas())
    job.start()

    while True:
        try:
            time.sleep(1)
        except ProgramKilled:
            print("Program killed: running cleanup code")
            job.stop()
            break


if __name__ == "__main__":
    main(sys.argv[1:])
