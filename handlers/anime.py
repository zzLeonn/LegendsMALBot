from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from main import app
from utils.jikan import search_anime

@app.on_message(filters.command("start"))
async def start_command(client, message):

    text = """
🤖 Welcome to Anime Metadata Bot

Usage:
/anime anime_name

Example:
/anime fire force
"""

    await message.reply_text(text)

@app.on_message(filters.command("anime"))
async def anime_command(client, message):

    if len(message.command) < 2:
        return await message.reply_text(
            "❌ Please provide an anime name."
        )

    query = " ".join(message.command[1:])

    anime = search_anime(query)

    if not anime:
        return await message.reply_text(
            "❌ Anime not found."
        )

    caption = f"""
🔥 <b>{anime['title']}</b>

⭐ <b>Score:</b> {anime['score']}
🎬 <b>Episodes:</b> {anime['episodes']}
📺 <b>Status:</b> {anime['status']}
🎭 <b>Genres:</b> {anime['genres']}

📖 <b>Synopsis:</b>
{anime['synopsis'][:500]}...
"""

    buttons = []

    if anime["trailer"]:
        buttons.append(
            [
                InlineKeyboardButton(
                    "🎬 Watch Trailer",
                    url=anime["trailer"]
                )
            ]
        )

    reply_markup = InlineKeyboardMarkup(buttons)

    await message.reply_photo(
        photo=anime["image"],
        caption=caption,
        reply_markup=reply_markup
    )