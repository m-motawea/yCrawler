import os
import string
import sqlite3
from pytube import YouTube


class Video:
    @staticmethod
    def _genTitle(title):
        """cleans video title from characters that cannot be represented in ascii or might break command line execution"""
        s = title.replace('"', '_').replace("'", '_')
        printable = set(string.printable)
        s = filter(lambda x: x in printable, s)
        return s

    def __init__(self, title, url, img_src, img_thumb, views=0, duration='', parent=''):
        """initiated with:
            - title: video title (str)
            - url: video url (str)
            - img_src: url of the original image (str)
            - img_thumb url of the thumb image (str)
            - duration: video duration (str)
            - parent: name of the parent playlist or channel (str) (not used)
        """
        self.title = self._genTitle(title)
        self.url = url
        if not img_src:
            img_src = ''
        if not img_thumb:
            img_thumb = ''
        self.img_src = {'url': img_src, 'path': ''}
        self.img_thumb = {'url': img_thumb, 'path': ''}
        self.views = views
        self.duration = duration
        self.parent = parent

    def save(self, path):
        """save video information and download images to the specified path"""
        #generating a path to download the images
        self.img_src['path'] = path + '/' + self.title.replace(' ', '_').replace('|', '_').replace('(', '_').replace(')', '_') + '.src.jpg'
        self.img_thumb['path'] = path + '/' + self.title.replace(' ', '_').replace('|', '_').replace('(', '_').replace(')', '_') + '.thumb.jpg'
        if self.img_src['url']:
            cmd1 = 'wget -O ' + self.img_src['path'] + ' "' + self.img_src['url'] + '"'
            os.system(cmd1)
        if self.img_thumb['url']:
            cmd2 = 'wget -O ' + self.img_thumb['path'] + ' "' + self.img_thumb['url'] + '"'
            os.system(cmd2)
        conn = sqlite3.connect('yCrawler.db')
        conn.execute('''CREATE TABLE IF NOT EXISTS VIDEO
         (ID INT PRIMARY KEY,
         TITLE           CHAR(50)    NOT NULL,
         PARENT           CHAR(50)    NOT NULL,
         VIEWS            BIGINT,
         URL        TEXT,
         IMG_SRC_URL      TEXT,
         IMG_SRC_PATH      TEXT,
         IMG_THUMB_URL      TEXT,
         IMG_THUMB_PATH      TEXT,
         DURATION         CHAR(12));''')
        conn.commit()
        conn.execute("INSERT INTO VIDEO (TITLE,VIEWS,PARENT,URL,IMG_SRC_URL,IMG_SRC_PATH, \
        IMG_THUMB_URL,IMG_THUMB_PATH,DURATION) VALUES ('{}', {}, '{}', '{}', '{}', '{}', '{}', '{}', '{}' );".format( \
        self.title, self.views, self.parent, self.url, self.img_src['url'], self.img_src['path'], self.img_thumb['url'], \
        self.img_thumb['path'], self.duration))
        conn.commit()
        conn.close()

    def update(self, views, duration):
        """updates views and duration of an existing video"""
        self.views = views
        self.duration = duration
        conn = sqlite3.connect('yCrawler.db')
        conn.execute('UPDATE VIDEO SET VIEWS = {}, DURATION = "{}" WHERE TITLE = "{}";'.format(self.views, self.duration, self.title))
        conn.commit()
        conn.close()

    @classmethod
    def get(cls, title):
        """returns a Video object with the same title as given"""
        title = cls._genTitle(title)
        conn = sqlite3.connect('yCrawler.db')
        conn.execute('''CREATE TABLE IF NOT EXISTS VIDEO
         (ID INT PRIMARY KEY,
         TITLE           CHAR(50)    NOT NULL,
         PARENT           CHAR(50)    NOT NULL,
         VIEWS            BIGINT,
         URL        TEXT,
         IMG_SRC_URL      TEXT,
         IMG_SRC_PATH      TEXT,
         IMG_THUMB_URL      TEXT,
         IMG_THUMB_PATH      TEXT,
         DURATION         CHAR(12));''')
        conn.commit()
        cursor = conn.execute('SELECT VIEWS,PARENT,URL,IMG_SRC_URL,IMG_SRC_PATH,IMG_THUMB_URL,IMG_THUMB_PATH FROM VIDEO WHERE TITLE="{}";'.format(title))
        data = cursor.fetchall()
        if len(data) == 0:
            return None
        row = data[0]
        v = cls(title=title, views=row[0], parent=row[1], url=row[2], img_src=row[3], img_thumb=row[5])
        v.img_src['path'] = row[4]
        v.img_thumb['path'] = row[5]
        conn.close()
        return v

    def download(self, path='.'):
        """downloads the video to the given path"""
        print('Downloading {} to {}'.format(self.title, path))
        YouTube(self.url).streams.filter(resolution='360p').first().download(path)