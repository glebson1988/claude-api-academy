from helpers import add_user_message, client, model

messages = []
add_user_message(messages, "Write a 1 sentence description of a fake database")

# 1. Raw stream: every event the API sends
print("=== Raw events ===")
stream = client.messages.create(
    model=model,
    max_tokens=1000,
    messages=messages,
    stream=True,
)

for event in stream:
    print(event)

# 2. Text only: the SDK helper yields just the text chunks
print("\n=== Text stream ===")
with client.messages.stream(
    model=model,
    max_tokens=1000,
    messages=messages,
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
print()

# 3. Stream the text, then get the complete message at the end
print("\n=== Final message ===")
with client.messages.stream(
    model=model,
    max_tokens=1000,
    messages=messages,
) as stream:
    for text in stream.text_stream:
        # Send each chunk to your client
        pass

    # Get the complete message for database storage
    final_message = stream.get_final_message()

print("".join(block.text for block in final_message.content if block.type == "text"))
print("stop_reason:", final_message.stop_reason, "| usage:", final_message.usage)
