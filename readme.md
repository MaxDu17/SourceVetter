# Ongoing developments
* Create database perusal script (in addition to dumping)
* Twitter live monitoring 
* Better selection and filtering features 

# What is this?
As a reseacher, I often need to keep up with current events! This means looking at arXiv feeds for my robotics research, and a whole ton of specialty sites & national news for my whale book. 
I find this information gathering process rather tedious, so I made this web scraper that does a coarse read of most relevant data streams and gives you a digest of what's happening.

# What can it do? 
This is an ongoing project and it will get more complicated as I work on it. Right now, it can extract keyword-bearing articles from...
* Any RSS news feed 
* Any YouTube channel
* Any Twitter user 
* Specialty sites Dolphin Project, PETA, The Dodo, ThemeParkInsider, New Yorker Fiction, Non Human Rights project, Inside The Magic 

# Setting things up
## Keywords
Create a `keywords.txt` file in the `streams/` folder that contains all the keywords that you want to search for. Separate out your strings by line breaks. Each string can be more than one word. Unless you're also interested in following the newest whales stuff, you should probably replace my keywords with yours.

I've included a `keyword_example.txt` file as an example of a keywords document. 
## RSS Feeds
Create a `rss_list.txt` file in the `streams/` folder that contains your relevant RSS feeds. Feel free to comment out the `CS_RSS_Reader` if you don't want to segregate data for different subjects. You can monitor multiple RSS feeds per RSS reader. My rss list should be a good start. 

## YouTube (skip if not needed)
Create a YouTube API key and save it under `secrets/youtube_api.txt`. Be careful not to share it. 

Create a `youtube.txt` file under `streams/` and put links to each YouTube channel along with a status. `GET_ALL` means take all the videos, and `KEYWORDS_ONLY` means take only the videos with matching keywords.

As a general note, you can put anything after your selection type token, as it is ignored. It's good to add comments, etc. 

You will need to get the YouTube unique channel ID, which you can get by going to any YouTube channel, viewing source, and searching for `youtube.com/channels/`

## Twitter (skip if not needed)
Create a twitter developer account and save the `bearer token` to the text file. Make sure that there is no trailing space or empty lines after it.

Create a `twitter.txt` file under `streams/` and put twitter user IDs (https://tweeterid.com/) along with the filter type. The format is the same as the YouTube parser. 

# Using it
## Starting the monitor 
Install requirements in `requirements.txt`. 
after you've installed your dependencies in `requirements.txt`. If you don't want push notifications, comment out those lines. 

If you are a CS researcher and just want to get an RSS feed of your favorite arXiv feeds with keyword filtering, use `CS_scraper_hub.py`. It has everything you need.

If you intend to do fun archival research or need to follow spicy developments on social media, you can use the `main_scraper_hub.py`. Just comment out anything you don't need. 

Leave the program running in the background and it will wake every hour. You will get a push notification if anything new is found in this hour. 

## Getting the digest
To get the digest, run `digest_reader.py` which will read the database and print out anything that is new. Just in case you didn't catch it, the output is also channeled into `DIGEST.txt`. After you run this code, all the new articles in the database will be marked as old.

## Developing your own translators
It is very simple to make your own extraction engine to blog-style websites, where each article is linked with a piece of text (i.e. an `<a>` html tag). If this is the case, you can take a look at `PETA.py` for an example. Most of the time, it's just finding the correct links. Sometimes you have to fiddle with the links (see `InsideTheMagic.py`). 

Future developments may make it possible to explore websites with more complicated formats (through Selenium). 


# FAQ
## How does it work? 
It's not the most sophisticated piece of code. It extracts the raw HTML of websites (or the json form of RSS feeds). Then, it extracts the relevant information and stores it in a SQL database. This database keeps track of which things we've seen so far. 

## Will you ever implement Facebook and instagram?
Not unless Facebook/Instagram gives a good API, which currently it is not. 

## What if I accidentally corrupted/deleted the database?
Not a big deal! The only purpose of the database is to keep track of what we've seen so far. Worst case you start with a blank database and on the first run, you get a large load of information. But the next scan, all of it will have been logged in the database and things will be back to normal.
