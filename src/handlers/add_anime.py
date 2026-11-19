import os
import sqlite3
from pathlib import Path

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters
)

from src.config import ADMIN_IDS
from src.services.database import add_anime


# =========================
# STATES
# =========================
TITLE, LINK, PHOTO, PHOTO_NAME = range(4)


# =========================
# IMAGE SAVE PATH
# =========================
PROJECT_ROOT = Path(__file__).resolve().parents[2]
IMAGE_FOLDER = PROJECT_ROOT / "assets" / "images"

# Create folder automatically
os.makedirs(IMAGE_FOLDER, exist_ok=True)


# =========================
# CANCEL KEYBOARD
# =========================
cancel_keyboard = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(
            "❌ Cancel",
            callback_data="cancel_addanime"
        )
    ]
])


# =========================
# START COMMAND
# =========================
async def addanime_start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return ConversationHandler.END

    if not update.effective_user:
        return ConversationHandler.END

    user_id = update.effective_user.id

    # Admin check
    if user_id not in ADMIN_IDS:

        await update.message.reply_text(
            "❌ You are not allowed to use this command."
        )

        return ConversationHandler.END

    await update.message.reply_text(
        "🎬 Send anime title",
        reply_markup=cancel_keyboard
    )

    return TITLE


# =========================
# TITLE
# =========================
async def get_title(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return TITLE

    if context.user_data is None:
        return ConversationHandler.END

    context.user_data["title"] = (
        (update.message.text or "").strip()
    )

    await update.message.reply_text(
        "🔗 Send anime link collection",
        reply_markup=cancel_keyboard
    )

    return LINK


# =========================
# LINK
# =========================
async def get_link(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return LINK

    if context.user_data is None:
        return ConversationHandler.END

    context.user_data["link"] = (
        (update.message.text or "").strip()
    )

    await update.message.reply_text(
        "🖼 Send anime thumbnail photo",
        reply_markup=cancel_keyboard
    )

    return PHOTO


# =========================
# PHOTO
# =========================
async def get_photo(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return PHOTO

    if context.user_data is None:
        return ConversationHandler.END

    # Handle normal photo
    if update.message.photo:

        photo = update.message.photo[-1]

        context.user_data["photo_file_id"] = (
            photo.file_id
        )

    # Handle image document
    elif (
        update.message.document
        and update.message.document.mime_type
        and update.message.document.mime_type.startswith("image/")
    ):

        context.user_data["photo_file_id"] = (
            update.message.document.file_id
        )

    else:

        await update.message.reply_text(
            "❌ Please send an image.",
            reply_markup=cancel_keyboard
        )

        return PHOTO

    await update.message.reply_text(
        "📝 Send image filename\n\nExample:\nnaruto.jpg",
        reply_markup=cancel_keyboard
    )

    return PHOTO_NAME


# =========================
# PHOTO NAME
# =========================
async def get_photo_name(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return PHOTO_NAME

    if context.user_data is None:
        return ConversationHandler.END

    photo_name = (
        (update.message.text or "").strip()
    )

    # Invalid Windows filename chars
    invalid_chars = r'<>:"/\|?*'

    for char in invalid_chars:
        photo_name = photo_name.replace(
            char,
            "_"
        )

    # Add extension automatically
    if not (
        photo_name.endswith(".jpg")
        or photo_name.endswith(".png")
        or photo_name.endswith(".jpeg")
        or photo_name.endswith(".webp")
    ):
        photo_name += ".jpg"

    title = context.user_data.get(
        "title"
    )

    link = context.user_data.get(
        "link"
    )

    photo_file_id = context.user_data.get(
        "photo_file_id"
    )

    # Missing data check
    if not title or not link or not photo_file_id:

        await update.message.reply_text(
            "❌ Missing anime data."
        )

        if context.user_data:
            context.user_data.clear()

        return ConversationHandler.END

    # Full save path
    save_path = IMAGE_FOLDER / (
        photo_name
    )

    # Prevent overwrite
    if os.path.exists(save_path):

        await update.message.reply_text(
            "❌ File already exists.\nChoose another filename."
        )

        return PHOTO_NAME

    try:

        # Get Telegram file
        tg_file = await context.bot.get_file(
            photo_file_id
        )

        # Download locally
        await tg_file.download_to_drive(str(save_path))

    except Exception as e:

        await update.message.reply_text(
            f"❌ Failed to save image.\n\n{e}"
        )

        if context.user_data:
            context.user_data.clear()

        return ConversationHandler.END

    # Database image path
    db_photo_path = f"assets/images/{photo_name}"

    # Save anime to database
    try:
        add_anime(
            title=title,
            link=link,
            photo=db_photo_path,
            photo_file_id=photo_file_id,
        )
    except sqlite3.Error:
        await update.message.reply_text(
            "❌ Failed to add anime to the database. Please check the bot logs."
        )
        if context.user_data:
            context.user_data.clear()
        return ConversationHandler.END

    await update.message.reply_text(
        f"""
✅ Anime added successfully

🎬 Title:
{title}

🖼 Image Saved:
{save_path}

📂 Database Path:
{db_photo_path}
"""
    )

    # Clear temporary data
    if context.user_data:
        context.user_data.clear()

    return ConversationHandler.END


# =========================
# CANCEL COMMAND
# =========================
async def cancel(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if update.message:

        await update.message.reply_text(
            "❌ Add anime cancelled."
        )

    if context.user_data:
        context.user_data.clear()

    return ConversationHandler.END


# =========================
# CANCEL BUTTON
# =========================
async def cancel_button(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    if not query:
        return ConversationHandler.END

    await query.answer()

    if context.user_data:
        context.user_data.clear()

    # Delete message
    if query.message:
        await query.message.delete()

    return ConversationHandler.END


# =========================
# CONVERSATION HANDLER
# =========================
addanime_handler = ConversationHandler(

    entry_points=[

        CommandHandler(
            "addanime",
            addanime_start
        )

    ],

    states={

        TITLE: [

            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                get_title
            )

        ],

        LINK: [

            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                get_link
            )

        ],

        PHOTO: [

            MessageHandler(
                (
                    filters.PHOTO
                    | filters.Document.IMAGE
                ),
                get_photo
            )

        ],

        PHOTO_NAME: [

            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                get_photo_name
            )

        ]

    },

    fallbacks=[

        CommandHandler(
            "cancel",
            cancel
        ),

        CallbackQueryHandler(
            cancel_button,
            pattern="^cancel_addanime$"
        )

    ]

)