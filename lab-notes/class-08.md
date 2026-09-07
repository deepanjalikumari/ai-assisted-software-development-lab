# Week 01 AI Log

## Tool used

I used ChatGPT as an AI assistant to help me understand and complete the Hackattic **Help Me Unpack** challenge.

## Prompt given

I gave ChatGPT the instructions for the Hackattic Help Me Unpack challenge and asked for help with implementing the solution in Python. I also used it to understand how to decode the provided bytes and unpack the required integer and floating-point values.

## What AI produced

The AI helped me write Python code using only the standard library. It suggested using:

* `urllib.request` to GET the problem and POST the solution
* `json` to handle the API responses
* `base64` to decode the encoded bytes
* `struct` to unpack signed integers, unsigned integers, shorts, floats, and doubles
* An environment variable to keep my Hackattic access token out of the source code

The final code fetched my problem, decoded the bytes, extracted the required values, created the solution JSON, and submitted it to Hackattic.

## What I changed manually

I manually set up my Hackattic account and obtained my access token.

I stored the token in the `HACKATTIC_TOKEN` environment variable instead of putting the secret key directly in the Python file.

I also checked the Hackattic challenge page myself to verify the API requirements and used the generated problem data from my own account.

## How I verified it

I ran the Python program from my terminal.

The program successfully fetched the problem, unpacked the 32 bytes, and submitted the calculated values to Hackattic.

The server returned:

```json
{"result": "passed"}
```

This confirmed that my solution was correct.

## What I still do not understand

I understand the overall process of fetching the problem, decoding the Base64 data, unpacking the bytes, and submitting the result.

I still want to understand the `struct` format characters such as `<i`, `<I`, `<h`, `<f`, `<d`, and `>d` in more detail, especially how little-endian and big-endian byte ordering affect the interpretation of the bytes.
