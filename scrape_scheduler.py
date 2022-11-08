import time
from plyer import notification
from datetime import datetime
import os

import extraction_engines

from database import SQLDatabase
from extraction_engines.RSS_Feeds import RSSReader
from extraction_engines.DODO import DODO_Daily
from extraction_engines.PETA import PETA_Media_News_Releases
from extraction_engines.YouTube import YouTubeChannelSweep
from extraction_engines.DolphinProject import DolphinProject

PAUSE = 3600

master_dataset = SQLDatabase("logs/database.db") # Database(50)

RSS_Reader = RSSReader("keyword.txt", "rss_list.txt")
PETA_Reader = PETA_Media_News_Releases("keyword.txt")
DODO_Reader = DODO_Daily("keyword.txt")
YouTube_Reader = YouTubeChannelSweep("keyword.txt", "youtube.txt")
DP_Reader = DolphinProject("keyword.txt")

#TODO: create augmenting keywords for every RSS reader
source_dict = { "news_articles" : RSS_Reader, #link, metadata
                              "twitter_posts": None,
                              "youtube_videos": YouTube_Reader,
                              "instagram_posts": None,
                              "PETA" : PETA_Reader ,
                              "DODO": DODO_Reader,
                              "DolphinProject": DP_Reader}

notification.notify(
    title = 'Current Event Monitor',
    message = 'The current event monitor is up and running! Scanning every 1 hours',
    app_icon = None,
    timeout = 10,
)

answer = input("do you want burn-in round?") #for the filterless engines (like some YouTube channels), we get a
# large influx of data to begin with, some of which is old data. When we burn-in, we accept that everything is old and clear the digest
# TODO make this better
num_ignored = 0
if answer == "y":
    for key, reader in source_dict.items():
        if reader is not None:
            print(key)
            url_dict = reader.grab_relevant_links()
            num_new_articles = master_dataset.update(url_dict, key)
            num_ignored += num_new_articles
    print(f"Ignored {num_ignored} articles.")
    # master_dataset.clear_digest()

while True:
    total_items = 0
    for key, reader in source_dict.items():
        if reader is not None:
            url_dict = reader.grab_relevant_links()
            num_new_articles = master_dataset.update(url_dict, key)
            print(f"{num_new_articles} proposed new elements of type {key}")
            total_items += num_new_articles

    if total_items > 0:
        notification.notify(
            title='Current Event Monitor',
            message=f"This hour, there were {total_items} detected! Check your digest file!",
            app_icon=None,
            timeout=10,
        )

    current_time = time.time()
    print(f"{total_items} found this hour. Next scan scheduled for {datetime.fromtimestamp(current_time + PAUSE)}")

    time.sleep(PAUSE)
