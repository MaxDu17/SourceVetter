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
from extraction_engines.NewYorkerFiction import NewYorkerFiction
from extraction_engines.BehindTheThrills import BehindThrills
from extraction_engines.Twitter import TwitterSweep
from extraction_engines.NonHumanRights import NonHumanRightsBlog

PAUSE = 3600
YOUTUBE_SKIP = 6 #every six iterations do youtube due to the quota

CS_RSS_Reader = RSSReader("streams/keyword_CS.txt", "streams/rss_list_CS.txt")
RSS_Reader = RSSReader("streams/keyword.txt", "streams/rss_list.txt")

YouTube_Reader = YouTubeChannelSweep("streams/keyword.txt", "streams/youtube.txt")
Twitter_Reader = TwitterSweep("streams/keyword.txt", "streams/twitter.txt")

# special interest
PETA_Reader = PETA_Media_News_Releases("streams/keyword.txt")
DODO_Reader = DODO_Daily("streams/keyword.txt")
DP_Reader = DolphinProject() # don't include a keyword file to get all results
NewYorkerFiction_Reader = NewYorkerFiction()
BehindThrills_Reader = BehindThrills("streams/keyword.txt")
NonHumanRights_Reader = NonHumanRightsBlog() # don't include a keyword file to get all results


source_dict = {"news_articles" : RSS_Reader, "cs_arxiv" : CS_RSS_Reader,
                              "youtube_videos": YouTube_Reader,
                              "twitter": Twitter_Reader,
                              "PETA" : PETA_Reader ,
                              "DODO": DODO_Reader,
                              "DolphinProject": DP_Reader,
                              "New_Yorker_Fiction": NewYorkerFiction_Reader,
                              "Behind_Thrills" : BehindThrills_Reader,
                              "Non_Human_Rights" : NonHumanRights_Reader
            }

master_dataset = SQLDatabase("logs/database.db", tables = source_dict.keys()) # Database(50)

notification.notify(
    title = 'Current Event Monitor',
    message = 'The current event monitor is up and running! Scanning every 1 hours',
    app_icon = None,
    timeout = 10,
)

count = 0
while True:
    total_items = 0
    for key, reader in source_dict.items():
        if key == "youtube_videos" and count % YOUTUBE_SKIP != 0: #prevents hitting the quota
            continue

        if reader is not None:
            url_dict = reader.grab_relevant_links()
            num_new_articles = master_dataset.update(url_dict, key)
            print(f"{num_new_articles} proposed new elements of type {key}")
            total_items += num_new_articles

    if total_items > 0:
        notification.notify(
            title='Current Event Monitor',
            message=f"This hour, there were {total_items} detected! Run the digest reader for more info.",
            app_icon=None,
            timeout=10,
        )

    current_time = time.time()
    print(f"{total_items} found this hour. Next scan scheduled for {datetime.fromtimestamp(current_time + PAUSE)}")

    time.sleep(PAUSE)
    count += 1
