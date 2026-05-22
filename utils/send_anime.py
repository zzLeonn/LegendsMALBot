from telegram.ext import ContextTypes


async def send_anime(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    anime
):

    caption = f"""
🐥 {anime['title']} | MM Subbed |

🔗 Link Collection:
{anime['link']}
"""

    await context.bot.send_photo(
        chat_id=chat_id,
        photo=anime["photo_file_id"],
        caption=caption
    )