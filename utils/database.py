import sqlite3


def get_db_connection():

    conn = sqlite3.connect("anime.db")

    conn.row_factory = sqlite3.Row

    return conn


def get_all_anime():

    conn = get_db_connection()

    anime_list = conn.execute(
        "SELECT * FROM anime"
    ).fetchall()

    conn.close()

    return anime_list


def get_anime_by_title(title):

    conn = get_db_connection()

    anime = conn.execute(
        "SELECT * FROM anime WHERE title = ?",
        (title,)
    ).fetchone()

    conn.close()

    if anime:
        return dict(anime)

    return None