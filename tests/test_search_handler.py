import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from telegram import InlineQueryResultArticle, InlineQueryResultCachedPhoto
from telegram.error import BadRequest

from src.handlers.search import inline_query


class InlineSearchTests(unittest.IsolatedAsyncioTestCase):
    @patch("src.handlers.search.search_anime")
    async def test_invalid_cached_photo_retries_without_photos(self, search):
        search.return_value = [
            {
                "id": 1,
                "title": "Example Anime",
                "link": "https://example.com",
                "photo_file_id": "invalid-file-id",
            }
        ]
        inline = SimpleNamespace(
            query="example",
            answer=AsyncMock(
                side_effect=[
                    BadRequest(
                        "Wrong remote file identifier specified: "
                        "can't unserialize it. wrong last symbol"
                    ),
                    None,
                ]
            ),
        )

        await inline_query(SimpleNamespace(inline_query=inline), None)

        self.assertIsInstance(
            inline.answer.await_args_list[0].kwargs["results"][0],
            InlineQueryResultCachedPhoto,
        )
        self.assertIsInstance(
            inline.answer.await_args_list[1].kwargs["results"][0],
            InlineQueryResultArticle,
        )

    @patch("src.handlers.search.search_anime")
    async def test_unrelated_bad_request_is_raised(self, search):
        search.return_value = [
            {
                "id": 1,
                "title": "Example Anime",
                "link": "https://example.com",
                "photo_file_id": "valid-file-id",
            }
        ]
        inline = SimpleNamespace(
            query="example",
            answer=AsyncMock(side_effect=BadRequest("query is too old")),
        )

        with self.assertRaises(BadRequest):
            await inline_query(SimpleNamespace(inline_query=inline), None)

        inline.answer.assert_awaited_once()


if __name__ == "__main__":
    unittest.main()
