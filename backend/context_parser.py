import re

KNOWN_ENTITIES = ["dolphins", "lakers", "india", "python"]


def parse_context(password):
    entities = [w for w in KNOWN_ENTITIES if w.lower() in password.lower()]
    year_match = re.search(r'(19|20)\d{2}', password)
    year = int(year_match.group()) if year_match else None
    return {"entities": entities, "year": year}
