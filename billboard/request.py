import requests

def get_billboard_data(api_key):
    url = "https://api.billboard.com/charts/hot-100"
    params = {
        "api_key": api_key,
        "limit": 10
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed to fetch data from Billboard API")
        return None

# Replace 'YOUR_API_KEY' with your actual Billboard API key
api_key = 'YOUR_API_KEY'
data = get_billboard_data(api_key)

if data:
    for song in data['charts'][0]['entries']:
        print(f"{song['rank']}. {song['title']} by {song['artist']}")
