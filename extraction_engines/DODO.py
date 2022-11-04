from bs4 import BeautifulSoup
import requests
from extraction_engines.Translator import Translator
from extraction_engines.Translator import get_keywords

import time
import tqdm

# may have to use selenium for the archival sweep
# TODO archival sweep

class DODO_Daily(Translator):
    def __init__(self, keywords_file):
        self.relevant_prefixes = ["/daily-dodo", "/videos"]  # the links to the pages that matter
        self.url = "https://www.thedodo.com/daily-dodo"
        self.root_url = "https://www.thedodo.com"
        relevant_words = get_keywords(keywords_file)
        super().__init__(relevant_words)
        # for forward-facing mode, use only the first page

    def grab_relevant_links(self, special_url=None):
        url = self.url if special_url is None else special_url
        page = requests.get(url=url)
        soup = BeautifulSoup(page.content, features="html.parser")
        link_dict = {}
        for link in soup.find_all('a'):  # find buttons
            url = link.get("href")
            title = link.text

            title = title.lower() if title is not None else title

            for prefix in self.relevant_prefixes:
                if url is not None and url.startswith(prefix):
                    for word in self.relevant_words:
                        if title is not None and word in title:
                            link_dict[self.root_url + url] = ''.join(e for e in title if e.isalnum() or e == " ") #stripping special characters
                            break
                    break
        return link_dict

    def archival_search(self, pages_deep = 2):
        pass #this requires selenium!

if __name__ == "__main__":
    word_list = get_keywords("../keyword.txt")
    dodo_trans = DODO_Daily(word_list)
    print(dodo_trans.grab_relevant_links())
    quit()



