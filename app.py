import os
from env import set_env
import db
from Spotify import SpotifyAPI
from send_email import send_email

# API information
set_env()
SPOTIFY_CLIENT_ID = os.environ.get('CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.environ.get('CLIENT_SECRET')


# Instance of the Spotify Class
spotify = SpotifyAPI(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
access_token = spotify.authorize()['access_token'] # Get token
# Get data from the Spotify API
playlist_results = spotify.find_playlist(id='')
date_updated = playlist_results['date_updated']
playlist = playlist_results['playlist']
artists_top_listeners = spotify.find_artists_by_monthly_listeners(playlist=playlist)
artists_popularity = spotify.find_artists_by_popularity(playlist=playlist)

# Save to the database
db.create_database()

# Check if a table with the same data was already in the database
if db.check_duplicates(f'TOP_ARTISTS_MONTHLY_LISTENERS_{date_updated}') and db.check_duplicates(f'TOP_ARTISTS_POPULARITY_{date_updated}'):
    print('The chart is the same as the last time you checked\n')
    # Print results in the console
    print('Artists by monthly listeners:')
    print(*artists_top_listeners, sep='\n')
    print('\nArtists by popularity:')
    print(*artists_popularity, sep='\n')
    # Ask for email
    answer = input('Do you want to send another email? (Y/N)\n')
    if answer.upper() == 'Y':
        # Send email
        send_email(date=date_updated, content=[artists_top_listeners, artists_popularity])
    else:
        print('\nProgram ended\n')
else:
    # Create table for top artists monthly listeners and then add the data inside the table
    db.create_table(f'TOP_ARTISTS_MONTHLY_LISTENERS_{date_updated}', 'position')
    for i in artists_top_listeners:
        db.create_row(table_name=f'TOP_ARTISTS_MONTHLY_LISTENERS_{date_updated}', second_col='position', artist=i[0], position=i[1])

    # Create table for top artists by popularity and then add the data inside the table
    db.create_table(f'TOP_ARTISTS_POPULARITY_{date_updated}', 'popularity')
    for i in artists_popularity:
        db.create_row(table_name=f'TOP_ARTISTS_POPULARITY_{date_updated}', second_col='popularity', artist=i[0], position=i[1])

    # Send email
    send_email(date=date_updated, content=[artists_top_listeners, artists_popularity])