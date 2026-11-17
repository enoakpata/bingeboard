import os, requests
from dotenv import load_dotenv

load_dotenv()
r = requests.get(
    "https://api.themoviedb.org/3/search/tv",
    headers={"Authorization": f"Bearer {os.environ['TMDB_TOKEN']}"},
    params={"query": "Abbott Elementary"},
)
print(r.status_code)
print(r.json()["results"][0]["name"], r.json()["results"][0]["id"])