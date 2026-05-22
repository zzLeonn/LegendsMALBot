import json

from rapidfuzz import process

from utils.database import (
    get_all_anime
)


# =========================
# SEARCH ANIME
# =========================
def search_anime(
    query
):

    anime_rows = get_all_anime()

    choices = {}

    for anime in anime_rows:

        anime_dict = dict(anime)

        # Main title
        choices[
            anime_dict["title"]
        ] = anime_dict

        # Aliases
        aliases_raw = anime_dict.get(
            "aliases"
        )

        if aliases_raw:

            try:

                aliases = json.loads(
                    aliases_raw
                )

            except Exception:

                aliases = []

            for alias in aliases:

                choices[
                    alias
                ] = anime_dict

    # =========================
    # FUZZY SEARCH
    # =========================
    results = process.extract(
        query.lower(),
        choices.keys(),
        limit=5,
        score_cutoff=50
    )

    final_results = []

    added = set()

    for result in results:

        anime = choices[
            result[0]
        ]

        if anime["title"] not in added:

            final_results.append(
                anime
            )

            added.add(
                anime["title"]
            )

    return final_results