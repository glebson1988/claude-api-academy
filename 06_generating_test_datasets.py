import json

from helpers import add_assistant_message, add_user_message, chat

# Prompt v1 that the dataset will evaluate (used in later lessons)
# prompt = f"""
# Please provide a solution to the following task:
# {task}
# """


def generate_dataset():
    prompt = """
Generate an evaluation dataset for a prompt evaluation. The dataset will be used to evaluate prompts that generate Python, JSON, or Regex specifically for AWS-related tasks. Generate an array of JSON objects, each representing task that requires Python, JSON, or a Regex to complete.

Example output:
```json
[
  {
    "task": "Description of task",
    "format": "python" or "json" or "regex"
  },
  ...additional
]
```

* Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a single regex
* Focus on tasks that do not require writing much code

Please generate 3 objects.
"""

    messages = []
    add_user_message(messages, prompt)
    add_assistant_message(messages, "```json")
    text = chat(messages, stop_sequences=["```"])
    return json.loads(text)


dataset = generate_dataset()
print(json.dumps(dataset, indent=2))

with open("dataset.json", "w") as f:
    json.dump(dataset, f, indent=2)
