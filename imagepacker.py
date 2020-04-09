import sys
import patoolib
import patoolib.programs.rar
import shutil
import os
import threading
import time
import glob
from datetime import datetime as dt
from os.path import basename
from constants import EMPTY, ERROR
from environ import Environ


class ImagePacker():

    def __init__(self, imagesDirectory, processedDirectory, area):

        self.counter = 3
        self.prefix = ''
        self.postfix = ''
        ENV = Environ().get()
        try:
            # debug
            # print(ENV)
            self.prefix = ENV.get('SAI_PREFIX', '')
            self.postfix= ENV.get('SAI_POSTFIX', '')
            self.counter = int(ENV.get('SAI_COUNT', 3))
        except Exception as e:
            print('Error: config.env has wrong format!')

        self.currentDirectory = CURRENT_DIR if imagesDirectory == "" else imagesDirectory

        # for freeze
        if getattr(sys, 'frozen', False):
        # frozen
            dir_ = os.path.dirname(sys.executable)
        else:
        # unfrozen
            dir_ = os.path.dirname(os.path.realpath(__file__))
            
        self.tempDirectory = dir_ + "\\temp\\"
        self.currentDirectory = dir_ + "\\data\\" if imagesDirectory == "" else imagesDirectory
        self.processedDirectory = dir_ + "\\processed\\" if processedDirectory == "" else processedDirectory
    
        self.area = area
        

    def _filebrowser(self, constellation="", dir="", ext=""):
        "Returns files with an extension"
        # debug
        # print(f"{dir}{constellation}*{ext}")
        return [f for f in glob.glob(dir+constellation+"*"+ext)]

    # get files array, sort it by file time in file name
    # custom sort function

    def _sortByNamePart(self, inputStr):
        # Make date part of the string being our sort key
        # TODO it's better to filter using basename of file
        pos = inputStr.rfind("\\")
        return inputStr[pos+6:-4]

    def _getImageFiles(self, curArea):

        files = self._filebrowser(
            curArea, self.currentDirectory, ".fts")
        # for debug
        # print(files)

        # three first files from sorted list or less
        newFiles = sorted(files, key=self._sortByNamePart)
        filesToArchive = []
        filesToDelete = []
        
        lastIndex = self.counter if len(newFiles) >= self.counter else 0
        for x in range(0, lastIndex):
            print(newFiles[x])
            filesToArchive.append(basename(newFiles[x]))
            filesToDelete.append(newFiles[x])

        return filesToArchive, filesToDelete

    def _deleteImages(self, files):
        deletingError = False
        for f in range(0, len(files)):
            try:
                os.remove(files[f])
            except OSError:
                deletingError = True
                print("Error, can't delete file: ", files[f])
                pass

        if deletingError:
            return ERROR
        else:
            return None

    def _moveImages(self, files):
        movingError = False
        for f in range(0, len(files)):
            # if file already exists, do not move
            if not os.path.isfile(self.processedDirectory + basename(files[f])):       
                try:                
                    shutil.move(files[f], self.processedDirectory)
                except OSError:
                    movingError = True
                    print("Error, can't move file: ", files[f])
                    pass

        if movingError:
            return ERROR
        else:
            return None

    def packImagesForArea(self, area):
        cwd = os.getcwd()
        # debug
        # print(currentDirectory)
        files, filesToDelete = self._getImageFiles(area)
        # files = ""
        if len(files) == 0:
            return EMPTY
        os.chdir(self.currentDirectory)
        archiveFileName = self.tempDirectory + area + "_" + \
            dt.now().strftime("%Y%m%d-%H%M%S") + self.postfix + ".rar"
        patoolib.create_archive(archiveFileName, files, verbosity=1)
        resp = patoolib.test_archive(archiveFileName, verbosity=1)

        # debug
        # print(resp)
        if resp == ERROR:
            print(resp)
            
        os.chdir(cwd)

        resd = self._moveImages(filesToDelete)
        if (resd != None or resp != None):
            return ERROR

        return archiveFileName
