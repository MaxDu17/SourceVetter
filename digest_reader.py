# this file looks through the sql database and allows you to digest the existing content

# should be a UI that prints out the digest to a text file and resetsd it
# alternatively, print out tghem one by one and ask if you want to clear

from database import SQLDatabase
from datetime import datetime
master_dataset = SQLDatabase("logs/database.db") # Database(50)

def pretty_print(item):
    print()
    print(item[0])
    requoted_string = item[1].replace("&quot", "'")
    print("\tAdditional Information", requoted_string)
    print("\tAdded time: ", datetime.fromtimestamp(item[2]))

undigested = master_dataset.get_digest()
digest_total = sum([len(collection) for key, collection in undigested.items()])
with open("logs/DIGEST.txt", "w", encoding="utf-8") as f:
    f.write(master_dataset.digest_repr())

print("******************* DATABASE DIGESTER ********************")
print(f"You have {digest_total} items to digest.")

NUMBER_TO_DIGEST_TODAY = 300 #this prevents you from sifting through like 5000 different things at once
counter = 0
for modality, collection in undigested.items():
    for item in collection:
        pretty_print(item)
        master_dataset.clear_digest(modality, item[0])
        counter += 1
        if counter > NUMBER_TO_DIGEST_TODAY:
            print("it's time to take a break!! Let's do this again next time.")
            print(master_dataset.get_stats())
            quit()
    input("next?")

print(master_dataset.get_stats())
