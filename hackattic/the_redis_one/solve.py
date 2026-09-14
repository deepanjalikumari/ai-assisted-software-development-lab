import os
import json
import base64
import urllib.request
from datetime import timezone

from rdbtools import RdbParser, RdbCallback


TOKEN = os.environ["HACKATTIC_TOKEN"]

BASE_URL = "https://hackattic.com/challenges/the_redis_one"


class Callback(RdbCallback):

    def __init__(self, check_key):
        super().__init__(False)

        self.databases = set()
        self.emoji_value = None
        self.expiry_millis = None
        self.check_key = check_key
        self.check_type = None

    def start_database(self, db_number):
        self.databases.add(db_number)

    def get_expiry_millis(self, expiry):
        if expiry is not None:
            return int(
                expiry.replace(tzinfo=timezone.utc).timestamp() * 1000
            )

    def set(self, key, value, expiry, info):
        key_text = key.decode("utf-8", errors="replace")

        # Save the value of the emoji key.
        if any(ord(c) > 127 for c in key_text):
            self.emoji_value = value.decode(
                "utf-8",
                errors="replace"
            )

        # Check requested key type.
        if key_text == self.check_key:
            self.check_type = "string"

        # Save expiry.
        if expiry is not None:
            self.expiry_millis = self.get_expiry_millis(expiry)

    def start_hash(self, key, length, expiry, info):
        key_text = key.decode("utf-8", errors="replace")

        if key_text == self.check_key:
            self.check_type = "hash"

        if expiry is not None:
            self.expiry_millis = self.get_expiry_millis(expiry)

    def start_list(self, key, length, expiry, info):
        key_text = key.decode("utf-8", errors="replace")

        if key_text == self.check_key:
            self.check_type = "list"

        if expiry is not None:
            self.expiry_millis = self.get_expiry_millis(expiry)

    def start_set(self, key, length, expiry, info):
        key_text = key.decode("utf-8", errors="replace")

        if key_text == self.check_key:
            self.check_type = "set"

        if expiry is not None:
            self.expiry_millis = self.get_expiry_millis(expiry)

    def start_sorted_set(self, key, length, expiry, info):
        key_text = key.decode("utf-8", errors="replace")

        if key_text == self.check_key:
            self.check_type = "zset"

        if expiry is not None:
            self.expiry_millis = self.get_expiry_millis(expiry)


def get_problem():
    url = BASE_URL + "/problem?access_token=" + TOKEN

    with urllib.request.urlopen(url) as response:
        return json.loads(response.read().decode())


def submit_solution(solution):
    url = BASE_URL + "/solve?access_token=" + TOKEN

    data = json.dumps(solution).encode()

    request = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json"
        },
        method="POST"
    )

    with urllib.request.urlopen(request) as response:
        return response.read().decode()


def main():

    print("Getting fresh problem...")

    problem = get_problem()

    check_key = problem["requirements"]["check_type_of"]

    print("Check key:", check_key)

    # Decode the base64 RDB.
    rdb_data = base64.b64decode(problem["rdb"])

    # Hackattic intentionally tampers with the first 5 bytes.
    # Change "mySQL" back to "REDIS".
    rdb_data = b"REDIS" + rdb_data[5:]

    rdb_file = "hackattic/the_redis_one/fresh.rdb"

    with open(rdb_file, "wb") as f:
        f.write(rdb_data)

    # Parse the Redis snapshot.
    callback = Callback(check_key)

    parser = RdbParser(callback)
    parser.parse(rdb_file)

    print("\nDatabases found:")
    print(sorted(callback.databases))

    print("\nDatabase count:")
    print(len(callback.databases))

    print("\nEmoji key value:")
    print(callback.emoji_value)

    print("\nExpiry timestamp:")
    print(callback.expiry_millis)

    print("\nRequested key type:")
    print(check_key, "=", callback.check_type)

    # Build final answer.
    solution = {
        "db_count": len(callback.databases),
        "emoji_key_value": callback.emoji_value,
        "expiry_millis": callback.expiry_millis,
        check_key: callback.check_type
    }

    print("\nSolution:")
    print(json.dumps(solution, indent=2))

    print("\nSubmitting...")

    result = submit_solution(solution)

    print("\nHackattic response:")
    print(result)


if __name__ == "__main__":
    main()