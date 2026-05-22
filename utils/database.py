import sqlite3
import logging

logger = logging.getLogger(__name__)


# =========================
# DB CONNECTION
# =========================
def get_db_connection():

    conn = sqlite3.connect("anime.db")

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