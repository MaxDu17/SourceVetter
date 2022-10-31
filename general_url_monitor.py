from urllib.request import urlopen
from bs4 import BeautifulSoup

import requests

# url = "https://www.thedodo.com/daily-dodo"
url = "https://www.peta.org/media/news-releases/" #a<href> is what is good
# url = "https://www.seaworldofhurt.com/news/"
test = requests.get(url = url)
soup = BeautifulSoup(test.content, features="html.parser")


# kill all script and style elements
for script in soup(["script", "style"]):
    script.extract()    # rip it out

import ipdb
ipdb.set_trace()
# get text
text = soup.get_text()
 # break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
text = '\n'.join(chunk for chunk in chunks if chunk)
