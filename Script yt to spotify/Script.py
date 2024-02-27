from googleapiclient.discovery import build
import pandas as pd
import privatecontent as pc


# YouTube API setup
api_key = pc.ytkey
youtube = build('youtube', 'v3', developerKey=api_key)
pageToken = None
# Fetch YouTube playlist information
playlist_id = 'PLCMoFg5w7yOy4VwiN8PVtrbSiGVezYRHM'
playlist_data = []
while True:
    request = youtube.playlistItems().list(
        part='snippet,contentDetails',
        playlistId=playlist_id,
        maxResults=90,
        pageToken=pageToken
    )
    response = request.execute()
    # Process current page
    for playlist_item in response['items']:
        video_title = playlist_item['snippet'].get('title')
        channel_title = playlist_item['snippet'].get('videoOwnerChannelTitle', 'unknown')
        playlist_data.append([video_title, channel_title])

    # Check for next page
    pageToken = response.get('nextPageToken')
    if not pageToken:
        break

# Create a DataFrame
#youtube_playlist_df = pd.DataFrame(playlist_data, columns=['Title', 'Channel'])

csv_file_path = 'C:\\Users\\leone\\OneDrive\\Desktop\\Jr Portafolio\\Projects\\Script yt to spotify\\phonk_playlists.csv'
excel_file_path = 'C:\\Users\\leone\\OneDrive\\Desktop\\Jr Portafolio\\Projects\\Script yt to spotify\\BTMH_playlists.xlsx'

#Save to CSV
#youtube_playlist_df.to_csv(csv_file_path, index=False)

#Save to Excel
#youtube_playlist_df.to_excel(excel_file_path, index=False)

# Print video titles (optional)
for playlist_item in response['items']:
    video_title = playlist_item['snippet']['title']
    channel_title = playlist_item['snippet'].get('videoOwnerChannelTitle')
    print(f"{video_title} , {channel_title}")


# Create a DataFrame with the song titles and the channel name 'keshi' for all entries
song_titles_new_playlist = [
    "TUCA_DONKA", "FIM_DO_MUNDO", "MTG_-_PIPISKA_FOGO_PARAR", "BESTA_FERA", "MONTAGEM_-_SUCESSO",
    "MTG_-_PISTA_TOMA", "RITMO_BRUTALISMO", "ALORS_BRAZIL", "YUM_YUM", "LAUGH_IN_HELL",
    "PSYCHO_FUNK", "Esse_Baile", "The_Automotivo_Infernal_1.0_-_Purple", "Phonk_Bachi_Bachi",
    "INSONIA", "CURSEDEVIL, DJ FKU, D4C - MTG NASCIDO NO INFERNO HELLBORN 2.0", "OBRIGADO_AGRESSIVO",
    "PHONK_BRASILEIRO_FRESCO", "PR_IN_RIO", "TREINAMENTO_DE_FORÇA", "Montagem_-_Risada_Alucinante",
    "ultraphunk", "Sequência_da_Dz7", "TERÁ_MATANÇA", "AUTOMOTIVO_ASSOMBRA_LUARA", "saiyan",
    "PYPY", "AREAMATE_MIZ", "AWAKE", "BB_Funk", "C_O_V_E_N", "DANÇA_SELVAGEM", "muscle_muscle_[Luffy_gear5]"
]
new_playlist_df = pd.DataFrame({
    'Title': song_titles_new_playlist,
    'Channel': ['phonk'] * len(song_titles_new_playlist)
})
new_playlist_df.to_csv(csv_file_path, index=False)