from tqdm import tqdm

from input.variables import (
    API_KEY,
    CLIENT_ID,
    CLIENT_SECRET,
    PLAYLIST_ID,
    QUEUE,
    REDIRECT_URI,
    USERNAME,
)
from settings import TrackSplitSettings
from util import addUriToPlaylist, getUriFromUpload, splitAudioFile

SETTINGS = TrackSplitSettings()

def main():   
    for element in QUEUE:
        # prepare audio files
        files = splitAudioFile(element, SETTINGS)

        # get spotify URIs
        uris = []
        for file in tqdm(files, desc="Analyzing segments"):
            uri = getUriFromUpload(file, API_KEY)
            if uri == "add later":
                try:
                    print("previous uri:", uris[-1])
                except IndexError:
                    # this is the first song
                    pass
                continue
            if uri is not None and uri not in uris:
                uris.append(uri)

        # add songs to playlist
        addUriToPlaylist(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, USERNAME, PLAYLIST_ID, uris)


if __name__ == "__main__":
    main()