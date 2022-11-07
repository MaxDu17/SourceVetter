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
        for modality in self.modalities:
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {modality} (url TEXT PRIMARY KEY, title TEXT, date_inserted INTEGER, digested INTEGER)")
        self.connection.commit()

    def update(self, info_dict, category):
        # requirements: info dict to contain key as URL, value as plaintext information
        for url, text in info_dict.items():
            counts = self.cursor.execute(f"SELECT COUNT(1) FROM {category} WHERE url = '{url}'").fetchall()
            if counts[0][0] == 0:
                self.cursor.execute(f"INSERT INTO {category} VALUES ('{url}', '{text}', {int(time.time())}, 0)")
        self.connection.commit()

    def get_digest(self):
        undigested_list = list()
        for modality in self.modalities:
            undigested_list.extend(self.cursor.execute(f"SELECT * FROM {modality} WHERE digested = 0").fetchall())
        return undigested_list

    def clear_digest(self, modality = None, key = None):
        if modality and key is not None:
            self.cursor.execute(f"UPDATE {modality} SET digested = 1 WHERE url = '{key}'")
        else:
            for modality in self.modalities: #mass clearing
                self.cursor.execute(f"UPDATE {modality} SET digested = 1")

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

# rolling database. Contains the past N elements of interest. This is a redundancy prevention system. Losing this database is not catastrophic
class Database():
    def __init__(self, top_n = 100, base_dir = "logs/"):
        self.modality_dict = {"news_articles" : OrderedDict(), #link, metadata
                              "twitter_posts": OrderedDict(),
                              "youtube_videos": OrderedDict(),
                              "instagram_posts": OrderedDict(),
                              "PETA" : OrderedDict(),
                              "DODO": OrderedDict(),
                              "DolphinProject": OrderedDict()}

        self.base_dir = base_dir
        self.top_n = top_n
        self.digest = copy.deepcopy(self.modality_dict) #what you missed while you were gone! A mirror of self.modality_dict

    def update(self, info_dict, category):
        new_articles = 0 #how many things were added to the database
        for key, value in info_dict.items():
            if self.in_database(key, category): #don't add things that we have already seen
                continue
            new_articles += 1
            self.modality_dict[category][key] = value
            self.digest[category][key] = value
            while len(self.modality_dict[category]) > self.top_n: #keeping history somewhat short
                self.modality_dict[category].popitem(last = False)
        return new_articles

    def get_digest(self):
        return self.digest_repr()

    def clear_digest(self):
        for value in self.digest.values():
            value.clear() #clear each ordered dictionary

    # saves the contents of the database to a pickle file and text file for easy reading
    def save_database(self):
        with open(self.base_dir + "database.pkl", "wb") as f:
            pickle.dump((self.modality_dict, self.digest), f)
        with open(self.base_dir + "database_readable.txt", "w") as f:
            f.write(self.__repr__())

    # load the contents of the database from a pickle file
    def load_database(self, filename = "database.pkl"):
        # TODO: if the current modality dict has more keys, add the additional keys as blank ones (allows hot-swapping)
        if os.path.exists(self.base_dir + filename):
            print(f"Loaded database at {self.base_dir + filename}")
            with open(self.base_dir + filename, "rb") as f:
                self.modality_dict, self.digest = pickle.load(f)
        else:
            print("No database! Making a blank one!")

    # check database for the presence of some object
    def in_database(self, key, category):
        return key in self.modality_dict[category]

    def digest_repr(self):
        repr_string = "//////////////// DIGEST CONTENTS /////////////// \n"
        for modality in self.digest:
            if len(self.digest[modality]) > 0:
                repr_string += ("------------------- " + modality.upper() + " ------------------- \n")
                for item in self.digest[modality]:
                    repr_string += ("Link: " + item + " \t \t Metadata: " + self.digest[modality][item] + "\n")
                repr_string += "======================================================= \n"
        return repr_string

    def __repr__(self):
        repr_string = "//////////////// DATABASE CONTENTS /////////////// \n"
        for modality in self.modality_dict:
            repr_string += ("------------------- " + modality.upper() + " ------------------- \n")
            for item in self.modality_dict[modality]:
                repr_string += ("Link: " + item + " \t \t Metadata: " + self.modality_dict[modality][item] + "\n")
            repr_string += "======================================================= \n"
        return repr_string

if __name__ == "__main__":
    d = SQLDatabase("test.db")
    # some simple tests to check functionality
    # d = Database(5)

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
    print(d.get_digest()) #to show the user interface
    print(d)

