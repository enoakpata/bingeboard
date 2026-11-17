# --- Tools we need ---
import os        # reads settings from your computer (like your token)
import time      # lets us pause before retrying
import requests  # sends requests to websites/APIs
from dotenv import load_dotenv  # reads the .env file
import pandas as pd  # makes it easy to work with tables of data

# --- Setup ---
load_dotenv()  # load TMDB_TOKEN from .env so Python can see it
BASE = "https://api.themoviedb.org/3"  # TMDB's main address; every request starts with this

# One ongoing connection to TMDB, with your token attached to every request
session = requests.Session()
session.headers.update({"Authorization": f"Bearer {os.environ['TMDB_TOKEN']}"})


def get(path, **params):
    """Ask TMDB for something. Retries if TMDB says 'slow down'."""
    for attempt in range(5):  # try up to 5 times
        # Send the request: full address + options (like page=1). Give up if no reply in 10s.
        r = session.get(f"{BASE}{path}", params=params, timeout=10)

        if r.status_code == 429:      # 429 = "too many requests"
            time.sleep(2 ** attempt)  # wait 1s, 2s, 4s, 8s, 16s
            continue                  # then try again

        r.raise_for_status()  # any other error (e.g. 401 wrong token) → stop with a clear message
        return r.json()       # success: turn TMDB's reply into a Python dictionary

    # Only reached if all 5 attempts failed
    raise RuntimeError(f"Gave up on {path}")


ids = []  # empty list that will collect every show ID

# Loop over pages 1 to 150 (20 shows per page → about 3,000 shows)
for page in range(1, 151):   
    data = get("/discover/tv", sort_by="vote_count.desc", page=page)

    # Add every show ID on this page to our list
    ids.extend([show["id"] for show in data["results"]])  
    print(f"Page {page} done, {len(ids)} IDs so far")  # progress, so you know it's not frozen
    
#grab extra reality shows (Reality's TMDB genre ID is 10764)
for page in range(1, 11):    # 10 pages × 20 = up to 200 reality shows
    data = get("/discover/tv", with_genres=10764, sort_by="vote_count.desc", page=page)
    ids.extend(show["id"] for show in data["results"])

# Check for duplicates: a list keeps repeats, a set doesn't
print(len(ids), len(set(ids)))

ids = list(dict.fromkeys(ids))   # remove duplicates but keep the original order
# Save to a CSV file in your data folder
pd.DataFrame({"id": ids}).to_csv("data/show_ids.csv", index=False)   