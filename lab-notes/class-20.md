Class 20 — Teach Your Agent

I

1. File I wrote
File: new-feature skill (.claude/skills/new-feature/SKILL.md) in our group's hackathon repo (cs437-9-hack, campus cab sharing).
Pull request: https://github.com/GellaNagaSaiKrishna/cs437-9-hack/pull/9

2. How I adapted it
I changed only names and commands to match our repo: statements are headings like "### S<N> — <title>" in SPEC.md, tests are classes named S<N>_<CamelCaseTitle> in tests/test_spec.py, and the test command is python3 -m unittest discover -s tests -v. My teammates had already merged spec-status and test-breaker, so new-feature was the file left.

3. Trial run
Request: "A student cannot create a slot whose pickup time is in the past."
The skill made the branch feature/S26-no-past-pickup, wrote S26 in SPEC.md and a test, then stopped at step 3 because the new test passed before any code change. It explained that Store.create_slot already refuses times within 15 minutes of the server clock, so this was a gap in the spec, not in the code.
It also noticed that a NaN pickup time slips past the check. I asked it to tighten S26. The new NaN and infinity tests failed first (sqlite3.IntegrityError), then it added a math.isfinite check in app/store.py. All 56 tests passed, /spec-status showed 26 green, and it made one commit. I did not push or merge that practice branch.

4. One thing Claude did wrong before I fixed the file
On the first trial, the statement Claude wrote (a slot cannot be created with a pickup time in the past) was already true in the code, so its test passed without any code change and the run stopped with no failing test. Claude had only restated an existing rule as a new statement, and it missed the real gap (a NaN pickup time) until it was asked. I fixed this by telling it to tighten S26 to cover past and non-finite times, which gave a real failing test first.
