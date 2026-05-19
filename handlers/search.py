from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from utils.database import load_anime_data
from utils.fuzzy_search import search_anime

anime_data = load_anime_data()

async def search_handler(update, context):
    query = " ".join(context.args)

    if not query:
        await update.message.reply_text(
            "Usage:\n/search anime name"
        )
        return

    results = search_anime(query, anime_data)

    if not results:
        await update.message.reply_text(
            "No anime found."
        )
        return

    keyboard = []

    for anime in results:
        keyboard.append([
            InlineKeyboardButton(
                anime["title"],
                callback_data=anime["title"]
            )
        ])

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🔍 Search Results:",
        reply_markup=reply_markup
    )