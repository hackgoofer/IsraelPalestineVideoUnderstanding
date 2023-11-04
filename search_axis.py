from datetime import datetime, timedelta
import isodate
import pytz
import json
import glob
from dotenv import load_dotenv
import os
import requests
import json
from datetime import datetime
load_dotenv()

API_URL = os.getenv("12LABS_API_URL")
assert API_URL, "API_URL not found in .env file"

API_KEY = os.getenv("12LABS_API_KEY")
assert API_KEY, "API_KEY not found in .env file"

def search(text: str, data=None):
    if data is None:
      data = {}

    headers = {
      "x-api-key": API_KEY
    }

    count = 1
    json_data = {
        "query": text,
        "index_id": os.getenv("INDEX_ID"),
        "search_options": ["visual", "conversation", "text_in_video"],
        "operator": "or",
        "page_limit": 50
    }
    grabbed_data = set()
    SEARCH_URL = f"{API_URL}/search"
    response = requests.post(SEARCH_URL, headers=headers, json=json_data)
    print(f"Status code: {response.status_code}")
    response_data = response.json()["data"]
    next_page_token = response.json()["page_info"]["next_page_token"]
    for r in response_data:
        video_id = r.get("video_id")

        print(r)
        if video_id and video_id not in grabbed_data and video_id in videoID_to_youtubeID:
            data.setdefault(video_id, {})[text] = {
                "score": r.get("score"),
                "start": r.get("start"),
                "end": r.get("end"),
            }
            grabbed_data.add(video_id)
            data.setdefault(video_id, {})["youtube"] = videoID_to_youtubeID[video_id]

    print(f"grabbed: {len(grabbed_data)}")

    while len(grabbed_data) != 10:
        count += 1
        SEARCH_URL = f"{API_URL}/search/{next_page_token}"
        response = requests.post(SEARCH_URL, headers=headers, json=data)
        print (f"Status code: {response.status_code}")
        response_data = response.json()["data"]
        if "next_page_token" not in response.json()["page_info"]:
            break
        
        next_page_token = response.json()["page_info"]["next_page_token"]
        for r in response_data:
            video_id = r["video_id"]
            if video_id and video_id not in grabbed_data and video_id in videoID_to_youtubeID:
                data.setdefault(video_id, {})[text] = {
                    "score": r.get("score"),
                    "start": r.get("start"),
                    "end": r.get("end"),
                }
                data.setdefault(video_id, {})["youtube"] = videoID_to_youtubeID[video_id]
            grabbed_data.add(video_id)
        print(f"grabbed: {len(grabbed_data)}")

    return data


def normalize(data, key):
    max_score = max([item[key]['score'] for item in data.values() if key in item])
    min_score = min([item[key]['score'] for item in data.values() if key in item])
    for video_id, item in data.items():
        if key in item:
            item[key]['score'] = (item[key]['score'] - min_score) / (max_score - min_score) * 100

import json
with open('v2yIDMap.json', 'r') as json_file:
    videoID_to_youtubeID = json.load(json_file)
    print(videoID_to_youtubeID)

videoID_data = search("pro-palestinian", {})
search("violence", videoID_data)
normalize(videoID_data, "pro-palestinian")
normalize(videoID_data, "violence")

import pdb; pdb.set_trace()

with open('search_index4.json', 'w') as json_file:
    json.dump(videoID_data, json_file)



