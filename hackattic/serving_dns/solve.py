import json
import os
import threading
import time
import urllib.request

from dnslib import QTYPE, RR
from dnslib.server import BaseResolver, DNSServer


HOST = "0.0.0.0"
PORT = 5327

BASE_URL = "https://hackattic.com/challenges/serving_dns"
TOKEN = os.environ["HACKATTIC_TOKEN"]


class Resolver(BaseResolver):
    def __init__(self, records):
        self.records = records

    def resolve(self, request, handler):
        reply = request.reply()

        query_name = str(request.q.qname).rstrip(".").lower()
        query_type = QTYPE[request.q.qtype]

        for record in self.records:
            record_name = record["name"].rstrip(".").lower()
            record_type = record["type"]
            data = record["data"]

            # Exact record
            if not record_name.startswith("*."):
                if query_name != record_name:
                    continue
                answer_name = record_name

            # Wildcard record
            else:
                suffix = record_name[1:]

                if not query_name.endswith(suffix):
                    continue

                if query_name == record_name[2:]:
                    continue

                # The answer must use the actual queried name.
                answer_name = query_name

            if query_type != record_type and query_type != "ANY":
                continue

            if record_type == "A":
                rr = RR.fromZone(
                    f"{answer_name} 60 IN A {data}"
                )[0]

            elif record_type == "AAAA":
                rr = RR.fromZone(
                    f"{answer_name} 60 IN AAAA {data}"
                )[0]

            elif record_type == "TXT":
                rr = RR.fromZone(
                    f'{answer_name} 60 IN TXT "{data}"'
                )[0]

            elif record_type == "RP":
                rr = RR.fromZone(
                    f"{answer_name} 60 IN RP {data}. ."
                )[0]

            else:
                continue

            reply.add_answer(rr)

        return reply


def fetch_problem():
    url = f"{BASE_URL}/problem?access_token={TOKEN}"

    with urllib.request.urlopen(url) as response:
        return json.load(response)


def submit_solution():
    url = f"{BASE_URL}/solve?access_token={TOKEN}"

    payload = json.dumps({
        "dns_ip": "204.168.202.138",
        "dns_port": PORT,
    }).encode()

    request = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(request) as response:
        return response.read().decode()


def main():
    # Start listening BEFORE fetching the problem.
    # This is important because Hackattic gives only 60 seconds.
    server = DNSServer(
        Resolver([]),
        port=PORT,
        address=HOST,
    )

    server_thread = threading.Thread(
        target=server.start,
        daemon=True,
    )
    server_thread.start()

    time.sleep(0.5)

    print(f"DNS server listening on {HOST}:{PORT}")

    # Fetch the problem only after the server is ready.
    problem = fetch_problem()
    records = problem["records"]

    print("Problem received:")
    for record in records:
        print(record)

    # Load the records into the running resolver.
    server.resolver.records = records

    print("Submitting solution...")

    try:
        result = submit_solution()
        print("Hackattic response:")
        print(result)
    finally:
        server.stop()


if __name__ == "__main__":
    main()
