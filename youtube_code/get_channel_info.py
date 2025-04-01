from googleapiclient.discovery import build
import json
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)

def clean_json(data):

    for video in data.get('items', []):
        title = video['snippet']['title']
        video_id = video['id']
        view_count = video['statistics']['viewCount']
        like_count = video['statistics']['likeCount']
        comment_count = video['statistics']['commentCount']
        published_at = video['snippet']['publishedAt']
        description = video['snippet']['description']
        

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
    
    channel_id = 'UCqECaJ8Gagnn7YCbPEzWH6g'
    response = youtube.channels().list(
        part='snippet,contentDetails,statistics',
        id=channel_id
    ).execute()

    print_channel_info(response)

def videos_mas_vistos():
    
    response = youtube.videos().list(
        part='snippet,statistics',
        chart='mostPopular', 
        # regionCode='PE',
        maxResults=10
    ).execute()

    # Imprime la respuesta
    # print(response)
    clean_json(response)


consulta_canal()