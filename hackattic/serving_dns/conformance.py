
import socket
import sys

from dnslib import DNSRecord, QTYPE, RCODE


def query(server, port, name, record_type):
    request = DNSRecord.question(name, record_type)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(2)
            sock.sendto(request.pack(), (server, port))
            data, _ = sock.recvfrom(4096)
        return DNSRecord.parse(data)
    except (OSError, ValueError) as exc:
        return f"{type(exc).__name__}: {exc}"


def check_query(server, port, name, record_type, expected):
    response = query(server, port, name, record_type)

    if isinstance(response, str):
        return [f"{name} {record_type}: {response}"]

    failures = []
    answers = [
        rr for rr in response.rr
        if QTYPE[rr.rtype] == record_type
    ]

    if response.header.rcode != RCODE.NOERROR:
        failures.append(
            f"{name} {record_type}: expected NOERROR, "
            f"got {RCODE[response.header.rcode]}"
        )

    if not answers:
        failures.append(f"{name} {record_type}: no matching answer")
    elif expected and not any(expected in str(rr.rdata) for rr in answers):
        failures.append(
            f"{name} {record_type}: expected data containing "
            f"{expected!r}; got {[str(rr.rdata) for rr in answers]}"
        )

    return failures


def main():
    if len(sys.argv) != 4:
        print(
            'Usage: python conformance.py ADDRESS PORT '
            '"TYPE name expected_data|TYPE name expected_data"'
        )
        return

    server = sys.argv[1]

    try:
        port = int(sys.argv[2])
        if not 1 <= port <= 65535:
            raise ValueError
    except ValueError:
        print("Port must be an integer from 1 to 65535.")
        return

    records = []
    for item in sys.argv[3].split("|"):
        parts = item.split(maxsplit=2)
        if len(parts) != 3:
            print(f"Invalid record specification: {item!r}")
            return
        record_type, name, expected = parts
        record_type = record_type.upper()

        if record_type not in QTYPE.reverse:
            print(f"Unsupported record type: {record_type}")
            return

        records.append((record_type, name, expected))

    failures = []

    # Test every supplied name with and without its trailing dot.
    for record_type, name, expected in records:
        for query_name in dict.fromkeys((name, name.rstrip("."))):
            failures.extend(
                check_query(server, port, query_name, record_type, expected)
            )

    # Ask for a different type for each supplied name.
    for record_type, name, _ in records:
        alternate = "AAAA" if record_type != "AAAA" else "A"
        response = query(server, port, name, alternate)

        if isinstance(response, str):
            failures.append(f"{name} {alternate}: {response}")
        elif any(QTYPE[rr.rtype] != alternate for rr in response.rr):
            failures.append(
                f"{name} {alternate}: returned an unrelated record type"
            )

    # A nonexistent name should produce NXDOMAIN, not silence or NOERROR.
    missing_name = "conformance-missing.invalid."
    response = query(server, port, missing_name, "A")

    if isinstance(response, str):
        failures.append(f"{missing_name} A: {response}")
    elif response.header.rcode != RCODE.NXDOMAIN:
        failures.append(
            f"{missing_name} A: expected NXDOMAIN, "
            f"got {RCODE[response.header.rcode]}"
        )

    # The tenth sequential query should still receive a valid response.
    for i in range(1, 11):
        record_type, name, _ = records[0]
        response = query(server, port, name, record_type)

        if isinstance(response, str):
            failures.append(f"Query {i}: {response}")
        elif response.header.rcode != RCODE.NOERROR:
            failures.append(
                f"Query {i}: got {RCODE[response.header.rcode]}"
            )
        elif i == 10 and not response.rr:
            failures.append("Query 10: response contained no answers")

    # If the supplied records include a wildcard, test another subdomain.
    wildcard_records = [
        record for record in records if record[1].startswith("*.")
    ]

    for record_type, wildcard_name, expected in wildcard_records:
        suffix = wildcard_name[1:]
        test_name = "conformance-check" + suffix
        failures.extend(
            check_query(server, port, test_name, record_type, expected)
        )

    print("FAILURES:")
    if failures:
        for failure in failures:
            print(f"- {failure}")
    else:
        print("None")


if __name__ == "__main__":
    main()
