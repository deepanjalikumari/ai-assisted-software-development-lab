# Week 04 AI Log

## Tool used

I used ChatGPT inside VS Code to help me solve four Hackattic challenges: the Redis collision challenge, the WebSocket challenge, the Visual Basic Math challenge, in the project. 

## Prompt given

I asked ChatGPT to help me solve each Hackattic challenge step by step. For the Redis collision task, I asked how to detect the collision pattern and structure the result. For the WebSocket challenge, I asked how to connect to the server, read messages, and send the required payload. For the Visual Basic Math challenge, I asked how to fetch the image, parse the arithmetic lines, and submit the final result. In each case, I asked for simple Python code and for guidance on validating the answer against the Hackattic API.

## What AI produced

The AI produced code and explanations for all four tasks:

- Redis collision: a strategy for inspecting the challenge data and identifying the correct value to submit.
- WebSocket: example client code to connect to the socket, read the challenge data, and send the endpoint response.
- Visual Basic Math: a script that fetched the challenge, downloaded the image, OCR-ed the math lines, parsed the operations, and calculated the final answer.
- General validation flow: command patterns for running scripts, inspecting API responses, and checking whether the server accepted the result.


## What I changed manually

I changed the AI-generated work in several important ways:

- I kept the API token in the local `.env` file instead of hardcoding it into the script.
- I verified the challenge-specific logic myself instead of trusting the AI output blindly.
- I adjusted the OCR and parsing logic for the Visual Basic Math challenge because the generated image sometimes produced broken or incomplete results.
- I manually inspected the saved PNG and cross-checked the mathematical operations before submitting the final answer.
- I validated the output from the actual Hackattic server rather than assuming the script was correct.

## How I verified it

I verified each challenge by running the Python script in the terminal and checking the real API response from Hackattic. For the math challenge, I confirmed the final result only after reading the image and computing the arithmetic manually when OCR did not produce a complete set of rows. The successful verification came from the server response containing a solved message, which showed that my result was accepted.

## What I still do not understand

I still do not fully understand the exact internal logic behind all challenge generators, especially the WebSocket and Redis collision tasks. I understand the general structure and the API flow, but I want more practice with socket communication, collision detection, and data parsing so I can solve these problems without depending on trial and error. I also want a more reliable way to handle OCR on generated images, because the Visual Basic Math challenge still depends heavily on image recognition quality.
