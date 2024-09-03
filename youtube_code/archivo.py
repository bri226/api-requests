from googleapiclient.discovery import build
import json

# Reemplaza 'YOUR_API_KEY' con tu clave de API real
api_key = 'AIzaSyBD9eHrHmsHrTQA-eV87CR0ZB2T2ANg5TE'
youtube = build('youtube', 'v3', developerKey=api_key)

def clean_json(data):

    # Procesa cada video en la respuesta
    for video in data.get('items', []):
        title = video['snippet']['title']
        video_id = video['id']
        view_count = video['statistics']['viewCount']
        like_count = video['statistics']['likeCount']
        comment_count = video['statistics']['commentCount']
        published_at = video['snippet']['publishedAt']
        description = video['snippet']['description']
        
        # Imprime los detalles del video
        print(f"Video Title: {title}")
        print(f"Video ID: {video_id}")
        print(f"Views: {view_count}")
        print(f"Likes: {like_count}")
        print(f"Comments: {comment_count}")
        print(f"Published at: {published_at}")
        print(f"Description: {description[:50]}...")  # muestra solo los primeros 50 caracteres
        print("-" * 50)  # separador para cada video


def print_channel_info(data):
    print("Channel Information:")
    for item in data['items']:
        print(f"  Title: {item['snippet']['title']}")
        print(f"  Description: {item['snippet']['description'].strip()}")
        print(f"  Custom URL: {item['snippet']['customUrl']}")
        print(f"  Published At: {item['snippet']['publishedAt']}")
        print(f"  Thumbnails:")
        for size, thumbnail in item['snippet']['thumbnails'].items():
            print(f"    {size.capitalize()} - {thumbnail['url']} ({thumbnail['width']}x{thumbnail['height']})")
        print(f"  Total Views: {item['statistics']['viewCount']}")
        print(f"  Subscriber Count: {item['statistics']['subscriberCount']}")
        print(f"  Video Count: {item['statistics']['videoCount']}")
        print("-" * 50)
        
def consulta_canal():
    
    # Obtén detalles del canal por ID de canal
    channel_id = 'UCqECaJ8Gagnn7YCbPEzWH6g'  # Por ejemplo, ID del canal de Google Developers
    response = youtube.channels().list(
        part='snippet,contentDetails,statistics',
        id=channel_id
    ).execute()

    print_channel_info(response)

def videos_mas_vistos():
    
    # Solicita la lista de los videos más populares
    response = youtube.videos().list(
        part='snippet,statistics', # Información a obtener
        chart='mostPopular',                      # Especifica que quieres los videos más populares
        # regionCode='PE',                          # Opcional: código del país para filtrar los videos populares en esa región
        maxResults=10                             # Cantidad de resultados a retornar
    ).execute()

    # Imprime la respuesta
    # print(response)
    clean_json(response)


consulta_canal()