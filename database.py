from collections import OrderedDict
import pickle
import os


# rolling database. Contains the past N elements of interest. This is a redundancy prevention system. Losing this database is not catastrophic
class Database():
    def __init__(self, top_n = 100):
        self.modality_dict = {"news_articles" : OrderedDict(), #link, metadata
                              "twitter_posts": OrderedDict(),
                              "youtube_videos": OrderedDict(),
                              "instagram_posts": OrderedDict()}

        self.base_dir = "logs/"
        self.top_n = top_n
        self.digest = [] #what you missed while you were gone!

    def update(self, items, category):
        for item in items:
            assert len(item) == 2
            if self.in_database(item, category):
                continue
            self.modality_dict[category][item[0]] = item[1]
            self.digest.append(item)
            while len(self.modality_dict[category]) > self.top_n: #keeping history somewhat short
                self.modality_dict[category].popitem(last = False)

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
        if os.path.exists(self.base_dir + filename):
            with open(self.base_dir + filename, "rb") as f:
                self.modality_dict = pickle.load(f)
        else:
            print("No database! Making a blank one!")

    # check database for the presence of some object
    def in_database(self, item, category):
        #item is a tuple (key, metadata)
        return item[0] in self.modality_dict[category]

    def __repr__(self):
        repr_string = "//////////////// DATABASE CONTENTS /////////////// \n"
        for modality in self.modality_dict:
            repr_string += ("------------------- " + modality.upper() + " ------------------- \n")
            for item in self.modality_dict[modality]:
                repr_string += ("\t Link: " + item + " \t \t Metadata: " + self.modality_dict[modality][item] + "\n")
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


