# Week 03 AI Log

## Tool used
GitHub Copilot in VS Code with OpenRouter.

## Prompt given

1. Add two personas, a terse senior engineer and a Socratic tutor, using system prompts.
2. Display input tokens, output tokens, and a running session total.
3. Limit the conversation to a 4,000-token budget.
4. Add `calculator` and `read_file` tools and allow the model to chain tools.
5. Add `write_file` and `run_bash`, but ask for confirmation before running either dangerous tool.
6. Use the tools as a small coding agent: read `games/week-01/game.js`, then add a comment to it.

## What AI produced
The agent loop now supports selectable personas, live token accounting, context trimming, chained tools, and confirmation guardrails. It can read repository files and, after confirmation, write files or run shell commands.

## What I changed manually
I tested both personas with the same question and approved the file edit when prompted. I also corrected the `.env` format so it uses `OPENROUTER_API_KEY=...` and kept the API key out of commits.

## How I verified it
I ran module 03 with the senior and tutor personas. The senior gave a short direct answer, while the tutor asked guiding questions. I verified the tool schemas and local tool functions, saw token totals increase, tested the real `game.js` read, and confirmed that `write_file` asked for approval before editing.

## What I still do not understand
I want to understand how the model decides which tool to call, how tool results are represented in the conversation, and how the 4,000-token budget should summarise old messages instead of only removing them.
