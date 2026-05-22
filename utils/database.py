import sqlite3
import logging
from utils.aliases import (
    generate_aliases
)
logger = logging.getLogger(__name__)


# =========================
# DB CONNECTION
# =========================
def get_db_connection():

    conn = sqlite3.connect(
        "anime.db",
        timeout=10
    )

    conn.row_factory = sqlite3.Row

    return conn
# =========================
# GET ALL ANIME
# =========================
def get_all_anime():

    try:

        conn = get_db_connection()

        anime_list = conn.execute(
            "SELECT * FROM anime"
        ).fetchall()

        conn.close()

        return [dict(anime) for anime in anime_list]

    except Exception as e:

        logger.error(f"Database error: {e}")

        return []


# =========================
# GET ANIME BY ID
# =========================
def get_anime_by_id(anime_id: int):

    try:

        conn = get_db_connection()

        anime = conn.execute(
            "SELECT * FROM anime WHERE id = ?",
            (anime_id,)
        ).fetchone()

        conn.close()

        if anime:
            return dict(anime)

        return None

    except Exception as e:

        logger.error(f"Database error: {e}")

        return None
    
# =========================
# ADD ANIME
# =========================
def add_anime(
    title,
    link,
    photo_file_id,
    photo
):

    conn = None

    try:

        conn = get_db_connection()

        # Generate aliases automatically
        aliases = generate_aliases(
            title
        )

        conn.execute(
            """
            INSERT INTO anime (
                title,
                aliases,
                photo,
                link,
                photo_file_id
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                title,
                aliases,
                photo,
                link,
                photo_file_id
            )
        )

        conn.commit()

        logger.info(
            f"Added anime: {title}"
        )

    except Exception as e:

        logger.error(
            f"Failed to add anime: {e}"
        )

    finally:

        if conn:
            conn.close()