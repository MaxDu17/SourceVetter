import requests
import json
from Translator import Translator
from Translator import get_keywords

with open("../secrets/youtube_api.txt") as f:
    API_KEY = f.readline()

class YouTube(Translator):
    def __init__(self, relevant_words, channel_url, max_results = 20):
        self.channel_id = channel_url.split("/")[-1]
        self.max_results = max_results
        self.search_query = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={self.channel_id}&part=snippet,id&order=date&maxResults={self.max_results}"
        self.video_root = "https://www.youtube.com/watch?v="
        super().__init__(relevant_words)

    def grab_relevant_links(self):
        page = requests.get(url=self.search_query)
        videos = json.loads(page.text)["items"]
        link_dict = {}
        for video in videos:
            try:
                video_id = video["id"]["videoId"]  # sometimes you don't hit a video and you hit a playlist for some reason
            except:
                continue
            publish_time = video["snippet"]["publishedAt"]
            title = video["snippet"]["title"].lower()
            for word in self.relevant_words:
                if title is not None and word in title:
                    link_dict[title] = self.video_root + video_id
        return link_dict


if __name__ == "__main__":
    word_list = get_keywords("../keyword.txt")
    youtube_channel = YouTube(["tesla"], "https://www.youtube.com/channel/UC2nhCnIGssNalfnHgcaglBQ")
    print(youtube_channel.grab_relevant_links())
    quit()
