from utils.database import load_anime_data

anime_data = load_anime_data()

async def button_callback(update, context):
    query = update.callback_query
    await query.answer()

    anime_title = query.data

    anime = next(
        (
            a for a in anime_data
            if a["title"] == anime_title
        ),
        None
    )

    if not anime:
        return

    caption = f"""
🐥 {anime['title']} | MM Subbed |

Genres - {anime['genres']}
Studio - {anime['studio']}
Episodes - {anime['episodes']}

🔗 Link Collection:
{anime['link']}
"""

    with open(anime["photo"], "rb") as photo:
        await query.message.reply_photo(
            photo=photo,
            caption=caption
        )