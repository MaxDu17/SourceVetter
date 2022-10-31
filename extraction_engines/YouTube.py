from bs4 import BeautifulSoup
import requests
import json
from Translator import Translator
import time
import tqdm
from Translator import get_keywords

with open("../secrets/youtube_api.txt") as f:
    API_KEY = f.readline() #"AIzaSyATjYPjE31HbOJYDZgjcIQmapaA7EtIoBc"

CHANNELID = "UC2nhCnIGssNalfnHgcaglBQ"
request = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={CHANNELID}&part=snippet,id&order=date&maxResults=20"


page = requests.get(url = request)
videos = json.loads(page.text)["items"]

for video in videos:
    try:
        video_id = video["id"]["videoId"] #sometimes you don't hit a video and you hit a playlist for some reason
    except:
        continue
    publish_time = video["snippet"]["publishedAt"]
    title = video["snippet"]["title"]
    print(title)
# items -> list of videos -> id/videoId, snipped/publishedAt, title,

import ipdb
ipdb.set_trace()
