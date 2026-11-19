import re
import json


def generate_aliases(
    title: str
):

    aliases = set()

    title = title.lower()

    # Original
    aliases.add(title)

    # Remove spaces
    aliases.add(
        title.replace(" ", "")
    )

    # Remove punctuation
    clean = re.sub(
        r"[^a-z0-9 ]",
        "",
        title
    )

    aliases.add(clean)

    aliases.add(
        clean.replace(" ", "")
    )

    # Season replacements
    replacements = {
        "season 1": "s1",
        "season 2": "s2",
        "season 3": "s3",
        "season 4": "s4",
        "season 5": "s5"
    }

    for old, new in replacements.items():

        if old in title:

            aliases.add(
                title.replace(
                    old,
                    new
                )
            )

    # Acronym
    words = clean.split()

    if len(words) >= 2:

        acronym = "".join(
            word[0]
            for word in words
        )

        aliases.add(acronym)

    # Return JSON string
    return json.dumps(
        sorted(aliases)
    )