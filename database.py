from collections import OrderedDict
import pickle
import os


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
        self.digest = [] #what you missed while you were gone!

    def update(self, info_dict, category):
        new_articles = 0 #how many things were added to the database
        for key, value in info_dict.items():
            if self.in_database(key, category): #don't add things that we have already seen
                continue
            new_articles += 1
            self.modality_dict[category][key] = value
            self.digest.append((category, key))
            while len(self.modality_dict[category]) > self.top_n: #keeping history somewhat short
                self.modality_dict[category].popitem(last = False)
        return new_articles

    def get_digest(self):
        return self.digest

    def clear_digest(self):
        self.digest.clear()

    # saves the contents of the database to a pickle file and text file for easy reading
    def save_database(self):
        with open(self.base_dir + "database.pkl", "wb") as f:
            pickle.dump(self.modality_dict, f)
        with open(self.base_dir + "database_readable.txt", "w") as f:
            f.write(self.__repr__())

    # load the contents of the database from a pickle file
    def load_database(self, filename = "database.pkl"):
        # TODO: if the current modality dict has more keys, add the additional keys as blank ones (allows hot-swapping)
        if os.path.exists(self.base_dir + filename):
            with open(self.base_dir + filename, "rb") as f:
                self.modality_dict = pickle.load(f)
        else:
            print("No database! Making a blank one!")

    # check database for the presence of some object
    def in_database(self, key, category):
        return key in self.modality_dict[category]

    def __repr__(self):
        repr_string = "//////////////// DATABASE CONTENTS /////////////// \n"
        for modality in self.modality_dict:
            repr_string += ("------------------- " + modality.upper() + " ------------------- \n")
            for item in self.modality_dict[modality]:
                repr_string += ("Link: " + item + " \t \t Metadata: " + self.modality_dict[modality][item] + "\n")
            repr_string += "======================================================= \n"
        return repr_string

if __name__ == "__main__":
    # some simple tests to check functionality
    d = Database(5)

    items = [
        ("test1.com", "metadata 1"),
        ("test2.com", "metadata 2"),
        ("test3.com", "metadata 3"),
        ("test4.com", "metadata 4"),
    ]
    d.update(items, "news_articles")

    items = [
        ("test5.com", "metadata 5"),
        ("test6.com", "metadata 6"),
        ("test7.com", "metadata 7"),
        ("test8.com", "metadata 8"),
    ]
    d.update(items, "news_articles") #show that we can wrap around

    non_distinct_items = [
        ("test5.com", "metadata 5"),
        ("test10.com", "metadata 10"),
    ]
    d.update(non_distinct_items, "news_articles")
    print(d.get_digest()) #to show the user interface
    d.save_database()
    print(d)

    # show that we can reload the database
    e = Database(5)
    e.load_database()
    print(e)


