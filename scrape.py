from apiclient.discovery import build
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

DEVELOPER_KEY = os.getenv("GOOGLE_DEVELOPER")
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def youtube_search(query, max_results=40, order="relevance", token=None, location=None, location_radius=None):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    videos_map = set()
    videos = []
    count = 0
    pageToken = None

    while len(videos) < max_results:
        search_response = youtube.search().list(
            q=query,
            relevanceLanguage="en",
            type="video",
            regionCode='IQ',
            pageToken=pageToken,
            order=order,
            part="id,snippet",
            maxResults=min(50, max_results - len(videos)),
            location=location,
            locationRadius=location_radius
        ).execute()

        print(f"total videos fetched so far: {len(videos)}")
        pageToken = search_response.get('nextPageToken')
        if not pageToken:
            break
            
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                title = search_result['snippet']['title']
                videoId = search_result['id']['videoId']
                channelId = search_result['snippet']['channelId']
                channel_response = youtube.channels().list(
                    part='statistics',
                    id=channelId
                ).execute()
                # subscriber_count = int(channel_response['items'][0]['statistics']['subscriberCount'])

                # if subscriber_count < 10_000_000:
                video_response = youtube.videos().list(
                    part='contentDetails',
                    id=videoId
                ).execute()
                duration = isodate.parse_duration(video_response['items'][0]['contentDetails']['duration'])
                published_at = isodate.parse_datetime(search_result['snippet']['publishedAt'])
                if duration.total_seconds() >= 30 and duration.total_seconds() != 0 and duration.total_seconds()/60 <= 5 and (datetime.now(pytz.UTC) - published_at).days < 5 and (videoId not in videos_map):
                    videos_map.add(videoId)
                    videos.append((title, videoId))

        filename = f'IQ_40/english_videos_{count}.json'
        with open(filename, 'w') as json_file:
            json.dump(videos, json_file)
        count += 1

    return videos

def load_existing_videos(filename):
    try:
        with open(filename, 'r') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return []

def filter_individuals_videos(videos, existing_videos):
    major_media = ["CNN", "BBC", "Fox News", "MSNBC", "Al Jazeera", "The Guardian", "The New York Times", "The Washington Post", "Reuters", "Associated Press"]
    individual_videos = []
    for video in videos:
        if not any(media in video[0] for media in major_media) and video not in existing_videos:
            individual_videos.append(video)
    return individual_videos

existing_videos = []
for file in glob.glob("loaded_videos/*.json"):
    with open(file, 'r') as json_file:
        existing_videos.extend(json.load(json_file))

# english_videos = youtube_search("Israel Hamas war")
english_videos = youtube_search("Israel Palestine Conflict Latest")
filtered_english_videos = filter_individuals_videos(english_videos, existing_videos)


timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f'loaded_videos/english_videos_{timestamp}.json'
with open(filename, 'w') as json_file:
    json.dump(filtered_english_videos, json_file)

print(f"Done processing... unfiltered: {len(english_videos)}, filtered: {len(filtered_english_videos)}")
