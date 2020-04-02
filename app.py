import patoolib
import os
import threading
import time
import glob
from datetime import datetime as dt
from itertools import starmap

currentDirectory = os.path.dirname(os.path.abspath(__file__)) + "\\data\\"
tempDirectory = os.path.dirname(os.path.abspath(__file__)) + "\\temp\\"


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

    print(currentDirectory)
    print(*files)

    patoolib.create_archive(
        tempDirectory + "test" + "_" + "photo" + "_" + dt.now().strftime("%Y%m%d-%H%M%S") + ".rar", (files, currentDirectory))


def filebrowser(constellation="", dir="", ext=""):
    "Returns files with an extension"
    # debug
    # print(f"{dir}{constellation}*{ext}")
    return [f for f in glob.glob(f"{dir}{constellation}*{ext}")]


# get files array, sort it by file time in file name
# custom sort function

def sortByNamePart(inputStr):
    # Make date part of the string being our sort key
    pos = inputStr.rfind("\\")
    return inputStr[pos+6:-4]


AREAS = prepareAreas()
# debug
print(AREAS)

curConstellation = "Lyr"
files = filebrowser(curConstellation, currentDirectory, ".fts")
# for debug
# print(files)
newFiles = sorted(files, key=sortByNamePart)
lastIndex = 3 if len(newFiles) >= 3 else len(newFiles)
for x in range(0, lastIndex):
    print(newFiles[x])
    # thread = ImagePacker(packImages(currentDirectory, tempDirectory))
    # thread.start()
    # # show message
    # thread.join()


print("archiving files ... ")
print(newFiles[0:3])
fileNames = (' '.join(map(str, newFiles)))
print(fileNames)
packImages(newFiles)

#thread = ImagePacker(starmap(packImages, newFiles))
# thread.start()
# # show message
# thread.join()
print("files packed")
