from telegram import Update

from telegram.ext import (
    ContextTypes
)

from utils.database import (
    get_anime_by_title
)


async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.callback_query:
        return

    query = update.callback_query

    if not query.message:
        return

    await query.answer()

    anime_title = query.data

    anime = get_anime_by_title(
        anime_title
    )

    if not anime:
        return

    caption = f"""
🐥 {anime['title']} | MM Subbed |

🤩 - - - - | • | - - - - 🤩

🔗 Link Collection:
{anime['link']}
"""

    try:

        with open(anime["photo"], "rb") as photo:

            await context.bot.send_photo(
                chat_id=query.message.chat.id,
                photo=photo,
                caption=caption
            )

    except FileNotFoundError:

        await context.bot.send_message(
            chat_id=query.message.chat.id,
            text=caption
        )

    # Delete search result buttons
    await query.message.delete()