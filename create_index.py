import requests
import glob
from pprint import pprint
import os

from dotenv import load_dotenv
load_dotenv()

API_URL = os.getenv("12LABS_API_URL")
assert API_URL, "API_URL not found in .env file"

API_KEY = os.getenv("12LABS_API_KEY")
assert API_KEY, "API_KEY not found in .env file"

INDEXES_URL = f"{API_URL}/indexes"

INDEX_NAME = "youtube" # Use a descriptive name for your index 

headers = {
	"x-api-key": API_KEY
}

data = {
  "engines": [
    {
      "engine_name": "marengo2.5",
      "engine_options": ["visual", "conversation", "text_in_video", "logo"]
    },
    {
      "engine_name": "pegasus1",
      "engine_options": ["visual", "conversation"]
    }
  ],
  "index_name": INDEX_NAME,
  "addons": ["thumbnail"] # (Optional) This line enables the logo detection feature. 
}

response = requests.post(INDEXES_URL, headers=headers, json=data)
INDEX_ID = response.json().get('_id')
print (f'Status code: {response.status_code}')
pprint (response.json())

# {'_id': '652b22023c4a426cf3f4f717'}