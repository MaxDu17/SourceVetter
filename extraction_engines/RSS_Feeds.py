import feedparser
from extraction_engines.Translator import Translator
from extraction_engines.Translator import get_keywords
import tqdm

class RSSReader(Translator):
    def __init__(self, keywords_file, rss_file):
        relevant_words = get_keywords(keywords_file)
        self.rss_links = self.get_url_list(rss_file)
        super().__init__(relevant_words)

    def get_url_list(self, file):
        url_list = list()
        with open(file) as f:
            for line in f:
                url = line.strip("\n")
                url_list.append(url)
        return url_list

    def extract_rss(self, url):
        # returns list of newsfeed dict entries from the rss feed
        NewsFeed = feedparser.parse(url)

        return NewsFeed.entries

    def find_matches(self, keyword_list, feed_list):
        # returns a dict of URLs + titles when matching
        url_dict = {}
        keywords_found = set()
        for feed in feed_list:
            title = feed["title"].lower()
            summary = feed["summary"].lower() if "summary" in feed else ""
            for keyword in keyword_list:
                if keyword in title or keyword in summary:
                    keywords_found.add(keyword)
                    url_dict[feed["link"]] = title
                    break
        return url_dict, keywords_found

    def grab_relevant_links(self):
        url_master_dict = {}
        keywords_found = set()
        for url in tqdm.tqdm(self.rss_links):
            feed_list = self.extract_rss(url)
            urls_dict, keywords = self.find_matches(self.relevant_words, feed_list)
            if len(urls_dict) > 0:
                url_master_dict.update(urls_dict) #if there is a duplicate key, overwrite with current, and that's ok
            keywords_found.update(keywords)
        print(f"Keywords_found: {keywords_found}")
        return url_master_dict

if __name__ == "__main__":
    reader = RSSReader("../keyword.txt", "../rss_list.txt")
    print(reader.grab_relevant_links())
