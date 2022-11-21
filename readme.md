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
Create a `keywords.txt` file in the `streams/` folder that contains all the keywords that you want to search for. Separate out your strings by line breaks. Each string can be more than one word.

I've included a `keyword_example.txt` file as an example of a keywords document. 
## RSS Feeds
Create a `rss_list.txt` file in the `streams/` folder that contains your relevant RSS feeds. Feel free to comment out the `CS_RSS_Reader` if you don't want to segregate data for different subjects. You can monitor multiple RSS feeds per RSS reader.

## YouTube 
Create a YouTube API key and save it under `secrets/youtube_api.txt`. Be careful not to share it. 

Create a `youtube.txt` file under `streams/` and put links to each YouTube channel along with a status. `GET_ALL` means take all the videos, and `KEYWORDS_ONLY` means take only the videos with matching keywords.

As a general note, you can put anything after your selection type token, as it is ignored. It's good to add comments, etc. 

You will need to get the YouTube unique channel ID, which you can get by going to any YouTube channel, viewing source, and searching for `youtube.com/channels/`

## Twitter
Create a twitter developer account and save the `bearer token` to the text file. Make sure that there is no trailing space or empty lines after it.

Create a `twitter.txt` file under `streams/` and put twitter user IDs (https://tweeterid.com/) along with the filter type. The format is the same as the YouTube parser. 
# Using it
## Starting the monitor 
Just run the `main_scraper_hub.py` after you've installed your dependencies in `requirements.txt`. This program will run through all data streams every hour (with the exception of YouTube, due to quota issues). 

You will get a push notification if anything new is found in this hour. 

## Getting the digest
To get the digest, run `digest_reader.py` which will read the database and print out anything that is new. Just in case you didn't catch it, the output is also channeled into `DIGEST.txt`. After you run this code, all the new articles in the database will be marked as old.

# How does it work? 
It's not the most sophisticated piece of code. It uses a hodgepodge of libraries to get information. Then, it extracts the relevant information and stores it in a SQL database. This database keeps track of which things we've seen so far. 
