import time
from rss_parser import scan_rss
from plyer import notification
import datetime


notification.notify(
    title = 'Current Event Monitor',
    message = 'The current event monitor is up and running! Scanning every 2 hours',
    app_icon = None,
    timeout = 10,
)

num_scans = 0
while True:
    interest_list = scan_rss("rss_list.txt", "keyword.txt")
    print("done scanning!")
    if len(interest_list) > 0:
        now = datetime.datetime.now()
        notification.notify(
            title='Current Event Monitor',
            message='New articles with keyword match detected! Check log files.',
            app_icon=None,
            timeout=10,
        )
        with open(f"logs/{now.year}_{now.month}_{now.day}_{now.hour}_{now.minute}.txt", "w") as f:
            for url in interest_list:
                print(url)
                f.write(url)
                f.write("\n")
    else:
        print("no results found right now! Check back later")
    time.sleep(7200)



