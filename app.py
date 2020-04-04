import patoolib
import os
import threading
import time
import glob
from datetime import datetime as dt
from os.path import basename
from filesender import FileUploader, send_post, getinfo

currentDirectory = os.path.dirname(os.path.abspath(__file__)) + "\\data\\"
tempDirectory = os.path.dirname(os.path.abspath(__file__)) + "\\temp\\"

server = 'http://127.0.0.1:5001'


def prepareAreas():
    areasFile = open('areas.txt', 'r')
    areasList = areasFile.read().splitlines()
    areasFile.close()
    return areasList


class ImagePacker(threading.Thread):

    def __init__(self, function_that_works):
        threading.Thread.__init__(self)
        self.runnable = function_that_works
        self.daemon = True

    def run(self):
        self.runnable()


def packImages(files):
    cwd = os.getcwd()
    # debug
    # print(currentDirectory)
    os.chdir(currentDirectory)
    archiveFileName = tempDirectory + "test" + "_" + "photo" + "_" + \
        dt.now().strftime("%Y%m%d-%H%M%S") + ".rar"
    patoolib.create_archive(archiveFileName, files, verbosity=1)
    os.chdir(cwd)
    return archiveFileName


def filebrowser(constellation="", dir="", ext=""):
    "Returns files with an extension"
    # debug
    # print(f"{dir}{constellation}*{ext}")
    return [f for f in glob.glob(f"{dir}{constellation}*{ext}")]


# get files array, sort it by file time in file name
# custom sort function

def sortByNamePart(inputStr):
    # Make date part of the string being our sort key
    # TODO it's better to filter using basename of file
    pos = inputStr.rfind("\\")
    return inputStr[pos+6:-4]


AREAS = prepareAreas()
# debug
print(AREAS)

curConstellation = "Lyr"
files = filebrowser(curConstellation, currentDirectory, ".fts")
# for debug
# print(files)

# three first files from sorted list or less
newFiles = sorted(files, key=sortByNamePart)
filesToArchive = []
lastIndex = 3 if len(newFiles) >= 3 else len(newFiles)
for x in range(0, lastIndex):
    print(newFiles[x])
    filesToArchive.append(basename(newFiles[x]))

getinfo(url=server)

# debug
# print(filesToArchive)

print("archiving files ... ")
zipFileName = packImages(filesToArchive)
print(f"files packed. zip file name: {zipFileName}")

result = send_post(server, zipFileName, os.path.getsize(zipFileName))
print(result)

# thread = ImagePacker(packImages(filesToArchive))
# thread.start()
# show message
# thread.join()
