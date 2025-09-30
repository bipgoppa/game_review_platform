import requests
from django.conf import settings

def get_igdb_access_token():
    url = "https://id.twitch.tv/oauth2/token"

    params = {'client_id' : settings.IGDB_CLIENT_ID,
              'client_secret' : settings.IGDB_CLIENT_SECRET,
              'grant_type': 'client_credentials'}
    
    response = requests.post(url, params=params)

    response.raise_for_status()

    return response.json()['access_token']

def search_igdb_games(query):
    access_token = get_igdb_access_token()

    headers = {'Client-ID' : settings.IGDB_CLIENT_ID,
               'Authorization' : f'Bearer {access_token}'
               }
    
    body = f'search "{query}"; fields name, cover.url; limit 20;'

    response = requests.post("https://api.igdb.com/v4/games", headers=headers, data= body)

    print(f"IGDB API Status Code: {response.status_code}")
    print(f"IGDB API Response: {response.json()}")

    response.raise_for_status()

    return response.json()

def get_igdb_game_details(game_id):
    access_token = get_igdb_access_token()

    headers = {'Client-ID' : settings.IGDB_CLIENT_ID,
               'Authorization' : f'Bearer {access_token}'
               }
    
    body = f'fields name, cover.url; where id = {game_id};'

    response = requests.post("https://api.igdb.com/v4/games", headers=headers, data= body)

    response.raise_for_status()

    results = response.json()

    if results:
        return results[0]
    else:
        return None

    