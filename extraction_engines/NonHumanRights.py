from bs4 import BeautifulSoup
import requests
from extraction_engines.Translator import Translator
import time
import tqdm
from extraction_engines.Translator import get_keywords


def oauth(r):
    # a cheap trick to get this website to work
    r.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    return r

class NonHumanRightsBlog(Translator):
    def __init__(self, keywords_file = None):
        self.relevant_prefix = "https://www.nonhumanrights.org/blog/" #the links to the pages that matter
        self.url = "https://www.nonhumanrights.org/blog/"
        if keywords_file is not None:
            relevant_words = get_keywords(keywords_file)
        else:
            relevant_words = []
        super().__init__(relevant_words)


    # for forward-facing mode, use only the first page
    def grab_relevant_links(self, special_url = None):
        url = self.url if special_url is None else special_url
        page = requests.get(url, auth = oauth)
        soup = BeautifulSoup(page.content, features="html.parser")

        link_dict = {}
        for link in soup.find_all('a'): #find buttons
            url = link.get("href")
            title = link.text
            title = title.lower() if title is not None else title
            if url is not None and self.relevant_prefix in url:
                if len(self.relevant_words) > 0:
                    for word in self.relevant_words:
                        if title is not None and word in title:
                            link_dict[url] = title
                            break
                else:
                    link_dict[url] = title

        return link_dict

    # for archival sweep, use this function
    def iterate_through_database(self, limit):
        master_link_dict = {}
        for i in tqdm.tqdm(range(limit)):
            sub_dict = self.grab_relevant_links(special_url = self.iterable_url_prefix + str(i) + "/")
            master_link_dict.update(sub_dict)
            time.sleep(1) #intentional bottlneck to prevent scrape detectors from kicking us out
        return master_link_dict



if __name__ == "__main__":
    # trans = NonHumanRightsBlog("../streams/keyword.txt")
    trans = NonHumanRightsBlog()
    # print(PETA_trans.grab_relevant_links())
    print(trans.grab_relevant_links())
    quit()
