# gdrive.py
from __future__ import print_function

import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from googleapiclient.http import MediaFileUpload

from threading import Thread
from queue import Queue

#from httplib2 import Credentials

from utils import FileUtil
from garbage import Garbage

import logging
from log import Log

class GDrive(Thread):
    def __init__(self, thread, que, config):
        super().__init__()
        self.deamon     = True
        self.__thread   = thread
        self.__images   = que
        self.__config   = config
        self.__creds    = None
        self.__service  = None
        self.__prepare()
        self.__garbage  = Garbage(config)
        
    def run(self):
        Log.log().info("start run")
        self.__connect()
        # 1. find folder
        # 2. if not foler, create it
        folderId = self.__folder()
        while self.__thread.is_alive():
            while not self.__images.empty():
                self.__upload(folderId)
                
    def prepared(self):
        if self.__creds and self.__creds.valid:
            Log.log().info("google dirve token acepted")
            return True
        if self.__creds and self.__creds.expired:
            Log.log().error("google drive token expired")
        return False
        
    def __upload(self, folder):
        shortName, fullName = self.__images.get()
        file_metadata       = {'name': shortName, 'parents': [folder]}
        media               = MediaFileUpload(fullName, mimetype = 'image/png', resumable = True)
        file                = self.__service.files().create(body = file_metadata, media_body = media, fields = 'id').execute()
        self.__cleanup(shortName)
        
    def __prepare(self):
        if os.path.exists(self.__config.googleToken()):
            Log.log().info("google dirve token exist")
            self.__creds = Credentials.from_authorized_user_file(self.__config.googleToken(), self.__config.googleScopes())
        
        if not self.__creds or not self.__creds.valid:
            if self.__creds and self.__creds.expired and self.__creds.refresh_token:
                self.__creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.__config.googleCredentials(), self.__config.googleScopes())
                self.__creds = flow.run_local_server(port = 0)
            
            with open(self.__config.googleToken(), 'w') as token:
                token.write(self.__creds.to_json())
                Log.log().info("google dirve token get successfully")
            
    def __connect(self):
        try:
            self.__service = build("drive", "v3", credentials = self.__creds, static_discovery = False)
        except HttpError as error:
            Log.log().critical("google drive connect error")
            Log.log().critical(error)
            self.__thread.cancel()
            
    
    def __folder(self):
        try:
            # find folder
            query       = f"mimeType='application/vnd.google-apps.folder' and name = '{self.__config.googleFolder()}'"
            page_token  = None
            response    = self.__service.files().list(  q           = query,
                                                        spaces      = 'drive',
                                                        fields      = 'nextPageToken, files(id, name)',
                                                        pageToken   = page_token).execute()
            folders     = response.get("files", [])
            folderId    = ''
            if len(folders) == 0:
                file_meta   = {"name": self.__config.googleFolder(), "mimeType": "application/vnd.google-apps.folder"}
                folder      = self.__service.files().create(body = file_meta, fields = "id").execute()
                folderId    = folder.get("id")
            else:
                folderId    = folders[0].get("id")
            return folderId
        except HttpError as error:
            Log.log().critical("google drive upload error")
            Log.log().critical(error)
            self.__thread.cancel()
            with self.__images.mutex:
                self.__images.queue.clear()
            return ''
        
    def __cleanup(self, file):
        if self.__config.imageDelete():
            self.__garbage.cleanup(file)
    

if __name__ == "__main__":
    import time
    
    from config import ConfigFactory
    from config import Project
    from imagefactory import ImageFactory
    from log import LogType
    
    def sub():
        cfg         = ConfigFactory.config(Project.SCREENSHOTGDRIVE)
        Log.create(LogType.CONSOLE, "", "", logging.INFO)
        Log.log().info("start program")
        Log.log().info("interval : {0}, ratio : {1}, path : {2}".format(cfg.interval(), cfg.imageRatio(), cfg.imagePath()))
        
        images      = Queue()
        imgFactory  = ImageFactory(images, cfg)
        gdrive      = GDrive(imgFactory, images, cfg)

        if gdrive.prepared():
            imgFactory.start()
            gdrive.start()
        
            while imgFactory.is_alive():
                time.sleep(0.001)
                continue
        
        
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/drive']

    def sample():
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('F:\\zmalin.github\\study\\python\\test_project\\google_drive\\google\\token.json'):
            creds = Credentials.from_authorized_user_file('F:\\zmalin.github\\study\\python\\test_project\\google_drive\\google\\token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('F:\\zmalin.github\\study\\python\\test_project\\google_drive\\google\\credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('F:\\zmalin.github\\study\\python\\test_project\\google_drive\\google\\token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            service = build('drive', 'v3', credentials=creds)
        
            # create folder
            if True:
                folder_name = "images"
                """"
                file_meta   = {"name": folder_name, "mimeType": "application/vnd.google-apps.folder"}
                folder      = service.files().create(body = file_meta, fields = "id").execute()
                folderId    = folder.get("id")
                print("folder id : {0}".format(folderId))
                """
                query       = f"mimeType='application/vnd.google-apps.folder' and name = '{folder_name}'"
                page_token  = None
                response    = service.files().list( q           = query,
                                                    spaces      = 'drive',
                                                    fields      = 'nextPageToken, files(id, name)',
                                                    pageToken   = page_token).execute()
                folders     = response.get("files", [])
                print("folder count : {0}".format(len(folders)))
                folderId   = folders[0].get("id")
                print("folder id : {0}, type : {1}".format(folderId, type(folderId)))
            
                shortName = "2022.07.27.10.15.33.png"
                fullName = "C:\\Users\\donghoon.lee\\oybproject\\image\\2022.07.27.10.15.33.png"
                file_metadata = {'name': shortName, 'parents': [folderId]}
                media = MediaFileUpload(fullName, mimetype = 'image/png', resumable = True)
                file = service.files().create(body = file_metadata, media_body = media, fields = 'id').execute()
            

            """"
            # Call the Drive v3 API
            results = service.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()
            items = results.get('files', [])

            if not items:
                print('No files found.')
                return
            print('Files:')
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id']))
            """
        except HttpError as error:
            # TODO(developer) - Handle errors from drive API.
            print(f'An error occurred: {error}')
        
    def main():
        sub()
        #sample()
        
    main()