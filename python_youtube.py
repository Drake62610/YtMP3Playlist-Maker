from pytube import YouTube
from urllib.request import urlopen
import requests
import sys
import subprocess
from bs4 import BeautifulSoup
from os import system, listdir, rename, makedirs
from os.path import isfile, join, exists
import logging
from logging.handlers import RotatingFileHandler

DOWLOAD_LOCATION = 'YoutubeVideo/'
MP3_LOCATION = 'YoutubeMP3/'

#Creation of directories if needed
if not exists(DOWLOAD_LOCATION):
    makedirs(DOWLOAD_LOCATION)
if not exists(MP3_LOCATION):
    makedirs(MP3_LOCATION)

#Creation of the logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
file_handler = RotatingFileHandler('activity.log', 'a', 1000000, 1)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)

# Function that will simulate a search on youtube and return the link of the top video
# Input : textToSearch is the keywords entered in the youtube search
def youtubeSearch(textToSearch):
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)     Chrome/37.0.2049.0 Safari/537.36'}
    #textToSearch = 'One Piece Opening 1'
    url = "https://www.youtube.com/results?search_query=\'" + textToSearch + "\'"
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html,"html.parser")
    link = soup.find(attrs={'class':'yt-uix-tile-link'})
    return ('http://www.youtube.com' + link['href'])

# Function that will download a video on youtube
#
def youtubedownload(textToSearch, ismp3=True):
    #Download video
    link = youtubeSearch(textToSearch)
    target = YouTube(link)
    logger.info('Program associated ' + textToSearch + ' to ' + target.title)
    target.streams.first().download(DOWLOAD_LOCATION)
    logger.info(target.title + ' downloaded')

    #convert to mp3
    if ismp3:
        for f in listdir(DOWLOAD_LOCATION):
            pass
        video = DOWLOAD_LOCATION + f
        mp3 = MP3_LOCATION +  f + '.mp3'
        #call ffmpeg
        logger.debug('ffmpeg -n -i ' + '"' + video + '"' + ' -ab 128k ' + '"' + mp3 + '"')
        system('ffmpeg -n -i ' + '"' + video + '"' + ' -ab 128k ' + '"' + mp3 + '"')
        logger.debug('rm ' + '"' + video + '"')
        system('rm ' + '"' + video + '"')
        logger.info(textToSearch + ' converted to mp3')

# Display help
def help():
    print('usage :')
    print('python_youtube.py list.txt')
    print('\n[optional] \n-mp4 download videos \n-mp3 default option convert to mp3')
    print('\n list.txt must contains what you want to download from youtube with a separation of a back to line')

if __name__ == '__main__':
    try:
        #get arguments and check them
        list = sys.argv[1]
        list.split('.txt')[0]
        try:
            mp3 = sys.argv[2]
            if mp3 == '-mp4':
                mp3 = False
            else:
                mp3 = True
        except:
            mp3 = True
        #file verification
        if not exists(list):
            logger.warning('File does not exist')
            raise Exception
        else:
            #We can finaly work
            with open(list, 'r',errors='ignore') as data:
                for line in data:
                    youtubedownload(line)
    except Exception as e:
        help()
