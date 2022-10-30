import feedparser

def extract_rss(url):
    # returns list of newsfeed dict entries from the rss feed
    NewsFeed = feedparser.parse(url)
    return NewsFeed.entries

def get_keywords(filename):
    word_list = list()
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if len(line) > 0:
                word_list.append(line.lower())
    return word_list


def find_matches(keyword_list, feed_list):
    # returns a list of URLs with matching
    url_list = list()
    for feed in feed_list:
        title = feed["title"].lower()
        summary = feed["summary"].lower() if "summary" in feed else ""
        for keyword in keyword_list:
            if keyword in title or keyword in summary:
                url_list.append(feed["link"])
                break
    return url_list

def scan_rss(rss_links, keyword_links):
    # master function that takes in a list of RSS feeds and keywords and spits back a list of URLs of interest
    words_list = get_keywords(keyword_links)
    url_list = list()
    with open(rss_links) as f:
        for line in f:
            url = line.strip("\n")
            print(f"Scanning {url}...")
            feed_list = extract_rss(url)
            urls_of_interest = find_matches(words_list, feed_list)
            if len(urls_of_interest) > 0:
                url_list.extend(urls_of_interest)
    return list(set(url_list)) #removes dup[licates

if __name__ == "__main__":
    print(scan_rss("rss_list.txt", "keyword.txt"))
