import json
import os
from pathlib import Path
import re
import urllib.request
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract

SCRIPT_DIR = Path(__file__).resolve().parent
HACKATTIC_DIR = SCRIPT_DIR.parent
BASE_URL = "https://hackattic.com/challenges/visual_basic_math"


def get_token():
    token = os.environ.get("HACKATTIC_TOKEN")
    if token:
        return token

    env_path = HACKATTIC_DIR / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            name, separator, value = line.partition("=")
            if separator and name.strip() == "HACKATTIC_TOKEN":
                return value.strip().strip('"').strip("'")

    raise RuntimeError(
        "HACKATTIC_TOKEN was not found. Add it to hackattic/.env."
    )


def get_problem():
    token = get_token()
    url = f"{BASE_URL}/problem?access_token={token}"
    with urllib.request.urlopen(url) as response:
        return json.loads(response.read().decode())


def download_image(image_url):
    path = SCRIPT_DIR / "math_problem.png"
    urllib.request.urlretrieve(image_url, path)
    print(f"OCR image saved at: {path}")
    return path


def read_image(path):
    image = Image.open(path).convert("L")
    pixels = image.load()
    bands = []
    in_band = False
    for y in range(image.height):
        has_ink = any(pixels[x, y] < 245 for x in range(image.width))
        if has_ink and not in_band:
            start = y
            in_band = True
        elif not has_ink and in_band:
            bands.append((start, y))
            in_band = False
    if in_band:
        bands.append((start, image.height))

    if len(bands) != 8:
        raise ValueError(f"Expected 8 image rows, detected {len(bands)}")

    rows = []
    for start, end in bands:
        top = max(0, start - 4)
        bottom = min(image.height, end + 4)
        row = image.crop((0, top, image.width, bottom))
        row = row.resize((row.width * 4, row.height * 4), Image.Resampling.LANCZOS)
        row = ImageEnhance.Contrast(row).enhance(2).filter(ImageFilter.SHARPEN)
        rows.append(
            pytesseract.image_to_string(
                row,
                config="--psm 7 -c tessedit_char_whitelist=+-*/xX÷0123456789",
            ).strip()
        )
    return "\n".join(rows)


def parse_operations(text):
    ops = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue

        line = line.replace(" ", "")
        line = line.replace("×", "*")
        line = line.replace("x", "*")
        line = line.replace("X", "*")
        line = line.replace("÷", "/")
        line = re.sub(r"^[^+\-*/]+", "", line)
        line = re.sub(r"^([*/])\1+", r"\1", line)

        match = re.fullmatch(r"([+\-*/])(-?\d+)", line)
        if not match:
            continue

        op = match.group(1)
        num = int(match.group(2))
        ops.append((op, num))
    return ops


def apply_operations(ops):
    result = 0
    for op, num in ops:
        if op == "+":
            result += num
        elif op == "-":
            result -= num
        elif op == "*":
            result *= num
        elif op == "/":
            result = result // num
    return result


def submit(result):
    token = get_token()
    payload = json.dumps({"result": result}).encode()
    req = urllib.request.Request(
        f"{BASE_URL}/solve?access_token={token}",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as response:
        return response.read().decode()


def main():
    problem = get_problem()
    image_path = download_image(problem["image_url"])
    text = read_image(image_path)
    print("OCR output:\n", text)

    ops = parse_operations(text)
    print("Parsed operations:", ops)

    if len(ops) != 8:
        raise ValueError(f"Expected 8 operations, but OCR parsed {len(ops)}")

    result = apply_operations(ops)
    print("Final result:", result)

    response = submit(result)
    print("Hackattic response:")
    print(response)

    if "solved" in response or "passed" in response:
        print("SUCCESS: Hackattic accepted the answer.")
    else:
        print("NOT PASSED: Hackattic did not confirm success.")


if __name__ == "__main__":
    main()
