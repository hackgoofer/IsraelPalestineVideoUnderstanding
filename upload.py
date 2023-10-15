from apiclient.discovery import build
from datetime import datetime, timedelta
import isodate
import pytz
import json
import glob
from dotenv import load_dotenv
import os
import requests
load_dotenv()

API_URL = os.getenv("12LABS_API_URL")
assert API_URL, "API_URL not found in .env file"

API_KEY = os.getenv("12LABS_API_KEY")
assert API_KEY, "API_KEY not found in .env file"

print(f"API_URL: {API_URL}")
print(f"API_KEY: {API_KEY}")

def upload_video(video):
    # Set the header of the request
    headers = {
        "x-api-key": API_KEY
    }

    # Declare the /tasks/external-provider endpoint
    TASKS_URL = f"{API_URL}/tasks/external-provider"

    # Construct the body of the request
    data = {
        "index_id": "652b22023c4a426cf3f4f717",  # Specify the unique ID of the index
        "url": f"https://youtu.be/{video}",  # Specify the YouTube URL of the video
        # "video_url": "https://www.youtube.com/watch?v=LOtmTmxjFX4"
    }

    # Upload the video
    print(f"{video}: ploading video")
    response = requests.post(TASKS_URL, headers=headers, json=data)
    print(f"{video}: uploaded video")

    # Store the ID of the task in a variable named TASK_ID
    TASK_ID = response.json().get("_id")
  
    # Print the status code and response
    print(f"Status code: {response.status_code}\t TASK ID: {TASK_ID}")
    print(response.json())
    return 200 <=  response.status_code < 300


# Read the data of format [(title, videoID)] from the json files in loaded_video folder
loaded_videos = []
for file in glob.glob("ready_to_upload/*.json"):
    with open(file, 'r') as json_file:
        loaded_videos.extend(json.load(json_file))

uploaded_video_set = set([
    "vHaHzr5M7gk", "cWxC3I_GdP8", "LOtmTmxjFX4", "I9ThaXIPw7A", "pRGIkD-MvE0",
    "3toseG9-F7I", "bMQM8PwSZyo", "dG-a1izGNL4", "9j6u6Y-EGZc", "SGV3Vceq8wQ",
    "sxsyxwg60kA", "61Hpx-90MWs", "rUZLlzQVsr4", "7Y9fHUOhTMY", "JtQDGdezVjY",
    "6Clbb0ul_qg"
])
for video in loaded_videos:
    if video[1] not in uploaded_video_set:
        success = upload_video(video[1])
        print(f"success: {success}")
        if success:
            uploaded_video_set.add(video[1])

import json
with open('uploaded.json', 'w') as json_file:
    json.dump(list(uploaded_video_set), json_file)

print(f"Done uploading videos onto index, total uploaded: {len(list(uploaded_video_set))}")
    

