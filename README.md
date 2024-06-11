# spotifyd-notify.py
Python script to send a notification on a song change with the song information using Spotify-TUI and Notify-Send

# Installation
- Clone the repo or download the python file
- Set your environment variables:
  - $SPOTIFY_CLIENT_ID
  - $SPOTIFY_CLIENT_SECRET
  - $USER
- Configure spotifyd to run the script on song change hook

# Dependencies
- Python3
- spotifyd
- Spotify-TUI
- notify-send
  ### Python Packages
- sys
- os
- subprocess
- requests
- base64
- urllib.request: urlretrieve
