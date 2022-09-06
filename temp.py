import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from itunesLibrary import library
import pandas as pd
import json
import os
import time
from random import sample
from difflib import SequenceMatcher
import datetime as dt

# Credentials you get from registering a new application

playlist_name = 'iTunes Migration ' + str(dt.datetime.now())
filepath = 'data/Library.xml'

os.environ["SPOTIPY_CLIENT_ID"] = str(cid)
os.environ["SPOTIPY_CLIENT_SECRET"] = str(secret)
os.environ["SPOTIPY_REDIRECT_URI"] = str(redirect_uri)

scope = 'playlist-modify-public'

token = SpotifyOAuth(scope=scope, username=user_name)
sp1 = spotipy.Spotify(auth_manager=token)


# ########################################################
def get_itunes(filepath, format='txt'):

  tracks = []

  if format == 'txt':
    with open(filepath, encoding='UTF-16') as fp:
        line = fp.readline()
        cnt = 1
        while line:
                if cnt == 1 :
                    header = line.strip().split('\t')

                try:
                    line = fp.readline()
                    line_list = line.strip().split('\t')
                    tracks.append(line_list[0:2])
            
                except:
                    print(line)
                cnt += 1
    return tracks

###########################################################
def parse_itunes(file):
    lib = library.parse(file)
    json_file = []

    musicItems = set(lib.getPlaylist("Music").items)
    musicItems = sorted(list(musicItems),key=lambda k: (k.artist if k.artist else '',k.title if k.title else '',k.album if k.album else ''))
    
    for item in musicItems:
        # print({'artist': item.artist, 'track': item.title })
        json_file.append({'artist': item.artist, 'track': item.title })

    # json_file = json.dumps(json_file)    

    return json_file


# ########################################################
def search_spotify(track_name, artist):

    token = SpotifyOAuth(scope=scope, username=user_name)
    sp = spotipy.Spotify(auth_manager=token)

    results = sp.search(q="track:" + track_name, type="track")
    items_list = results['tracks']['items'] 

    data = []

    for item in items_list:

        search = str(track_name) + str(artist)
        resp = item['name'] + item['artists'][0]['name']
        seq = SequenceMatcher(None, search, resp).ratio()
        data.append({'track': item['name'], 'artist': item['artists'][0]['name'], 'input_track': track_name, 'input_artist': artist, 'uri': item['uri'], 'ratio': seq  })


        # if item['name'] == track_name and item['artists'][0]['name'] == artist :
        #     data.append({'track': item['name'], 'artist': item['artists'][0]['name'], 'uri': item['uri'], 'match': True, 'ratio': str(seq)  })
        # else:
        #     data.append({'track': item['name'], 'artist': item['artists'][0]['name'], 'uri': item['uri'], 'match': False, 'ratio': str(seq)  })

  


    if len(data) > 0:     
        return  data[0]
    else:
        return {'track': None, 'artist': None, 'input_track': track_name, 'input_artist': artist, 'uri': None, 'ratio': 0}


#####################################################################
def divide_chunks(l, n):
     
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]


##################################################################### 
def load_tracks(playlist_name, track_list):

    token = SpotifyOAuth(scope=scope, username=user_name)
    sp3 = spotipy.Spotify(auth_manager=token)

    play_list_obj = sp3.user_playlist_create(user=user_name, name=playlist_name, public=True)
    playlist_id = play_list_obj['id']

    tracks = []
    for track in track_list:

        tracks.append(track['uri'])

    x = list(divide_chunks(tracks, 100))

    for tracks_chunk in x:
        sp3.user_playlist_add_tracks(user=user_name, playlist_id=playlist_id, tracks=tracks_chunk)
        print('loaded chunks')


################################################################################
def main(limit=None):

    music_list = parse_itunes(file=filepath)

    if limit:
        music_list = sample(music_list, limit)

    
    track_list = []
    failed_list = []
    count = 0

    for music in music_list:
        count = count + 1
        print(music, count)
        search = search_spotify(track_name = music['track'], artist=music['artist'])
        time.sleep(2)

        if search['ratio'] > .50 and search['artist'] == search['input_artist']:
            track_list.append(search)
        else:
            failed_list.append(search)

    json_failed = json.dumps(failed_list)
    with open("data/failed.json", "w") as outfile:
        outfile.write(json_failed)

    json_passed = json.dumps(track_list)
    with open("data/passed.json", "w") as outfile:
        outfile.write(json_passed)


if __name__ == "__main__":
   main()    