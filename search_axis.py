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

