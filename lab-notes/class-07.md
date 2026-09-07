# Week 01 AI Log

## Tool used

OpenRouter — `google/gemma-4-26b-a4b-it:free`

## Prompt given

### Hole 1

Write only Python function rev(s) returning s reversed.

### Hole 2

Write only top_word(text): lowercase whitespace-split words, return most frequent; ties go to earliest occurrence.

### Hole 3

Write only line_stats(path): read path and return (line count via splitlines(), total whitespace words, longest line length).

### Hole 4

Write only parse_config(text): skip blank/# lines; split each line on first ':'; strip key/value; digit-only values become int, others stay strings.

## What AI produced

The AI generated the Python functions for all four holes. All four solutions passed the hidden tests.

## What I changed manually

I did not manually modify the generated solutions. I saved the code produced by the AI and used it for scoring.

## How I verified it

I used `score.py` to run the hidden tests and calculate the prompt + code token score.

* Hole 1: **29**
* Hole 2: **100**
* Hole 3: **227**
* Hole 4: **270**

All four holes passed.

## What I still do not understand

I need to understand how the tokenization used by `score.py` affects the final score and how to write shorter prompts that still reliably produce correct code.

# Class 07 — Prompt Golf

## Hole 1 — Reverse

**Best prompt:**
Write only Python function rev(s) returning s reversed.

**Score:** 29

**What I cut:**
Kept the prompt short while specifying the required function.

**AI use:**
Typist — AI generated the function from my prompt.

## Hole 2 — Top Word

**Best prompt:**
Write only top_word(text): lowercase whitespace-split words, return most frequent; ties go to earliest occurrence.

**Score:** 100

**What I cut:**
Specified only the essential rules needed to pass the hidden tests.

**AI use:**
Typist — AI generated the function from my prompt.

## Hole 3 — Line Stats

**Best prompt:**
Write only line_stats(path): read path and return (line count via splitlines(), total whitespace words, longest line length).

**Score:** 227

**What I cut:**
Kept the file-reading and required statistics rules concise.

**AI use:**
Typist — AI generated the function from my prompt.

## Hole 4 — Parse Config

**Best prompt:**
Write only parse_config(text): skip blank/# lines; split each line on first ':'; strip key/value; digit-only values become int, others stay strings.

**Score:** 270

**What I cut:**
Combined all parsing rules into one concise prompt.

**AI use:**
Typist — AI generated the function from my prompt.
