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

filename = "highlight_summaries.csv"

def generate_summary(videoID, videoID_to_filename):
    SUMMARIZE_URL = f"{API_URL}/summarize"
    headers = {
        "x-api-key": API_KEY
    }

    data = {
      "video_id": videoID,
      "type": "summary",
      "prompt": "Summarize if this video is pro-israel or pro-palestine or else and how violent it is."
    }

    response = requests.post(SUMMARIZE_URL, headers=headers, json=data)
    print(f"{videoID}: status code - {response.status_code}")

    summary_data = response.json()
    print(summary_data)

    with open(filename, 'a') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow([videoID, videoID_to_filename[videoID][0], videoID_to_filename[videoID][1], summary_data.get('summary')])

def generate_prompt(videoID, videoID_to_filename):
    SUMMARIZE_URL=f"{API_URL}/generate"
    headers = {
        "x-api-key": API_KEY
    }

    data = {
      "video_id": videoID,
      "prompt": "Summarize video in one paragraph, just describe the content."
    }

    response = requests.post(SUMMARIZE_URL, headers=headers, json=data)
    print(f"{videoID}: status code - {response.status_code}")

    summary_data = response.json()
    # print(summary_data)

    with open(filename, 'a') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow([videoID, videoID_to_filename[videoID][0], videoID_to_filename[videoID][1], summary_data.get('data')])

def generate_highlight(videoID, videoID_to_filename):
    SUMMARIZE_URL=f"{API_URL}/summarize"
    headers = {
        "x-api-key": API_KEY
    }

    data = {
      "video_id": videoID,
      "type": "highlight",
    }

    response = requests.post(SUMMARIZE_URL, headers=headers, json=data)
    print(f"{videoID}: status code - {response.status_code}")

    summary_data = response.json()
    if "highlights" not in summary_data:
        print(summary_data)
        return
    
    highlights = summary_data.get("highlights")
    with open(filename, 'a') as f:
        writer = csv.writer(f, delimiter='\t')
        for highlight in highlights:
            if videoID_to_filename[videoID][1] != "":
                writer.writerow([videoID, videoID_to_filename[videoID][0], videoID_to_filename[videoID][1], highlight["highlight"], highlight["highlight_summary"], highlight["start"], highlight["end"]])

def retrive_videos_from_index():
    # Retrieve the unique identifier of the existing index
    INDEX_ID = os.getenv("INDEX_ID")
    print (INDEX_ID)
    assert INDEX_ID
    videoID_to_filename = {}

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
    videoID_to_filename = {item["_id"]: (item['metadata']['filename'], item['metadata']['youtube'] if 'youtube' in item['metadata'] else "") for item in data}

    while (len(data) == 10):
        count += 1
        INDEXES_VIDEOS_URL = f"{API_URL}/indexes/{INDEX_ID}/videos?page={count}"
        response = requests.get(INDEXES_VIDEOS_URL, headers=headers)
        print(f'Status code: {response.status_code}')
        print(len(data)) 
        data = response.json()["data"]
        new_batch = {}
        for item in data:
            youtube = ""
            if "youtube" not in item['metadata']:
                print(item)
            else:
                youtube = item['metadata']['youtube']
            new_batch[item["_id"]] = (item['metadata']['filename'], youtube)
        videos += data
        videoID_to_filename = {**videoID_to_filename, **new_batch}
  
    return videos, videoID_to_filename

already_summarized_videos = set()
with open(filename, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        already_summarized_videos.add(row[0])

videos, videoID_to_filename = retrive_videos_from_index()
with open('indexed_videos_1.json', 'w') as f:
    json.dump(videos, f)

for video in videos:
    if video["_id"] not in already_summarized_videos:
        generate_highlight(video["_id"], videoID_to_filename)
