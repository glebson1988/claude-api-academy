# Building with the Claude API

Runnable notebooks and a cheat sheet for the Anthropic Academy course
[Building with the Claude API](https://academy.claude.com/courses/building-with-the-claude-api).
One notebook per lesson, grouped by course module. Every notebook is committed with its outputs,
so you can read the results right here on GitHub.

## Setup

Requires [uv](https://docs.astral.sh/uv/) and an Anthropic API key.

```bash
uv sync                      # creates .venv with Python 3.15 and all dependencies
cp .env.example .env         # then put your key into .env
```

`.env` is git-ignored. Notebooks call `load_dotenv()`, which finds `.env` in the repo root
from any module folder. `ANTHROPIC_BASE_URL` is optional: this repo runs through OpenRouter,
which accepts the course model name `claude-haiku-4-5` as is.
The RAG notebooks (module 5) need OpenRouter: embeddings come from its `/v1/embeddings` endpoint.

## Running

- **VS Code / Cursor**: open a notebook, *Select Kernel* → `.venv/bin/python`
- **Command line** (runs all cells and saves the outputs into the notebook):

  ```bash
  uv run jupyter nbconvert --to notebook --execute --inplace 02_prompt_evaluation/04_code_based_grading.ipynb
  ```

Every run makes real API calls. Notebooks are self-contained: each one defines the client and the
helpers it needs, the way the course does it.

## Course map

### Module 1: Accessing Claude with the API

📁 [`01_accessing_claude_with_the_api/`](./01_accessing_claude_with_the_api/)

| Notebook | What it shows |
|---|---|
| [`01_making_a_request`](./01_accessing_claude_with_the_api/01_making_a_request.ipynb) | One `messages.create` call, reading text, `stop_reason` and `usage` |
| [`02_multi_turn_conversations`](./01_accessing_claude_with_the_api/02_multi_turn_conversations.ipynb) | The API is stateless: keep the history and resend it |
| [`03_system_prompts`](./01_accessing_claude_with_the_api/03_system_prompts.ipynb) | `system` sets the role: a math tutor that guides instead of answering |
| [`04_temperature`](./01_accessing_claude_with_the_api/04_temperature.ipynb) | Same prompt 5 times at 0.0 and 1.0: identical vs varied answers |
| [`05_response_streaming`](./01_accessing_claude_with_the_api/05_response_streaming.ipynb) | Raw stream events, `text_stream`, `get_final_message()` |
| [`06_structured_data`](./01_accessing_claude_with_the_api/06_structured_data.ipynb) | Clean JSON with an assistant prefill and a stop sequence |

### Module 2: Prompt evaluation

📁 [`02_prompt_evaluation/`](./02_prompt_evaluation/) · dataset: [`dataset.json`](./02_prompt_evaluation/dataset.json)

The prompt under test turns an AWS task into Python, JSON or a regex.

| Notebook | What it shows |
|---|---|
| [`01_generating_test_datasets`](./02_prompt_evaluation/01_generating_test_datasets.ipynb) | Claude generates test cases (`task` + expected `format`) |
| [`02_running_the_eval`](./02_prompt_evaluation/02_running_the_eval.ipynb) | `run_prompt` → `run_test_case` → `run_eval`, placeholder score |
| [`03_model_based_grading`](./02_prompt_evaluation/03_model_based_grading.ipynb) | Claude grades each output: strengths, weaknesses, reasoning, score |
| [`04_code_based_grading`](./02_prompt_evaluation/04_code_based_grading.ipynb) | Syntax validators + stricter prompt, score = (model + syntax) / 2 |

### Module 3: Prompt engineering

📁 [`03_prompt_engineering/`](./03_prompt_engineering/) · evaluator: [`prompt_evaluator.py`](./03_prompt_engineering/prompt_evaluator.py)

The prompt under test writes a one-day meal plan for an athlete.

| Notebook | What it shows |
|---|---|
| [`01_prompt_engineering`](./03_prompt_engineering/01_prompt_engineering.ipynb) | The improve-and-measure loop, `PromptEvaluator`, a naive baseline prompt |
| [`02_being_clear_and_direct`](./03_prompt_engineering/02_being_clear_and_direct.ipynb) | First line as a direct instruction with an action verb |
| [`03_being_specific`](./03_prompt_engineering/03_being_specific.ipynb) | Output guidelines vs process steps; adds guidelines |
| [`04_structure_with_xml_tags`](./03_prompt_engineering/04_structure_with_xml_tags.ipynb) | Wraps the athlete data in `<athlete_information>` |
| [`05_providing_examples`](./03_prompt_engineering/05_providing_examples.ipynb) | One-shot: `<sample_input>` + `<ideal_output>` + why it is ideal |

Each notebook changes one thing in the previous prompt and is graded on the same `dataset.json`.

### Module 4: Tool use with Claude

📁 [`04_tool_use/`](./04_tool_use/)

The project: Claude sets reminders with three tools: current time, date arithmetic, set a reminder.

| Notebook | What it shows |
|---|---|
| [`01_tool_functions`](./04_tool_use/01_tool_functions.ipynb) | A tool is a plain function: `get_current_datetime`, input validation, error text |
| [`02_tool_schemas`](./04_tool_use/02_tool_schemas.ipynb) | JSON schema for the tool, Claude writes one, first request with `tools=[...]` |
| [`03_handling_message_blocks`](./04_tool_use/03_handling_message_blocks.ipynb) | `text` + `tool_use` blocks, keeping them in history, helpers that return the whole `Message` |
| [`04_sending_tool_results`](./04_tool_use/04_sending_tool_results.ipynb) | Full round trip by hand: run the function, send `tool_result`, get the answer |
| [`05_multi_turn_conversations_with_tools`](./04_tool_use/05_multi_turn_conversations_with_tools.ipynb) | "103 days from today": two tools in a row, rounds run one by one |
| [`06_implementing_multiple_turns`](./04_tool_use/06_implementing_multiple_turns.ipynb) | The loop: `run_conversation`, `run_tools`, `run_tool`; parallel calls, a chain, an error and a retry |
| [`07_using_multiple_tools`](./04_tool_use/07_using_multiple_tools.ipynb) | `set_reminder` as a third tool: four steps to add a tool, a chain of all three |
| [`08_the_text_edit_tool`](./04_tool_use/08_the_text_edit_tool.ipynb) | Built-in text editor: Claude asks, our `TextEditorTool` edits files in a sandbox |

Tool functions and schemas: [`tools.py`](./04_tool_use/tools.py), [`text_editor.py`](./04_tool_use/text_editor.py).
Fine-grained tool calling (lesson 29) has no notebook: through OpenRouter it made no visible difference.

### Module 5: Retrieval Augmented Generation

📁 [`05_rag/`](./05_rag/)

The document: the course's [`report.md`](./05_rag/report.md), an annual report of a made-up company with one section per department.

| Notebook | What it shows |
|---|---|
| [`01_text_chunking_strategies`](./05_rag/01_text_chunking_strategies.ipynb) | Chunking by size, sentence and section on one report; which chunks mix two sections |
| [`02_text_embeddings`](./05_rag/02_text_embeddings.ipynb) | `generate_embedding` with Voyage through OpenRouter; a question scored against three sections |
| [`03_implementing_the_rag_flow`](./05_rag/03_implementing_the_rag_flow.ipynb) | The five steps with `VectorIndex`, `query` vs `document` embeddings, plus Claude's answer from the found chunks |
| [`04_bm25_lexical_search`](./05_rag/04_bm25_lexical_search.ipynb) | BM25: tokens and IDF weights, exact IDs vs plain words against vector search, stop words |
| [`05_a_multi_index_rag_pipeline`](./05_rag/05_a_multi_index_rag_pipeline.ipynb) | `Retriever` with RRF over both indexes; where merging helps and where it buries the answer |

Chunking: [`chunking.py`](./05_rag/chunking.py). Embeddings: [`embeddings.py`](./05_rag/embeddings.py). Indexes: [`vector_index.py`](./05_rag/vector_index.py), [`bm25_index.py`](./05_rag/bm25_index.py). Hybrid search: [`retriever.py`](./05_rag/retriever.py).

### Module 6: Features of Claude

📁 [`06_features_of_claude/`](./06_features_of_claude/)

| Notebook | What it shows |
|---|---|
| [`01_extended_thinking`](./06_features_of_claude/01_extended_thinking.ipynb) | `thinking` + `text` blocks, cost, where the signature is checked, redacted thinking, limits through OpenRouter |
| [`02_image_support`](./06_features_of_claude/02_image_support.ipynb) | Image blocks, what an image costs in tokens, fire risk from satellite images: bare question vs step-by-step prompt |
| [`03_pdf_support`](./06_features_of_claude/03_pdf_support.ipynb) | A base64 PDF document block, a one-sentence summary of the course's `earth.pdf`, and token usage through OpenRouter |
| [`04_citations`](./06_features_of_claude/04_citations.ipynb) | PDF and plain text citation requests, metadata checks, and the absence of structured citations on the tested OpenRouter Haiku and Sonnet routes |
| [`05_prompt_caching`](./06_features_of_claude/05_prompt_caching.ipynb) | Cache rules and explicit tool/system breakpoints: writes, reads, partial reuse, invalidation, and measured usage through OpenRouter |
| [`06_code_execution_and_files_api`](./06_features_of_claude/06_code_execution_and_files_api.ipynb) | Files API upload, native execution probe, OpenRouter hosted shell adaptation, downloaded churn metrics and SVG plot, and independent checks |

## Cheat sheet

### Requests

```python
client = Anthropic()  # reads ANTHROPIC_API_KEY
message = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1000,                  # hard cap on output tokens
    messages=[{"role": "user", "content": "..."}],
    system="You are ...",             # optional: role and rules
    temperature=0.0,                  # optional: 0.0 focused ... 1.0 creative (default)
    stop_sequences=["```"],           # optional: stop when this text appears
)
text = "".join(b.text for b in message.content if b.type == "text")
```

- **Content is a list of blocks** (text, tool use, thinking...). `message.content[0].text` works
  without tools, but type checkers flag it, so join the text blocks.
- **`stop_reason`**: `end_turn` (done), `max_tokens` (cut off), `stop_sequence`, `tool_use`.
- **Multi-turn**: the API remembers nothing. Append every reply as `{"role": "assistant", ...}`
  and resend the whole list.
- **`system=None` is rejected**: add optional params to the request only when they are set.
- **Temperature**: low for extraction, classification, code; high for ideas and writing.
  Test it with an open question; "2 + 2" looks the same at any temperature.

### Streaming

```python
with client.messages.stream(model=model, max_tokens=1000, messages=messages) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
    final_message = stream.get_final_message()  # full message for storage
```

Raw events (`stream=True`): `message_start` → `content_block_start` → many `content_block_delta`
→ `content_block_stop` → `message_delta` (stop reason, usage) → `message_stop`.

### Structured output: prefill + stop sequence

```python
add_user_message(messages, "Generate a very short event bridge rule as json")
add_assistant_message(messages, "```json")       # Claude thinks the block is already open
text = chat(messages, stop_sequences=["```"])    # stop when it tries to close it
data = json.loads(text.strip())
```

Works for any wrapper Claude would use (` ```python `, ` ```code `, CSV).
Prefill works on Haiku 4.5; newer models may reject it and offer structured outputs instead.

### Prompt evaluation

The loop: **draft a prompt → dataset → run each case → grade → change the prompt → compare averages.**
A prompt tested once is a guess: real users send inputs you never tried.

- **Dataset**: a JSON array of test cases, by hand or generated by a fast model (Haiku).
  Freeze it, so every prompt version is graded on the same cases.
- **Graders**:

  | Grader | How | Good for |
  |---|---|---|
  | Code | parse or check the output in code | format, syntax, length, required words |
  | Model | another Claude call scores it | quality, task following, completeness |
  | Human | a person reviews it | anything, but slow and tedious |

- **Model grader**: ask for strengths, weaknesses and reasoning before the score,
  otherwise scores cluster around 6. Put the task and output in XML tags (`<task>`, `<solution>`).
- **Code grader**: `json.loads`, `ast.parse` (parses, never runs the code), `re.compile`;
  10 if it parses, 0 if not. `re.compile` accepts almost any text, so prose passes the regex check.
- **Combine**: `score = (model_score + syntax_score) / 2`, adjust the weights to what matters.

### Prompt engineering

**Set a goal → first prompt → evaluate → apply one technique → re-evaluate.** One change at a time.

```python
evaluator = PromptEvaluator(max_concurrent_tasks=3)   # low concurrency avoids rate limits
evaluator.generate_dataset(task_description="...", prompt_inputs_spec={"height": "..."},
                           output_file="dataset.json", num_cases=3)
evaluator.run_evaluation(run_prompt_function=run_prompt, dataset_file="dataset.json",
                         extra_criteria="The output should include: ...")
```

`extra_criteria` are mandatory: missing one caps the score at 3. Results go to `output.json` and
`output.html` (git-ignored). A low first score is normal; it is the baseline to beat.

| Technique | How | Use when |
|---|---|---|
| Clear and direct | Open with an instruction and an action verb, not a question | Always |
| Specific: guidelines | List the qualities of a good output (length, parts, format) | Almost every prompt |
| Specific: steps | Tell Claude how to work through the problem | Complex reasoning, decisions |
| XML tags | Wrap data in descriptive tags: `<athlete_information>...</athlete_information>` | Long context, mixed content, many variables |
| Examples | `<sample_input>` + `<ideal_output>` + a line on why it is ideal | Corner cases, exact format or tone, ambiguous inputs |

```text
Generate a one-day meal plan for an athlete that meets their dietary restrictions.   <- clear and direct

<athlete_information>                                                                 <- XML tags
- Height: ...
</athlete_information>

Guidelines:                                                                           <- being specific
1. Include accurate daily calorie amount
...

Here is an example with a sample input and an ideal output:                           <- examples
<sample_input>...</sample_input>
<ideal_output>...</ideal_output>
This example is ideal because ...
```

- **Take examples from your own eval**: a top-scoring output. Use an input that is not in the
  dataset, otherwise the example leaks the answer.
- **Examples get copied**, structure included: the example has 6 meals, so outputs had 6 meals
  too and lost points on a test case that asked for exactly 4.
- **Check `stop_reason`**: with `max_tokens=1000` most meal plans were cut off before the end, and a
  missing dinner cost more than any prompt technique gained. Raised to 2000 in `prompt_evaluator.py`.
- **A plateau means hidden criteria**: around 7 the points are lost on test-case rules the prompt never
  mentions ("exactly 4 meals", "30 g protein per meal", "3,500-4,000 kcal"). No wording technique fixes
  that; either the prompt gets those inputs, or the criteria are too strict.

### Tool use

Claude never runs anything: it asks for a tool by name with arguments, your code runs it
and sends the result back. That is two API calls per tool round trip.

1. Your request: user question + tool descriptions
2. Claude replies with a tool request (name + arguments) instead of an answer
3. Your code runs the function
4. You send the result back, Claude writes the final answer

Tool functions: descriptive names, validate inputs, raise errors with clear messages
(Claude reads them and can retry with fixed arguments).

```python
get_current_datetime_schema = ToolParam({              # ToolParam: type checking only
    "name": "get_current_datetime",
    "description": "What it does. When to use it. What it returns.",   # 3-4 sentences
    "input_schema": {                                  # JSON Schema of the arguments
        "type": "object",
        "properties": {
            "date_format": {"type": "string", "description": "...", "default": "%Y-%m-%d %H:%M:%S"},
        },
        "required": [],
    },
})
response = client.messages.create(..., tools=[get_current_datetime_schema])
# response.stop_reason == "tool_use", response.content has a tool_use block: name + input
```

Let Claude write schemas: paste the function and ask for "a valid JSON schema spec for the
purposes of tool calling".

- **`response.content` is a list of blocks**: `text` (optional) and `tool_use` (`id`, `name`, `input`).
- **Keep every block in history**: `{"role": "assistant", "content": response.content}`, not just the text.
- **Helpers change**: `chat()` takes `tools` and returns the whole `Message`
  (you need `stop_reason` and the blocks); `text_from_message()` pulls the text out.

```python
tool_use = next(b for b in response.content if b.type == "tool_use")   # not content[0] / [1]
result = get_current_datetime(**tool_use.input)                        # input is a dict of kwargs
add_user_message(messages, [{
    "type": "tool_result",
    "tool_use_id": tool_use.id,   # which request this answers
    "content": result,            # a string
    "is_error": False,
}])
response = chat(messages, tools=[...])  # still send the tools: the history refers to them
```

History of one round trip: user question → assistant `tool_use` → user `tool_result` → assistant text.

**Several tools in a row**: Claude asks for the next tool only after it sees the previous result
("today's date" → "add 103 days"). The number of rounds is unknown, so the code loops:
call Claude → if `stop_reason == "tool_use"`, run the tools and send the results → repeat.

```python
def run_conversation(messages):
    while True:
        response = chat(messages, tools=tools)
        add_assistant_message(messages, response)
        if response.stop_reason != "tool_use":
            break
        add_user_message(messages, run_tools(response))   # one tool_result per tool_use block
    return messages
```

- **`run_tools`**: a reply can hold several `tool_use` blocks (independent values are asked for at once).
  Output goes in as `json.dumps(output)`.
- **Errors**: catch any exception and send `"Error: ..."` with `is_error: True`. Claude reads it and
  retries, e.g. with the right `input_format`.
- **`run_tool`**: name → function routing; a new tool is one more branch, the loop does not change.
- **Good schema descriptions prevent errors**: asked for "fortnights", Claude read the list of units
  and called with 6 weeks instead.
- **Adding a tool** = function + schema + entry in `tools` + branch in `run_tool`. Claude picks the
  order: "in 2 weeks at 10am" ran `get_current_datetime` → `add_duration_to_datetime` → `set_reminder`.
- **A tool that returns nothing** still needs a `tool_result`: `json.dumps(None)` is `"null"`.
- **Check what Claude passes on**: it got "12:00:00 AM" (midnight) and set the reminder for
  `T12:00:00` (noon). If one tool returned ISO like the next one expects, there would be no AM/PM to convert.
- **Fine-grained tool calling**: with streaming, tool arguments arrive as `input_json` events
  (`partial_json` = the new chunk, `snapshot` = everything so far). By default the API buffers and
  validates each top-level key; fine-grained mode sends chunks at once, so the JSON can be invalid:
  wrap `json.loads(snapshot)` in `try`. The default is fine for most apps.

#### Text editor tool

```python
{"type": "text_editor_20250728", "name": "str_replace_based_edit_tool"}   # the stub; Claude 3: text_editor_20250124 / str_replace_editor
```

- Built-in = Claude knows the schema. **Your code runs the commands**: `view`, `create`,
  `str_replace` (exactly one match), `insert`; the course class adds `undo_edit`.
- Keep every path inside one root folder: check with `Path.is_relative_to`, not `startswith`
  (`/sandbox-evil` starts with `/sandbox`).
- OpenRouter rejects the stub (`Unknown server-tool shorthand`); a regular tool with the same name and
  commands works the same way.

### RAG

**Chunking**: cut the document so that each chunk holds one topic.

| Strategy | Function | Use when |
|---|---|---|
| Size + overlap | `chunk_by_char(text, 150, 20)` | anything, code included; the production fallback |
| Sentence + overlap | `chunk_by_sentence(text, 5, 1)` | most plain text |
| Structure | `chunk_by_section(text)` | you control the format (`## ` headers) |
| Semantic | (no code in the course) | relevance matters more than cost |

- On `report.md` (14 sections): size 150/20 gives 141 chunks, 17 of them mix two sections; sentence 5/1 gives
  33 and 15; section gives 15 and 0.
- A header without a period sticks to the next sentence; a size cut separates it from its text.
- Section chunks are uneven (69 to 2187 characters); long sections can be split again by sentence or size.
- Overlap must be smaller than the chunk, or the loop never moves on.

**Embeddings**: text → a list of numbers that stands for its meaning (`voyage-4-large`: 1024 numbers).
Anthropic has no embedding model; the course uses VoyageAI.

```python
generate_embedding("How many bugs did engineers fix?", input_type="query")   # one vector
generate_embedding(chunks, input_type="document")                            # a list of vectors
```

- `input_type`: `"query"` for the question, `"document"` for the chunks; Voyage tunes the vectors for search.
- **Cosine similarity** compares two vectors; Voyage vectors have length 1, so it is the dot product.
- The question about bugs scored 0.333 against the software section and about 0.1 against the
  medical and security ones, though none of them contains the word "bug". The ranking matters, not the value.

**The RAG flow**:

```python
chunks = chunk_by_section(text)                                   # 1. chunk
embeddings = generate_embedding(chunks, input_type="document")    # 2. embed (one request)
store = VectorIndex()                                             # 3. store
for embedding, chunk in zip(embeddings, chunks):
    store.add_vector(embedding, {"content": chunk})
query = generate_embedding(question, input_type="query")          # 4. embed the question
results = store.search(query, k=2)                                # 5. [(doc, distance), ...], closest first
# 6. put the found chunks into the prompt in XML tags, ask Claude to answer only from them
```

- Cosine **distance** = 1 - similarity: smaller is closer.
- Summaries win searches: "What did the software engineering dept do?" ranked the Executive Summary
  above the software section, which was only second. With `k=1` the answer would miss it.
- `"document"` for the chunks separates relevant from irrelevant better: third place at 0.741 against
  0.648, while with `"query"` the top three were within 0.02.
- 2 chunks in the prompt: 731 input tokens instead of the whole report (about 4600).

**BM25** (lexical search): matches words, not meaning. Rare terms weigh more (IDF), repeats help less
and less (`k1`), long chunks are penalized (`b`). No API calls.

**Hybrid search with RRF**: run both indexes, merge by rank, since their scores are on different scales.

```python
retriever = Retriever(BM25Index(), VectorIndex(embedding_fn=generate_embedding))
retriever.add_documents([{"content": chunk} for chunk in chunks])
retriever.search(question, k=3)        # RRF_score(doc) = sum of 1 / (k_rrf + rank), k_rrf = 60
```

Rank of the right section, 15 chunks:

| Question | Vector | BM25 | RRF | RRF `k_rrf=1` |
|---|---|---|---|---|
| What happened with INC-2023-Q4-011? | 1 | 2 | 2 | 2 |
| TIMEOUT_QUERY_DB_0xDEADBEEF | 1 | 1 | 1 | 1 |
| What did the software engineering dept do last year? | 2 | 3 | 2 | 2 |
| Which team stopped hackers from breaking in? | 1 | - | **13** | 3 |

- `voyage-4-large` found the exact IDs by itself; the course shows semantic search missing them.
- When one index has the answer and the other has nothing, RRF buries it: one first place gives
  `1/61`, two mediocre places give more. Hybrid search is not automatically better; evaluate it on your questions.
- BM25 matches common words (`with`, `the`), which adds noise; a tokenizer without stop words helps
  where the words exist (software question: 3 → 2), not where they don't (hackers).

### Extended thinking

```python
params["max_tokens"] = thinking_budget + 1000                  # must be larger than the budget
params["thinking"] = {"type": "enabled", "budget_tokens": 1024}  # 1024 is the minimum
```

- The reply: `thinking` (reasoning + `signature`), then `text`. `redacted_thinking` has only encrypted `data`.
- Thinking tokens are billed as output: 232 → 381 tokens, 2.2 → 3.1 s on a one-paragraph answer.
- Send thinking blocks back unchanged. The API checks the **signature** when Claude continues its own turn
  (tool loop): an edited signature gives `400 Invalid signature`; edited text passes, because Claude 4 returns
  a summary in `thinking` and the full reasoning is encrypted in the signature.
- Blocks from earlier turns are dropped by the API, so a plain follow-up works with or without them.
- The magic test string returns about 60 `redacted_thinking` blocks; they go back like normal ones.
- **Through OpenRouter the limits are not enforced**: prefill silently turns thinking off (no thinking
  block, no error); a budget below 1024 or `max_tokens` below the budget pass too. Check the blocks you get back.
- Turn it on only after prompt work and evals stop improving accuracy.

### Images

```python
{"type": "image", "source": {"type": "base64", "media_type": "image/png",
                             "data": base64.standard_b64encode(path.read_bytes()).decode()}}
```

- Image and text blocks go together in one user message. Up to 100 images, 5 MB each, base64 or URL.
- Cost is about `width * height / 750` tokens, but large images are scaled down first: a 1256x1790 image
  should cost 2997 tokens and cost 1555. Expect at most about 1600 tokens per image.
- `client.messages.count_tokens` returns 404 through OpenRouter; a `max_tokens=1` request gives `usage.input_tokens`.
- Fire risk, 7 images x 3 runs: the bare question gave the same rating every run on 5 of 7, but it said 3
  in 18 of 21 answers. The step-by-step course prompt used the whole scale (4 for the two most overgrown
  homes, every run) and wavered on the borderline ones. Stable is not the same as right: label images and run an eval.

### PDFs

```python
{"type": "document", "source": {"type": "base64", "media_type": "application/pdf",
                                "data": base64.standard_b64encode(path.read_bytes()).decode()}}
```

- Send the document block and the text question in the same user message, as with images.
- Base64 encodes the PDF for transport; no local text extraction is needed.
- The notebook checks this format through OpenRouter with the course's `earth.pdf` and prints token usage.

### Citations

```python
document["title"] = "earth.pdf"
document["citations"] = {"enabled": True}
for block in response.content:
    if block.type == "text":
        print(block.text, block.citations)
```

- Citations belong to individual text blocks; joining only `.text` discards them.
- PDF citations use 1-based page ranges; plain text citations use 0-based character ranges.
  Both end positions are exclusive; `document_index` starts at 0.
- OpenRouter tests with Haiku 4.5 and Sonnet 4.5 returned answers without structured citations for both formats.
  Raw HTTP JSON also contained an empty citation list for a plain text request. Native citation support
  was not confirmed; the notebook reports this explicitly and validates metadata when citations exist.

### Prompt caching

```python
tools_clone = tools.copy()
tools_clone[-1] = {**tools_clone[-1], "cache_control": {"type": "ephemeral"}}
system_blocks = [{"type": "text", "text": system_prompt,
                  "cache_control": {"type": "ephemeral"}}]
```

- Prefix order is tools → system → messages; content through each breakpoint must match.
  Changing the question after the cached system prefix can still reuse that prefix.
- Default TTL is 5 minutes, refreshed on hits; `ttl="1h"` costs more to write.
  Up to four explicit breakpoints are allowed. Short prefixes do not establish cache entries.
- The notebook uses Sonnet 4.5 (1024-token minimum) so the existing reminder schemas qualify
  on their own; Haiku 4.5 needs 4096 tokens. The long system context is module 5's report.
- Inspect `cache_creation_input_tokens` and `cache_read_input_tokens`, rather than inferring
  hits from elapsed time. The experiment checks a short prefix, initial writes, repeat reads,
  a tool-prefix hit after a system change, and invalidation after a first-tool change.
- The original tool schemas stay unchanged. Tools are supplied for caching, with execution disabled.

### Code execution and the Files API

- Upload inputs with `client.beta.files.upload`; the returned file ID references provider-side storage.
- The tested OpenRouter endpoint accepts Files API uploads but rejects the native
  `code_execution_20250825` and older `20250522` tool types with `Unknown server-tool shorthand`.
- The practical notebook uses `openrouter:shell` with `engine="openrouter"` and attaches the uploaded
  CSV through `parameters.environment.file_ids`. This is a provider adaptation; generated code runs
  in its remote sandbox. The native lesson uses `container_upload` instead.
- Actual server results supply container file IDs. Promote the generated JSON and SVG into Files API
  storage, download them, and delete only workspace files created by the run. Local outputs are kept
  in `06_features_of_claude/code_execution_output/`; container copies retain the provider's lifetime.
- Validate server-generated metrics against the local CSV. Churn associations do not establish causation.

## Results so far

| Notebook | Prompt | Average score |
|---|---|---|
| `02/03_model_based_grading` | "Please solve the following task" | 7.33 |
| `02/04_code_based_grading` | + "only code, no commentary", ` ```code ` prefill | 7.83 |
| `03/01_prompt_engineering` | "What should this person eat?" (baseline) | 2.33 |
| `03/02_being_clear_and_direct` | "Generate a one-day meal plan..." | 7.0 |
| `03/03_being_specific` | + guidelines | 8.0 |
| `03/04_structure_with_xml_tags` | + `<athlete_information>` | 7.33 |
| `03/05_providing_examples` | + one example | 7.67 |

Module 3 runs use `max_tokens=2000`. The course reports 2.32 → 3.92 → 7.86 for the first three steps.
Here the big jump comes from the first line alone; after that the scores sit between 7 and 8 and
their order changes from run to run (see "A plateau means hidden criteria" above). Scores move
between runs: the outputs and the model grader are not deterministic, and with 3 test cases one
output moves the average by about 1 point.

## Differences from the course code

- **Text extraction**: all text blocks are joined instead of `message.content[0].text`.
- **`stop_sequences=None`** instead of a mutable `[]` default, sent only when set.
- **Model grader prompt**: the lesson page uses a plain string, so `{task}` / `{solution}` are never
  filled in. The course notebook uses an f-string with XML tags, which is what is used here.
- **`grade_syntax`** is called on the lesson page but not shown; it is taken from the course notebook.
- **`PromptEvaluator`** is the course class from `001_prompting.ipynb`, moved into a module.
  Small fixes: numeric prompt inputs no longer crash grading, the HTML report escapes model output.
  `max_tokens` is 2000 instead of 1000, so long meal plans are not cut off.
- **`get_current_datetime_schema`**: the lesson's description is one sentence; here it has the
  3-4 sentences the lesson recommends.
- **`tools.py`**: the course pastes its ready-made tools into every notebook; here they live in one
  module, with `ToolParam` around each schema.
- **The `tool_use` block is found by type**, not by `response.content[0]` / `[1]` as in the lessons:
  its position depends on whether Claude wrote text first.
- **Datasets are frozen**: generation cells only write `dataset.json` if it does not exist.
  All module 3 notebooks use the same dataset, so their scores can be compared.
- **The example in `03/05`** is for an athlete outside the dataset (the course uses a profile that
  matches a test case). It was generated by the `03/04` prompt, scored 9, and two slips were fixed by hand.
- **Text editor tool**: OpenRouter rejects the built-in stub, so `08` sends the expanded schema as a
  regular tool. `TextEditorTool` is the course class, shorter: `pathlib`, `is_relative_to` for the path
  check, in-memory backups for `undo_edit` instead of a `.backups` folder. Claude works in a temp folder,
  and the notebook runs the tests Claude wrote.
- **Chunking**: `chunk_by_section` splits before the header, so each chunk keeps its `## ` (the course
  splits on `\n## ` and drops it). Both overlap functions raise `ValueError` when the overlap is not
  smaller than the chunk (the course loops forever). `chunk_by_sentence` stops after the chunk that
  reaches the end (the course can add one more chunk made only of overlap sentences).
