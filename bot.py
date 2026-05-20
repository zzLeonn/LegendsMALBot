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