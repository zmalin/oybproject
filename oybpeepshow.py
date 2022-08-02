from Socket_Singleton import Socket_Singleton

from config import ConfigFactory
from config import Project
from imagefactory import ImageFactory
from log import Log
from log import LogType
from utils import DirUtil
from garbageschedule import GarbageSchedule

if __name__ == "__main__":
    def main():
        Socket_Singleton()
        
        config      = ConfigFactory.config(Project.SCREENSHOTSHARED)
        Log.create(LogType.FILE, DirUtil.dir("log"), config.log(), config.logLevel())
        Log.log().info("peep show start.")
        capturer    = ImageFactory(config)
        garbage     = GarbageSchedule(config)
        capturer.start()
        garbage.start(capturer)
        capturer.join()
        garbage.stop()
        Log.log().info("peep show finish.")
    
    main()