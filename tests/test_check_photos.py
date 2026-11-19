import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from telegram.error import BadRequest

from src.handlers.check_photos import check_photos_handler


class CheckPhotosTests(unittest.IsolatedAsyncioTestCase):
    @patch("src.handlers.check_photos.get_all_anime")
    @patch("src.handlers.check_photos.ADMIN_IDS", [42])
    async def test_admin_gets_validation_report(self, get_all_anime):
        get_all_anime.return_value = [
            {"title": "Good ID", "photo_file_id": "usable-id"},
            {"title": "Broken ID", "photo_file_id": "broken-id"},
            {"title": "No ID", "photo_file_id": None},
        ]
        reply_text = AsyncMock()
        context = SimpleNamespace(
            bot=SimpleNamespace(
                get_file=AsyncMock(
                    side_effect=[
                        None,
                        BadRequest("wrong remote file identifier"),
                    ]
                )
            )
        )
        update = SimpleNamespace(
            message=SimpleNamespace(reply_text=reply_text),
            effective_user=SimpleNamespace(id=42),
        )

        await check_photos_handler(update, context)

        report = reply_text.await_args.args[0]
        self.assertIn("Good ID — RESOLVES", report)
        self.assertIn("Broken ID — REJECTED", report)
        self.assertIn("No ID — MISSING", report)
        self.assertIn("CachedPhoto compatibility is not verified", report)

    @patch("src.handlers.check_photos.get_all_anime")
    @patch("src.handlers.check_photos.ADMIN_IDS", [42])
    async def test_non_admin_cannot_run_check(self, get_all_anime):
        reply_text = AsyncMock()
        context = SimpleNamespace(
            bot=SimpleNamespace(get_file=AsyncMock())
        )
        update = SimpleNamespace(
            message=SimpleNamespace(reply_text=reply_text),
            effective_user=SimpleNamespace(id=7),
        )

        await check_photos_handler(update, context)

        reply_text.assert_awaited_once_with(
            "❌ You are not allowed to use this command."
        )
        get_all_anime.assert_not_called()
        context.bot.get_file.assert_not_awaited()


if __name__ == "__main__":
    unittest.main()
