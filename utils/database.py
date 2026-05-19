import json

def load_anime_data():
    with open("anime_data.json", "r", encoding="utf-8") as file:
        return json.load(file)