import logging

from telegram import Update

from telegram.ext import (
    ContextTypes
)

from utils.database import (
    get_all_anime,
    get_anime_by_id
)

from utils.send_anime import (
    send_anime
)

from handlers.list_anime import (
    build_list_keyboard
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

    # =========================
    # LIST PAGINATION
    # =========================
    if data.startswith("list_"):

        try:

            page = int(
                data.split("_")[1]
            )

        except (
            ValueError,
            IndexError
        ):

            return

        anime_list = get_all_anime()

        reply_markup = build_list_keyboard(
            anime_list,
            page
        )

        try:

            await query.edit_message_text(
                "📚 Available Anime",
                reply_markup=reply_markup
            )

        except Exception as e:

            logger.warning(
                f"Failed to edit list page: {e}"
            )

        return

    # =========================
    # ANIME BUTTONS
    # =========================
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

        await query.edit_message_text(
            "❌ Anime not found."
        )

        return

    # Show loading instantly
    try:

        await query.edit_message_text(
            f"⏳ Loading {anime['title']}..."
        )

    except Exception as e:

        logger.warning(
            f"Failed to edit loading message: {e}"
        )

    # Send anime
    await send_anime(
        context=context,
        chat_id=query.message.chat.id,
        anime=anime
    )

    # Remove loading message
    try:

        await query.message.delete()

    except Exception as e:

        logger.warning(
            f"Failed to delete loading message: {e}"
        )