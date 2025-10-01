# music-scanner
*Recognize all songs in a long audio file*

>
> **NOTE:**
> 
> This is a small personal project from 2023, and it's not super polished. It depends on an API for song recognition that is **not available anymore**.
>
> Song recognition would have to be reimplemented with a different API to get this working again.
>
> This is a small project I created out of interest.
>

### Purpose

Find all songs in a long audio file and add them to a Spotify playlist automatically.

This works by splitting the file into small parts, analyzing some of them, removing duplicates, and matching to Spotify. It can be helpful if you would like to e.g. create a playlist of all songs from a radio broadcast or a DJ set.

### Usage

1. Create and activate the **venv** to access all required modules.

2. Adjust **settings** (optional)
    - By default, the analyzer splits all tracks into segments of 5 seconds, and leaves a gap of 120 seconds between each segment.
    - You can adjust this to your needs.

3. Add **API keys**
    - Fill in the details in `input/variables.py` for
        - your Spotify API key,
        - your audd.io API key,
        - and your desired audio files that should be analyzed.
    - Here, you should also specify the playlist that the analyzer saves the recognized songs to.
