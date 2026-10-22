import argparse

from .replay import replay_scenario


def main():
    parser = argparse.ArgumentParser(
        description="Replay an elevator scenario."
    )

    parser.add_argument(
        "scenario",
        help="Path to scenario JSON file",
    )

    parser.add_argument(
        "--log",
        required=True,
        help="Path to output JSONL log",
    )

    args = parser.parse_args()

    replay_scenario(
        scenario_path=args.scenario,
        log_path=args.log,
    )


if __name__ == "__main__":
    main()