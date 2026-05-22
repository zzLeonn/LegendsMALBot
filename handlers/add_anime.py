from telegram import Update

from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    filters
)

from config import ADMIN_IDS

from utils.database import (
    add_anime
)


# =========================
# STATES
# =========================
TITLE, LINK, PHOTO = range(3)


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
        "🎬 Send anime title"
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
        update.message.text
    )

    await update.message.reply_text(
        "🔗 Send anime link collection"
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
        update.message.text
    )

    await update.message.reply_text(
        "🖼 Send anime thumbnail photo"
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

    if not update.message.photo:

        await update.message.reply_text(
            "❌ Please send a photo."
        )

        return PHOTO

    # Highest quality photo
    photo = update.message.photo[-1]

    photo_file_id = photo.file_id

    title = context.user_data.get(
        "title"
    )

    link = context.user_data.get(
        "link"
    )

    # Safety checks
    if not title or not link:

        await update.message.reply_text(
            "❌ Missing anime data."
        )

        context.user_data.clear()

        return ConversationHandler.END

    # Save anime to database
    add_anime(
        title=title,
        link=link,
        photo_file_id=photo_file_id
    )

    await update.message.reply_text(
        f"✅ Anime added successfully\n\n🎬 {title}"
    )

    # Clear temp data
    context.user_data.clear()

    return ConversationHandler.END


# =========================
# CANCEL
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
                filters.PHOTO,
                get_photo
            )

        ]

    },

    fallbacks=[

        CommandHandler(
            "cancel",
            cancel
        )

    ]

)