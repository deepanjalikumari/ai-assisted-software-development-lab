def parse_config(text: str) -> dict:
    """
    Parse a simple key-value configuration string.

    - Blank lines and lines starting with '#' are ignored.
    - Each non‑comment line is split on the first ':'.
    - Both key and value are stripped of surrounding whitespace.
    - If the stripped value consists only of digits, it is converted to int;
      otherwise it remains a string.

    Args:
        text: The configuration text.

    Returns:
        A dictionary mapping keys to their parsed values (int or str).
    """
    config = {}
    for line in text.splitlines():
        stripped = line.strip()
        # Skip empty lines and comments
        if not stripped or stripped.startswith('#'):
            continue
        # Split on the first colon only
        if ':' not in stripped:
            continue  # or raise ValueError depending on desired strictness
        key, value = stripped.split(':', 1)
        key = key.strip()
        value = value.strip()
        # Convert digit‑only values to int
        if value.isdigit():
            value = int(value)
        config[key] = value
    return config
