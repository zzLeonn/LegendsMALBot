import json

from rapidfuzz import process

from utils.database import (
    get_all_anime
)


def search_anime(query):

    anime_rows = get_all_anime()

    choices = {}

    for anime in anime_rows:

        anime_dict = dict(anime)

        # Main title
        choices[anime_dict["title"]] = anime_dict

        # Aliases
        aliases = json.loads(
            anime_dict["aliases"]
        )

        for alias in aliases:

            choices[alias] = anime_dict

    # Fuzzy search
    results = process.extract(
        query,
        choices.keys(),
        limit=5,
        score_cutoff=50
    )

    final_results = []

    added = set()

    for result in results:

        anime = choices[result[0]]

        # Prevent duplicates
        if anime["title"] not in added:

            final_results.append(anime)

            added.add(anime["title"])

    return final_results