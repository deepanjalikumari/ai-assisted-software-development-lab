import argparse
import json
import tempfile
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from .replay import replay_scenario


PROJECT_ROOT = Path(__file__).resolve().parents[1]
UI_ROOT = PROJECT_ROOT / "ui"


class ElevatorRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(UI_ROOT), **kwargs)

    def do_GET(self):
        if urlparse(self.path).path == "/api/scenarios":
            scenarios = []
            for path in sorted((PROJECT_ROOT / "scenarios").glob("*.json")):
                scenario = json.loads(path.read_text())
                scenarios.append(
                    {
                        "file": path.name,
                        "description": scenario.get("description", path.stem),
                        "scenario": scenario,
                    }
                )
            self._send_json({"scenarios": scenarios})
            return

        super().do_GET()

    def do_POST(self):
        if urlparse(self.path).path != "/api/replay":
            self.send_error(404)
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            if not 0 < content_length <= 1_000_000:
                raise ValueError("Request body must be between 1 byte and 1 MB.")
            scenario = json.loads(self.rfile.read(content_length))
            with tempfile.TemporaryDirectory(prefix="elevator-web-") as directory:
                scenario_path = Path(directory) / "scenario.json"
                log_path = Path(directory) / "events.jsonl"
                scenario_path.write_text(json.dumps(scenario))
                replay_scenario(str(scenario_path), str(log_path))
                events = [
                    json.loads(line)
                    for line in log_path.read_text().splitlines()
                ]
            self._send_json({"events": events})
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
            self.send_error(400, str(error))
        except RuntimeError as error:
            self.send_error(422, str(error))

    def _send_json(self, payload):
        encoded = json.dumps(payload).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


def main():
    parser = argparse.ArgumentParser(description="Run the elevator simulator web UI.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), ElevatorRequestHandler)
    print(f"Elevator UI: http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()