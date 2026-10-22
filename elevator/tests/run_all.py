import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROJECT_ROOT.parent
CHECKER = PROJECT_ROOT / "tests" / "check.py"


def run(*command):
    return subprocess.run(
        command,
        cwd=REPOSITORY_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def main():
    scenarios = sorted((PROJECT_ROOT / "scenarios").glob("*.json"))
    bad_logs = sorted((PROJECT_ROOT / "tests" / "bad-logs").glob("rule-*.jsonl"))

    if len(scenarios) < 3:
        print("Expected at least three scenario files.", file=sys.stderr)
        return 1
    if len(bad_logs) < 7:
        print("Expected at least one bad log for each of the seven rules.", file=sys.stderr)
        return 1

    with tempfile.TemporaryDirectory(prefix="elevator-logs-") as temporary_directory:
        log_directory = Path(temporary_directory)
        for scenario in scenarios:
            log_path = log_directory / f"{scenario.stem}.jsonl"
            replay = run(
                sys.executable,
                "-m",
                "elevator.src.main",
                str(scenario),
                "--log",
                str(log_path),
            )
            if replay.returncode != 0:
                print(f"FAIL replay {scenario.name}\n{replay.stdout}{replay.stderr}", file=sys.stderr)
                return 1

            if scenario.stem == "parallel-cars":
                events = [json.loads(line) for line in log_path.read_text().splitlines()]
                first_arrivals = {}
                for event in events:
                    if event.get("event") == "arrive":
                        first_arrivals.setdefault(event["elevator"], event["t"])
                if first_arrivals != {0: 2.0, 1: 2.0}:
                    print(
                        f"FAIL parallel car timing: expected both first arrivals at t=2, got {first_arrivals}",
                        file=sys.stderr,
                    )
                    return 1

            checked = run(sys.executable, str(CHECKER), str(scenario), str(log_path))
            if checked.returncode != 0:
                print(f"FAIL good scenario {scenario.name}\n{checked.stdout}{checked.stderr}", file=sys.stderr)
                return 1
            print(f"PASS scenario {scenario.name}")

    for bad_log in bad_logs:
        match = re.fullmatch(r"rule-(\d+)", bad_log.stem)
        if match is None:
            print(f"Invalid bad-log filename: {bad_log.name}", file=sys.stderr)
            return 1

        expected_rule = int(match.group(1))
        scenario = bad_log.with_name(f"{bad_log.stem}.scenario.json")
        if not scenario.is_file():
            print(f"Missing scenario for {bad_log.name}", file=sys.stderr)
            return 1

        checked = run(sys.executable, str(CHECKER), str(scenario), str(bad_log))
        reported_rules = {
            int(rule)
            for rule in re.findall(r"^rule (\d+) ", checked.stdout, re.MULTILINE)
        }
        if checked.returncode == 0 or reported_rules != {expected_rule}:
            print(
                f"FAIL bad log {bad_log.name}: expected only rule {expected_rule}\n"
                f"{checked.stdout}{checked.stderr}",
                file=sys.stderr,
            )
            return 1
        print(f"PASS catches rule {expected_rule} ({bad_log.name})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())