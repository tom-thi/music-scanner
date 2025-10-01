import requests
from settings import TrackSplitSettings
from pydub import AudioSegment
from tqdm import tqdm
import spotipy
from spotipy.oauth2 import SpotifyOAuth


def getUriFromUpload(filePath: str, apiKey: str) -> str | None:
    # create payload for request
    data = {
        "return": "spotify",
        "api_token": apiKey
    }
    files = {
        'file': open(filePath, 'rb'),
    }

    # perform request
    result = requests.post("https://api.audd.io/", data=data, files=files).json()
    
    # check validity of response
    if result["status"] != "success":
        print(f"Audio recognition unsuccessful:\n{result}\nskipping segment:\n{filePath}")
        return None
    if result["result"] is None:
        return None 

    # unpack result
    try:
        return result["result"]["spotify"]["uri"]
    except KeyError:
        print(f"Unexpected reply from audd.io, likely not available on Spotify.\nIf valid, you can add this song later:\n{result}")
        return "add later"


def splitAudioFile(inputFilePath: str, trackSplitSettings: TrackSplitSettings) -> list[str]:
    audio = AudioSegment.from_file(inputFilePath)
    allFilePaths = []

    total_duration = len(audio)
    current_position = 0
    segment_number = 0

    # initialize progress bar
    step_in_ms = (trackSplitSettings.gap_duration_in_s + trackSplitSettings.segment_duration_in_s) * 1000
    pbar = tqdm(range(total_duration), desc="Splitting audio track", )

    while current_position < total_duration:
        start_time = current_position
        end_time = min(current_position + trackSplitSettings.segment_duration_in_s * 1000, total_duration)

        # Extract the segment
        segment = audio[start_time:end_time]

        # Export the segment to a new file
        output_file = f"cache/audio_segment{segment_number}.mp3"
        segment.export(output_file, format="mp3")
        allFilePaths.append(output_file)

        # Move to the next segment (considering the gap)
        current_position = end_time + trackSplitSettings.gap_duration_in_s * 1000
        segment_number += 1

        # Update the progress bar
        pbar.update(step_in_ms)
        pbar.refresh()

    # return a list with all created segment's file paths
    return allFilePaths


def addUriToPlaylist(clientId: str, clientSecret: str, redirectUri: str, username: str, playlistId: str, uris: list[str]):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=clientId,
                                                client_secret=clientSecret,
                                                redirect_uri=redirectUri,
                                                scope="playlist-modify-private"))
    try: 
        sp.user_playlist_add_tracks(username, playlistId, uris, position = 0)
    except spotipy.exceptions.SpotifyException:
        print(uris)
