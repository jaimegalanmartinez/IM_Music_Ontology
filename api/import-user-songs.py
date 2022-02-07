#! /usr/bin/python3

import requests
import os.path
import sys
import pathlib

scriptPath = str(pathlib.Path(__file__).parent.resolve())
tokenPath = scriptPath + '/.token.secret'
apiBase = 'https://api.spotify.com/v1'

if len(sys.argv) > 1:
    numberOfSongs = sys.argv[1]
else:
    numberOfSongs = '10'

if not os.path.isfile(tokenPath):
    print('Missing token file')
    exit(1)

with open(tokenPath, 'r') as file:
    token = file.read().rstrip()

headers = {'Authorization': 'Bearer ' + token,
           'Content-Type': 'application/json',
           'Accept': 'application/json'}

resp = requests.get(apiBase + '/me/tracks?limit=' + numberOfSongs, headers=headers)

if not resp.status_code == 200:
    print('Failed to fetch songs: ' + resp.json()['error']['message'])
    exit(1)

favoriteSongs = resp.json()['items']

for song in favoriteSongs:
    track = song['track']
    print(track['artists'][0]['name'] + " - " + track['name'])
