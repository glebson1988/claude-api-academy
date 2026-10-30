"""Text editor tool for lesson 08: file operations that Claude asks for, done by our code.

The commands match Anthropic's built-in text editor tool (view, create, str_replace, insert)
plus undo_edit from the course class. All paths are resolved inside one root folder.
"""

from pathlib import Path

from anthropic.types import ToolParam


class TextEditorTool:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.backups = {}  # path -> list of earlier contents, newest last

    def _validate_path(self, path):
        abs_path = (self.root / path).resolve()
        # is_relative_to, not startswith: "/sandbox-evil" starts with "/sandbox" too
        if not abs_path.is_relative_to(self.root):
            raise ValueError(f"Access denied: '{path}' is outside the allowed directory")
        return abs_path

    def _backup(self, abs_path):
        self.backups.setdefault(abs_path, []).append(abs_path.read_text(encoding="utf-8"))

    def view(self, path, view_range=None):
        abs_path = self._validate_path(path)
        if abs_path.is_dir():
            return "\n".join(sorted(entry.name for entry in abs_path.iterdir()))
        if not abs_path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        lines = abs_path.read_text(encoding="utf-8").split("\n")
        start, end = view_range or [1, len(lines)]
        if end == -1:
            end = len(lines)
        return "\n".join(f"{number}: {line}" for number, line in enumerate(lines[start - 1 : end], start))

    def create(self, path, file_text):
        abs_path = self._validate_path(path)
        if abs_path.exists():
            raise FileExistsError(f"File already exists: {path}. Use str_replace to modify it.")
        abs_path.parent.mkdir(parents=True, exist_ok=True)
        abs_path.write_text(file_text, encoding="utf-8")
        return f"Successfully created {path}"

    def str_replace(self, path, old_str, new_str):
        abs_path = self._validate_path(path)
        if not abs_path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        content = abs_path.read_text(encoding="utf-8")
        match_count = content.count(old_str)
        if match_count == 0:
            raise ValueError("No match found for replacement. Please check your text and try again.")
        if match_count > 1:
            raise ValueError(
                f"Found {match_count} matches for replacement text. "
                "Please provide more context to make a unique match."
            )

        self._backup(abs_path)
        abs_path.write_text(content.replace(old_str, new_str), encoding="utf-8")
        return "Successfully replaced text at exactly one location."

    def insert(self, path, insert_line, new_str):
        abs_path = self._validate_path(path)
        if not abs_path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        lines = abs_path.read_text(encoding="utf-8").split("\n")
        if not 0 <= insert_line <= len(lines):
            raise IndexError(f"Line number {insert_line} is out of range. File has {len(lines)} lines.")

        self._backup(abs_path)
        lines[insert_line:insert_line] = new_str.split("\n")
        abs_path.write_text("\n".join(lines), encoding="utf-8")
        return f"Successfully inserted text after line {insert_line}"

    def undo_edit(self, path):
        abs_path = self._validate_path(path)
        if not self.backups.get(abs_path):
            raise FileNotFoundError(f"No previous edits to undo for {path}")
        abs_path.write_text(self.backups[abs_path].pop(), encoding="utf-8")
        return f"Successfully restored {path}"


# The built-in tool is a two-line stub that Anthropic expands into a full schema.
# OpenRouter rejects the stub, so this is the expanded form as a regular tool.
text_editor_schema = ToolParam({
    "name": "str_replace_based_edit_tool",
    "description": "A text editor for viewing, creating and editing files. "
    "Paths are relative to the project root. "
    "view: show a file with line numbers (optionally only view_range), or list a directory. "
    "create: create a new file with file_text; fails if the file exists. "
    "str_replace: replace old_str with new_str; old_str must match exactly one location, "
    "including whitespace, so view the file first. "
    "insert: insert new_str after line insert_line (0 = at the start of the file). "
    "undo_edit: revert the last str_replace or insert on a file.",
    "input_schema": {
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "enum": ["view", "create", "str_replace", "insert", "undo_edit"],
                "description": "The operation to run.",
            },
            "path": {
                "type": "string",
                "description": "File or directory path relative to the project root, e.g. 'main.py' or '.'.",
            },
            "view_range": {
                "type": "array",
                "items": {"type": "integer"},
                "description": "view only: [start_line, end_line], 1-based and inclusive; end_line -1 means the end of the file.",
            },
            "file_text": {
                "type": "string",
                "description": "create only: the full content of the new file.",
            },
            "old_str": {
                "type": "string",
                "description": "str_replace only: the exact text to replace.",
            },
            "new_str": {
                "type": "string",
                "description": "str_replace: the replacement text. insert: the text to insert.",
            },
            "insert_line": {
                "type": "integer",
                "description": "insert only: the line number after which new_str is inserted.",
            },
        },
        "required": ["command", "path"],
    },
})
