import logging
from pathlib import Path
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


# Create logs folder
Path("logs").mkdir(
    exist_ok=True
)

# Logging setup
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

def main():

    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

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
        InlineQueryHandler(
            inline_query
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            button_handler
        )
    )

    print("Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()