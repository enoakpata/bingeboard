# Shared TMDB setup: any script can import `get` from here.
import os        # reads your token from the environment
import time      # lets us pause before retrying
import requests  # sends requests to the API
from dotenv import load_dotenv  # reads the .env file

load_dotenv()  # load TMDB_TOKEN from .env
BASE = "https://api.themoviedb.org/3"  # TMDB's main address

# One ongoing connection with your token attached to every request
session = requests.Session()
session.headers.update({"Authorization": f"Bearer {os.environ['TMDB_TOKEN']}"})


def get(path, **params):
    """Ask TMDB for something. Retries if TMDB says 'slow down'."""
    for attempt in range(5):  # try up to 5 times
        r = session.get(f"{BASE}{path}", params=params, timeout=10)
        if r.status_code == 429:      # 429 = too many requests
            time.sleep(2 ** attempt)  # wait 1s, 2s, 4s, 8s, 16s, then retry
            continue
        r.raise_for_status()  # any other error → stop with a clear message
        return r.json()       # success: reply as a Python dictionary
    raise RuntimeError(f"Gave up on {path}")  # all 5 attempts failed