- **`VectorIndex`** is the course class, shorter: no type checks on every number, `math.dist` and
  `math.hypot` for the distances. Same interface (`add_vector`, `add_document`, `search`).
- **Image support**: the satellite images are the course's (`images/prop1-7.png`). The fire risk prompt
  gets one extra line, `RATING: N`, to read the number off; both prompts run 3 times on every image.
- **Extended thinking**: the course `chat` as is (with `stop_sequences=None`). Added: the cost comparison,
  the signature check in a tool loop, and what OpenRouter does with prefill and thinking.
- **`BM25Index`** is the course class, shorter (`Counter` for document frequencies, `idf()` public
  to show the weights). Same tokenizer, scores and `exp(-0.1 * score)` normalization.
- **`VectorIndex.add_documents`** embeds all documents in one request (the course adds documents one
  by one, one request each); its `embedding_fn` gets `input_type`: `"document"` when adding, `"query"` when searching.
- **`Retriever`** is the course logic; the lesson page only shows a skeleton, the code is from the course notebook.
- **The RAG flow notebook** embeds chunks with `input_type="document"` (the course uses `"query"`
  for both) and adds step 6, Claude's answer from the found chunks, which this lesson leaves out.
- **Embeddings** go through OpenRouter (`httpx` POST to `/v1/embeddings`, the key from `.env`) instead
  of the `voyageai` package and a separate `VOYAGE_API_KEY`. The model is `voyage-4-large`
  (`voyage-3-large` is not on OpenRouter). `generate_embedding` takes a text or a list already;
  the course adds the list form in the next lesson.
- **Each module 3 notebook writes its own report** (`output_02.json`, `output_02.html`, ...).

## Credits

Course: [Anthropic Academy](https://academy.claude.com/courses/building-with-the-claude-api).
