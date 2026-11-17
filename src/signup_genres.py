import pandas as pd

df = pd.read_csv("data/shows.csv")

# Use the same romance keywords you settled on in the notebook
ROMANCE_KEYWORDS = {"romance", "love", "romantic comedy", "first love", "love triangle", "gay romance", "slow burn romance", "star crossed lovers", "friends to lovers",
                    "friends in love", "love at first sight", "office romance", "love affair", "enemies to lovers", "high school romance", "forbidden love"}


def has_genre(genres, name):
    """True if `name` is one of the show's TMDB genres (genres look like 'Drama|Comedy')."""
    return isinstance(genres, str) and name in genres.split("|")


def is_romance(keywords):
    """True if any of the show's keywords is one of the romance keywords."""
    return isinstance(keywords, str) and any(
        k.lower() in ROMANCE_KEYWORDS for k in keywords.split("|")
    )


def signup_labels(row):
    """Work out which sign-up genres one show belongs to. Returns a list of labels."""
    g, lang = row["genres"], row["language"]   # this show's genres and language
    labels = []

    # Simple ones: copied straight from TMDB genres
    for name in ["Drama", "Comedy", "Sci-Fi & Fantasy", "Action & Adventure",
                 "Crime", "Mystery", "Documentary", "Reality"]:
        if has_genre(g, name):
            labels.append(name)

    # Combined / built ones
    if has_genre(g, "Family") or has_genre(g, "Kids"):
        labels.append("Family & Kids")                     # two small genres merged
    if has_genre(g, "Animation") and lang == "ja":
        labels.append("Anime")                             # Japanese animation
    if has_genre(g, "Animation") and lang != "ja":
        labels.append("Animation")                         # everything else animated
    if has_genre(g, "Drama") and lang == "ko":
        labels.append("K-Drama")                           # Korean drama
    if is_romance(row["keywords"]):
        labels.append("Romance")                           # from keywords (TMDB has no TV romance genre)

    return labels


# Apply to every show (axis=1 means "one row at a time"), then join into "A|B|C" text
df["signup_genres"] = df.apply(signup_labels, axis=1).str.join("|")
df.to_csv("data/shows.csv", index=False)   # save back with the new column

# --- Check: how many shows per sign-up genre? ---
counts = df["signup_genres"].str.split("|").explode().value_counts()
print(counts)
print((df["signup_genres"] == "").sum(), "shows have no sign-up genre")   # shows that fit none

none = df[df["signup_genres"].isna() | (df["signup_genres"] == "")]   # blank = fits no sign-up genre
print(none[["name", "genres", "language"]])                          # what are they?

# Drop shows that fit no sign-up genre (a few soaps and news shows)
before = len(df)
df = df[df["signup_genres"].fillna("") != ""]   # fillna("") turns missing into blank, then keep non-blank rows
print(f"Dropped {before - len(df)} shows, {len(df)} left")