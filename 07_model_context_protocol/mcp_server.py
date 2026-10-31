from mcp.server.fastmcp import Context, FastMCP
from mcp.types import SamplingMessage, TextContent
from core.root_access import get_root_paths, require_allowed_path

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}



from pydantic import Field
from mcp.server.fastmcp.prompts import base


@mcp.tool(
    name="read_doc_contents",
    description="Read the contents of a document and return it as a string.",
)
def read_document(
    doc_id: str = Field(description="Id of the document to read"),
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")

    return docs[doc_id]


@mcp.tool(
    name="edit_document",
    description="Edit a document by replacing a string in the documents content with a new string",
)
def edit_document(
    doc_id: str = Field(description="Id of the document that will be edited"),
    old_str: str = Field(
        description="The text to replace. Must match exactly, including whitespace"
    ),
    new_str: str = Field(
        description="The new text to insert in place of the old text"
    ),
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")

    docs[doc_id] = docs[doc_id].replace(old_str, new_str)

@mcp.tool()
async def summarize(text_to_summarize: str, ctx: Context):
    await ctx.info("Preparing text for summarization...")
    await ctx.report_progress(0, 100, "Preparing text")
    prompt = f"""
    Please summarize the following text:
    {text_to_summarize}
    """

    await ctx.info("Sending a sampling request to the client. Waiting for Claude...")
    await ctx.report_progress(20, 100, "Waiting for Claude")
    result = await ctx.session.create_message(
        messages=[
            SamplingMessage(
                role="user",
                content=TextContent(
                    type="text",
                    text=prompt
                )
            )
        ],
        max_tokens=4000,
        system_prompt="You are a helpful research assistant",
    )

    if result.content.type == "text":
        await ctx.info("Summary is ready.")
        await ctx.report_progress(100, 100, "Done")
        return result.content.text
    else:
        raise ValueError("Sampling failed")

@mcp.tool()
async def list_roots(ctx: Context) -> list[str]:
    """List directories the client has made available for filesystem tools."""
    return [str(path) for path in await get_root_paths(ctx)]


@mcp.tool()
async def read_dir(path: str, ctx: Context) -> list[str]:
    """List entry names in a directory. Use an absolute path inside a client root."""
    directory = await require_allowed_path(path, ctx)
    if not directory.is_dir():
        raise ValueError(f"Path is not a directory: {path}")
    try:
        return sorted(entry.name for entry in directory.iterdir())
    except OSError as exc:
        raise ValueError(f"Could not read directory: {exc}") from exc


@mcp.tool()
async def read_file(path: str, ctx: Context) -> str:
    """Read a UTF-8 text file. Use an absolute path inside a client root."""
    file = await require_allowed_path(path, ctx)
    if not file.is_file():
        raise ValueError(f"Path is not a regular file: {path}")
    try:
        return file.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise ValueError(f"Could not read UTF-8 text file: {exc}") from exc


@mcp.resource("docs://documents", mime_type="application/json")
def list_docs() -> list[str]:
    return list(docs.keys())


@mcp.resource("docs://documents/{doc_id}", mime_type="text/plain")
def fetch_doc(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    return docs[doc_id]


@mcp.prompt(
    name="format",
    description="Rewrites the contents of the document in Markdown format.",
)
def format_document(
    doc_id: str = Field(description="Id of the document to format"),
) -> list[base.Message]:
    prompt = f"""
    Your goal is to reformat a document to be written with markdown syntax.

    The id of the document you need to reformat is:
    <document_id>
    {doc_id}
    </document_id>

    Add in headers, bullet points, tables, etc as necessary. Feel free to add in extra text, but don't change the meaning of the report.
    Use the 'edit_document' tool to edit the document. After the document has been edited, respond with the final version of the doc. Don't explain your changes.
    """

    return [base.UserMessage(prompt)]


if __name__ == "__main__":
    mcp.run(transport="stdio")
