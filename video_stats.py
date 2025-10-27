import requests
import json

import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")

YOUR_API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = "MrBeast"
maxResults = 50



def get_playlist_id():

    try:

        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={YOUR_API_KEY}"


        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        #print(json.dumps(data,indent=4))

        channel_items = data["items"][0]

        channel_playlist_id = channel_items["contentDetails"]["relatedPlaylists"]["uploads"]

        #print(channel_playlist_id)
        return channel_playlist_id
    except requests.exceptions.RequestException as e:
        raise e
    

playlistid = get_playlist_id()


def get_video_id(playlistid):
    
    video_ids = []
    pageToken = None
    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId={playlistid}&key={YOUR_API_KEY}"


    
    try:
        while True:
            url = base_url
            if pageToken:
                url += f"&pageToken={pageToken}"
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()
            for item in data.get('items',[]):
                print(item)
                video_id = item["contentDetails"]["videoId"]
                video_ids.append(video_id)
            pageToken = data.get('nextPageToken')
            if not pageToken:
                break  
        return video_ids      
    except requests.exceptions.RequestException as e:
        raise e


if __name__ == "__main__":
    playlistid = get_playlist_id()
    print(playlistid)
    print(get_video_id(playlistid))

