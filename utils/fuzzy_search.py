from rapidfuzz import process

def search_anime(query, anime_list, limit=5):
    searchable = {}

    for anime in anime_list:
        searchable[anime["title"]] = anime

        for alias in anime.get("aliases", []):
            searchable[alias] = anime

    results = process.extract(
        query,
        searchable.keys(),
        limit=limit
    )

    unique_results = []
    seen = set()

    for result in results:
        anime = searchable[result[0]]

        if anime["title"] not in seen:
            unique_results.append(anime)
            seen.add(anime["title"])

    return unique_results