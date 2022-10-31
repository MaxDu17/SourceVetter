from bs4 import BeautifulSoup
import requests
import json
from Translator import Translator
import time
import tqdm
from Translator import get_keywords

with open("../secrets/youtube_api.txt") as f:
    API_KEY = f.readline()

class YouTube(Translator):
    def __init__(self, relevant_words, channel_id, max_results = 20):
        self.channel_id = channel_id
        self.max_results = max_results
        self.search_query = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={self.channel_id}&part=snippet,id&order=date&maxResults={self.max_results}"
        super().__init__(relevant_words)

    def grab_relevant_links(self):
        page = requests.get(url=self.search_query)
        videos = json.loads(page.text)["items"]

        for video in videos:
            try:
                video_id = video["id"]["videoId"]  # sometimes you don't hit a video and you hit a playlist for some reason
            except:
                continue
            publish_time = video["snippet"]["publishedAt"]
            title = video["snippet"]["title"]
            print(title)
            for word in self.relevant_words:
                if title is not None and word in title:

            if url is not None and self.relevant_prefix in url:
                for word in self.relevant_words:
                    if title is not None and word in title:
                        link_dict[title] = url
                        break

# CHANNELID = "UC2nhCnIGssNalfnHgcaglBQ"
# request = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={CHANNELID}&part=snippet,id&order=date&maxResults=20"



# items -> list of videos -> id/videoId, snipped/publishedAt, title,

import ipdb
ipdb.set_trace()
