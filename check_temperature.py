from helpers import add_user_message, chat

RUNS = 5
PROMPT = "Invent a name for a coffee shop. Reply with the name only."

for temperature in (0.0, 1.0):
    answers = []
    for _ in range(RUNS):
        messages = []
        add_user_message(messages, PROMPT)
        answers.append(chat(messages, temperature=temperature).strip())

    print(f"=== temperature={temperature}: {len(set(answers))} unique of {RUNS} ===")
    for answer in answers:
        print(" ", answer)
