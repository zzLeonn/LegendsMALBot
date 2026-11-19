from telegram import Update
from telegram.error import BadRequest, TelegramError
from telegram.ext import ContextTypes

from src.config import ADMIN_IDS
from src.services.database import get_all_anime


async def check_photos_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if not update.message:
        return

    user = update.effective_user

    if not user or user.id not in ADMIN_IDS:
        await update.message.reply_text(
            "❌ You are not allowed to use this command."
        )
        return

    anime_list = get_all_anime()

    if not anime_list:
        await update.message.reply_text(
            "❌ No anime available to check."
        )
        return

    counts = {
        "resolves": 0,
        "rejected": 0,
        "missing": 0,
        "check errors": 0,
    }
    report_lines = [
        "📸 Photo ID check",
        "RESOLVES means Telegram accepted the ID; CachedPhoto compatibility "
        "is not verified.",
        "",
    ]

    for anime in anime_list:
        title = " ".join(str(anime.get("title") or "Untitled").split())
        file_id = anime.get("photo_file_id")

        if not file_id:
            status = "MISSING"
            counts["missing"] += 1
        elif not isinstance(file_id, str):
            status = "REJECTED: file ID is not text"
            counts["rejected"] += 1
        else:
            try:
                await context.bot.get_file(file_id)
            except BadRequest as error:
                detail = " ".join(str(error).split())
                status = f"REJECTED: {detail[:160]}"
                counts["rejected"] += 1
            except TelegramError as error:
                detail = " ".join(str(error).split())
                status = f"CHECK ERROR: {detail[:160]}"
                counts["check errors"] += 1
            else:
                status = "RESOLVES"
                counts["resolves"] += 1

        report_lines.append(f"{title} — {status}")

    report_lines.extend([
        "",
        (
            "Totals: "
            f"{counts['resolves']} resolve, "
            f"{counts['rejected']} rejected, "
            f"{counts['missing']} missing, "
            f"{counts['check errors']} check errors."
        ),
        "Re-upload rejected images as photos, not documents.",
    ])

    message = ""

    for line in report_lines:
        if len(message) + len(line) + 1 > 3500:
            await update.message.reply_text(message.rstrip())
            message = ""

        message += f"{line}\n"

    if message:
        await update.message.reply_text(message.rstrip())
