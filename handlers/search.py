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

from utils.fuzzy_search import search_anime


# =========================
# /SEARCH COMMAND
# =========================
async def search_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return

    if not context.args:

        await update.message.reply_text(
            "Usage:\n/search anime name"
        )

        return

    query = " ".join(context.args)

    results = search_anime(query)

    if not results:

        await update.message.reply_text(
            "❌ No anime found."
        )

        return

    keyboard = []

    for anime in results:

        keyboard.append([
            InlineKeyboardButton(
                anime["title"],
                callback_data=f"anime_{anime['id']}"
            )
        ])

    reply_markup = InlineKeyboardMarkup(keyboard)

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

    query = update.inline_query.query.strip()

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
                id=str(anime["id"]),

                title=anime["title"],

                description="Anime Link Collection",

                input_message_content=InputTextMessageContent(
                    caption
                )
            )

        )

    await update.inline_query.answer(
        articles,
        cache_time=1,
        is_personal=True
    )