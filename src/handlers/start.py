from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    ContextTypes
)


async def start_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return

    caption = """
🌟 Legends MAL Anime Search Bot 🌟

🇲🇲 မြန်မာ

ဒီ Bot လေးက Legends Anime MM Subbed Channel ထဲမှာ တင်ထားတဲ့ Anime တွေကို အလွယ်တကူ ရှာဖွေပေးနိုင်ပါတယ်။

🔍 Anime Name ရိုက်ပြီး ချက်ချင်းရှာနိုင်ပါတယ်။

📌 Features
• Anime Link Collection များ
• Movies & Seasons များ
• MM Subbed Anime များ
• @LegendsMALbot ကို Mention ခေါ်ပြီး Anime Link တွေကို ဘယ် Chat မှာမဆို Share လုပ်နိုင်ပါတယ်။

📌 Commands
/search anime name
→ Anime ရှာရန်

━━━━━━━━━━━━━━

🇬🇧 English

This bot helps you quickly search anime currently uploaded in Legends Anime MM Subbed channel.

✨ Features
• Anime Link Collections
• Movies & Seasons
• MM Subbed Anime
• Mention @LegendsMALbot in any chat to instantly share anime links with others.

📌 Commands
/search anime name
→ Search anime instantly

━━━━━━━━━━━━━━

Main Channel
https://t.me/+EyIDvbx2mkNhNWE1

Review Channel
https://t.me/+dKZL1b8ZWMU5ZjBl

✨ Enjoy Watching Anime ✨
"""

    keyboard = [
        [
            InlineKeyboardButton(
                "🔍 Search Anime",
                switch_inline_query_current_chat=""
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(
        keyboard
    )

    from pathlib import Path

    banner_path = Path(__file__).resolve().parents[2] / "assets" / "images" / "start_banner.jpg"

    with open(banner_path, "rb") as photo:

        await update.message.reply_photo(
            photo=photo,
            caption=caption,
            reply_markup=reply_markup
        )