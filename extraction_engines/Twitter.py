import requests
import json
from extraction_engines.Translator import Translator
from extraction_engines.Translator import get_keywords
import tqdm

# https://developer.twitter.com/apitools/api?endpoint=%2F2%2Fusers%2F%7Bid%7D%2Ftweets&method=get

with open("../secrets/twitter_api.txt") as f:
    bearer_token = f.readlines()[-1] #stored as the last line in my api text file


class TwitterSweep(Translator):
    def __init__(self, keywords_file, channels_file, max_results = 5):
        relevant_words = get_keywords(keywords_file)
        self.user_id, self.filter_states = self.get_channels_list(channels_file)
        self.max_results = max_results
        super().__init__(relevant_words)

    def bearer_oauth(self, r):
        r.headers["Authorization"] = f"Bearer {bearer_token}"
        # r.headers["User-Agent"] = "v2TweetLookupPython"
        return r

    def grab_channel_feed(self, user_id):
        request = f"https://api.twitter.com/2/users/{user_id}/tweets?max_results={self.max_results}&tweet.fields=author_id,created_at,id,text"
        response = requests.request("GET", request, auth=self.bearer_oauth)
        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )
        return response.json()

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
        for user_id, filter_state in tqdm.tqdm(zip(self.user_id, self.filter_states)):
            feed = self.grab_channel_feed(user_id)
            for post in feed["data"]:
                post_id = post["id"]
                publish_time = post["created_at"].split("T")[0]
                text = post["text"].lower()
                text= "".join(ch for ch in text if ch.isalnum() or ch in " +=-_!@#$%^&*()[]{}\|:;,<.>/?")

                url = f"https://twitter.com/{user_id}/status/{post_id}"
                if filter_state == "GET_ALL":
                    link_dict[url] = f"PUBLISHED {publish_time}: {text}"
                elif filter_state == "KEYWORDS_ONLY":
                    for word in self.relevant_words:
                        if word in text:
                            link_dict[url] = f"PUBLISHED {publish_time}: {text}"
                            break
                else:
                    print(filter_state)
                    raise Exception("invalid filter state!")

        return link_dict

    # TODO: live monitoring of stream
    # TODO Archival search of tweet

if __name__ == "__main__":
    yt = TwitterSweep("../streams/keyword.txt", "../streams/twitter.txt")
    print(yt.grab_relevant_links())
