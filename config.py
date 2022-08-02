# config.py
import os
import json
from enum import Enum
import socket
import utils
import logging

class Config:
    def __init__(self):
        self._data = {}
        
    def log(self):
        pass

    #protected
    def _prepare(self, name):
        configFile = utils.DirUtil.dir() + name
        if not os.path.exists(configFile):
            self.__createDefault(configFile)
        self.__loadConfig(configFile)
    
    #private
    def __loadConfig(self, file):
        with open(file, 'r') as f:
            self._data = json.load(f)

    def __createDefault(self, file):
        with open(file, 'w', encoding="UTF8") as f:
            json.dump(self._data, f, ensure_ascii = False, indent = 4)

class ScreenShotConfig(Config):
    def __init__(self):
        super().__init__()
        self._data["interval"]      = 1
        self._data["image_ratio"]   = 0.5
        self._data["image_delete"]  = True
        self._data["google_folder"] = "hotel"
        self._prepare("screenshot.json")
        self.__imagePath            = utils.DirUtil.dir("image")
        self.__googlePath           = utils.DirUtil.dir("google")
        
    # public
    def log(self):
        return "oybphotographer.log"
    
    def interval(self):
        return float(self._data["interval"] * 60)
    
    def imageRatio(self):
        return self._data["image_ratio"]
    
    def imageDelete(self):
        return self._data["image_delete"]
    
    def imagePath(self):
        return self.__imagePath
    
    def googleToken(self):
        return self.__googlePath + "token.json"
    
    def googleCredentials(self):
        return self.__googlePath + "credentials.json"
    
    def googleScopes(self):
        return ['https://www.googleapis.com/auth/drive']
    
    def googleFolder(self):
        return self._data["google_folder"]

class ScreenStreamConfig(Config):
    def __init__(self):
        super().__init__()
        self._data["ip"]      = socket.gethostbyname(socket.gethostname())
        self._data["port"]    = 9999
        self._prepare("screenstream.json")
    
    # public
    def log(self):
        return "oybstream.log"
    
    def ip(self):
        return self._data["ip"]
    
    def port(self):
        return self._data["port"]
    
class ScreenShotSharedConfig(Config):
    def __init__(self):
        super().__init__()
        self._data["interval"]          = 1
        self._data["image_ratio"]       = 0.5
        self._data["cleanup_interval"]  = 2
        self._data["cleanup_time"]      = "00:00:00"
        self._data["shared_folder"]     = "C:\\oybproject\\shared files"   #total path
        self._data["log_level"]         = "INFO"
        self._prepare("screenshotshared.json")
        utils.DirUtil.makeFolder(self._data["shared_folder"])
        self.__sharedPath               = self._data["shared_folder"] + "\\"
        
        # public
    def log(self):
        return "oybpeepshow.log"
    
    def interval(self):
        return float(self._data["interval"] * 60)
    
    def imageRatio(self):
        return self._data["image_ratio"]
    
    def cleanupInterval(self):
        return self._data["cleanup_interval"]
    
    def cleanupTime(self):
        return self._data["cleanup_time"]
    
    def imagePath(self):
        return self.__sharedPath
    
    def logLevel(self):
        if self._data["log_level"] == "CRITICAL" or self._data["log_level"] == "FATAL":
            return logging.FATAL
        elif self._data["log_level"] == "ERROR":
            return logging.ERROR
        elif self._data["log_level"] == "WARNING" or self._data["log_level"] == "WARN":
            return logging.WARN
        elif self._data["log_level"] == "INFO":
            return logging.INFO
        elif self._data["log_level"] == "DEBUG":
            return logging.DEBUG
        return logging.NOTSET
        
class Project(Enum):
    SCREENSHOTGDRIVE    = 1
    SCREENSTREAM        = 2
    SCREENSHOTSHARED    = 3

class ConfigFactory:
    @staticmethod
    def config(project):
        projects = {
            project.SCREENSHOTGDRIVE: ScreenShotConfig,
            project.SCREENSTREAM: ScreenStreamConfig,
            project.SCREENSHOTSHARED: ScreenShotSharedConfig, 
        }
        return projects[project]()
    
if __name__ == "__main__":
    def main():
        """"
        screenshot = ConfigFactory.config(Project.SCREENSHOTGDRIVE)
        print("screenshot interval:{0}, ratio:{1}".format(screenshot.interval(), screenshot.imageRatio()))
        print("screenshot token: {0}".format(screenshot.googleToken()))
        print("screenshot credentials: {0}".format(screenshot.googleCredentials()))
        """
        
        """"
        screenstream = ConfigFactory.config(Project.SCREENSTREAM)
        print("screenstream ip:{0}, port:{1}".format(screenstream.ip(), screenstream.port()))
        """
        
        screenshotshared = ConfigFactory.config(Project.SCREENSHOTSHARED)
        print("screenshotshared interval:{0}, ratio:{1}".format(screenshotshared.interval(), screenshotshared.imageRatio()))
        print("screenshotshared cleanupinterval:{0}, cleanuptime:{1}, sharedpath:{2}".format(screenshotshared.cleanupInterval(), screenshotshared.cleanupTime(), screenshotshared.imagePath()))
        
    main()