import logging

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InlineQueryResultCachedPhoto,
    InputTextMessageContent
)

from telegram.ext import (
    ContextTypes
)
from telegram.error import BadRequest

from src.services.fuzzy_search import (
    search_anime
)

logger = logging.getLogger(__name__)


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
                callback_data=f"anime_{anime['id']}"
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

    query = (
        update.inline_query.query or ""
    ).strip()

    if not query:
        return

    results = search_anime(query)

    articles = []
    fallback_articles = []

    for anime in results:

        message_text = (
            f"🎬 <b>{anime['title']}</b>\n\n"
            f"🔗 <b>Link Collection</b>\n"
            f"{anime['link']}"
        )

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "📺 Open Collection",
                    url=anime["link"]
                )
            ]
        ])

        fallback_articles.append(
            InlineQueryResultArticle(
                id=str(anime["id"]),
                title=anime["title"],
                description="🇲🇲 Myanmar Subbed Anime",
                reply_markup=keyboard,
                input_message_content=InputTextMessageContent(
                    message_text,
                    parse_mode="HTML"
                )
            )
        )

        photo_file_id = anime.get("photo_file_id")

        if photo_file_id:
            articles.append(
                InlineQueryResultCachedPhoto(
                    id=str(anime["id"]),
                    photo_file_id=photo_file_id,
                    title=anime["title"],
                    description="🇲🇲 Myanmar Subbed Anime",
                    caption=message_text,
                    parse_mode="HTML",
                    reply_markup=keyboard
                )
            )
        else:
            articles.append(
                InlineQueryResultArticle(
                    id=str(anime["id"]),
                    title=anime["title"],
                    description="🇲🇲 Myanmar Subbed Anime",
                    reply_markup=keyboard,
                    input_message_content=InputTextMessageContent(
                        message_text,
                        parse_mode="HTML"
                    )
                )
            )

    try:
        await update.inline_query.answer(
            results=articles,
            cache_time=1,
            is_personal=True
        )
    except BadRequest as error:
        error_message = str(error).casefold()

        if (
            "wrong remote file identifier" not in error_message
            and "can't unserialize it" not in error_message
        ):
            raise

        logger.warning(
            "Cached photo ID was rejected; retrying inline search without photos: %s",
            error
        )
        await update.inline_query.answer(
            results=fallback_articles,
            cache_time=1,
            is_personal=True
        )