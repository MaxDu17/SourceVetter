import time
from plyer import notification
from datetime import datetime
import os

import extraction_engines

from database import SQLDatabase
from extraction_engines.RSS_Feeds import RSSReader

PAUSE = 3600
YOUTUBE_SKIP = 6 #every six iterations do youtube due to the quota

CS_RSS_Reader = RSSReader("streams/keyword_CS.txt", "streams/rss_list_CS.txt")

source_dict = {"cs_arxiv" : CS_RSS_Reader,
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
