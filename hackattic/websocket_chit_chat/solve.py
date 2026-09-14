import os
import json
import time
import asyncio
import urllib.request
import websockets


TOKEN = os.environ["HACKATTIC_TOKEN"]

BASE_URL = "https://hackattic.com/challenges/websocket_chit_chat"

INTERVALS = [700, 1500, 2000, 2500, 3000]


def get_problem():
    url = f"{BASE_URL}/problem?access_token={TOKEN}"

    with urllib.request.urlopen(url) as response:
        return json.loads(response.read().decode())


def submit_solution(secret):
    url = f"{BASE_URL}/solve?access_token={TOKEN}"

    data = json.dumps({
        "secret": secret
    }).encode()

    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(request) as response:
        return response.read().decode()


async def websocket_chat(token):

    url = f"wss://hackattic.com/_/ws/{token}"

    print("Connecting to WebSocket...")

    async with websockets.connect(url) as websocket:

        print("Connected!")

        # Start timing from the moment the WebSocket connection opens
        previous_ping = time.perf_counter()

        while True:

            message = await websocket.recv()

            now = time.perf_counter()

            print("Received:", message)

            if message == "ping!":

                elapsed_ms = (now - previous_ping) * 1000

                previous_ping = now

                print(f"Measured interval: {elapsed_ms:.2f} ms")

                detected = min(
                    INTERVALS,
                    key=lambda x: abs(x - elapsed_ms)
                )

                print(f"Detected interval: {detected} ms")

                await websocket.send(str(detected))

            elif message == "good!":

                print("Correct!")

            elif message.startswith("hello!"):

                print("Starting timer...")

            else:

                print("Server message:", message)

                if "the solution to this challenge is" in message:

                    secret = message.split('"')[1]

                    print("Secret:", secret)

                    return secret


async def main():

    print("Getting WebSocket token...")

    problem = get_problem()

    websocket_token = problem["token"]

    print("Received WebSocket token.")

    secret = await websocket_chat(websocket_token)

    print("Secret received:")
    print(secret)

    result = submit_solution(secret)

    print("Hackattic response:")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())