import logging
from pathlib import Path
from warnings import filterwarnings
from telegram.warnings import PTBUserWarning

filterwarnings(
    action="ignore",
    message=r".*per_message=False.*",
    category=PTBUserWarning,
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    InlineQueryHandler
)

from config import BOT_TOKEN

from handlers.start import (
    start_handler
)

from handlers.fileid import (
    get_file_id
)

from handlers.search import (
    search_handler,
    inline_query
)

from handlers.callbacks import (
    button_handler
)

from handlers.list_anime import (
    list_handler
)
from handlers.add_anime import (
    addanime_handler
)


# =========================
# CREATE LOGS FOLDER
# =========================
Path("logs").mkdir(
    exist_ok=True
)


# =========================
# LOGGING SETUP
# =========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(
            "logs/bot.log",
            encoding="utf-8"
        ),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


# =========================
# GLOBAL ERROR HANDLER
# =========================
async def error_handler(update, context):

    logger.error(
        msg="Exception while handling update:",
        exc_info=context.error
    )


# =========================
# MAIN FUNCTION
# =========================
def main():

    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    # =========================
    # COMMAND HANDLERS
    # =========================
    app.add_handler(
        CommandHandler(
            "start",
            start_handler
        )
    )

    app.add_handler(
        CommandHandler(
            "search",
            search_handler
        )
    )

    app.add_handler(
        CommandHandler(
            "list",
            list_handler
        )
    )

    app.add_handler(
        CommandHandler(
            "fileid",
            get_file_id
        )
    )
    app.add_handler(
        addanime_handler
    )

    # =========================
    # INLINE QUERY HANDLER
    # =========================
    app.add_handler(
        InlineQueryHandler(
            inline_query
        )
    )

    # =========================
    # CALLBACK BUTTON HANDLER
    # =========================
    app.add_handler(
        CallbackQueryHandler(
            button_handler
        )
    )

    # =========================
    # ERROR HANDLER
    # =========================
    app.add_error_handler(
        error_handler
    )

    print("Bot is running...")

    # =========================
    # START BOT
    # =========================
    app.run_polling()


# =========================
# RUN BOT
# =========================
if __name__ == "__main__":
    main()