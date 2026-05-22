from pathlib import Path
import logging

logger = logging.getLogger(__name__)


# =========================
# SEND ANIME
# =========================
async def send_anime(
    context,
    chat_id,
    anime
):

    caption = f"""
🐥 {anime['title']} | MM Subbed |

🤩 - - - - | • | - - - - 🤩

🔗 Link Collection:
{anime['link']}
"""

    photo_path = Path(
        anime["photo"]
    )

    try:

        # Send photo if image exists
        if photo_path.exists():

            with open(photo_path, "rb") as photo:

                await context.bot.send_photo(
                    chat_id=chat_id,
                    photo=photo,
                    caption=caption
                )

        else:

            logger.warning(
                f"Missing image: {photo_path}"
            )

            await context.bot.send_message(
                chat_id=chat_id,
                text=caption
            )

    except Exception as e:

        logger.error(
            f"Failed to send anime: {e}"
        )

        await context.bot.send_message(
            chat_id=chat_id,
            text="❌ Failed to send anime."
        )