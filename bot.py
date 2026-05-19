import json
from rapidfuzz import process

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

# =========================
# BOT TOKEN
# =========================
BOT_TOKEN = "8871787485:AAGe9k-PK9LgfTHhtppmm8eXXAUU4x7W6PE"


# =========================
# LOAD ANIME DATABASE
# =========================
with open("anime_data.json", "r", encoding="utf-8") as file:
    anime_list = json.load(file)


# =========================
# SEARCH FUNCTION
# =========================
def search_anime(query):
    choices = {}

    for anime in anime_list:
        # Main title
        choices[anime["title"]] = anime

        # Aliases
        for alias in anime["aliases"]:
            choices[alias] = anime

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


# =========================
# /SEARCH COMMAND HANDLER
# =========================
async def search_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    # No anime name provided
    if not context.args:
        await update.message.reply_text(
            "Usage:\n/search anime name"
        )
        return

    # Combine arguments
    query = " ".join(context.args)

    # Search anime
    results = search_anime(query)

    # No results
    if not results:
        await update.message.reply_text(
            "❌ No anime found."
        )
        return

    # Create buttons
    keyboard = []

    for anime in results:
        keyboard.append([
            InlineKeyboardButton(
                anime["title"],
                callback_data=anime["title"]
            )
        ])

    reply_markup = InlineKeyboardMarkup(
        keyboard
    )

    # Send search results
    await update.message.reply_text(
        "🔍 Search Results",
        reply_markup=reply_markup,
        reply_to_message_id=update.message.message_id
    )


# =========================
# BUTTON HANDLER
# =========================
async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query

    await query.answer()

    anime_title = query.data

    # Find selected anime
    anime = next(
        (
            a for a in anime_list
            if a["title"] == anime_title
        ),
        None
    )

    if not anime:
        return

    # Caption
    caption = f"""
🐥 {anime['title']} | MM Subbed |

🤩 - - - - | • | - - - -

🔗 Link Collection:
{anime['link']}
"""

    # Send anime poster
    try:
        with open(anime["photo"], "rb") as photo:
            await query.message.reply_photo(
                photo=photo,
                caption=caption
            )

    # If image missing
    except FileNotFoundError:
        await query.message.reply_text(
            caption
        )


# =========================
# MAIN FUNCTION
# =========================
def main():
    app = Application.builder().token(
        BOT_TOKEN
    ).build()

    # /search command
    app.add_handler(
        CommandHandler(
            "search",
            search_handler
        )
    )

    # Button clicks
    app.add_handler(
        CallbackQueryHandler(
            button_handler
        )
    )

    print("Bot is running...")

    app.run_polling()


# =========================
# START BOT
# =========================
if __name__ == "__main__":
    main()