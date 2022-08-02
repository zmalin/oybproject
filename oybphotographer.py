from queue import Queue
from Socket_Singleton import Socket_Singleton
import time
import logging

from config import ConfigFactory
from config import Project
from imagefactory import ImageFactory
from gdrive import GDrive
from log import Log
from log import LogType
from utils import DirUtil

if __name__ == "__main__":
    def main():
        Socket_Singleton()
        
        config      = ConfigFactory.config(Project.SCREENSHOTGDRIVE)
        Log.create(LogType.FILE, DirUtil.dir("log"), config.log(), logging.INFO)
        Log.log().info("program start")
        buffer      = Queue()
        capturer    = ImageFactory(config, buffer)
        sender      = GDrive(capturer, buffer, config)
        
        if sender.prepared():
            capturer.start()
            sender.start()
        
        while capturer.is_alive():
            time.sleep(0.001)
            continue
        
        Log.log().info("program end")
        
    main()