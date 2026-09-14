from rdbtools import RdbParser, RdbCallback
from datetime import datetime, timezone


class Callback(RdbCallback):

    def start_database(self, db_number):
        print("DATABASE:", db_number)

    def set(self, key, value, expiry, info):
        print(
            "KEY:",
            key.decode("utf-8", errors="replace"),
            "| VALUE:",
            value,
            "| TYPE: string",
            "| EXPIRY:",
            expiry
        )

    def start_hash(self, key, length, expiry, info):
        print(
            "KEY:",
            key.decode("utf-8", errors="replace"),
            "| TYPE: hash",
            "| EXPIRY:",
            expiry
        )

    def start_list(self, key, length, expiry, info):
        print(
            "KEY:",
            key.decode("utf-8", errors="replace"),
            "| TYPE: list",
            "| EXPIRY:",
            expiry
        )

    def start_set(self, key, length, expiry, info):
        print(
            "KEY:",
            key.decode("utf-8", errors="replace"),
            "| TYPE: set",
            "| EXPIRY:",
            expiry
        )

    def start_sorted_set(self, key, length, expiry, info):
        print(
            "KEY:",
            key.decode("utf-8", errors="replace"),
            "| TYPE: zset",
            "| EXPIRY:",
            expiry
        )


callback = Callback(False)

parser = RdbParser(callback)

parser.parse("hackattic/the_redis_one/dump.rdb")