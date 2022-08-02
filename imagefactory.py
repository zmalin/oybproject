# imagefactory.py

from PIL import ImageGrab
from functools import partial
from queue import Queue
from threading import Timer
import time

from utils import FileUtil

import logging
from log import Log

class ImageFactory(Timer):
    def __init__(self, config, que = None):
        super().__init__(config.interval(), self.__capture)
        self.daemon     = True
        
        self.__images   = que
        self.__config   = config
        time.sleep(1)
        self.__capture()
        
    def run(self):
        Log.log().info("start run")
        while not self.finished.wait(self.__config.interval()):
            self.function(*self.args, **self.kwargs)
        
    def __capture(self):
        ImageGrab.grab  = partial(ImageGrab.grab, all_screens = True)
        origin          = ImageGrab.grab()
        width           = int(float(origin.size[0]) * self.__config.imageRatio())
        height          = int(float(origin.size[1]) * self.__config.imageRatio())
        copy            = origin.resize((width, height))
        
        try:
            shortName   = FileUtil.makeName("png")
            fullName    = self.__config.imagePath() + shortName
            copy.save(fullName)
            if self.__images:
                self.__images.put((shortName, fullName))
        except:
            Log.log().error("file save")
            self.cancel()

if __name__ == "__main__":
    from config import ConfigFactory
    from config import Project
    from log import LogType

    def main():
        """"
        cfg         = ConfigFactory.config(Project.SCREENSHOTGDRIVE)
        Log.create(LogType.CONSOLE, "", "", logging.INFO)
        Log.log().info("start program")
        Log.log().info("interval : {0}, ratio : {1}, path : {2}".format(cfg.interval(), cfg.imageRatio(), cfg.imagePath()))
        
        images      = Queue()
        imgFactory  = ImageFactory(cfg, images)
        imgFactory.start()
        
        while imgFactory.is_alive():
            time.sleep(0.001)
            continue
        """
        
        cfg         = ConfigFactory.config(Project.SCREENSHOTSHARED)
        Log.create(LogType.CONSOLE, "", "", logging.INFO)
        Log.log().info("start peep show")
        print("screenshotshared interval:{0}, ratio:{1}".format(cfg.interval(), cfg.imageRatio()))
        print("screenshotshared cleanupinterval:{0}, cleanuptime:{1}, sharedpath:{2}".format(cfg.cleanupInterval(), cfg.cleanupTime(), cfg.imagePath()))
        
        imgFactory  = ImageFactory(cfg)
        imgFactory.start()
        
        
        imgFactory.join()
        
        
    main()
