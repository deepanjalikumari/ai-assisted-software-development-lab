# Class 12 AI Log

## Part built

Built the elevator project in `elevator/`: a simulated-time lift scheduler, JSON scenario replay, event logging, a browser UI, and a checker for the seven safety rules. Added six scenarios and one isolated bad-log example for each rule.

## AI use

AI helped implement and debug the lift scheduler, including concurrent lift movement and direction-aware hall-call service. It also helped create the log-only checker, bad-log fixtures, one-command test runner, responsive UI, and README. I used the browser to try scenario replays and view lift positions, directions, doors, and button lights.

## Verification

Ran `python3 elevator/tests/run_all.py`. All six good scenarios passed the checker, and each bad log was rejected for exactly its intended rule. The scenarios cover hall calls, inside-floor requests, door reopening, calls during travel, and concurrent lifts.