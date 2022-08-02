from utils import FileUtil

class Garbage:
    def __init__(self, config):
        self.__config = config
        
    def cleanup(self, current):
        paths = []
        files = FileUtil.files(self.__config.imagePath(), current)
        for file in files:
            paths.append(self.__config.imagePath() + file)
        for file in paths:
            FileUtil.remove(file)

if __name__ == "__main__":
    from config import ConfigFactory
    from config import Project
    
    def main():
        cfg     = ConfigFactory.config(Project.SCREENSHOTGDRIVE)
        garbage = Garbage(cfg)
        garbage.cleanup("2022.07.28.00.01.56.png")
        
    main()