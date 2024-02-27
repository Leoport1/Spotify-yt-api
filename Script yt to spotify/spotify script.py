import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import re
from fuzzywuzzy import process
import privatecontent as pc


c_id = pc.spotify_id
c_sc = pc.spotify_secret
print(type(c_id))
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = c_id,
                                               client_secret = c_sc,
                                               redirect_uri="http://localhost:8888/callback",
                                               scope="playlist-modify-public"))

# Read the CSV file
youtube_playlist_df = pd.read_csv('phonk_playlists.csv')

# Filter out rows where 'Channel' is 'unknown'
youtube_playlist_df = youtube_playlist_df[(youtube_playlist_df['Channel'].str.lower() != 'unknown') & (youtube_playlist_df['Title'].str.lower() != 'Private video')]

def clean_title(title):
    # Remove common fluff from titles
    fluff_patterns = [
        r'(?i)\((official|remastered|explicit).*?\)',  # Target specific types of content in parentheses
        r'(?i)\[official video\]',  # Target only 'official video' in square brackets
        r'(?i)\blive (at|in|version|performance)\b',
        r'(?i)\[(official\s)?music video\]',  # Matches [Music Video] and [Official Music Video]
        r'(?i)\(music video\)',  # Matches (Music Video)
        r'(?i)\bHQ\b',  # Matches HQ
        r'(?i)\bLyrics\b',  # Matches Lyrics
        r'(?i)High quality',  # Matches High quality
        r'(?i)\([^)]*\)'
    ]
    for pattern in fluff_patterns:
        title = re.sub(pattern, '', title, flags=re.IGNORECASE)
    # Remove extra spaces and trim
    return ' '.join(title.split()).strip()

def find_best_spotify_match(sp, search_title ,search_channel):
    # Search Spotify for the track
    query = f"{search_title}"
    result = sp.search(q=query, type='track', limit=5)  # Increase limit to get more results

    # Extract Spotify track names and artists
    spotify_tracks = [(track['name'], track['artists'][0]['name'], track['id'],track['popularity']) for track in result['tracks']['items']]
    filtered_tracks = [track for track in spotify_tracks if '16-bit' not in track[0].lower()]
    # Use fuzzy matching to find the best match
    best_match, best_score, best_id = None, 0, None
    for spotify_title, spotify_artist, spotify_id,popularity in filtered_tracks:
        # Create a combined string of title and artist for comparison
        ## combined_spotify = f"{spotify_title} {spotify_artist}"
        ## combined_search = f"{search_title} {search_artist}"

        # Calculate match score
        score = process.extractOne(search_title, [spotify_title])[1]
        print(f"Matching score for '{spotify_title}': {score}") 
        # Update best match if this score is the highest
        if score > best_score:
            best_score = score
            best_match = spotify_title  # or use spotify_title if you prefer
            best_id = spotify_id

    return best_id if best_score >= 75 else None  # Only return match if score is above 75

def create_spotify_playlist(sp, playlist_name, tracks_info):
    # Create a new Spotify playlist
    user_id = sp.current_user()['id']
    playlist = sp.user_playlist_create(user_id, playlist_name)

    # Search for each track on Spotify
    spotify_track_ids = []
    for track in tracks_info:
        clean_tit = clean_title(track['Title'])
        normalt = track['Title']
        clean_art = clean_title(track['Channel'])  # Adjust as needed
        print(clean_tit)
        #print(clean_art)
        best_match_id = find_best_spotify_match(sp, clean_tit,clean_art)
        if best_match_id:
            spotify_track_ids.append(best_match_id) # Agrega el id de la cancion a la lista de ids que seran agregados a la playlist
        else: 
            print(f"No match found for: {clean_tit}")

    # Add tracks to the new playlist
    if spotify_track_ids:
        sp.user_playlist_add_tracks(user_id, playlist['id'], spotify_track_ids)

    return playlist['id']

# Convert to list of dictionaries
tracks_info = youtube_playlist_df.to_dict('records')

playlist_id = create_spotify_playlist(sp, "brazilian phonk",tracks_info)
print(f"Spotify Playlist Created: {playlist_id}")



