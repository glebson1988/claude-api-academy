from helpers import add_assistant_message, add_user_message, chat

# Start with an empty message list
messages = []

# Add the initial user question
add_user_message(messages, "Define quantum computing in one sentence")

# Get Claude's response
answer = chat(messages, temperature=0.0)
print("Answer 1:", answer)

# Add Claude's response to the conversation history
add_assistant_message(messages, answer)

# Add a follow-up question
add_user_message(messages, "Write another sentence")

# Get the follow-up response with full context
final_answer = chat(messages, temperature=0.0)
print("Answer 2:", final_answer)
