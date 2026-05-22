import logging

from telegram import Update

from telegram.ext import (
    ContextTypes
)

from utils.database import (
    get_anime_by_id
)

from utils.send_anime import (
    send_anime
)

logger = logging.getLogger(__name__)


# =========================
# BUTTON HANDLER
# =========================
async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    # Safety check
    if not update.callback_query:
        return

    query = update.callback_query

    # Safety check
    if not query.message:
        return

    # Answer callback safely
    try:

        await query.answer()

    except Exception as e:

        logger.warning(
            f"Failed to answer callback query: {e}"
        )

        return

    # Get callback data safely
    data = query.data

    if not data:
        return

    # Validate callback format
    if not data.startswith("anime_"):

        logger.warning(
            f"Invalid callback data: {data}"
        )

        return

    # Extract anime ID safely
    try:

        anime_id = int(
            data.split("_")[1]
        )

    except (
        ValueError,
        IndexError
    ):

        logger.warning(
            f"Invalid anime ID: {data}"
        )

        return

    # Fetch anime from database
    anime = get_anime_by_id(
        anime_id
    )

    # Anime not found
    if not anime:

        await query.message.reply_text(
            "❌ Anime not found."
        )

        return

    # Send anime
    await send_anime(
        context=context,
        chat_id=query.message.chat.id,
        anime=anime
    )

    # Delete old search message safely
    try:

        await query.message.delete()

    except Exception as e:

        logger.warning(
            f"Failed to delete message: {e}"
        )