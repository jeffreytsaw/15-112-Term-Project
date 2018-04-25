import urllib
import urllib.request 
import urllib.parse
import urllib.error
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import spotipy.util as util
from bs4 import BeautifulSoup
import ssl
import webbrowser
import time

client_credentials_manager = SpotifyClientCredentials(client_id = '443233bf388d4a47835be511e0696f78',
client_secret = '78af78c1c779463db9028e56a4dcfb26')
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
spotify.trace=False

def show_tracks(results):
    tracks = []
    for i, item in enumerate(results['items']):
        track = item['track']
        tracks.append(track['name'])
        # print("   %d %32.32s %s" % (i, track['artists'][0]['name'], track['name']))
    return tracks


def getTracks(emotion):
    if emotion == 'anger':
        emotion = 'angry songs'
    elif emotion == 'sadness':
        emotion = 'sad songs'
    allTracks = []
    playlistList = spotify.search(q = emotion, type = 'playlist')
    for playlist in playlistList['playlists']['items']:
        try:
            results = spotify.user_playlist(playlist['owner']['id'],playlist['id'],
            fields = 'tracks, next')
            tracks = results['tracks']
            allTracks.extend(show_tracks(tracks))
        except:
            continue
    return list(set(allTracks))


def getDuration(songName):
    results = spotify.search(q = songName, type = 'track')
    uri = results['tracks']['items'][0]['uri']
    return spotify.audio_analysis(uri)['track']['duration']


def getURL(songName):
    textToSearch = songName
    query = urllib.parse.quote(songName)
    url = "http://www.youtube.com/results?search_query=" + query
    context = ssl._create_unverified_context()
    response = urllib.request.urlopen(url,context = context)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    count = 0
    for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
        if count == 0:
            return ('https://www.youtube.com' + vid['href'])
        count += 1


def playPlaylist(emotion):
    if emotion == 'sad':
        return playPlaylist('sad songs')
    elif emotion == 'angry':
        return playPlaylist('angry songs')
    tracks = getTracks(emotion)
    for track in tracks:
        duration = getDuration(track) + 8 #adds offset
        url = getURL(track)
        webbrowser.open(url)
        time.sleep(duration)


    
# 
# textToSearch = 'Spirits'
# query = urllib.parse.quote(textToSearch)
# url = "http://www.youtube.com/results?search_query=" + query
# context = ssl._create_unverified_context()
# response =  urllib.request.urlopen(url, context = context)     
# html = response.read()
# soup = BeautifulSoup(html, "html.parser")
# count = 0
# for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
#     if count == 1:
#         print ('https://www.youtube.com' + vid['href'])
#     count += 1
# # webbrowser.open('http://www.google.com')
    


# result = spotify.search(q = 'sad Songs', type = 'playlist')
# for playlist in result['playlists']['items']:
#     print()
#     print (playlist['name'])
#     print('  total tracks', playlist['tracks']['total'])
#     try:
#         results = spotify.user_playlist('spotify',playlist['id'], 
#         fields="tracks,next")
#         tracks = results['tracks']
#         print (show_tracks(tracks))
#         while tracks['next']:
#             tracks = spotify.next(tracks)
#             show_tracks(tracks)
#     except:
#         pass
#     
    



#Search's for track, gets uri, and gets duration#

# results = spotify.search(q = 'Spirits', type = 'track')
# print (results['tracks']['items'][0]['name']) 
# print (results['tracks']['items'][0]['uri'])
# uri = results['tracks']['items'][0]['uri']
# print (spotify.audio_analysis(uri)['track']['duration'])






# lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'
# 
# results = spotify.artist_top_tracks(lz_uri)
# 
# for track in results['tracks'][:10]:
#     print ('track    : ' + track['name'])
#     print ('audio    : ' + track['preview_url'])
#     print ('cover art: ' + track['album']['images'][0]['url'])
#     print ('duration: ' + track['duration_ms'])

# print (spotify)
# happyID = 'happy'
# results = spotify.search(q = happyID, type = 'playlist')
# print (results['playlists']['items'][0]['owner'])



# birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
# results = spotify.artist_albums(birdy_uri, album_type='album') 
# albums = results['items']
# while results['next']:
#     results = spotify.next(results)
#     albums.extend(results['items'])
# for album in albums: print (album['name'])



# export SPOTIPY_CLIENT_ID = 443233bf388d4a47835be511e0696f78
# export SPOTIPY_CLIENT_SECRET = 78af78c1c779463db9028e56a4dcfb26
# # export SPOTIPY_REDIRECT_URI='your-app-redirect-url
# def playSongs(emotion, username):
#     spotify = spotipy.Spotify()
#     happyID = (
#     'https://open.spotify.com/user/spotify/playlist/37i9dQZF1DXdPec7aLTmlC?')
#     results = spotify.search(q = 'weezer', limit  = 30)
#     for i, t in enumerate(results['tracks']['items']):
#         print(' ', i, t['name'])
#     
    
    
    
    # scope = ''
    # token = util.prompt_for_user_token(username,scope)
    # if token:
    #     sp = spotipy.Spotify(auth = token)
    #     sp.trace = False
    #     results = sp.current_user_playlists(limit = 50)
    #     return results
    # else:
    #     print("Can't get token for", username)
   
    

    