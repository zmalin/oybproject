#import time
from config import ConfigFactory
from config import Project
from config import ScreenStreamConfig
from streaming import ScreenShareClient

if __name__ == "__main__":
    def main():
        cfg = ConfigFactory.config(Project.SCREENSTREAM)
        print("ip : {0}, port : {1}".format(cfg.ip(), cfg.port()))
        
        sender = ScreenShareClient(cfg.ip(), cfg.port())
        sender.start_stream()
        
        while input("") != "STOP":
            #time.sleep(0.001)
            continue
        
        sender.stop_stream()
        
    main()
