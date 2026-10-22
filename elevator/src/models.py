from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Set, Optional


class Direction(Enum):
    UP = "up"
    DOWN = "down"
    IDLE = "idle"


class DoorState(Enum):
    OPEN = "open"
    CLOSED = "closed"


@dataclass
class Elevator:
    elevator_id: int
    floor: int = 0
    direction: Direction = Direction.IDLE
    door: DoorState = DoorState.CLOSED

    # Floor buttons pressed inside this elevator
    floor_requests: Set[int] = field(default_factory=set)
    call_requests: Set[CallRequest] = field(default_factory=set)

    # Time at which the elevator's doors should close automatically
    door_close_time: Optional[float] = None
    next_arrival_time: Optional[float] = None


@dataclass(frozen=True)
class CallRequest:
    floor: int
    direction: Direction


@dataclass
class ScenarioEvent:
    time: float
    event_type: str
    floor: Optional[int] = None
    direction: Optional[Direction] = None
    elevator_id: Optional[int] = None


@dataclass
class ButtonState:
    """
    Stores all currently lit buttons.

    Call buttons:
        (floor, direction)

    Floor buttons:
        (elevator_id, floor)
    """

    call_buttons: Set[CallRequest] = field(default_factory=set)

    floor_buttons: Set[tuple[int, int]] = field(default_factory=set)