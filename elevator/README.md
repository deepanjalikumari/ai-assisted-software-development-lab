# Elevator Bank

Supports 2–20 floors and 1–4 lifts. All movement and door timing uses simulated time.

## Run

Start the UI: `python3 -m elevator.src.web` (open http://127.0.0.1:8000).

Replay and check every scenario, including all seven bad logs: `python3 elevator/tests/run_all.py`.

## Dispatch And Service

Good service means low passenger wait, measured from each call's `light_on` to its matching `light_off`; compare mean and maximum wait. Assign calls first to a car moving toward the caller in the requested direction, then the nearest idle car, then the nearest car. Ties go to the lower lift number. Cars serve stops ahead before reversing.

Scenarios each include a `description` stating what they test. The checker uses only scenario and log files.
