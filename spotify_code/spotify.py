import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from colorama import Fore
import time

client_id = 'f3074e88dcee4d308c1258ab616be574'
client_secret = '1d933a2161dc4d4cbd30608af2d9aeed'

credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=credentials)

artist_name = 'Little Mix'
result = sp.search(q='artist:' + artist_name, type='artist')
artist = result['artists']['items'][0]

albums = sp.artist_albums(artist['id'],album_type='album')

for album in albums['items']:
    print(Fore.RED)
    print(f"Álbum: {album['name']} - Lanzamiento: {album['release_date']} - Total tracks: {album['total_tracks']}")
    print(Fore.WHITE)
    tracks = sp.album_tracks(album['id'])
    for track in tracks['items']:
        track_details = sp.track(track['id'])
        album_name = track_details['album']['name'].lower()
        #if "remix" in album_name or "expanded" in album_name or "deluxe" in album_name or "edition" in album_name:
        if "expanded" not in album_name:
            continue  # Salta este track si contiene las palabras clave
        print("--------------")
        print(f"ÁLBUM: {track_details['album']['name']}")
        print(f"Pista: {track_details['name']} - Popularidad: {track_details['popularity']}")
        print(f"Duración: {track_details['duration_ms']} ms")
        print(f"Explícito: {'Sí' if track_details['explicit'] else 'No'}")
        print(f"Previsualización: {track_details['preview_url']}")
    print("*************************")
    time.sleep(5)  # Retraso para evitar exceder los límites de la API
    
print



