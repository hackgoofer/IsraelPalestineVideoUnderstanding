

import os
import json
import requests
import os
import csv
from dotenv import load_dotenv
import json

load_dotenv()

API_URL = os.getenv("12LABS_API_URL")
assert API_URL, "API_URL not found in .env file"

API_KEY = os.getenv("12LABS_API_KEY")
assert API_KEY, "API_KEY not found in .env file"

INDEX_ID = os.getenv("INDEX_ID")
assert INDEX_ID, "INDEX_ID not found in .env file"

def get_title_to_youtubeID():
    title_to_youtubeID = {}
    directory = 'ready_to_upload'
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            with open(os.path.join(directory, filename), 'r') as f:
                videos = json.load(f)
                for video in videos:
                    title, youtubeID = video
                    title_to_youtubeID[title] = youtubeID
    return title_to_youtubeID


def retrive_videos_from_index():
    # Retrieve the unique identifier of the existing index
    INDEX_ID = os.getenv("INDEX_ID")
    print (INDEX_ID)
    assert INDEX_ID
    filename_to_videoid = {}

    # Set the header of the request
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    count = 1
    # List all the videos in an index
    INDEXES_VIDEOS_URL = f"{API_URL}/indexes/{INDEX_ID}/videos?page={count}"
    response = requests.get(INDEXES_VIDEOS_URL, headers=headers)
    print(f'Status code: {response.status_code}')
    data = response.json()["data"]
    videos = data
    filename_to_videoid = {item['metadata']['filename'] : item["_id"] for item in data}

    while (len(data) == 10):
        count += 1
        INDEXES_VIDEOS_URL = f"{API_URL}/indexes/{INDEX_ID}/videos?page={count}"
        response = requests.get(INDEXES_VIDEOS_URL, headers=headers)
        print(f'Status code: {response.status_code}')
        print(len(data)) 
        data = response.json()["data"]
        new_batch = {item['metadata']['filename']: item["_id"] for item in data}
        videos += data
        filename_to_videoid = {**filename_to_videoid, **new_batch}
  
    return videos, filename_to_videoid

_, filename_to_videoid = retrive_videos_from_index()
title_to_youtubeID = get_title_to_youtubeID()

import pdb; pdb.set_trace();
data = {}
for filename, videoID in filename_to_videoid.items():
    if filename in title_to_youtubeID:
        data[filename] = (videoID, title_to_youtubeID[filename])
    else:
        print("filename not found")
        print(filename)
        print(videoID)

import pdb; pdb.set_trace();

for filename, (videoID, youtubeID) in data.items():
    VIDEOS_URL = f"{API_URL}/indexes/{INDEX_ID}/videos/{videoID}"
    headers = {
        "x-api-key": API_KEY
    }
    data = {
        "metadata": {
            "youtube": youtubeID
        }
    }
    response = requests.put(VIDEOS_URL, headers=headers, json=data)
    print(f'{videoID}, {youtubeID}: Status code- {response.status_code}')
    if not 200 <=  response.status_code < 300:
        import pdb; pdb.set_trace()
        print(response)

