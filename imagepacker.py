import sys
import patoolib
import patoolib.programs.rar
import shutil
import os
import time
import glob
import re
from datetime import datetime as dt
from os.path import basename
from constants import EMPTY, ERROR
from environ import Environ


class ImagePacker():
    archext = ".rar"

    def __init__(self, imagesDirectory="", processedDirectory="", area="", tempDirectory=""):

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
            print('!--> Error: config.env has wrong format!')        

        # for freeze
        if getattr(sys, 'frozen', False):
        # frozen
            dir_ = os.path.dirname(sys.executable)
        else:
        # unfrozen
            dir_ = os.path.dirname(os.path.realpath(__file__))
            
        self.tempDirectory = dir_ + "\\temp\\" if tempDirectory == "" else tempDirectory
        self.currentDirectory = dir_ + "\\data\\" if imagesDirectory == "" else imagesDirectory
        self.processedDirectory = dir_ + "\\processed\\" if processedDirectory == "" else processedDirectory
    
        self.area = area
        

    def _filebrowser(self, constellation="", dir="", ext=""):
        "Returns files with an extension"
        files = []
        pattern = r"(^" + constellation + "(_|-SF_).*\\" + ext + ")"
        # debug
        # print(pattern)        
        match = re.compile(pattern)
        fileList =  [f for f in os.listdir(dir) if re.search(match, f)]
        for f in fileList:
            files.append(os.path.join(dir,f))

        return files

    # get files array, sort it by file time in file name
    # custom sort function
    def _sortByNamePart(self, inputFileName):
        # Make date part of the string being our sort key        
        filename = basename(inputFileName)
        pos = filename.find("_")
        # debug
        # print(filename[pos+1:-4])
        return filename[pos+1:-4]

    def _sortByArchiveName(self, archiveFileName):
        filename = basename(archiveFileName)
        pos = filename.rfind(self.archext)
        filename = filename[:pos]        
        if (self.postfix != ""):
            pos = filename.rfind(self.postfix)
            filename = filename[:pos]

        # debug
        # print(filename)                      
        
        pos = filename.find("_")
        strdate = filename[:pos]
        pos = filename.rfind("_")
        strtime = filename[pos:]
        criteria = (strdate+strtime).replace("-","").replace("_","")
        # debug        
        # print(criteria)
        return criteria

    def getArchiveFiles(self):
        files = [f for f in glob.glob(self.tempDirectory+ "*" + self.archext)]
        # debug
        # print(files)
        return sorted(files, key = self._sortByArchiveName)
        

    def _getImageFiles(self, curArea):
        files = self._filebrowser(
            curArea, self.currentDirectory, ".fts")
        # debug
        # print(files)

        # three first files from sorted list or less
        newFiles = sorted(files, key=self._sortByNamePart)
        filesToArchive = []
        filesToDelete = []
        
        lastIndex = self.counter if len(newFiles) >= self.counter else 0
        for x in range(0, lastIndex):
            # debug
            # print(newFilex[x])
            #access = os.access(newFiles[x], os.W_OK)
            #if not access:             
            #    filesToArchive = []
            #    filesToDelete = []
            #    break
            

            #access = os.access(self.currentDirectory, os.F_OK)
            #access = os.access(newFiles[x], os.F_OK)
            #if not access:             
            #   filesToArchive = []
            #    filesToDelete = []
            #    break
            
            # debug
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
                print("!--> Error, can't delete file: ", files[f])
                pass

        if deletingError:
            return ERROR
        else:
            return None

    def _moveImages(self, files):
        movingError = False
        deletingError = False
        for f in range(0, len(files)):
            # if file already exists, do not move, just delete
            if not os.path.isfile(os.path.join(self.processedDirectory,basename(files[f]))):       
                try:                
                    shutil.move(files[f], self.processedDirectory)
                except OSError:
                    movingError = True
                    print("!--> Error, can't move file: ", files[f])
                    pass
            else:
                try:
                    os.remove(files[f])
                except OSError:
                    deletingError = True
                    print("!--> Error, can't delete file: ", files[f])
                    pass                

        if movingError or deletingError:
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
        
        archiveFileName = self.tempDirectory  + \
            dt.now().strftime("%Y-%m-%d") + "_" + self.prefix + area + "_" + \
            dt.now().strftime("%H%M%S") + self.postfix + self.archext
        
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
