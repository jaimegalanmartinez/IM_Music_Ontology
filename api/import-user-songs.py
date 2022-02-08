#! /usr/bin/python3

import requests
import os.path
import sys
import pathlib

# -------------------------------------------------------------------------------------------------------------

apiBase = 'https://api.spotify.com/v1'
apiHeaders = {}


def apiInit(token):
    global apiHeaders

    apiHeaders = {'Authorization': 'Bearer ' + token,
                  'Content-Type': 'application/json',
                  'Accept': 'application/json'}
    return


def apiFetch(endpoint):
    global apiHeaders
    global apiBase

    resp = requests.get(apiBase + endpoint, headers=apiHeaders)

    if not resp.status_code == 200:
        print('Failed to fetch API: ' + resp.json()['error']['message'])
        exit(1)

    return resp.json()


def getToken():
    scriptPath = str(pathlib.Path(__file__).parent.resolve())
    tokenPath = scriptPath + '/.token.secret'

    if not os.path.isfile(tokenPath):
        print('Missing token file')
        exit(1)

    with open(tokenPath, 'r') as file:
        return file.read().rstrip()


def removePrefix(text, prefix):
    return text[text.startswith(prefix) and len(prefix):]

# -------------------------------------------------------------------------------------------------------------


if len(sys.argv) > 1:
    numberOfSongs = sys.argv[1]
else:
    numberOfSongs = '10'

apiInit(getToken())

idList = []
songInfo = {}
url = '/me/tracks?limit=' + numberOfSongs
favoriteSongs = apiFetch(url)['items']

for song in favoriteSongs:
    track = song['track']
    id = removePrefix(track['uri'], 'spotify:track:')

    idList.append(id)
    songInfo[id] = {
        'artist': track['artists'][0]['name'],
        'name': track['name'],
        'album': track['album']['name'],
        'releaseYear': track['album']['release_date'][0: 4],
        'durationSec': str(int(track['duration_ms'] / 1000))
    }

url = '/audio-features?ids=' + ','.join(idList)
songDetails = apiFetch(url)['audio_features']

for info in songDetails:
    id = info['id']

    songInfo[id]['energy'] = str(int(info['energy']*100))
    songInfo[id]['acousticness'] = str(int(info['acousticness']*100))
    songInfo[id]['danceability'] = str(int(info['danceability']*100))
    songInfo[id]['instrumentalness'] = str(int(info['instrumentalness']*100))
    songInfo[id]['happiness'] = str(int(info['valence']*100))
    songInfo[id]['tempo'] = str(int(info['tempo']))

    print(songInfo[id])
