import json
from pathlib import Path


class EventLogger:
    """
    Writes one JSON object per line.

    The assignment requires JSON Lines format.
    """

    def __init__(self, output_path: str):
        self.output_path = Path(output_path)

        # Make sure the parent directory exists.
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        # Start with a fresh log for every replay.
        self.output_path.write_text("")

    def log(self, event: dict):
        """
        Write one event as one JSON object on one line.
        """

        with self.output_path.open("a") as file:
            file.write(json.dumps(event, separators=(",", ":")) + "\n")

    def light_on_call(self, time: float, floor: int, direction: str):
        self.log(
            {
                "t": time,
                "event": "light_on",
                "button": "call",
                "floor": floor,
                "dir": direction,
            }
        )

    def light_off_call(self, time: float, floor: int, direction: str):
        self.log(
            {
                "t": time,
                "event": "light_off",
                "button": "call",
                "floor": floor,
                "dir": direction,
            }
        )

    def light_on_floor(self, time: float, elevator: int, floor: int):
        self.log(
            {
                "t": time,
                "event": "light_on",
                "button": "press",
                "elevator": elevator,
                "floor": floor,
            }
        )

    def light_off_floor(self, time: float, elevator: int, floor: int):
        self.log(
            {
                "t": time,
                "event": "light_off",
                "button": "press",
                "elevator": elevator,
                "floor": floor,
            }
        )

    def arrive(
        self,
        time: float,
        elevator: int,
        floor: int,
        direction: str,
    ):
        self.log(
            {
                "t": time,
                "elevator": elevator,
                "floor": floor,
                "dir": direction,
                "event": "arrive",
            }
        )

    def door_open(
        self,
        time: float,
        elevator: int,
        floor: int,
        direction: str,
    ):
        self.log(
            {
                "t": time,
                "elevator": elevator,
                "floor": floor,
                "dir": direction,
                "event": "door_open",
            }
        )

    def door_close(
        self,
        time: float,
        elevator: int,
        floor: int,
        direction: str,
    ):
        self.log(
            {
                "t": time,
                "elevator": elevator,
                "floor": floor,
                "dir": direction,
                "event": "door_close",
            }
        )