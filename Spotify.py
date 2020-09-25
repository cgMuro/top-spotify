import requests
import base64

# Playlist id
TOP_ARTIST_PLAYLIST_ID = '33Re55lSgkd5XzB6YMhFZA'


class SpotifyAPI:
    '''This class is used to manage requests to the Spotify API'''
    
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = ''

    def authorize(self):
        # Spotify Authorization
        client_creds = f'{self.client_id}:{self.client_secret}'
        client_creds_b64 = base64.b64encode(client_creds.encode())
        # POST request to Spotify API
        res = requests.post(
            url='https://accounts.spotify.com/api/token', 
            data={
                'grant_type': 'client_credentials'
            }, 
            headers={
            'Authorization': f'Basic {client_creds_b64.decode()}'
        })
        # Validate the response
        try:
            res.raise_for_status()
            res = res.json()
            self.access_token = res['access_token']
            return {
                'access_token': res['access_token'],
                'expires_in': res['expires_in']
            }
        except Exception as err:
            print('There was something wrong.')
            print(err)

    def find_playlist(self, id):
        # Get playlist by id
        id = TOP_ARTIST_PLAYLIST_ID if id == '' else id
        # Get playlist from Spotify API
        res = requests.get( 
            f'https://api.spotify.com/v1/playlists/{id}',
            headers={
                'Authorization' : f'Bearer {self.access_token}'
            }
        )
        # Validate the response
        try:
            res.raise_for_status()
            res = res.json()
            playlist = res['tracks']['items']
            date_updated = res['name'].split(' ')[-1].replace('.', '_')
            return {
                'date_updated': date_updated,
                'playlist': playlist
            }
        except Exception as err:
            print('There was something wrong.')
            print(err)
    
    def find_artists_by_monthly_listeners(self, playlist):
        # Get artists inside the playlist
        artists = [{'name': playlist[i]['track']['artists'][0]['name'], 'id': playlist[i]['track']['artists'][0]['id']} for i in range(len(playlist))]

        # Remove duplicates
        set_ = set()
        result = []
        for a in artists:
            t = tuple(a.items())
            if t not in set_:
                set_.add(t)
                result.append(a)
        # Get only the top 10 artists
        artists_list = result[:10]

        # Create top artists list
        top_artists = []

        for i in artists_list:
            # Append a tuple with name and ranking for each artist
            top_artists.append((i['name'], artists_list.index(i) + 1))
        
        return top_artists

    def find_artists_by_popularity(self, playlist):
        # Get artists
        artists = [{'name': playlist[i]['track']['artists'][j]['name'], 'id': playlist[i]['track']['artists'][j]['id']} for i in range(len(playlist)) for j in range(len(playlist[i]['track']['artists']))]

        # Remove duplicates
        set_ = set()
        result = []
        for a in artists:
            t = tuple(a.items())
            if t not in set_:
                set_.add(t)
                result.append(a)
        artists_list = result

        # Get the popularity of each artist
        positions =  []
        for artist in range(len(artists_list)):
            id = artists_list[artist]['id']
            # Get artist from Spotify API
            res = requests.get(
                f'https://api.spotify.com/v1/artists/{id}',
                headers={
                    'Authorization' : f'Bearer {self.access_token}'
                }
            )
            # Validate response
            try:
                res.raise_for_status()
                res = res.json()
                positions.append((res['name'], res['popularity']))
            except Exception as err:
                print('Something went wrong.')
                print(err)
        # Sort top_artists list and get the top 10
        top_artists = sorted(positions, key=lambda tuple: tuple[1], reverse=True)[:10]

        return top_artists