from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent
)

from telegram.ext import (
    ContextTypes
)

from utils.fuzzy_search import (
    search_anime
)


# =========================
# /SEARCH COMMAND
# =========================
async def search_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return

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
# INLINE SEARCH
# =========================
async def inline_query(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.inline_query:
        return

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