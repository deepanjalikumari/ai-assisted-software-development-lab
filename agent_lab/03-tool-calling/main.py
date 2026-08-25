import json
import os
import sys
import argparse
from openai.types.chat import ChatCompletionMessageParam

# Allow importing from the shared common package and local directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from common import DEFAULT_MODEL

from llm import PERSONAS, call_llm, create_initial_messages
from tools import AVAILABLE_TOOLS, TOOLS_SCHEMA

parser = argparse.ArgumentParser(description="Interactive tool-calling chat")
parser.add_argument("model", nargs="?", default=DEFAULT_MODEL, help="OpenRouter model name")
parser.add_argument("--persona", choices=sorted(PERSONAS), default="senior")
parser.add_argument("--question", help="Ask one question immediately after startup")
args = parser.parse_args()
model = args.model

messages: list[ChatCompletionMessageParam] = create_initial_messages(args.persona)
session_input_tokens = 0
session_output_tokens = 0

print(f"--- Chat with Tools Started (Model: {model}, Persona: {args.persona}) ---")
print("Available tools: get_current_time, get_current_weather")
print("Type 'exit' or 'quit' to stop.\n")

# Interactive chat loop
while True:
    user_message = args.question if args.question is not None else input("User: ")
    args.question = None
    if user_message.strip().lower() in ["exit", "quit"]:
        print("Exiting chat. Bye!")
        break

    # 1. Append user input to history
    messages.append({"role": "user", "content": user_message})

    # 2. Call LLM with tool schemas
    response_message, usage = call_llm(messages, tools=TOOLS_SCHEMA, model=model)
    turn_input_tokens = usage.prompt_tokens if usage else 0
    turn_output_tokens = usage.completion_tokens if usage else 0
    session_input_tokens += turn_input_tokens
    session_output_tokens += turn_output_tokens

    # 3. Tool execution loop: handle function calls requested by the model
    while response_message.tool_calls:
        # Append the assistant's tool call request to history
        messages.append(
            {
                "role": "assistant",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        },
                    }
                    for tc in response_message.tool_calls
                    if tc.type == "function"
                ],
            }
        )

        for tool_call in response_message.tool_calls:
            if tool_call.type != "function":
                continue

            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            print(f"\n⚙️  Tool Call: {function_name}({arguments})")

            # Execute corresponding tool function
            tool_fn = AVAILABLE_TOOLS.get(function_name)
            result = tool_fn(**arguments) if tool_fn else f"Error: Tool '{function_name}' not found"

            print(f"📥 Tool Output: {result}\n")

            # Append tool result to conversation history
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result),
                }
            )

        # Let the model process the tool output and produce a reply (or call more tools)
        response_message, usage = call_llm(messages, tools=TOOLS_SCHEMA, model=model)
        if usage:
            turn_input_tokens += usage.prompt_tokens
            turn_output_tokens += usage.completion_tokens
            session_input_tokens += usage.prompt_tokens
            session_output_tokens += usage.completion_tokens

    assistant_reply = response_message.content or ""
    print(f"\nModel: {assistant_reply}\n")
    print("Token usage:")
    print(f"  Input tokens:  {turn_input_tokens}")
    print(f"  Output tokens: {turn_output_tokens}")
    print(f"  Session total: {session_input_tokens + session_output_tokens}")

    # 4. Append assistant's final text reply to history
    messages.append({"role": "assistant", "content": assistant_reply})
