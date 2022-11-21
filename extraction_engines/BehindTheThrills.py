from bs4 import BeautifulSoup
import requests
from extraction_engines.Translator import Translator
import time
import tqdm
from extraction_engines.Translator import get_keywords

class BehindThrills(Translator):
    def __init__(self, keywords_file):
        self.relevant_prefix = "https://behindthethrills.com/" #the links to the pages that matter
        self.url = "https://behindthethrills.com/seaworld-parks/"
        relevant_words = get_keywords(keywords_file)
        super().__init__(relevant_words)

    # for forward-facing mode, use only the first page
    def grab_relevant_links(self, special_url = None):
        url = self.url if special_url is None else special_url
        page = requests.get(url = url)
        soup = BeautifulSoup(page.content, features="html.parser")

        link_dict = {}
        for link in soup.find_all('a'): #find buttons
            url = link.get("href")
            title = link.text
            title = title.lower() if title is not None else title

            if url is not None and self.relevant_prefix in url:
                splits = url.split("/")
                if splits[-3].isnumeric(): #quick and dirty filter for blog pages
                    for word in self.relevant_words:
                        if title is not None and word in title and url not in link_dict:
                            link_dict[url] = title
                            break
        return link_dict


if __name__ == "__main__":
    trans = BehindThrills("../streams/keyword.txt")
    print(trans.grab_relevant_links())
    # print(PETA_trans.grab_relevant_links())
