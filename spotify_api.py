import refresh_user_auth as rua
import requests
import json

username = input('What is your spotify login username?: ')
seed_playlist = input('From which playlist would you like to fetch songs from?: ')
song = input('What song would you like to set as your seed (find songs similar to)?: ')
artist = input('Who is the artist of the song?: ')
user_auth_token = rua.get_user_auth()

def search_track_info() -> any:

    """Find track information given a song name"""

    search_url = 'https://api.spotify.com/v1/search'
    header = {'Authorization': f'Bearer {user_auth_token}'}
    track = {'q': f'{song}', 'type': 'track'}
    tracks_info = requests.get(search_url, headers=header, params=track)

    for item in tracks_info.json()['tracks']['items']:
        if item['album']['artists'][0]['name'] == artist:
            track_info = item

    return track_info


def get_my_playlists() -> any:

    """Get my playlist information"""

    currentuser_url = f'https://api.spotify.com/v1/users/{username}/playlists'
    header = {'Authorization': f'Bearer {user_auth_token}'}
    request_playlists = requests.get(currentuser_url, headers = header)

    return request_playlists.json()


def get_specific_playlist() -> any:

    """Used to get a specific playlist information"""

    playlist_info = get_my_playlists()
    playlists = playlist_info['items']

    for playlist in playlists:
        if playlist['name'] == seed_playlist:
            return playlist


def get_tracks_in_playlist() -> any:

    """Get tracks in playlist"""

    the_playlist = get_specific_playlist()
    playlist_id = the_playlist['id']
    playlist_tracks_endpoint = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    header = {'Authorization': f'Bearer {user_auth_token}'}
    track_info = requests.get(playlist_tracks_endpoint, headers=header)

    return track_info.json()


def get_recommendations() -> any:

    """Get recommendations for a seed song"""

    track_id = search_track_info()['id']

    rec_endpoint = 'https://api.spotify.com/v1/recommendations'
    header = {'Authorization': f'Bearer {user_auth_token}'}
    qpb = {'seed_tracks': f'{track_id}'}
    
    recommendations = requests.get(rec_endpoint, headers=header, params=qpb)

    print(recommendations.json())
    

def create_private_playlist() -> any:

    """Create a new private playlist for user"""
    new = input('What would you like the new playlist to be called?: ')
    currentuser_url = f'https://api.spotify.com/v1/users/{username}/playlists'
    header = {'Authorization': f'Bearer {user_auth_token}',
    'Content-Type': 'applicaion/json'}
    rbp_json = json.dumps({'name': f'{new}',
    'public': False,
    'description': 'New playlist made from python script'})
    new_playlist_request = requests.post(currentuser_url, data=rbp_json, headers=header)


if __name__ == "__main__":
    get_recommendations()