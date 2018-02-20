# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 02:10:58 2018

@author: WPF95
"""

from __future__ import print_function
import billboard
import pandas as pd  
import spotipy 
import sys
import spotipy.util as util
import os
from spotipy.oauth2 import SpotifyClientCredentials 
import time
import json
import pprint
from collections import OrderedDict
import csv
from dateutil import parser
from retrying import retry


os.environ["SPOTIPY_CLIENT_ID"] = '2db029a6b2c047819deabd13354b2068'
os.environ["SPOTIPY_CLIENT_SECRET"] = '215c52a45bf6495fab0440060ffb643d'
os.environ["SPOTIPY_REDIRECT_URI"] = 'http://www.baidu.com'

username ="geomcintire"
scope = 'user-library-read'
token = util.prompt_for_user_token(username, scope)
sp = spotipy.Spotify(auth=token)


def getdata():
    df = pd.read_csv("data.csv")
    n = len(df)
    value = df.values[n-1].tolist()
    date_last = value[17]
    rank_last = value[3]
    aa = parser.parse(date_last)
    del df
    chart = billboard.ChartData('hot-100',date=date_last)
    k = 0
    while (k+n)<50000:
        if(len(chart)==0):
            chart = billboard.ChartData('hot-100', date=chart.previousDate)
            print("no song")
            continue
        else:
            links = []
            for i in range(0,len(chart)):
                tmp=[]
                bb = parser.parse(chart.date)
                song = chart[i]
                a = song.title
                b = song.artist
                c = song.weeks
                d = song.rank
                if(bb<aa or d>rank_last):
                    tmp.append(a)
                    tmp.append(b)
                    tmp.append(c)
                    tmp.append(d)
                    result=sp.search(a,limit=1)
                    try:
                        data = result['tracks']['items']
                        tmp.append(data[0]['popularity'])
                        feature=sp.audio_features(data[0]['id'])
                        tmp.append(feature[0]['danceability'])
                        tmp.append(feature[0]['energy'])
                        tmp.append(feature[0]['key'])
                        tmp.append(feature[0]['loudness'])
                        tmp.append(feature[0]['mode'])
                        tmp.append(feature[0]['speechiness'])
                        tmp.append(feature[0]['acousticness'])
                        tmp.append(feature[0]['instrumentalness'])
                        tmp.append(feature[0]['liveness'])
                        tmp.append(feature[0]['valence'])
                        tmp.append(feature[0]['tempo'])
                        if(feature[0]['speechiness']>0.66):
                            tmp.append("spoken words")
                        elif(feature[0]['speechiness']>0.33):
                            tmp.append("music and speech")
                        else:
                            tmp.append("music")
                        tmp.append(chart.date)
                        links.append(tmp)
                        k = k+1
                        print(k+n)
                    except:
                        continue
            print(len(links))
            fd = open('data.csv','a',encoding='utf8',newline='')
            writer = csv.writer(fd, lineterminator = '\n')
            writer.writerows(links)
            fd.close()  
            chart = billboard.ChartData('hot-100', date=chart.previousDate)
            print("successflly")

    
getdata()
    
   
#my_df = pd.DataFrame(links)
#my_df.to_csv('data.csv',index = False, header =("title","artist","weeks","rank","popularity","danceability","energy","key","loudness",
#                                                     "mode","speechiness","acousticness","instrumentalness","liveness","valence","tempo","speech","date"))
#print("successful")