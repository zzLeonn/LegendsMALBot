from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    ContextTypes
)

from utils.database import (
    get_all_anime
)

# =========================
# SETTINGS
# =========================
ANIME_PER_PAGE = 8


# =========================
# BUILD KEYBOARD
# =========================
def build_list_keyboard(
    anime_list,
    page: int
):

    keyboard = []

    start = page * ANIME_PER_PAGE
    end = start + ANIME_PER_PAGE

    current_page = anime_list[start:end]

    # Anime buttons
    for anime in current_page:

        keyboard.append([
            InlineKeyboardButton(
                anime["title"],
                callback_data=f"anime_{anime['id']}"
            )
        ])

    # Navigation buttons
    nav_buttons = []

    if page > 0:

        nav_buttons.append(

            InlineKeyboardButton(
                "⬅ Prev",
                callback_data=f"list_{page-1}"
            )
        )

    if end < len(anime_list):

        nav_buttons.append(

            InlineKeyboardButton(
                "Next ➡",
                callback_data=f"list_{page+1}"
            )
        )

    if nav_buttons:
        keyboard.append(nav_buttons)

    return InlineKeyboardMarkup(keyboard)


# =========================
# /LIST COMMAND
# =========================
async def list_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return

    anime_list = get_all_anime()

    if not anime_list:

        await update.message.reply_text(
            "❌ No anime available."
        )

        return

    reply_markup = build_list_keyboard(
        anime_list,
        page=0
    )

    await update.message.reply_text(
        "📚 Available Anime",
        reply_markup=reply_markup
    )