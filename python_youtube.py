from pytube import YouTube
from urllib.request import urlopen
import requests
import sys
from bs4 import BeautifulSoup
from os import system

DOWLOAD_LOCATION = 'YoutubeVideo/'
MP3_LOCATION = 'YoutubeMP3/'

def youtubeSearch(textToSearch):
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)     Chrome/37.0.2049.0 Safari/537.36'}
    #textToSearch = 'One Piece Opening 1'
    url = "https://www.youtube.com/results?search_query=\'" + textToSearch + "\'"
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html,"html.parser")
    link = soup.find(attrs={'class':'yt-uix-tile-link'})
    return ('http://www.youtube.com' + link['href'])

def youtubedownload(textToSearch):
    link = youtubeSearch(textToSearch)
    target = YouTube(link)
    target.streams.first().download(DOWLOAD_LOCATION)
    video = DOWLOAD_LOCATION + target.title + '.webm'
    mp3 = MP3_LOCATION + target.title + '.mp3'

    system('ffmpeg -i ' + '"' + video + '"' + ' -ab 128k ' + '"' + mp3 + '"')
    system('rm ' + '"' + video + '"')

if __name__ == '__main__':
    list = sys.argv[1]
    with open(list, 'r',errors='ignore') as data:
        for line in data:
            youtubedownload(youtubeSearch(line))
