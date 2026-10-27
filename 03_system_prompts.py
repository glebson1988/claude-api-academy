from helpers import add_user_message, chat

messages = []
add_user_message(messages, "How do I solve 5x + 3 = 2x + 9 for x?")

# Without system prompt
answer = chat(messages)
print("=== Without system prompt ===")
print(answer)

# With system prompt
system = """
You are a patient math tutor.
Do not directly answer a student's questions.
Guide them to a solution step by step.
"""
answer = chat(messages, system=system, temperature=1.0)
print("\n=== With system prompt ===")
print(answer)
