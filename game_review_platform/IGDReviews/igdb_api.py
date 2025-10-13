import requests
from django.conf import settings

def get_igdb_access_token():
    #generate an API access token on demand, using our ID and SECRET
    url = "https://id.twitch.tv/oauth2/token"

    #formats our ID, and SECRET into a JSON object to pass in the post request
    params = {'client_id' : settings.IGDB_CLIENT_ID,
              'client_secret' : settings.IGDB_CLIENT_SECRET,
              'grant_type': 'client_credentials'}
    
    response = requests.post(url, params=params)

    #waits to verify that the post is successful for error handling
    response.raise_for_status()

    #returns the new access token
    return response.json()['access_token']

def search_igdb_games(query):
    # Search through the online database to get information about games
    access_token = get_igdb_access_token()

    headers = {'Client-ID' : settings.IGDB_CLIENT_ID,
               'Authorization' : f'Bearer {access_token}'
               }
    #runs a query in sqlpocalypse searching for 20 games, and returns the name, and cover url
    body = f'search "{query}"; fields name, cover.url; where game_type = 0; limit 20;'

    #stores the return of the sql search in an object response
    response = requests.post("https://api.igdb.com/v4/games", headers=headers, data= body)
    print(f"IGDB API Response: {response.json()}") 
    response.raise_for_status()
    #returns the json of the search results
    return response.json()

def get_igdb_game_details(game_id):
    #given a games unique identifier, return a broken down json of its information
    access_token = get_igdb_access_token()

    headers = {'Client-ID' : settings.IGDB_CLIENT_ID,
               'Authorization' : f'Bearer {access_token}'
               }
    #given a specific game id, it returns one games name and cover
    body = f'fields name, summary, cover.url; where id = {game_id};'

    response = requests.post("https://api.igdb.com/v4/games", headers=headers, data= body)

    response.raise_for_status()

    results = response.json()

    if results:
        return results[0]
    else:
        return None

    