from bs4 import BeautifulSoup
import requests
from extraction_engines.Translator import Translator

class NewYorkerFiction(Translator):
    def __init__(self): # no keywords; just search for all new
        self.relevant_prefix = "/magazine/" #the links to the pages that matter
        self.url = "https://www.newyorker.com/magazine/fiction"
        super().__init__([])

    # for forward-facing mode, use only the first page
    def grab_relevant_links(self):
        page = requests.get(url = self.url )
        soup = BeautifulSoup(page.content, features="html.parser")

        link_dict = {}
        for link in soup.find_all('a'): #find buttons
            url = link.get("href")
            title = link.text
            title = title.lower() if title is not None else title
            if url is not None and self.relevant_prefix in url:
                splits = url.split("/")
                # a little janky filter to get only the fiction articles
                if splits[-1][-1].isalpha() and splits[-2].isnumeric():
                    if f"https://www.newyorker.com{url}" not in link_dict:
                        link_dict[f"https://www.newyorker.com{url}"] = title

        return link_dict



if __name__ == "__main__":
    trans = NewYorkerFiction()
    # print(PETA_trans.grab_relevant_links())
    print(trans.grab_relevant_links())
    quit()
