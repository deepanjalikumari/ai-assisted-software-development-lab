
def line_stats(path):
    """
    Read the file at `path` and return a tuple:
    (line count via splitlines(), total whitespace-separated words, longest line length in characters).

    Parameters
    ----------
    path : str
        Path to the text file.

    Returns
    -------
    tuple[int, int, int]
        (number of lines, total words, length of the longest line)
    """
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.splitlines()
    line_count = len(lines)

    # total words: split each line by whitespace and sum
    total_words = sum(len(line.split()) for line in lines)

    # longest line length (0 if file is empty)
    longest_line = max((len(line) for line in lines), default=0)

    return line_count, total_words, longest_line