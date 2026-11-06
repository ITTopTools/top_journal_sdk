def to_camel(string: str) -> str:
    """Преобразует snake_case в camelCase (поля API используют camelCase)."""
    words = string.split("_")
    return words[0] + "".join(word.capitalize() for word in words[1:])
