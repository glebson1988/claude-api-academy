# Building with the Claude API

Runnable notebooks for the Anthropic Academy course
[Building with the Claude API](https://academy.claude.com/courses/building-with-the-claude-api).
There is one self-contained notebook per lesson, with saved outputs for reading on GitHub.

## Quick start

Requires [uv](https://docs.astral.sh/uv/) and an Anthropic API key.

```bash
uv sync                  # create .venv and install dependencies
cp .env.example .env     # then add your key to .env
```

This repository uses OpenRouter. `ANTHROPIC_BASE_URL` is optional; the model defaults to
`claude-haiku-4-5`. Module 5 requires OpenRouter for its `/v1/embeddings` endpoint.
`.env` is git-ignored and is loaded automatically by the notebooks.

- **VS Code / Cursor:** open a notebook and select `.venv/bin/python` as the kernel.
- **Command line:** execute a notebook and save its outputs:

  ```bash
  uv run jupyter nbconvert --to notebook --execute --inplace 02_prompt_evaluation/04_code_based_grading.ipynb
  ```

Every run makes real API calls. Each notebook defines the client and helpers it needs unless a
shared module is linked below.

## Course map

### 1. Accessing Claude with the API — [`01_accessing_claude_with_the_api/`](./01_accessing_claude_with_the_api/)

| Notebook | Focus |
|---|---|
| [`01_making_a_request`](./01_accessing_claude_with_the_api/01_making_a_request.ipynb) | Messages, text blocks, `stop_reason`, usage |
| [`02_multi_turn_conversations`](./01_accessing_claude_with_the_api/02_multi_turn_conversations.ipynb) | Resending conversation history |
| [`03_system_prompts`](./01_accessing_claude_with_the_api/03_system_prompts.ipynb) | Roles and rules with `system` |
| [`04_temperature`](./01_accessing_claude_with_the_api/04_temperature.ipynb) | Focused vs varied output |
| [`05_response_streaming`](./01_accessing_claude_with_the_api/05_response_streaming.ipynb) | Text streaming and final messages |
| [`06_structured_data`](./01_accessing_claude_with_the_api/06_structured_data.ipynb) | JSON via prefill and stop sequences |

### 2. Prompt evaluation — [`02_prompt_evaluation/`](./02_prompt_evaluation/)

| Notebook | Focus |
|---|---|
| [`01_generating_test_datasets`](./02_prompt_evaluation/01_generating_test_datasets.ipynb) | Generating test cases |
| [`02_running_the_eval`](./02_prompt_evaluation/02_running_the_eval.ipynb) | Running a prompt over a dataset |
| [`03_model_based_grading`](./02_prompt_evaluation/03_model_based_grading.ipynb) | Model-graded quality |
| [`04_code_based_grading`](./02_prompt_evaluation/04_code_based_grading.ipynb) | Syntax checks and combined scores |

Shared dataset: [`dataset.json`](./02_prompt_evaluation/dataset.json).

### 3. Prompt engineering — [`03_prompt_engineering/`](./03_prompt_engineering/)

| Notebook | Focus |
|---|---|
| [`01_prompt_engineering`](./03_prompt_engineering/01_prompt_engineering.ipynb) | The improve-and-measure loop |
| [`02_being_clear_and_direct`](./03_prompt_engineering/02_being_clear_and_direct.ipynb) | Direct instructions |
| [`03_being_specific`](./03_prompt_engineering/03_being_specific.ipynb) | Output guidelines |
| [`04_structure_with_xml_tags`](./03_prompt_engineering/04_structure_with_xml_tags.ipynb) | Structuring input with XML |
| [`05_providing_examples`](./03_prompt_engineering/05_providing_examples.ipynb) | One-shot examples |

Each notebook changes one thing and reuses the same dataset. Evaluator:
[`prompt_evaluator.py`](./03_prompt_engineering/prompt_evaluator.py).

### 4. Tool use — [`04_tool_use/`](./04_tool_use/)

| Notebook | Focus |
|---|---|
| [`01_tool_functions`](./04_tool_use/01_tool_functions.ipynb) | Functions, validation, errors |
| [`02_tool_schemas`](./04_tool_use/02_tool_schemas.ipynb) | JSON schemas and `tools=[...]` |
| [`03_handling_message_blocks`](./04_tool_use/03_handling_message_blocks.ipynb) | Text and `tool_use` blocks |
| [`04_sending_tool_results`](./04_tool_use/04_sending_tool_results.ipynb) | A complete tool round trip |
| [`05_multi_turn_conversations_with_tools`](./04_tool_use/05_multi_turn_conversations_with_tools.ipynb) | Sequential tool calls |
| [`06_implementing_multiple_turns`](./04_tool_use/06_implementing_multiple_turns.ipynb) | The tool-call loop |
| [`07_using_multiple_tools`](./04_tool_use/07_using_multiple_tools.ipynb) | Adding and chaining tools |
| [`08_the_text_edit_tool`](./04_tool_use/08_the_text_edit_tool.ipynb) | Sandbox file editing |

Shared code: [`tools.py`](./04_tool_use/tools.py), [`text_editor.py`](./04_tool_use/text_editor.py).
Fine-grained tool calling has no notebook because it made no visible difference through OpenRouter.

### 5. Retrieval Augmented Generation — [`05_rag/`](./05_rag/)

| Notebook | Focus |
|---|---|
| [`01_text_chunking_strategies`](./05_rag/01_text_chunking_strategies.ipynb) | Size, sentence and section chunks |
| [`02_text_embeddings`](./05_rag/02_text_embeddings.ipynb) | Voyage embeddings and similarity |
| [`03_implementing_the_rag_flow`](./05_rag/03_implementing_the_rag_flow.ipynb) | End-to-end vector RAG |
| [`04_bm25_lexical_search`](./05_rag/04_bm25_lexical_search.ipynb) | Keyword search with BM25 |
| [`05_a_multi_index_rag_pipeline`](./05_rag/05_a_multi_index_rag_pipeline.ipynb) | Hybrid retrieval with RRF |

Shared code: [`chunking.py`](./05_rag/chunking.py), [`embeddings.py`](./05_rag/embeddings.py),
[`vector_index.py`](./05_rag/vector_index.py), [`bm25_index.py`](./05_rag/bm25_index.py),
[`retriever.py`](./05_rag/retriever.py). Sample document: [`report.md`](./05_rag/report.md).

### 6. Features of Claude — [`06_features_of_claude/`](./06_features_of_claude/)

| Notebook | Focus |
|---|---|
| [`01_extended_thinking`](./06_features_of_claude/01_extended_thinking.ipynb) | Thinking blocks, signatures, cost |
| [`02_image_support`](./06_features_of_claude/02_image_support.ipynb) | Image input and evaluation |
| [`03_pdf_support`](./06_features_of_claude/03_pdf_support.ipynb) | Base64 PDF documents |
| [`04_citations`](./06_features_of_claude/04_citations.ipynb) | Citation metadata and provider limits |
| [`05_prompt_caching`](./06_features_of_claude/05_prompt_caching.ipynb) | Cache breakpoints, hits and invalidation |
| [`06_code_execution_and_files_api`](./06_features_of_claude/06_code_execution_and_files_api.ipynb) | Files API and remote code execution |

### 7. Model Context Protocol — [`07_model_context_protocol/`](./07_model_context_protocol/)

[`01_project_setup`](./07_model_context_protocol/01_project_setup.ipynb) starts with a chat baseline,
then smoke-tests the completed local MCP backend and a real model-to-tool round trip.
Shared code: [`mcp_client.py`](./07_model_context_protocol/mcp_client.py),
[`mcp_server.py`](./07_model_context_protocol/mcp_server.py), [`core/`](./07_model_context_protocol/core/).

```bash
uv run --with notebook jupyter notebook 07_model_context_protocol/01_project_setup.ipynb
uv run 07_model_context_protocol/main.py  # optional terminal interface
```

## Cheat sheet

### Basic requests

```python
client = Anthropic()  # reads ANTHROPIC_API_KEY
message = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1000,
    messages=[{"role": "user", "content": "..."}],
    system="You are ...",       # optional
    temperature=0.0,            # optional
    stop_sequences=["```"],    # optional
)
text = "".join(block.text for block in message.content if block.type == "text")
```

- The API is stateless: append each assistant response and resend the full history.
- Content is a list of blocks; find blocks by `type`, not by position.
- Common `stop_reason` values: `end_turn`, `max_tokens`, `stop_sequence`, `tool_use`.
- Omit optional parameters when unset; `system=None` is rejected.

```python
with client.messages.stream(model=model, max_tokens=1000, messages=messages) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
    final_message = stream.get_final_message()
```

For structured output, prefill the assistant with ` ```json ` and stop on ` ``` `, then parse the
returned text. This works with Haiku 4.5; newer models may require structured outputs instead.

### Evaluation and prompting

**Draft → freeze a dataset → run all cases → grade → change one thing → compare averages.**

- Use code graders for syntax/format and model graders for quality; combine scores when useful.
- Ask model graders for reasoning before the score and put inputs/outputs in XML tags.
- Start prompts with a direct instruction; specify the desired output, not unnecessary process steps.
- Use XML tags to separate context and examples to demonstrate ambiguous formats or tone.
- Check `stop_reason`: truncated output can hurt scores more than prompt wording helps.

### Tools

Claude requests a tool; **your code executes it** and returns the result.

```text
user question → assistant tool_use → user tool_result → assistant answer
                                      ↖ repeat for more tool rounds
```

- A tool needs a function, a JSON schema, a place in `tools`, and a routing branch.
- Preserve the complete assistant message, including every `tool_use` block.
- Return one `tool_result` per `tool_use`, matching its `tool_use_id`; keep sending the tool schemas.
- Send failures as `is_error: True` with a useful message so Claude can retry.
- The text editor is implemented locally; keep every path inside its sandbox root.

### RAG

```text
document → chunks → document embeddings → index
question → query embedding → search → matching chunks + question → Claude
```

- Use `input_type="document"` for indexed chunks and `input_type="query"` for questions.
- Vector search finds meaning; BM25 finds words. `Retriever` combines their rankings with RRF.
- Cosine **distance** is smaller for closer matches; embedding **similarity** is larger.
- Hybrid search is not automatically better: evaluate it on your own questions.
- Start with section chunks when the document has reliable headings; otherwise use sentence or
  size-based chunks with overlap smaller than the chunk size.

### Features and provider notes

| Topic | Remember |
|---|---|
| Extended thinking | `max_tokens` must exceed the thinking budget; return thinking blocks unchanged in tool loops. |
| Images / PDFs | Send base64 content and the question in the same user message. |
| Citations | Read citations from individual text blocks; joining only `.text` discards them. |
| Prompt caching | Cache a stable prefix in tools → system → messages order; inspect cache token usage, not latency. |
| Files / execution | Upload with `client.beta.files.upload`; this repo uses OpenRouter's hosted shell adaptation. |
| MCP | Use top-level `await` in Jupyter and open/close each MCP client in the same async task. |

OpenRouter does not enforce all native thinking limits, rejects the built-in text-editor and native
code-execution stubs, and did not return structured citations in the recorded tests. The notebooks
show the tested behavior and adaptations.

## Repository conventions

- Notebooks are self-contained and committed with outputs; generated evaluation reports are ignored.
- Test datasets are frozen so prompt versions remain comparable.
- Text is collected from all text blocks, and tool blocks are found by type.
- Shared helpers live beside their module's notebooks; large experiments and course-specific notes
  stay in the notebooks rather than this README.

## Credits

Course: [Anthropic Academy](https://academy.claude.com/courses/building-with-the-claude-api).
