from dnslib import RR, QTYPE
from dnslib.server import DNSServer, BaseResolver

class Resolver(BaseResolver):
    def resolve(self, request, handler):
        reply = request.reply()
        name = str(request.q.qname).rstrip(".").lower()
        qtype = QTYPE[request.q.qtype]

        if name == "plain-star.cz":
            if qtype in ("A", "ANY"):
                reply.add_answer(RR.fromZone(
                    "plain-star.cz. 60 IN A 1.191.1.80"
                )[0])

            if qtype in ("AAAA", "ANY"):
                reply.add_answer(RR.fromZone(
                    "plain-star.cz. 60 IN AAAA 10::6b63:3f39:4e6d:48bc"
                )[0])

            if qtype in ("RP", "ANY"):
                reply.add_answer(RR.fromZone(
                    "plain-star.cz. 60 IN RP abuse.plain-star.cz. ."
                )[0])

        elif name.endswith(".plain-star.cz"):
            if qtype in ("TXT", "ANY"):
                reply.add_answer(RR.fromZone(
                    '*.plain-star.cz. 60 IN TXT "aHR0cDovL3d3dy5yZmMtZWRpdG9yLm9yZy9yZmMvcmZjMTExOC50eHQ="'
                )[0])

        return reply

server = DNSServer(
    Resolver(),
    port=5327,
    address="0.0.0.0"
)

print("DNS server listening on 0.0.0.0:5327")
server.start()
