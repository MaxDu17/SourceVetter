from collections import OrderedDict
import pickle
import os
import copy
import time
from datetime import datetime

import sqlite3

class SQLDatabase():
    def __init__(self, database_name):
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()
        self.modalities = ["news_articles" , #link, metadata
                              "twitter_posts",
                              "youtube_videos",
                              "instagram_posts",
                              "PETA" ,
                              "DODO",
                              "DolphinProject"]

        self.maybe_reconstruct_database()

    def maybe_reconstruct_database(self):
        # should be robust to any new modalities added
        for modality in self.modalities:
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {modality} (url TEXT PRIMARY KEY, title TEXT, date_inserted INTEGER, digested INTEGER)")
        self.connection.commit()

    def update(self, info_dict, category):
        # requirements: info dict to contain key as URL, value as plaintext information
        new_element_count = 0
        for url, text in info_dict.items():
            counts = self.cursor.execute(f"SELECT COUNT(1) FROM {category} WHERE url = '{url}'").fetchall()
            if counts[0][0] == 0:
                try:
                    text = text.replace("'", "&quot")
                    self.cursor.execute(f"INSERT INTO {category} VALUES ('{url}', '{text}', {int(time.time())}, 0)")
                except:
                    print("Error prevented the logging of", category, url, text)
                new_element_count += 1
        self.connection.commit()
        return new_element_count

    def get_digest(self):
        undigested_dict = {}
        for modality in self.modalities:
            undigested_dict[modality] = self.cursor.execute(f"SELECT * FROM {modality} WHERE digested = 0").fetchall()
        return undigested_dict

    def clear_digest(self, modality = None, key = None):
        if modality and key is not None:
            self.cursor.execute(f"UPDATE {modality} SET digested = 1 WHERE url = '{key}'")
        else:
            for modality in self.modalities: #mass clearing
                self.cursor.execute(f"UPDATE {modality} SET digested = 1")
        self.connection.commit()

    def __repr__(self):
        repr_string = "//////////////// DATABASE CONTENTS /////////////// \n"
        for modality in self.modalities:
            repr_string += ("------------------- " + modality.upper() + " ------------------- \n")
            items = self.cursor.execute(f"SELECT * FROM {modality} ORDER BY digested DESC, date_inserted DESC").fetchall()
            for item in items:
                pretty_date = datetime.fromtimestamp(item[2])
                repr_string += f"Time Inserted: {pretty_date} \t Digested: {item[3] == 1} \t Link: {item[0]} \t \t Metadata: {item[1]}\n"
            repr_string += "======================================================= \n"
        return repr_string

    def digest_repr(self):
        repr_string = "//////////////// TO DIGEST CONTENTS /////////////// \n"
        for modality in self.modalities:
            repr_string += ("------------------- " + modality.upper() + " ------------------- \n")
            items = self.cursor.execute(
                f"SELECT * FROM {modality} WHERE digested = 0 ORDER BY date_inserted DESC").fetchall()
            for item in items:
                pretty_date = datetime.fromtimestamp(item[2])
                repr_string += f"Time Inserted: {pretty_date} \t Digested: {item[3] == 1} \t Link: {item[0]} \t \t Metadata: {item[1]}\n"
            repr_string += "======================================================= \n"
        return repr_string

if __name__ == "__main__":
    d = SQLDatabase("test.db")

    items = {
        "test1.com": "metadata 1",
        "test2.com": "metadata 2",
        "test3.com": "metadata 3",
        "test4.com": "metadata 4",
    }
    d.update(items, "news_articles")
    print(d)
    print(d.get_digest()) #to show the user interface


    items = {
       "test5.com": "metadata 5",
       "test6.com": "metadata 6",
       "test7.com": "metadata 7",
       "test8.com": "metadata 8",
    }
    d.update(items, "news_articles")

    non_distinct_items = {
        "test5.com": "metadata 5",
        "test10.com": "metadata 10",
    }

    d.update(non_distinct_items, "news_articles")
    print(d)
    print(d.get_digest()) #to show the user interface
    print(d.digest_repr())
