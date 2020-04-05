#!/usr/bin/env python
import json
from bs4 import BeautifulSoup as bs
import requests
import urllib.parse
import pyperclip
import spell
import re
import subprocess,os,sys

# Handle wrong spellings
query=input("Enter the movie name:\n")
query=spell.Check(query)
print("Searching for movie: ",query)
#Open Magnet Link
def open_magnet(magnet):
    if sys.platform.startswith('linux'):
        subprocess.Popen(['xdg-open', magnet],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elif sys.platform.startswith('win32'):
        os.startfile(magnet)
    elif sys.platform.startswith('cygwin'):
        os.startfile(magnet)
    elif sys.platform.startswith('darwin'):
        subprocess.Popen(['open', magnet],stdout=subprocess.PIPE, stderr=subprocess.PIPE)


# Handle Streaming

def peerflix_stream(magnet):
  cmd=("""peerflix \"%s\" --vlc""" % (magnet))
  os.system(cmd)
def handle_stream(magnet_link):
    selection=int(1)
    if selection==1:
        stream_handler=int(1)
        if stream_handler==1:
            peerflix_stream(magnet_link)
def yts_search(query):
    print("Welcome to YTS Movie Downloader.\n")
    url='https://yts.am/api/v2/list_movies.json?query_term='+query
    print("Searching......")
    source=requests.get(url).text
    loaded_json= (json.loads(source))
    print(loaded_json['status_message'])
    movie_data=(loaded_json['data'])
    try:
        movies=movie_data['movies']
        result=movies[0]
    except KeyError:
        print ('No movie named ',query,' found on YTS. Try with another providers.\n')
        exit()
    print("\nHere is your search result:\n")
    print('Title: ')
    print(result['title_long'])
    print()
    print('Rating: ')
    print(result['rating'])
    print()
    print('Summary: ')
    print(result['summary'])
    print()
    print('Language: ')
    print(result['language'])
    print()
    available_torrents=result['torrents']

    j=1
    for i in available_torrents:
        print (j,"Quality:",i['quality'],"Size:",i['size'])
        j=j+1
    choice=int(input("Enter your choice: "))
    choice=choice-1
    hash_code=available_torrents[choice]['hash']
    print("Building Magnet Link...")
    m2=hash_code
    m1='magnet:?xt=urn:btih:'
    m4='&tr='
    m5=['udp://open.demonii.com:1337/announce','udp://tracker.openbittorrent.com:80','udp://tracker.coppersurfer.tk:6969','udp://glotorrents.pw:6969/announce','udp://tracker.opentrackr.org:1337/announce','udp://torrent.gresille.org:80/announce','udp://p4p.arenabg.com:1337','udp://tracker.leechers-paradise.org:6969']
    URL_Movie_Name=result['title_long']+" ["+available_torrents[choice]['quality']+"] [YTS.AG]"
    URL_Encoded_Movie_Name=urllib.parse.quote_plus(URL_Movie_Name)
    m3='&dn='+URL_Encoded_Movie_Name
    trackers=""
    for i in range(len(m5)):
        trackers=trackers+m4+m5[i]
    magnet_link=m1+m2+m3+trackers
    print("Your magnet link is copied to your clipboard\n")
    #print(magnet_link)
    pyperclip.copy(magnet_link)
    handle_stream(magnet_link)

yts_search(query)
quit()
