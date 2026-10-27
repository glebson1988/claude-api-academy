import json

from helpers import add_assistant_message, add_user_message, chat

messages = []

add_user_message(messages, "Generate a very short event bridge rule as json")
# Prefill: Claude thinks it has already opened a json code block
add_assistant_message(messages, "```json")

# Stop as soon as Claude tries to close the code block
text = chat(messages, stop_sequences=["```"])
print("=== Raw text ===")
print(repr(text))

# Clean up and parse the JSON
clean_json = json.loads(text.strip())
print("\n=== Parsed ===")
print(type(clean_json).__name__, clean_json)
