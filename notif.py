#!/usr/bin/env python3

import sys
import os
import subprocess
import requests
import base64
from urllib.request import urlretrieve

try:
    debug = True if sys.argv[1] == "--debug" else False
except IndexError:
    debug = False

try:
    track_title = subprocess.getoutput(["spt pb -f %t"])
    track_artist = subprocess.getoutput(["spt pb -f %a"])
    track_status = subprocess.getoutput(["spt pb -f %f"])
    album_id = subprocess.getoutput(["spt pb --share-album"])
    if debug:
        print(
            "Title: "
            + track_title
            + "\nArtist: "
            + track_artist
            + "\nStatus: "
            + track_status
            + "\nAlbum ID: "
            + album_id
        )
except subprocess.CalledProcessError:
    print("Nothing Playing", flush=True)
    quit()

client_id = os.environ.get("SPOTIFY_CLIENT_ID")
client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")
user_name = os.environ.get("USER")
if client_id == None:
    print("Client ID not found in $SPOTIFY_CLIENT_ID")
    subprocess.call(["notify-send", "Client ID not found in $SPOTIFY_CLIENT_ID"])
    quit()
elif client_secret == None:
    print("Client Secret not found in $SPOTIFY_CLIENT_SECRET")
    subprocess.call(
        ["notify-send", "Client Secret not found in $SPOTIFY_CLIENT_SECRET"]
    )
    quit()
elif user_name == None:
    print("User not found n $USER")
    subprocess.call(["notify-send", "User not found in $USER"])
    quit()
elif (
    client_id == "Error: no context avaliable"
    or client_secret == "Error: no context avaliable"
):
    print("Error: no context avaliable from spt")
    subprocess.call(["notify-send", "Error: no context avaliable from spt"])
if debug:
    print("\nClient ID: " + client_id + "\nClient Secret: " + client_secret)

auth_req_body = {"grant_type": "client_credentials"}
encoded_client = base64.b64encode(
    (client_id + ":" + client_secret).encode("ascii")
).decode("ascii")
auth_req_headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": "Basic " + encoded_client,
}

auth_resp = requests.post(
    "https://accounts.spotify.com/api/token",
    data=auth_req_body,
    headers=auth_req_headers,
)

try:
    auth_key = auth_resp.json()["access_token"]
except KeyError:
    print("Error, authentication failed")
    subprocess.call(
        ["notify-send", "Error, authentication failed", str(auth_resp.text)]
    )
    quit()


album_req_headers = {"Authorization": "Bearer " + auth_key}
album_info = requests.get(
    "https://api.spotify.com/v1/albums/" + album_id.split("/")[-1],
    data="",
    headers=album_req_headers,
).json()

try:
    urlretrieve(album_info["images"][0]["url"], "cover.png")
except KeyError:
    print("Error retrieving album cover URL")
    subprocess.call(["notify-send", "Error retrieving album cover URL"])
    quit()

subprocess.call(
    [
        "notify-send",
        "--app-name=Spotify",
        "--icon=/home/" + "/.config/spotifyd/cover.png",
        "Now Playing: " + track_title + "",
        "by " + track_artist + " [" + track_status + "]",
    ]
)
