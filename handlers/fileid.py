from telegram import Update
from telegram.ext import ContextTypes


async def get_file_id(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return

    # Check if command is replying to a message
    if not update.message.reply_to_message:

        await update.message.reply_text(
            "❌ Reply to a photo with /fileid"
        )

        return

    replied = update.message.reply_to_message

    # Check if replied message has photo
    if not replied.photo:

        await update.message.reply_text(
            "❌ The replied message does not contain a photo."
        )

        return

    # Get highest quality photo
    photo = replied.photo[-1]

    # Send file_id
    await update.message.reply_text(
        f"📁 File ID:\n\n{photo.file_id}"
    )