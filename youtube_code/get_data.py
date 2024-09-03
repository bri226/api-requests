from googleapiclient.discovery import build
import pyodbc

api_key = 'AIzaSyBD9eHrHmsHrTQA-eV87CR0ZB2T2ANg5TE'
youtube = build('youtube', 'v3', developerKey=api_key)

def connect_to_db():
    # Conexión utilizando autenticación de Windows
    try:
        conn = pyodbc.connect('Driver={SQL Server};'
                        'Server=localhost\\SQLEXPRESS;'  # Asegúrate de tener el doble backslash
                        'Database=DB_BRILLITT;'
                        'Trusted_Connection=yes;')
        return conn
    except Exception as e:
        print("Hubo un error en la conexion: ",e)
        

def get_channel_uploads_list_id(channel_id, youtube):
    response = youtube.channels().list(
        part='contentDetails',
        id=channel_id
    ).execute()

    uploads_list_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    return uploads_list_id

def get_videos_from_playlist(playlist_id, youtube):
    videos = []
    next_page_token = None

    while True:
        response = youtube.playlistItems().list(
            part='snippet,contentDetails',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        video_ids = [item['contentDetails']['videoId'] for item in response['items']]
        stats_response = youtube.videos().list(
            part='snippet,statistics',
            id=','.join(video_ids)
        ).execute()
        
        # print(stats_response)

        for item, stats in zip(response['items'], stats_response['items']):
            video_data = {
                'video_id': item['contentDetails']['videoId'],
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'published_at': item['snippet']['publishedAt'],
                # 'view_count': stats['statistics']['viewCount'],
                'view_count': stats['statistics'].get('viewCount', 'None'),
                'channel_name': stats['snippet']['channelTitle']  # Añadiendo el nombre del canal
            }
            videos.append(video_data)

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return videos


def insert_video_info(videos, conn):
    cursor = conn.cursor()
    for video in videos:
        sql = '''
        INSERT INTO YouTubeVideos (VideoID, Canal, Titulo, Descripcion, PublicadoEn, Vistas)
        VALUES (?, ?, ?, ?, ?, ?)
        '''
        try:
            cursor.execute(sql, (video['video_id'],  video['channel_name'] ,video['title'], video['description'], video['published_at'], video['view_count']))
            conn.commit()
        except pyodbc.Error as e:
            print("Error al insertar datos:", e)
    cursor.close()


def main():
    api_key = 'AIzaSyBD9eHrHmsHrTQA-eV87CR0ZB2T2ANg5TE'
    youtube = build('youtube', 'v3', developerKey=api_key)
    channel_id = 'UCYLNGLIzMhRTi6ZOLjAPSmw'
    # channel_id = 'UCqECaJ8Gagnn7YCbPEzWH6g' # TAYLOR SWIFT
    uploads_list_id = get_channel_uploads_list_id(channel_id, youtube)
    videos = get_videos_from_playlist(uploads_list_id, youtube)
    conn = connect_to_db()
    insert_video_info(videos, conn)
    print("Datos cargados con éxito.")

if __name__ == "__main__":
    main()




