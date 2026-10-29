import ast
import json
import re
from statistics import mean

from helpers import add_assistant_message, add_user_message, chat


def run_prompt(test_case):
    """Merges the prompt and test case input, then returns the result"""
    prompt = f"""
Please solve the following task:

{test_case["task"]}

* Respond only with Python, JSON, or a plain Regex
* Do not add any comments or commentary or explanation
"""

    messages = []
    add_user_message(messages, prompt)
    # Prefill a generic code block so the model writes raw code only
    add_assistant_message(messages, "```code")
    output = chat(messages, stop_sequences=["```"])
    return output


def grade_by_model(test_case, output):
    # Create evaluation prompt
    # The course has a plain string here, so {task} and {solution} were never filled in
    eval_prompt = f"""
    You are an expert code reviewer. Evaluate this AI-generated solution.

    Task: {test_case["task"]}
    Solution: {output}

    Provide your evaluation as a structured JSON object with:
    - "strengths": An array of 1-3 key strengths
    - "weaknesses": An array of 1-3 key areas for improvement
    - "reasoning": A concise explanation of your assessment
    - "score": A number between 1-10
    """

    messages = []
    add_user_message(messages, eval_prompt)
    add_assistant_message(messages, "```json")

    eval_text = chat(messages, stop_sequences=["```"])
    return json.loads(eval_text)


def validate_json(text):
    try:
        json.loads(text.strip())
        return 10
    except json.JSONDecodeError:
        return 0


def validate_python(text):
    try:
        ast.parse(text.strip())
        return 10
    except SyntaxError:
        return 0


def validate_regex(text):
    try:
        re.compile(text.strip())
        return 10
    except re.error:
        return 0


def grade_syntax(output, test_case):
    """Picks the validator that matches the format the test case expects"""
    validators = {
        "json": validate_json,
        "python": validate_python,
        "regex": validate_regex,
    }
    return validators[test_case["format"]](output)


def run_test_case(test_case):
    """Calls run_prompt, then grades the result"""
    output = run_prompt(test_case)

    model_grade = grade_by_model(test_case, output)
    model_score = model_grade["score"]
    syntax_score = grade_syntax(output, test_case)
    score = (model_score + syntax_score) / 2

    return {
        "output": output,
        "test_case": test_case,
        "score": score,
        "model_score": model_score,
        "syntax_score": syntax_score,
        "reasoning": model_grade["reasoning"],
    }


def run_eval(dataset):
    """Loads the dataset and calls run_test_case with each case"""
    results = []

    for test_case in dataset:
        result = run_test_case(test_case)
        results.append(result)

    average_score = mean([result["score"] for result in results])
    print(f"Average score: {average_score}")

    return results


with open("dataset.json", "r") as f:
    dataset = json.load(f)

results = run_eval(dataset)

for result in results:
    print(
        f"\n[{result['score']}] model={result['model_score']} syntax={result['syntax_score']}"
        f" ({result['test_case']['format']}) {result['test_case']['task']}"
    )
    print(f"    output: {result['output'].strip()[:200]!r}")
    print(f"    {result['reasoning']}")
