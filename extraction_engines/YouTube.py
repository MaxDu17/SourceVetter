import requests
import json
from extraction_engines.Translator import Translator
from extraction_engines.Translator import get_keywords
import tqdm

with open("secrets/youtube_api.txt") as f:
    API_KEY = f.readline().strip("\n")

class YouTubeChannelSweep(Translator):
    def __init__(self, keywords_file, channels_file, max_results = 5):
        relevant_words = get_keywords(keywords_file)
        youtube_links, self.filter_states = self.get_channels_list(channels_file)

        self.channel_id = [channel_url.split("/")[-1] for channel_url in youtube_links]

        self.max_results = max_results
        self.video_root = "https://www.youtube.com/watch?v="
        super().__init__(relevant_words)

    def get_channels_list(self, file):
        url_list = list()
        filter_states = list()
        with open(file) as f:
            for line in f:
                line = line.strip("\n")
                info = line.split(" ")
                url_list.append(info[0])
                filter_states.append(info[1])
        return url_list, filter_states

    def grab_relevant_links(self):
        link_dict = {}
        for channel_id, filter_state in tqdm.tqdm(zip(self.channel_id, self.filter_states)):
            # print(channel_id)
            search_query = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={channel_id}&part=snippet,id&order=date&maxResults={self.max_results}"
            page = requests.get(url=search_query)
            try:
                videos = json.loads(page.text)["items"]
            except:
                print("quota reached!")
                return link_dict #bypass
            for video in videos:
                try:
                    video_id = video["id"][
                        "videoId"]  # sometimes you don't hit a video and you hit a playlist for some reason
                except:
                    continue
                publish_time = video["snippet"]["publishedAt"].split("T")[0]
                title = video["snippet"]["title"].lower()

                if filter_state == "GET_ALL":
                    link_dict[self.video_root + video_id] = f"PUBLISHED {publish_time}: {title}"
                elif filter_state == "KEYWORDS_ONLY":
                    for word in self.relevant_words:
                        if title is not None and word in title:
                            link_dict[self.video_root + video_id] = f"PUBLISHED {publish_time}: {title}"
                            break
                else:
                    print(filter_state)
                    raise Exception("invalid filter state!")

        return link_dict

class YouTube(Translator): #for single YouTube channel, mostly designed for archival work
    def __init__(self, relevant_words, channel_url, max_results = 20):
        self.channel_id = channel_url.split("/")[-1]
        self.max_results = max_results
        self.search_query = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={self.channel_id}&part=snippet,id&order=date&maxResults={self.max_results}"
        self.video_root = "https://www.youtube.com/watch?v="
        super().__init__(relevant_words)

    def grab_comments_from(self, link):
        pass #TODO

    def iterate_through_playlist(self, link):
        pass #TODO: read playlist and grab relevant keywords as link

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
                    link_dict[self.video_root + video_id] = title
                    break
        return link_dict


if __name__ == "__main__":
    # word_list = get_keywords("../keyword.txt")
    # youtube_channel = YouTube(["tesla"], "https://www.youtube.com/channel/UC2nhCnIGssNalfnHgcaglBQ")
    # print(youtube_channel.grab_relevant_links())
    # quit()
    yt = YouTubeChannelSweep("../streams/keyword.txt", "../streams/youtube.txt")
    print(yt.grab_relevant_links())

