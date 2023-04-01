"""Misc utils."""


def deslugify(slug: str) -> str:
    """De-slugify a string."""
    # Grab the last part of the path
    title = slug.split("/")[-1]

    # Remove common suffixes
    for suffix in (".html", ".htm", ".php"):
        title = title.removesuffix(suffix)

    # Replace common word separators with a space
    for char in ("-", "_"):
        title = title.replace(char, " ")

    # Capitalize first word
    title = title.capitalize()

    return title
