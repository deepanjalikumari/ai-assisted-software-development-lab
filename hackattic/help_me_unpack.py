import os
import json
import base64
import struct
import urllib.request


TOKEN = os.environ["HACKATTIC_TOKEN"]

BASE_URL = "https://hackattic.com"


# --------------------------------------------------
# 1. GET THE PROBLEM
# --------------------------------------------------

problem_url = (
    f"{BASE_URL}/challenges/help_me_unpack/problem"
    f"?access_token={TOKEN}"
)

with urllib.request.urlopen(problem_url) as response:
    problem = json.load(response)


# --------------------------------------------------
# 2. DECODE BASE64
# --------------------------------------------------

data = base64.b64decode(problem["bytes"])


# --------------------------------------------------
# 3. UNPACK VALUES
# --------------------------------------------------

# Signed 32-bit integer
int_value = struct.unpack("<i", data[0:4])[0]

# Unsigned 32-bit integer
uint_value = struct.unpack("<I", data[4:8])[0]

# Signed 16-bit short
short_value = struct.unpack("<h", data[8:10])[0]

# Bytes 10-11 are padding for native struct alignment

# 32-bit float
float_value = struct.unpack("<f", data[12:16])[0]

# 64-bit little-endian double
double_value = struct.unpack("<d", data[16:24])[0]

# 64-bit big-endian double
big_endian_double = struct.unpack(">d", data[24:32])[0]


# --------------------------------------------------
# 4. CREATE SOLUTION
# --------------------------------------------------

solution = {
    "int": int_value,
    "uint": uint_value,
    "short": short_value,
    "float": float_value,
    "double": double_value,
    "big_endian_double": big_endian_double,
}


# --------------------------------------------------
# 5. SUBMIT SOLUTION
# --------------------------------------------------

solve_url = (
    f"{BASE_URL}/challenges/help_me_unpack/solve"
    f"?access_token={TOKEN}"
)

request = urllib.request.Request(
    solve_url,
    data=json.dumps(solution).encode("utf-8"),
    headers={
        "Content-Type": "application/json"
    },
    method="POST",
)

with urllib.request.urlopen(request) as response:
    result = response.read().decode("utf-8")


print(result)