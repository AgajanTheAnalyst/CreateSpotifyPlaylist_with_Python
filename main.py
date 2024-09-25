import requests
from bs4 import BeautifulSoup

import spotipy
from spotipy.oauth2 import SpotifyOAuth


"""
Using BeautifulSoup to get the Billboards top songs for 2nd week of year 2010
"""

url = "https://www.billboard.com/charts/hot-100/2010-01-16/"
response = requests.get(url)
text = response.text

soup = BeautifulSoup(text, 'html.parser')
songs = soup.select("li ul li h3")

song_titles = [song.get_text().strip() for song in songs]


"""
Authenticating Spotipy
"""
client_id = "3aef422569444cc09dfd0057a98de726"
client_secret = "eca615be8b6b4c49b5ae91aaa841dc93"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret,
                                               redirect_uri='http://example.com',scope="playlist-modify-public"))



"""
Getting the song uris of our Billboard songs
"""
Song_Uris = []
for i in range(len(song_titles)):
    query = song_titles[i]
    result = sp.search(q=query,type='track',limit=1)
    new_uri = [uri['uri'] for uri in result['tracks']['items']]
    if new_uri:
        Song_Uris.append(new_uri[0])
    continue

"""
Creating a spotify playlist 
"""
user_id = sp.me()['id']

playlist_name = 'My_Playlist'

new_playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True, description='My songs')

playlist_id = new_playlist['id']

"""
Add songs to new created playlist
"""

sp.playlist_add_items(playlist_id=playlist_id, items=Song_Uris)


