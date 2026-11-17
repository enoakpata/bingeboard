import json
import os
import pandas as pd      # reads the CSV of IDs

rows = []

for filename in os.listdir("data/raw"):   # look at every file in data/raw
    with open(f"data/raw/{filename}", encoding="utf-8") as f:
        d = json.load(f)                           # load the file into a dictionary called d

    rows.append({
        "id": d["id"],
        "name": d["name"],
        "overview": d["overview"],

        # genres: a list of dicts → keep just the names, joined with "|" (e.g. "Drama|Sci-Fi & Fantasy")
        "genres": "|".join([g["name"] for g in d["genres"]]),       

        # keywords: same idea, but they live inside d["keywords"]["results"]
        "keywords": "|".join([k["name"] for k in d["keywords"]["results"]]),      

        # cast: only the first 5 actors (they're listed most important first)
        "cast": "|".join([actor["name"] for actor in d["credits"]["cast"][:5]]),          

        "seasons": d["number_of_seasons"],
        "episodes": d["number_of_episodes"],
        "status": d["status"],                     # e.g. "Returning Series", "Ended", "Canceled"
        "rating": d["vote_average"],
        "votes": d["vote_count"],
        "first_aired": d["first_air_date"],
        "last_aired": d["last_air_date"],
        "language": d["original_language"],
        "poster": d["poster_path"],                # half a URL; the website adds the start later
    })

df = pd.DataFrame(rows)                          # turn the list of dicts into a table
df.to_csv("data/shows.csv", index=False)         # save it

# --- Checks: always look at your data ---
print(df.shape)          # (rows, columns): should be (3000, 15)
print(df.head())         # first 5 rows
print(df.isna().sum())   # how many missing values in each column

# Count blank text ("") in the text columns: isna() doesn't catch these
for col in ["overview", "genres", "keywords", "cast"]:
    blank = (df[col] == "").sum()                      # True for each blank cell; sum counts them
    print(f"{col}: {blank} blank ({blank / len(df):.1%})")   # :.1% formats 0.05 as 5.0%
    
# Shows the engine can barely "see": no overview and no keywords
invisible = df[(df["overview"] == "") & (df["keywords"] == "")]   # & means both must be true
print(len(invisible))                                             # how many
print(invisible[["name", "language", "genres"]])                  # which ones