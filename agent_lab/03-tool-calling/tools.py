import datetime
import ast
import operator
from pathlib import Path
import subprocess
import urllib.parse
import urllib.request
import zoneinfo


# 1. Tool implementations
def get_current_time(city: str) -> str:
    """Get current date and time for a given city using Python stdlib."""
    normalized = city.strip().replace(" ", "_").lower()
    tz_name = next(
        (tz for tz in zoneinfo.available_timezones() if normalized in tz.lower()),
        "UTC",
    )
    now = datetime.datetime.now(zoneinfo.ZoneInfo(tz_name))
    return now.strftime(f"%Y-%m-%d %H:%M:%S ({tz_name})")


def get_current_weather(city: str) -> str:
    """Get current weather conditions for a city using wttr.in."""
    encoded_city = urllib.parse.quote(city.strip())
    url = f"https://wttr.in/{encoded_city}?format=%l:+%C+%t,+humidity+%h"
    req = urllib.request.Request(url, headers={"User-Agent": "curl/7.68.0"})
    with urllib.request.urlopen(req, timeout=5) as response:
        return response.read().decode("utf-8").strip()


def calculator(expression: str) -> str:
    """Evaluate a basic arithmetic expression without executing arbitrary code."""
    operations = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
    }

    def evaluate(node: ast.AST) -> float:
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in operations:
            return operations[type(node.op)](evaluate(node.left), evaluate(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in operations:
            return operations[type(node.op)](evaluate(node.operand))
        raise ValueError("Only basic arithmetic is allowed")

    return str(evaluate(ast.parse(expression, mode="eval")))


def read_file(path: str) -> str:
    """Read a UTF-8 text file inside the repository."""
    repository_root = Path(__file__).resolve().parents[2]
    requested_path = (repository_root / path).resolve()
    if repository_root not in requested_path.parents:
        raise ValueError("Path must stay inside the repository")
    return requested_path.read_text(encoding="utf-8")


def _repository_path(path: str) -> Path:
    repository_root = Path(__file__).resolve().parents[2]
    requested_path = (repository_root / path).resolve()
    if repository_root not in requested_path.parents:
        raise ValueError("Path must stay inside the repository")
    return requested_path


def write_file(path: str, content: str) -> str:
    """Write UTF-8 text to a file inside the repository."""
    requested_path = _repository_path(path)
    requested_path.write_text(content, encoding="utf-8")
    return f"Wrote {path}"


def run_bash(command: str) -> str:
    """Run a shell command from the repository root."""
    repository_root = Path(__file__).resolve().parents[2]
    result = subprocess.run(
        command,
        cwd=repository_root,
        shell=True,
        capture_output=True,
        text=True,
        timeout=30,
    )
    output = result.stdout + result.stderr
    return f"Exit code: {result.returncode}\n{output}".strip()


# 2. Tool dispatch registry mapping function names to callable Python functions
AVAILABLE_TOOLS = {
    "get_current_time": get_current_time,
    "get_current_weather": get_current_weather,
    "calculator": calculator,
    "read_file": read_file,
    "write_file": write_file,
    "run_bash": run_bash,
}

# 3. OpenAI-compatible tool definitions schema exposed to the model
TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current date and time for a given city or timezone.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name (e.g. Tokyo, London, New York, Kolkata)",
                    }
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get current weather conditions for a given city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name (e.g. Paris, Tokyo, Gandhinagar)",
                    }
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Calculate a basic arithmetic expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Arithmetic expression using numbers and +, -, *, /, %, or **",
                    }
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a UTF-8 text file using a path relative to the repository root.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Repository-relative path such as agent_lab/03-tool-calling/README.md",
                    }
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write UTF-8 text to a repository-relative file. Always ask the user for confirmation first.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Repository-relative file path"},
                    "content": {"type": "string", "description": "Complete file content to write"},
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_bash",
            "description": "Run a shell command in the repository. Always ask the user for confirmation first.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "Shell command to run"},
                },
                "required": ["command"],
            },
        },
    },
]
