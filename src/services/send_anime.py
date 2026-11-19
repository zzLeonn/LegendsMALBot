import os
from pathlib import Path

from telegram.ext import (
    ContextTypes
)


# =========================
# BASE IMAGE PATH
# =========================
PROJECT_ROOT = Path(__file__).resolve().parents[2]


# =========================
# SEND ANIME
# =========================
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

    # =========================
    # TRY TELEGRAM FILE ID FIRST
    # =========================
    photo_file_id = anime.get(
        "photo_file_id"
    )

    try:

        if photo_file_id:

            await context.bot.send_photo(
                chat_id=chat_id,
                photo=photo_file_id,
                caption=caption
            )

            return

    except Exception:

        pass

    # =========================
    # FALLBACK TO LOCAL IMAGE
    # =========================
    photo_path = anime.get(
        "photo"
    )

    if photo_path:

        normalized_photo_path = (
            Path("assets") / photo_path
            if photo_path.startswith("images/")
            else Path(photo_path)
        )
        full_path = PROJECT_ROOT / normalized_photo_path

        if os.path.exists(full_path):

            try:

                with open(full_path, "rb") as photo_file:

                    await context.bot.send_photo(
                        chat_id=chat_id,
                        photo=photo_file,
                        caption=caption
                    )

                    return

            except Exception:

                pass

    # =========================
    # FINAL FALLBACK
    # =========================
    await context.bot.send_message(
        chat_id=chat_id,
        text=f"""
🐥 {anime['title']} | MM Subbed |

🔗 Link Collection:
{anime['link']}

⚠️ Image unavailable.
"""
    )