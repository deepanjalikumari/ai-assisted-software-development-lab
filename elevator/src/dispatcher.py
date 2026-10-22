from .models import Elevator, Direction, CallRequest


class Dispatcher:
    """
    Chooses which elevator should handle an outside call.
    """

    def __init__(self, elevators: list[Elevator], top_floor: int):
        self.elevators = elevators
        self.top_floor = top_floor

    def choose_elevator(self, call: CallRequest) -> Elevator:
        """
        Choose the most suitable elevator for a call.

        Priority:
        1. Elevator already moving toward the caller
           in the same direction.
        2. Idle elevator.
        3. Nearest remaining elevator.

        The caller's request is then assigned to that elevator.
        """

        suitable = []

        for elevator in self.elevators:
            if elevator.door.value != "closed":
                continue

            # Elevator is moving UP and caller is above it.
            if (
                elevator.direction == Direction.UP
                and call.direction == Direction.UP
                and call.floor >= elevator.floor
            ):
                distance = abs(call.floor - elevator.floor)
                suitable.append((0, distance, elevator.elevator_id, elevator))

            # Elevator is moving DOWN and caller is below it.
            elif (
                elevator.direction == Direction.DOWN
                and call.direction == Direction.DOWN
                and call.floor <= elevator.floor
            ):
                distance = abs(call.floor - elevator.floor)
                suitable.append((0, distance, elevator.elevator_id, elevator))

        if suitable:
            suitable.sort(key=lambda item: item[:3])
            return suitable[0][3]

        # Next preference: idle elevator.
        idle = [
            elevator
            for elevator in self.elevators
            if elevator.direction == Direction.IDLE
            and elevator.door.value == "closed"
        ]

        if idle:
            return min(
                idle,
                key=lambda elevator: (
                    abs(elevator.floor - call.floor),
                    elevator.elevator_id,
                ),
            )

        # Finally choose the nearest elevator.
        return min(
            self.elevators,
            key=lambda elevator: (
                abs(elevator.floor - call.floor),
                elevator.elevator_id,
            ),
        )