import pyodbc
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from colorama import Fore

client_id = 'f3074e88dcee4d308c1258ab616be574'
client_secret = '1d933a2161dc4d4cbd30608af2d9aeed'

credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=credentials)

conn = pyodbc.connect('Driver={SQL Server};'
                        'Server=localhost\\SQLEXPRESS;'  # Asegúrate de tener el doble backslash
                        'Database=DB_BRILLITT;'
                        'Trusted_Connection=yes;')
cursor = conn.cursor()

def insert_data(query, params):
    cursor.execute(query, params)
    conn.commit()

# Función para verificar e insertar artistas
def ensure_artist(artist_id, artist_name):
    try:
        query = "SELECT id_artist FROM Artist WHERE id_artist = ?"
        cursor.execute(query, (artist_id,))
        data = cursor.fetchone()
        if not data:
            insert_artist = "INSERT INTO Artist (id_artist, name) VALUES (?, ?)"
            insert_data(insert_artist, (artist_id, artist_name))
    except Exception as e:
        print(f"Error ensuring artist: {e}")

# Buscar el artista por nombre y obtener álbumes
artist_name = 'Shakira'
result = sp.search(q='artist:' + artist_name, type='artist')
artist = result['artists']['items'][0]
artist_id = artist['id']

# Asegurarse de que el artista principal está insertado
ensure_artist(artist_id, artist['name'])

# Obtener y procesar álbumes
albums = sp.artist_albums(artist_id)
for album in albums['items']:
    album_id = album['id']
    insert_album = "INSERT INTO Album (id_album, name, id_artist, release_date, total_tracks, release_date_precision, url_spotify) VALUES (?, ?, ?, ?, ?, ?, ?)"
    insert_data(insert_album, (album_id, album['name'], artist_id, album['release_date'], album['total_tracks'], album['release_date_precision'], album['external_urls']['spotify']))

    # Obtener y procesar pistas de cada álbum
    tracks = sp.album_tracks(album_id)
    for track in tracks['items']:
        track_id = track['id']
        track_details = sp.track(track_id)
        insert_track = "INSERT INTO Track (id_track, id_album, name, popularity, duration_ms, explicit, preview_url) VALUES (?, ?, ?, ?, ?, ?, ?)"
        insert_data(insert_track, (track_id, album_id, track_details['name'], track_details['popularity'], track_details['duration_ms'], track_details['explicit'], track_details['preview_url']))

        # Procesar artistas colaboradores (si los hay)
        for artist_collab in track['artists']:
            ensure_artist(artist_collab['id'], artist_collab['name'])
            if artist_collab['id'] != artist_id:  # Asegurarse de que no sea el artista principal
                insert_collab = "INSERT INTO Collaboration (id_track, id_artist) VALUES (?, ?)"
                insert_data(insert_collab, (track_id, artist_collab['id']))

# Cerrar la conexión a la base de datos
cursor.close()
conn.close()