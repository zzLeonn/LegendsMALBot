import sqlite3
import json
from telegram import InputFile
from rapidfuzz import process

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    InlineQueryHandler
)

# =========================
# BOT TOKEN
# =========================
BOT_TOKEN = "8871787485:AAGe9k-PK9LgfTHhtppmm8eXXAUU4x7W6PE"


# =========================
# DATABASE CONNECTION
# =========================
def get_db_connection():
    conn = sqlite3.connect("anime.db")
    conn.row_factory = sqlite3.Row
    return conn


# =========================
# GET ALL ANIME FROM DB
# =========================
def get_all_anime():
    conn = get_db_connection()

    anime_list = conn.execute(
        "SELECT * FROM anime"
    ).fetchall()

    conn.close()

    return anime_list

# =========================
# /START COMMAND
# =========================
async def start_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    caption = """
🌟 Legends MAL Anime Search Bot 🌟

🇲🇲 မြန်မာ

ဒီ Bot လေးက Legends Anime MM Subbed Channel ထဲမှာ တင်ထားတဲ့ Anime တွေကို အလွယ်တကူ ရှာဖွေပေးနိုင်ပါတယ်။

🔍 Anime Name ရိုက်ပြီး ချက်ချင်းရှာနိုင်ပါတယ်။

📌 Features
• Anime Link Collection များ
• Movies & Seasons များ
• MM Subbed Anime များ
• @LegendsMALbot ကို Mention ခေါ်ပြီး Anime Link တွေကို ဘယ် Chat မှာမဆို Share လုပ်နိုင်ပါတယ်။

📌 Commands
/search anime name
→ Anime ရှာရန်

━━━━━━━━━━━━━━

🇬🇧 English

This bot helps you quickly search anime currently uploaded in Legends Anime MM Subbed channel.

✨ Features
• Anime Link Collections
• Movies & Seasons
• MM Subbed Anime
• Mention @LegendsMALbot in any chat to instantly share anime links with others.

📌 Commands
/search anime name
→ Search anime instantly

━━━━━━━━━━━━━━

📢 "Main Channel"
https://t.me/+EyIDvbx2mkNhNWE1

📝 "Review Channel"
https://t.me/+dKZL1b8ZWMU5ZjBl

✨ Enjoy Watching Anime ✨
"""

    keyboard = [
        [
            InlineKeyboardButton(
                "🔍 Search Anime",
                switch_inline_query_current_chat="/search "
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(
        keyboard
    )

    with open("start_banner.jpg", "rb") as photo:

        await update.message.reply_photo(
            photo=photo,
            caption=caption,
            reply_markup=reply_markup
        )

# =========================
# SEARCH FUNCTION
# =========================
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


# =========================
# GET SINGLE ANIME
# =========================
def get_anime_by_title(title):

    conn = get_db_connection()

    anime = conn.execute(
        "SELECT * FROM anime WHERE title = ?",
        (title,)
    ).fetchone()

    conn.close()

    if anime:
        return dict(anime)

    return None


# =========================
# /SEARCH COMMAND
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

    # Send results
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

    # Get anime from DB
    anime = get_anime_by_title(
        anime_title
    )

    if not anime:
        return

    # Caption
    caption = f"""
🐥 {anime['title']} | MM Subbed |

🤩 - - - - | • | - - - - 🤩

🔗 Link Collection:
{anime['link']}
"""

    # Send anime poster
    try:

        with open(anime["photo"], "rb") as photo:

            await context.bot.send_photo(
                chat_id=query.message.chat_id,
                photo=photo,
                caption=caption
            )

    # If image missing
    except FileNotFoundError:

        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=caption
        )

    # Delete search results AFTER sending
    await query.message.delete()
# =========================
# INLINE SEARCH
# =========================
async def inline_query(update, context):

    query = update.inline_query.query

    if not query:
        return

    results = search_anime(query)

    articles = []

    for anime in results:

        caption = f"""
🐥 {anime['title']} | MM Subbed |

🔗 Link Collection:
{anime['link']}
"""

        articles.append(

            InlineQueryResultArticle(
                id=anime["title"],
                title=anime["title"],

                input_message_content=InputTextMessageContent(
                    caption
                ),

                description="Anime Link Collection"
            )

        )

    await update.inline_query.answer(
        articles,
        cache_time=1
    )
# =========================
# MAIN FUNCTION
# =========================
def main():

    app = Application.builder().token(
        BOT_TOKEN
    ).build()
    # /start command
    app.add_handler(
    CommandHandler(
        "start",
        start_handler
    )
)

    # /search command
    app.add_handler(
        CommandHandler(
            "search",
            search_handler
        )
    )
    #inlinehandler
    app.add_handler(
    InlineQueryHandler(inline_query)
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