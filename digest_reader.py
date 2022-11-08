# this file looks through the sql database and allows you to digest the existing content

# should be a UI that prints out the digest to a text file and resetsd it
# alternatively, print out tghem one by one and ask if you want to clear

from database import SQLDatabase
from datetime import datetime
master_dataset = SQLDatabase("logs/database.db") # Database(50)

def pretty_print(item):
    print()
    print(item[0])
    print("\tAdditional Information", item[1])
    print("\tAdded time: ", datetime.fromtimestamp(item[2]))

undigested = master_dataset.get_digest()

with open("logs/DIGEST.txt", "w") as f:
    f.write(master_dataset.digest_repr())

answer = input(f"Do you want to flush all? (y/any) ")
if answer == "y":
    master_dataset.clear_digest()
    print("Remember, all your digested content is in DIGEST.txt. Don't lose it!")
    quit()

for modality, collection in undigested.items():
    print(f"Looking at type {modality}")
    for item in collection:
        pretty_print(item)
        answer = input(f"Do you want to digest? (y/any)")
        if answer == 'y':
            master_dataset.clear_digest(modality, item[0])
