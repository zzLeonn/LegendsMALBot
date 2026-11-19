import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

admin_id = os.getenv("ADMIN_IDS")

if BOT_TOKEN is None:
    raise ValueError(
        "BOT_TOKEN not found in .env"
    )

if admin_id is None:
    raise ValueError(
        "ADMIN_IDS not found in .env"
    )

ADMIN_IDS = [
    int(admin_id)
]

BOT_TOKEN = str(BOT_TOKEN)