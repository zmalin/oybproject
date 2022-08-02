import time
from config import ConfigFactory
from config import Project
from config import ScreenStreamConfig
from streaming import StreamingServer


if __name__ == "__main__":
    def main():
        cfg = ConfigFactory.config(Project.SCREENSTREAM)
        print("ip : {0}, port : {1}".format(cfg.ip(), cfg.port()))
        
        receiver = StreamingServer(cfg.ip(), cfg.port())
        receiver.start_server()
        
        while input("") != "STOP":
            time.sleep(0.001)
            pass
        
        receiver.stop_server()
                
    main()