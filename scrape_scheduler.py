import time
from plyer import notification
from datetime import datetime
import os


import extraction_engines

from database import Database
from extraction_engines.RSS_Feeds import RSSReader
from extraction_engines.DODO import DODO_Daily
from extraction_engines.PETA import PETA_Media_News_Releases
# from extraction_engines.YouTube import YouTubeChannelSweep

PAUSE = 3600

master_dataset = Database(50)
master_dataset.load_database() #load from what we had

RSS_Reader = RSSReader("keyword.txt", "rss_list.txt")
PETA_Reader = PETA_Media_News_Releases("keyword.txt")
DODO_Reader = DODO_Daily("keyword.txt")
# YouTube_Reader = YouTubeChannelSweep("channels.txt")

source_dict = { "news_articles" : RSS_Reader, #link, metadata
                              "twitter_posts": None,
                              "youtube_videos": None,
                              "instagram_posts": None,
                              "PETA" : PETA_Reader ,
                              "DODO": DODO_Reader,
                              "DolphinProject": None}

notification.notify(
    title = 'Current Event Monitor',
    message = 'The current event monitor is up and running! Scanning every 1 hours',
    app_icon = None,
    timeout = 10,
)



while True:
    if not os.path.exists("logs/DIGEST.txt"): #this is when you have indicated that you are done perusing what is here so far
        answer = input("clear digest? (y/n)")
        if answer == "y":
            master_dataset.clear_digest()
    with open("logs/DIGEST.txt", "w") as f:
        f.writelines(master_dataset.get_digest())

    for key, reader in source_dict.items():
        if reader is not None:
            url_dict = reader.grab_relevant_links()
            num_new_articles = master_dataset.update(url_dict, key)
            print(f"{num_new_articles} proposed new elements of type {key}")
    current_time = time.time()
    print(f"Next scan scheduled for {datetime.fromtimestamp(current_time + PAUSE)}")

    master_dataset.save_database() #dump after every scan just in case we are killed
    time.sleep(PAUSE)



