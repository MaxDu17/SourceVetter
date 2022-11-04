import time
from plyer import notification
import datetime

from database import Database
from extraction_engines.RSS_Feeds import scan_rss
from extraction_engines.DODO import DODO_Daily
from extraction_engines.PETA import PETA_Media_News_Releases


master_dataset = Database(50)
master_dataset.load_database() #load from what we had

notification.notify(
    title = 'Current Event Monitor',
    message = 'The current event monitor is up and running! Scanning every 1 hours',
    app_icon = None,
    timeout = 10,
)

# update(self, items, category):


num_scans = 0
while True:
    url_dict = scan_rss("rss_list.txt", "keyword.txt")
    num_new_articles = master_dataset.update(url_dict, "news_articles")
    print(num_new_articles)
    print("done scanning!")
    # if len(interest_list) > 0:
    #     now = datetime.datetime.now()
    #     notification.notify(
    #         title='Current Event Monitor',
    #         message='New articles with keyword match detected! Check log files.',
    #         app_icon=None,
    #         timeout=10,
    #     )
    #     print("found!")
    #     with open(f"logs/{now.year}_{now.month}_{now.day}_{now.hour}_{now.minute}.txt", "w") as f:
    #         for url in interest_list:
    #             print(url)
    #             f.write(url)
    #             f.write("\n")
    # else:
    #     print("no results found right now! Check back later")

    master_dataset.save_database() #dump after every scan just in case we are killed
    time.sleep(3600)



