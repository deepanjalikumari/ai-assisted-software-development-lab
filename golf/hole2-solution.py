
def top_word(text):
    words = text.lower().split()
    if not words:
        return None
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    max_count = 0
    best_word = None
    for w in words:
        if freq[w] > max_count:
            max_count = freq[w]
            best_word = w
    return best_word