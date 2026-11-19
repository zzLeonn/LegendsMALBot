import json
import re

from rapidfuzz import fuzz

from src.services.database import get_all_anime


def _normalize(value):
    return re.sub(
        r"\s+",
        " ",
        re.sub(r"[^\w]+", " ", str(value).casefold()),
    ).strip()


def search_anime(query):
    query_normalized = _normalize(query)

    if not query_normalized:
        return []

    query_tokens = set(query_normalized.split())
    ranked_results = []

    for anime in get_all_anime():
        title = anime.get("title") or ""
        title_normalized = _normalize(title)
        candidates = [title]

        aliases_raw = anime.get("aliases")

        if aliases_raw:
            try:
                aliases = json.loads(aliases_raw)
            except (TypeError, ValueError):
                aliases = []

            if isinstance(aliases, list):
                candidates.extend(
                    alias for alias in aliases if isinstance(alias, str)
                )

        best_rank = None

        for candidate in candidates:
            candidate_normalized = _normalize(candidate)

            if not candidate_normalized:
                continue

            candidate_tokens = set(candidate_normalized.split())
            token_coverage = (
                len(query_tokens & candidate_tokens) / len(query_tokens)
            )
            similarity = max(
                fuzz.WRatio(query_normalized, candidate_normalized),
                fuzz.token_set_ratio(query_normalized, candidate_normalized),
            )
            rank = (
                int(query_normalized == title_normalized),
                int(query_normalized == candidate_normalized),
                int(
                    f" {query_normalized} "
                    in f" {candidate_normalized} "
                ),
                token_coverage,
                similarity,
                -len(candidate_normalized),
            )

            if best_rank is None or rank > best_rank:
                best_rank = rank

        if best_rank and (
            best_rank[0]
            or best_rank[1]
            or best_rank[2]
            or best_rank[4] >= 50
        ):
            ranked_results.append((best_rank, anime))

    ranked_results.sort(
        key=lambda result: (result[1].get("title") or "").casefold()
    )
    ranked_results.sort(key=lambda result: result[0], reverse=True)

    return [anime for _, anime in ranked_results[:15]]
