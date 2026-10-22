import json

from .logger import EventLogger
from .models import Direction
from .simulation import Simulation


def parse_direction(value: str) -> Direction:
    """Convert JSON direction to Direction enum."""

    if value == "up":
        return Direction.UP

    if value == "down":
        return Direction.DOWN

    raise ValueError(f"Invalid direction: {value}")


def load_scenario(path: str) -> dict:
    """Read and validate a scenario JSON file."""

    with open(path, "r") as file:
        scenario = json.load(file)

    floors = scenario.get("floors")
    elevators = scenario.get("elevators")
    events = scenario.get("events")

    if not isinstance(floors, int) or not 2 <= floors <= 20:
        raise ValueError("floors must be an integer from 2 to 20")

    if not isinstance(elevators, int) or not 1 <= elevators <= 4:
        raise ValueError("elevators must be an integer from 1 to 4")

    if not isinstance(events, list):
        raise ValueError("events must be a list")

    return scenario


def replay_scenario(
    scenario_path: str,
    log_path: str,
):
    """
    Replay a scenario using simulated time.
    """

    scenario = load_scenario(scenario_path)

    logger = EventLogger(log_path)

    simulation = Simulation(
        floors=scenario["floors"],
        elevator_count=scenario["elevators"],
        logger=logger,
    )

    # Scenario events must be processed in chronological order.
    events = sorted(
        scenario["events"],
        key=lambda event: event["t"],
    )

    for event in events:

        event_time = event["t"]

        if event_time < simulation.current_time:
            raise ValueError(
                "Scenario events must not occur in the past."
            )

        # Advance the simulation naturally until the event time.
        simulation.run_until(event_time)

        event_type = event["type"]

        if event_type == "call":

            direction = parse_direction(event["dir"])

            simulation.press_call_button(
                floor=event["floor"],
                direction=direction,
            )

        elif event_type == "press":

            simulation.press_floor_button(
                elevator_id=event["elevator"],
                floor=event["floor"],
            )

        elif event_type == "open":

            simulation.press_open_button(
                elevator_id=event["elevator"],
            )

        elif event_type == "close":

            simulation.press_close_button(
                elevator_id=event["elevator"],
            )

        else:
            raise ValueError(
                f"Unknown event type: {event_type}"
            )

    # After the final scenario event, finish all requests.
    simulation.run_until_idle()

    return simulation