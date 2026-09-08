import os
import json
import base64
import hashlib
import urllib.request


# Read Hackattic access token from environment variable.
TOKEN = os.environ["HACKATTIC_TOKEN"]

BASE_URL = "https://hackattic.com/challenges/collision_course"


# Two different 128-byte messages with the same MD5 hash.
# Both have MD5:
# 79054025255fb1a26e4bc422aef54eb4
COLLISION_1 = bytes.fromhex(
    "d131dd02c5e6eec4693d9a0698aff95c"
    "2fcab58712467eab4004583eb8fb7f89"
    "55ad340609f4b30283e488832571415a"
    "085125e8f7cdc99fd91dbdf280373c5b"
    "d8823e3156348f5bae6dacd436c919c6"
    "dd53e2b487da03fd02396306d248cda0"
    "e99f33420f577ee8ce54b67080a80d1e"
    "c69821bcb6a8839396f9652b6ff72a70"
)

COLLISION_2 = bytes.fromhex(
    "d131dd02c5e6eec4693d9a0698aff95c"
    "2fcab50712467eab4004583eb8fb7f89"
    "55ad340609f4b30283e4888325f1415a"
    "085125e8f7cdc99fd91dbd7280373c5b"
    "d8823e3156348f5bae6dacd436c919c6"
    "dd53e23487da03fd02396306d248cda0"
    "e99f33420f577ee8ce54b67080280d1e"
    "c69821bcb6a8839396f965ab6ff72a70"
)


def get_problem():
    url = f"{BASE_URL}/problem?access_token={TOKEN}"

    with urllib.request.urlopen(url) as response:
        return json.loads(response.read().decode())


def submit_solution(file1, file2):
    solution = {
        "files": [
            base64.b64encode(file1).decode(),
            base64.b64encode(file2).decode(),
        ]
    }

    data = json.dumps(solution).encode()

    url = f"{BASE_URL}/solve?access_token={TOKEN}"

    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(request) as response:
        return response.read().decode()


def main():
    # 1. Get the random string from Hackattic.
    problem = get_problem()

    include = problem["include"]

    print("Received include:")
    print(include)

    # 2. Append the SAME include string to both collision blocks.
    suffix = include.encode()

    file1 = COLLISION_1 + suffix
    file2 = COLLISION_2 + suffix

    # 3. Verify that the files are actually different.
    assert file1 != file2

    # 4. Verify that their MD5 hashes are identical.
    md5_1 = hashlib.md5(file1).hexdigest()
    md5_2 = hashlib.md5(file2).hexdigest()

    print("File 1 MD5:", md5_1)
    print("File 2 MD5:", md5_2)

    assert md5_1 == md5_2

    # 5. Submit to Hackattic.
    result = submit_solution(file1, file2)

    print("Hackattic response:")
    print(result)


if __name__ == "__main__":
    main()