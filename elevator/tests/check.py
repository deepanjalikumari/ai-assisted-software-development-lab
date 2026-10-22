import argparse
import json
from collections import defaultdict
from pathlib import Path


def _button_key(event):
	if event.get("button") == "call":
		return ("call", event.get("floor"), event.get("dir"))
	if event.get("button") == "press":
		return ("press", event.get("elevator"), event.get("floor"))
	return None


def check_log(scenario_path, log_path):
	scenario = json.loads(Path(scenario_path).read_text())
	top_floor = scenario["floors"] - 1
	records = []
	violations = []

	for line_number, line in enumerate(Path(log_path).read_text().splitlines(), 1):
		try:
			event = json.loads(line)
		except json.JSONDecodeError as error:
			raise ValueError(f"invalid JSON on log line {line_number}: {error}") from error
		records.append((line_number, event))

	def report(rule, line_number, event, message):
		event_time = event.get("t", "?")
		violations.append(
			f"rule {rule} at t={event_time} line {line_number}: {message}"
		)

	serving_elevator = {}
	for index, (_, event) in enumerate(records):
		if event.get("event") != "light_off" or event.get("button") != "call":
			continue
		call_key = _button_key(event)
		for _, candidate in reversed(records[:index]):
			if (
				candidate.get("event") == "door_open"
				and candidate.get("floor") == event.get("floor")
				and candidate.get("t") == event.get("t")
				and candidate.get("dir") in (event.get("dir"), "idle")
			):
				serving_elevator[call_key] = candidate.get("elevator")
				break

	active_buttons = {}
	open_events = []
	open_doors = {}
	previous_directions = {}
	pending_calls = set()
	pending_floor_buttons = defaultdict(set)
	served_elevators = defaultdict(set)

	for line_number, event in records:
		event_type = event.get("event")
		floor = event.get("floor")
		elevator = event.get("elevator")

		if isinstance(floor, int) and not 0 <= floor <= top_floor:
			report(2, line_number, event, f"floor {floor} is outside 0..{top_floor}")

		if event_type in ("light_on", "light_off"):
			key = _button_key(event)
			if key is None:
				continue

			if event_type == "light_on":
				if key in active_buttons:
					report(7, line_number, event, "button received a second light_on before light_off")
					continue
				active_buttons[key] = (line_number, event)
				if key[0] == "call":
					pending_calls.add(key)
				else:
					pending_floor_buttons[key[1]].add(key[2])
				continue

			if key not in active_buttons:
				report(7, line_number, event, "light_off has no matching lit button")
				continue

			if key[0] == "press":
				matching_open = any(
					open_elevator == key[1]
					and open_floor == key[2]
					and open_time == event.get("t")
					and open_line > active_buttons[key][0]
					for open_elevator, open_floor, open_time, _, open_line in open_events
				)
			else:
				matching_open = any(
					open_floor == key[1]
					and open_time == event.get("t")
					and open_direction in (key[2], "idle")
					and open_line > active_buttons[key][0]
					for _, open_floor, open_time, open_direction, open_line in open_events
				)

			if not matching_open:
				report(7, line_number, event, "light_off is not paired with a qualifying door_open at the same time")

			del active_buttons[key]
			if key[0] == "call":
				pending_calls.discard(key)
			else:
				pending_floor_buttons[key[1]].discard(key[2])
			continue

		if event_type == "arrive" and elevator in open_doors:
			report(1, line_number, event, f"elevator {elevator} arrived while its doors were open")

		if event_type == "door_open":
			if elevator in open_doors:
				continue

			open_doors[elevator] = (floor, event.get("t"))
			open_events.append((elevator, floor, event.get("t"), event.get("dir"), line_number))
			direction = event.get("dir")
			has_floor_request = floor in pending_floor_buttons[elevator]
			has_call_request = any(
				call_floor == floor and call_direction == direction
				for _, call_floor, call_direction in pending_calls
			)
			if direction != "idle" and not has_floor_request and not has_call_request:
				report(5, line_number, event, "doors opened without a matching request")

			for call_key in pending_calls:
				if call_key[1] == floor and call_key[2] == direction:
					served_elevators[call_key].add(elevator)
					if len(served_elevators[call_key]) > 1:
						report(6, line_number, event, "more than one elevator opened for this lit call")

		elif event_type == "door_close":
			open_doors.pop(elevator, None)

		direction = event.get("dir")
		if event_type in ("arrive", "door_open", "door_close") and direction in ("up", "down"):
			previous = previous_directions.get(elevator)
			if previous is not None and previous[0] != direction:
				old_direction, old_floor = previous
				reversal_floor = floor if floor is not None else old_floor
				if old_direction == "up":
					has_ahead_floor_button = any(
						requested_floor > reversal_floor
						for requested_floor in pending_floor_buttons[elevator]
					)
					has_ahead_call = any(
						call_key[1] > reversal_floor
						and serving_elevator.get(call_key) == elevator
						for call_key in pending_calls
					)
				else:
					has_ahead_floor_button = any(
						requested_floor < reversal_floor
						for requested_floor in pending_floor_buttons[elevator]
					)
					has_ahead_call = any(
						call_key[1] < reversal_floor
						and serving_elevator.get(call_key) == elevator
						for call_key in pending_calls
					)
				if has_ahead_floor_button or has_ahead_call:
					report(4, line_number, event, f"elevator {elevator} reversed with a request still ahead")
			previous_directions[elevator] = (direction, floor)

	for key, (line_number, event) in active_buttons.items():
		report(3, line_number, event, f"{key[0]} button is still lit at end of log")

	return violations


def main():
	parser = argparse.ArgumentParser(description="Check an elevator JSONL log against the seven rules.")
	parser.add_argument("scenario", help="Scenario JSON file")
	parser.add_argument("log", help="Elevator JSONL log")
	args = parser.parse_args()

	try:
		violations = check_log(args.scenario, args.log)
	except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
		parser.error(str(error))

	if violations:
		print("\n".join(violations))
		return 1

	print("No rule violations.")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
