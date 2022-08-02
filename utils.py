# directory.py
import os
from datetime import datetime

class DirUtil:
    @staticmethod
    def dir(folder = ""):
        dirPath = os.path.expanduser('~') + "\\oybproject"
        if not DirUtil.makeFolder(dirPath):
            return ""
        
        dirPath += "\\"
        if folder:
            dirPath += folder
            if not os.path.exists(dirPath):
                #print("{0} create".format(dirPath))
                os.makedirs(dirPath)
            dirPath += "\\"
        return dirPath
    
    @staticmethod
    def makeFolder(folderPath):
        try:
            if not os.path.exists(folderPath):
                os.makedirs(folderPath)
            return True
        except OSError:
            return False

class FileUtil:
    @staticmethod
    def makeName(extension):
        return datetime.now().strftime("%Y.%m.%d.%H.%M.%S") + '.' + extension
    
    @staticmethod
    def remove(file):
        try:
            os.remove(file)
        except FileNotFoundError:
            pass
    
    @staticmethod
    def files(dir, exceptFile = ""):
        lst = []
        for file in os.listdir(dir):
            if (os.path.isfile(os.path.join(dir, file))):
                if file != exceptFile:
                    lst.append(file)
        return lst
    
if __name__ == "__main__":
    def main():
        #print(DirUtil.dir("aaa"))
        #print(FileUtil.makeName("png"))
        #result = FileUtil.files("C:\\Users\\donghoon.lee\\oybproject\\image\\", "2022.07.28.01.04.48.png")
        #print(result)
        DirUtil.makeFolder("E:\\temp\\oybproject\\shared files")
    
    main()