import datetime
import schedule
#import time
import os

from log import Log

from utils import FileUtil

class GarbageSchedule:
    def __init__(self, config):
        self.__config       = config
        # test
        """"
        self.__scheduler    = schedule.every(10).minutes.do(self.__cleanup)
        """
        self.__scheduler    = schedule.every().day.at(self.__config.cleanupTime()).do(self.__cleanup)
        
    def start(self, thread):
        while thread.is_alive():
            schedule.run_pending()
            #time.sleep(1)
    
    def stop(self):
        Log.log().info("grabage schedule stop")
        schedule.cancel_job(self.__scheduler)
    
    def __cleanup(self):
        Log.log().info("cleanup start")
        now     = datetime.datetime.now()
        files   = FileUtil.files(self.__config.imagePath())
        paths   = []
        for file in files:
            paths.append(self.__config.imagePath() + file)
            Log.log().debug("append file : {0}".format(self.__config.imagePath() + file))
            
        for file in paths:
            timediff = (now - datetime.datetime.fromtimestamp(os.path.getmtime(file)))
            # test
            """
            if (timediff / datetime.timedelta(minutes = 1) >= 10):
                FileUtil.remove(file)
                Log.log().debug("remove file : {0}".format(file))
                
            """
            if (timediff.days >= self.__config.cleanupInterval()):
                FileUtil.remove(file)
                Log.log().debug("remove file : {0}".format(file))
                
        Log.log().info("cleanup end")

if __name__ == "__main__":
    from config import ConfigFactory
    from config import Project
    
    def main():
        """"
        screenshotshared = ConfigFactory.config(Project.SCREENSHOTSHARED)
        scheduler = GarbageSchedule(screenshotshared)
        scheduler.start()
        """
        pass
    
    main()