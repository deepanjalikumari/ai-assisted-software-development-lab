# Class 13 AI Log

## I

I implemented Group 9's Fire mode in the Saab lift project. The event-driven simulation, cabin request sets, door timers, log checker, and test runner helped me work within the existing design.

What was missing: The simulator had no Fire or reset behavior. It continued to accept requests and used pending requests to decide where lifts stopped. The checker also assumed lights turn off only when a lift serves a request, and that every stop must be justified by a request.

What I did: I added Fire and reset handling, cleared lights and requests, sent lifts to floor 0 without intermediate stops, kept the ground-floor doors open until reset, and restored lifts to idle at floor 0. I updated the checker for the Fire-specific rule exceptions, added two scenarios and test coverage, updated the dashboard and README, and opened PR #12 without merging it. The unified test command passed.

What got in my way: The existing checker rules for request service and justified stops conflicted with Fire mode, so I needed to make those exceptions apply only between Fire and reset.
