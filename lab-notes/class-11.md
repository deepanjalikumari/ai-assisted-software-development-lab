
# Class 11 — Serving DNS Conformance

## Work completed
- Inspected `hackattic/serving_dns/solve.py`.
- Created and ran `hackattic/serving_dns/conformance.py`.
- Installed `dnslib` in the local virtual environment.
- Tested the DNS server on `127.0.0.1:5327`.

## Test results

- A query for `plain-star.cz.` returned `1.191.1.80`.
- AAAA query returned `10::6b63:3f39:4e6d:48bc`.
- RP query returned `abuse.plain-star.cz.`.
- TXT query for `test.plain-star.cz.` returned the configured TXT value.
- Queries with and without a trailing dot passed the supplied-record checks.
- Ten sequential A queries all received successful responses.
- A query for `missing.example.com` returned `NOERROR` with no answers.
- The conformance tester reported that `conformance-missing.invalid.` returned `NOERROR` instead of `NXDOMAIN`.

## What printing the records showed
The DNS response contained the requested record types and expected values for the supplied test records. The wildcard TXT response used `*.plain-star.cz.` as its answer owner name.



## Questions to review
- What information besides the name is included in a DNS query?
- Why is a domain registrar not needed for this challenge?
- What different causes can make a DNS server appear unresponsive?
- What is a wildcard record?
- Why should a server bind to `0.0.0.0` rather than only `127.0.0.1` when remote access is required?

## Reflection
The tests confirmed that my server answered the supplied record queries and remained responsive for ten sequential queries. They also revealed that a missing name received `NOERROR` instead of `NXDOMAIN`. I still need to verify remote reachability and review the viva questions.
