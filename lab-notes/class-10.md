# Week 10 AI Log

## Tool used

ChatGPT

## Prompt given

I asked ChatGPT to help me complete the Hackattic Serving DNS challenge, debug the DNS server, handle wildcard TXT records correctly, and prepare the required files for submission.

## What AI produced

AI helped me write a Python DNS server using `dnslib`, fetch the Hackattic problem, answer A, AAAA, RP, and wildcard TXT records, and submit the solution to Hackattic.

It also helped identify that wildcard TXT responses needed to use the actual queried hostname rather than the wildcard name.

## What I changed manually

I created the required files in my own repository:

* `hackattic/serving_dns/solve.py`
* `lab-notes/class-10.md`

I also ran the commands on the class server, tested the DNS server, and verified the Hackattic submission.

## How I verified it

I ran the DNS server on my assigned port `5327` and Hackattic successfully queried the server.

The final Hackattic response was:

```text
{"result": "passed"}
```

I also ran `git diff --check`, which completed without any errors.

## What I still do not understand

I understand the basic DNS server implementation and wildcard record handling, but I still need to understand the DNS protocol in more depth, especially how DNS resolution, ports, UDP packets, and wildcard records work internally.
