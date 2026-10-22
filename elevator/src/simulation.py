from .models import (
    Elevator,
    Direction,
    DoorState,
    CallRequest,
    ButtonState,
)
from .dispatcher import Dispatcher
from .logger import EventLogger


FLOOR_TRAVEL_TIME = 2.0
DOOR_OPEN_TIME = 3.0


class Simulation:
    """
    Event-driven elevator simulation.

    Time is simulated. No wall-clock waiting is used.
    """

    def __init__(
        self,
        floors: int,
        elevator_count: int,
        logger: EventLogger,
    ):
        if not 2 <= floors <= 20:
            raise ValueError("Number of floors must be between 2 and 20.")

        if not 1 <= elevator_count <= 4:
            raise ValueError("Number of elevators must be between 1 and 4.")

        self.top_floor = floors - 1

        self.elevators = [
            Elevator(elevator_id=i)
            for i in range(elevator_count)
        ]

        self.buttons = ButtonState()

        self.dispatcher = Dispatcher(
            self.elevators,
            self.top_floor,
        )

        self.logger = logger

        self.current_time = 0.0

    # ---------------------------------------------------------
    # BUTTON PRESSES
    # ---------------------------------------------------------

    def press_floor_button(self, elevator_id: int, floor: int):
        """
        Press a floor button inside an elevator.
        """

        elevator = self.elevators[elevator_id]

        if not 0 <= floor <= self.top_floor:
            raise ValueError("Invalid floor.")

        # Rule 7:
        # A lit button cannot receive another light_on.
        if floor in elevator.floor_requests:
            return

        elevator.floor_requests.add(floor)

        self.buttons.floor_buttons.add(
            (elevator_id, floor)
        )

        self.logger.light_on_floor(
            self.current_time,
            elevator_id,
            floor,
        )
        self._update_direction(elevator)

    def press_call_button(
        self,
        floor: int,
        direction: Direction,
    ):
        """
        Press an outside Up/Down call button.
        """

        if not 0 <= floor <= self.top_floor:
            raise ValueError("Invalid floor.")

        if floor == 0 and direction == Direction.DOWN:
            raise ValueError("Ground floor has no DOWN button.")

        if floor == self.top_floor and direction == Direction.UP:
            raise ValueError("Top floor has no UP button.")

        call = CallRequest(floor, direction)

        # Rule 7:
        # A lit button cannot receive another light_on.
        if call in self.buttons.call_buttons:
            return

        self.buttons.call_buttons.add(call)

        self.logger.light_on_call(
            self.current_time,
            floor,
            direction.value,
        )

        # Assign this call to exactly one elevator.
        elevator = self.dispatcher.choose_elevator(call)

        self._assign_call(elevator, call)

    # ---------------------------------------------------------
    # REQUEST ASSIGNMENT
    # ---------------------------------------------------------

    def _assign_call(
        self,
        elevator: Elevator,
        call: CallRequest,
    ):
        """
        Assign an outside call to one elevator.

        We represent the assigned call internally using a floor request.
        The original call remains lit until that elevator serves it.
        """

        elevator.call_requests.add(call)

        self._update_direction(elevator)

    # ---------------------------------------------------------
    # DIRECTION
    # ---------------------------------------------------------

    def _update_direction(self, elevator: Elevator):
        """
        Decide which direction the elevator should travel.

        Both inside floor requests and assigned outside calls
        are treated as pending stops.
        """

        if elevator.next_arrival_time is not None:
            return

        pending_floors = set(elevator.floor_requests)

        pending_floors.update(
            call.floor for call in elevator.call_requests
        )

        if not pending_floors:
            elevator.direction = Direction.IDLE
            return

        current = elevator.floor

        above = [
            floor for floor in pending_floors
            if floor > current
        ]

        below = [
            floor for floor in pending_floors
            if floor < current
        ]

        if elevator.direction == Direction.UP:
            if above:
                self._schedule_movement(elevator)
                return

            if below:
                elevator.direction = Direction.DOWN
                self._schedule_movement(elevator)
                return

        elif elevator.direction == Direction.DOWN:
            if below:
                self._schedule_movement(elevator)
                return

            if above:
                elevator.direction = Direction.UP
                self._schedule_movement(elevator)
                return

        # Elevator is idle or has no request in its
        # current direction.
        if above:
            elevator.direction = Direction.UP
        elif below:
            elevator.direction = Direction.DOWN
        else:
            elevator.direction = Direction.IDLE

        self._schedule_movement(elevator)

    def _schedule_movement(self, elevator: Elevator):
        if (
            elevator.door == DoorState.CLOSED
            and elevator.direction != Direction.IDLE
            and elevator.next_arrival_time is None
        ):
            elevator.next_arrival_time = self.current_time + FLOOR_TRAVEL_TIME

    # ---------------------------------------------------------
    # SERVING A FLOOR
    # ---------------------------------------------------------

    def open_doors(self, elevator: Elevator):
        """
        Open doors at the elevator's current floor.
        """

        if elevator.door == DoorState.OPEN:
            return

        elevator.door = DoorState.OPEN
        elevator.next_arrival_time = None
        elevator.door_close_time = (
            self.current_time + DOOR_OPEN_TIME
        )

        self.logger.door_open(
            self.current_time,
            elevator.elevator_id,
            elevator.floor,
            elevator.direction.value,
        )

    def close_doors(self, elevator: Elevator):
        """
        Close doors immediately.
        """

        if elevator.door == DoorState.CLOSED:
            return

        elevator.door = DoorState.CLOSED
        elevator.door_close_time = None

        self.logger.door_close(
            self.current_time,
            elevator.elevator_id,
            elevator.floor,
            elevator.direction.value,
        )
        self._schedule_movement(elevator)

    def serve_current_floor(self, elevator: Elevator):
        """
        Serve requests assigned to this elevator at its current floor.
        """

        floor = elevator.floor

        # -------------------------------------------------
        # Inside floor button
        # -------------------------------------------------

        if floor in elevator.floor_requests:

            self.logger.light_off_floor(
                self.current_time,
                elevator.elevator_id,
                floor,
            )

            self.buttons.floor_buttons.discard(
                (elevator.elevator_id, floor)
            )

            elevator.floor_requests.discard(floor)

        # -------------------------------------------------
        # Outside call assigned to this elevator
        # -------------------------------------------------

        calls_to_serve = [
            call
            for call in elevator.call_requests
            if call.floor == floor
            and self._call_matches_direction(
                elevator,
                call,
            )
        ]

        for call in calls_to_serve:

            self.logger.light_off_call(
                self.current_time,
                call.floor,
                call.direction.value,
            )

            self.buttons.call_buttons.discard(call)
            elevator.call_requests.discard(call)

        # Recalculate the next direction after serving.
        self._update_direction(elevator)

    def _handle_current_floor(self, elevator: Elevator):
        """Open for a request here only when the lift can serve it legally."""
        floor = elevator.floor
        calls_here = [
            call for call in elevator.call_requests if call.floor == floor
        ]
        has_floor_request = floor in elevator.floor_requests
        has_matching_call = any(
            self._call_matches_direction(elevator, call)
            for call in calls_here
        )

        if has_floor_request or has_matching_call:
            self.open_doors(elevator)
            self.serve_current_floor(elevator)
            return

        if not calls_here or elevator.direction == Direction.IDLE:
            return

        pending_floors = set(elevator.floor_requests)
        pending_floors.update(call.floor for call in elevator.call_requests)
        if elevator.direction == Direction.UP:
            has_stops_ahead = any(requested_floor > floor for requested_floor in pending_floors)
        else:
            has_stops_ahead = any(requested_floor < floor for requested_floor in pending_floors)

        if not has_stops_ahead:
            elevator.direction = calls_here[0].direction
            self.open_doors(elevator)
            self.serve_current_floor(elevator)

    def _call_matches_direction(
        self,
        elevator: Elevator,
        call: CallRequest,
    ) -> bool:
        """
        A call is served only when the elevator leaves
        the floor in the requested direction.

        If the elevator is idle at the floor, it can serve
        either direction.
        """

        if elevator.direction == Direction.IDLE:
            return True

        return elevator.direction == call.direction

    # ---------------------------------------------------------
    # ONE-FLOOR MOVEMENT
    # ---------------------------------------------------------

    def move_one_floor(self, elevator: Elevator):
        """
        Move an elevator exactly one floor.

        Travel time is always 2 simulated seconds.
        """

        if elevator.door != DoorState.CLOSED:
            raise RuntimeError("Safety violation: elevator moved with open door.")
        if elevator.direction == Direction.IDLE:
            return

        self.current_time += FLOOR_TRAVEL_TIME
        elevator.next_arrival_time = None
        self._move_at_current_time(elevator)

    # ---------------------------------------------------------
    # SIMULATION LOOP
    # ---------------------------------------------------------

    def run_until(self, target_time: float):
        """
        Advance the simulation until target_time.

        The simulation never jumps beyond target_time.
        """

        if target_time < self.current_time:
            raise ValueError(
                "Cannot run simulation backwards."
            )

        while True:
            self._serve_requests_at_current_floors()
            if not self._advance_one_event(target_time):
                return

    def _move_at_current_time(self, elevator: Elevator):
        """
        Move one floor at the current simulated time.
        """

        if elevator.door != DoorState.CLOSED:
            raise RuntimeError(
                "Safety violation: elevator moved with open door."
            )

        elevator.next_arrival_time = None

        if elevator.direction == Direction.IDLE:
            return

        if elevator.direction == Direction.UP:
            next_floor = elevator.floor + 1
        else:
            next_floor = elevator.floor - 1

        if not 0 <= next_floor <= self.top_floor:
            raise RuntimeError(
                "Safety violation: elevator exceeded floor bounds."
            )

        elevator.floor = next_floor

        self.logger.arrive(
            self.current_time,
            elevator.elevator_id,
            elevator.floor,
            elevator.direction.value,
        )
        self._handle_current_floor(elevator)
        if elevator.door == DoorState.CLOSED:
            self._update_direction(elevator)
            self._schedule_movement(elevator)

    def _serve_requests_at_current_floors(self):
        for elevator in self.elevators:
            if elevator.door != DoorState.CLOSED:
                continue
            if (
                elevator.floor in elevator.floor_requests
                or any(call.floor == elevator.floor for call in elevator.call_requests)
            ):
                self._handle_current_floor(elevator)

    def _advance_one_event(self, deadline: float) -> bool:
        event_times = []
        for elevator in self.elevators:
            self._schedule_movement(elevator)
            if elevator.door_close_time is not None:
                event_times.append(elevator.door_close_time)
            if elevator.next_arrival_time is not None:
                event_times.append(elevator.next_arrival_time)

        if not event_times or min(event_times) > deadline:
            self.current_time = deadline
            return False

        self.current_time = min(event_times)

        for elevator in self.elevators:
            if (
                elevator.door == DoorState.OPEN
                and elevator.door_close_time == self.current_time
            ):
                self.close_doors(elevator)

        for elevator in self.elevators:
            if elevator.next_arrival_time == self.current_time:
                self._move_at_current_time(elevator)

        return True

    def run_until_idle(self, max_time: float = 3600.0):
        """
        Run the simulation until:

        1. Every button is off.
        2. Every elevator is idle.
        3. Every elevator has closed doors.

        Or until max_time is reached.
        """

        while self.current_time <= max_time:
            self._serve_requests_at_current_floors()
            if self.is_idle():
                return
            if not self._advance_one_event(max_time):
                break

        raise RuntimeError("Simulation exceeded 3600 seconds.")

    def is_idle(self) -> bool:
        """
        Return True only when the complete system is finished.
        """

        if self.buttons.call_buttons:
            return False

        if self.buttons.floor_buttons:
            return False

        for elevator in self.elevators:

            if elevator.floor_requests:
                return False

            if elevator.direction != Direction.IDLE:
                return False

            if elevator.next_arrival_time is not None:
                return False

            if elevator.door != DoorState.CLOSED:
                return False

        return True

    # ---------------------------------------------------------
    # MANUAL DOOR BUTTONS
    # ---------------------------------------------------------

    def press_open_button(self, elevator_id: int):
        """
        Press the OPEN button.

        If the door is closing, reopen it.
        If already open, reset the automatic close timer.
        """

        elevator = self.elevators[elevator_id]

        # Doors can only be operated while the elevator
        # is stationary at a floor.
        if elevator.direction != Direction.IDLE:
            return

        if elevator.door == DoorState.OPEN:
            elevator.door_close_time = (
                self.current_time + DOOR_OPEN_TIME
            )
            return

        self.open_doors(elevator)

    def press_close_button(self, elevator_id: int):
        """
        Press the CLOSE button.

        The doors close immediately.
        """

        elevator = self.elevators[elevator_id]

        if elevator.door == DoorState.OPEN:
            self.close_doors(elevator)