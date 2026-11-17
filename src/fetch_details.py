import json
from tmdb_client import get   
import os
import pandas as pd      # reads the CSV of IDs

os.makedirs("data/raw", exist_ok=True)   # create data/raw folder (no error if it already exists)

ids = pd.read_csv("data/show_ids.csv")["id"].tolist()   # load the 3,000 IDs into a list

for i, show_id in enumerate(ids):        # enumerate gives a counter i (0, 1, 2...) alongside each ID
    path = f"data/raw/{show_id}.json"    # where this show's file will live

    if os.path.exists(path):                              
        continue                        

    # Ask TMDB for this show's full details, plus keywords and cast in the same request
    details = get(f"/tv/{show_id}", append_to_response="keywords,credits")   # BLANK 2: the endpoint is /tv/ followed by the ID

    with open(path, "w", encoding="utf-8") as f:   # open the file for writing
        json.dump(details, f)                       # save the whole reply into it

    if i % 100 == 0:                                # every 100 shows...
        print(f"{i} / {len(ids)} done")             # ...print progress