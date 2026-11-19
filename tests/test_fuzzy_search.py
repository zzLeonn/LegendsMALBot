import json
import unittest
from unittest.mock import patch

from src.services.fuzzy_search import search_anime


class SearchAnimeTests(unittest.TestCase):
    @patch("src.services.fuzzy_search.get_all_anime")
    def test_exact_alias_match_ranks_ahead_of_unrelated_titles(
        self, get_all_anime
    ):
        get_all_anime.return_value = [
            {"title": "Attack on Titan", "aliases": "[]"},
            {
                "title": "My Hero Academia",
                "aliases": json.dumps(["boku no hero academia"]),
            },
            {"title": "Blue Lock", "aliases": "[]"},
        ]

        results = search_anime("boku no hero academia")

        self.assertEqual(results[0]["title"], "My Hero Academia")

    @patch("src.services.fuzzy_search.get_all_anime")
    def test_best_fuzzy_keyword_match_ranks_first(self, get_all_anime):
        get_all_anime.return_value = [
            {"title": "Attack on Titan", "aliases": "[]"},
            {"title": "One Piece Film: Red", "aliases": "[]"},
            {"title": "One Piece Film: Z", "aliases": "[]"},
        ]

        results = search_anime("one piece fim red")

        self.assertEqual(results[0]["title"], "One Piece Film: Red")

    @patch("src.services.fuzzy_search.get_all_anime")
    def test_empty_query_returns_no_results(self, get_all_anime):
        self.assertEqual(search_anime("   "), [])
        get_all_anime.assert_not_called()


if __name__ == "__main__":
    unittest.main()
