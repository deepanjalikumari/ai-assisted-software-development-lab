#!/usr/bin/env python3
"""
CS437 Prompt Golf — scorer.

The game: you PROMPT an AI to write the function. Your score for a hole is
    prompt_tokens + solution_tokens
counted only if the solution passes every test. Lowest total across the holes wins.

Usage:
    python score.py <1|2|3|4> <your_prompt.txt> <the_ai_solution.py>

Everyone counts tokens with THIS script, so all groups are comparable. The
counter here approximates how language models tokenize (each word and each
punctuation mark is one token) — precise wording and short code both help.
"""
import re, sys, importlib.util, tempfile, os


def count_tokens(text):
    return len(re.findall(r"\w+|[^\w\s]", text))


def load(path):
    spec = importlib.util.spec_from_file_location("sol", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def check1(m):
    cases = [("hello", "olleh"), ("", ""), ("a", "a"), ("ab cd", "dc ba")]
    for s, want in cases:
        got = m.rev(s)
        if got != want:
            return f"rev({s!r}) returned {got!r}, expected {want!r}"
    return None


def check2(m):
    cases = [
        ("the cat the dog", "the"),
        ("a b b a", "a"),               # tie 2-2 -> first to appear
        ("Hello hello WORLD", "hello"), # lowercased
        ("one", "one"),
    ]
    for text, want in cases:
        got = m.top_word(text)
        if got != want:
            return f"top_word({text!r}) returned {got!r}, expected {want!r}"
    return None


def check3(m):
    content = "hello world\nfoo\n\nlongest line here now"
    fd, path = tempfile.mkstemp(suffix=".txt")
    try:
        with os.fdopen(fd, "w") as f:
            f.write(content)
        got = tuple(m.line_stats(path))
        want = (4, 7, 21)  # lines, words, longest-line length
        if got != want:
            return f"line_stats returned {got}, expected {want}"
    finally:
        os.remove(path)
    return None


def check4(m):
    cases = [
        ("# config\nname: Ada\nage: 36\n\ncity: London",
         {"name": "Ada", "age": 36, "city": "London"}),
        ("x: 5", {"x": 5}),
        ("# just a comment", {}),
        ("  key : value  ", {"key": "value"}),         # trimmed
        ("url: http://a.com:80", {"url": "http://a.com:80"}),  # split on first colon only
    ]
    for text, want in cases:
        got = m.parse_config(text)
        if got != want:
            return f"parse_config({text!r}) returned {got!r}, expected {want!r}"
    return None


CHECKS = {"1": check1, "2": check2, "3": check3, "4": check4}


def main():
    if len(sys.argv) != 4 or sys.argv[1] not in CHECKS:
        print(__doc__)
        sys.exit(1)
    hole, prompt_file, sol_file = sys.argv[1], sys.argv[2], sys.argv[3]
    prompt = open(prompt_file, encoding="utf-8").read()
    code = open(sol_file, encoding="utf-8").read()
    try:
        mod = load(sol_file)
    except Exception as e:
        print(f"✗ solution failed to import: {e}")
        sys.exit(1)
    err = CHECKS[hole](mod)
    if err:
        print(f"✗ FAIL — {err}")
        sys.exit(1)
    pt, ct = count_tokens(prompt), count_tokens(code)
    print(f"✓ PASS  hole {hole}")
    print(f"  prompt tokens : {pt}")
    print(f"  code tokens   : {ct}")
    print(f"  SCORE         : {pt + ct}   (lower is better)")


if __name__ == "__main__":
    main()
