"""Shared utilities: Anthropic client, file upload, streaming, CLI helpers."""

import os
import sys
from pathlib import Path

import anthropic
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.text import Text
from rich.rule import Rule

MODEL   = "claude-opus-4-8"
console = Console()


def make_client() -> anthropic.Anthropic:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        console.print("[bold red]Error:[/bold red] ANTHROPIC_API_KEY not set.")
        sys.exit(1)
    return anthropic.Anthropic(api_key=api_key)


def upload_file(client: anthropic.Anthropic, path: str) -> tuple[str, str]:
    """Upload a file to the Anthropic Files API. Returns (file_id, mime_type)."""
    p    = Path(path)
    ext  = p.suffix.lower()

    # Supported directly by Files API as "document"
    if ext == ".pdf":
        mime = "application/pdf"
    elif ext in (".txt", ".md"):
        mime = "text/plain"
    elif ext in (".png",):
        mime = "image/png"
    elif ext in (".jpg", ".jpeg"):
        mime = "image/jpeg"
    else:
        # For Word/Excel, extract text and upload as plain text
        mime = "text/plain"
        return _upload_as_text(client, p)

    with console.status(f"Uploading [bold]{p.name}[/bold]…"):
        with open(p, "rb") as f:
            uploaded = client.beta.files.upload(file=(p.name, f, mime))
    console.print(f"  [green]✓[/green] Uploaded: {p.name} → [dim]{uploaded.id}[/dim]")
    return uploaded.id, mime


def _upload_as_text(client: anthropic.Anthropic, p: Path) -> tuple[str, str]:
    """Extract text from Word/Excel and upload as plain text."""
    ext = p.suffix.lower()
    try:
        if ext in (".docx", ".doc"):
            from docx import Document
            doc  = Document(str(p))
            text = "\n".join(para.text for para in doc.paragraphs if para.text.strip())
        elif ext in (".xlsx", ".xls"):
            import openpyxl
            wb   = openpyxl.load_workbook(str(p), read_only=True, data_only=True)
            rows = []
            for ws in wb.worksheets:
                rows.append(f"=== Sheet: {ws.title} ===")
                for row in ws.iter_rows(values_only=True):
                    if any(c is not None for c in row):
                        rows.append("\t".join(str(c) if c is not None else "" for c in row))
            text = "\n".join(rows)
        else:
            with open(p, "r", errors="replace") as f:
                text = f.read()
    except Exception as e:
        console.print(f"  [yellow]Warning:[/yellow] Could not extract text from {p.name}: {e}")
        text = f"[File: {p.name} — could not extract text]"

    content = f"Document: {p.name}\n{'='*60}\n{text}"
    with console.status(f"Uploading [bold]{p.name}[/bold] (as text)…"):
        uploaded = client.beta.files.upload(
            file=(p.name + ".txt", content.encode("utf-8"), "text/plain")
        )
    console.print(f"  [green]✓[/green] Uploaded (text): {p.name} → [dim]{uploaded.id}[/dim]")
    return uploaded.id, "text/plain"


def build_file_content_blocks(file_ids_mimes: list[tuple[str, str]]) -> list[dict]:
    """Build content blocks for uploaded files."""
    blocks = []
    for fid, mime in file_ids_mimes:
        if "image" in mime:
            blocks.append({"type": "image", "source": {"type": "file", "file_id": fid}})
        else:
            blocks.append({"type": "document", "source": {"type": "file", "file_id": fid}})
    return blocks


def ask_for_files(client: anthropic.Anthropic) -> list[tuple[str, str]]:
    """Interactive prompt to upload files. Returns list of (file_id, mime_type)."""
    uploaded = []
    if not Confirm.ask("\n[bold]Upload documentation?[/bold] (PDF, Word, Excel, TXT)", default=False):
        return uploaded
    while True:
        path = Prompt.ask("  File path (leave empty to finish)")
        if not path:
            break
        path = path.strip().strip('"').strip("'")
        if not Path(path).exists():
            console.print(f"  [red]File not found:[/red] {path}")
            continue
        try:
            fid, mime = upload_file(client, path)
            uploaded.append((fid, mime))
        except Exception as e:
            console.print(f"  [red]Upload failed:[/red] {e}")
        if not Confirm.ask("  Add another file?", default=False):
            break
    return uploaded


def stream_and_collect(client: anthropic.Anthropic, system: str,
                        messages: list[dict], tools: list[dict] | None = None,
                        betas: list[str] | None = None) -> anthropic.types.Message:
    """Stream a Claude message and collect the final response."""
    # Cache the (large, stable) system prompt so repeated agent turns reuse the
    # prefix instead of re-billing it at full input price.
    system_blocks = [{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}]
    kwargs = dict(
        model      = MODEL,
        max_tokens = 8192,
        thinking   = {"type": "adaptive"},
        system     = system_blocks,
        messages   = messages,
    )
    if tools:
        kwargs["tools"]       = tools
        kwargs["tool_choice"] = {"type": "auto"}
    if betas:
        kwargs["betas"] = betas

    thinking_shown = False
    with client.beta.messages.stream(**kwargs) as stream:
        for event in stream:
            if hasattr(event, "type"):
                if event.type == "content_block_start":
                    block = event.content_block
                    if block.type == "thinking" and not thinking_shown:
                        console.print("\n[dim italic]Claude is thinking…[/dim italic]")
                        thinking_shown = True
                    elif block.type == "text":
                        if thinking_shown:
                            console.print()
                            thinking_shown = False
                elif event.type == "content_block_delta":
                    if hasattr(event, "delta"):
                        d = event.delta
                        if hasattr(d, "type") and d.type == "text_delta":
                            console.print(d.text, end="", markup=False)
        console.print()
        return stream.get_final_message()


def print_banner(title: str, subtitle: str = ""):
    console.print()
    console.print(Panel(
        Text.from_markup(f"[bold white]{title}[/bold white]\n[dim]{subtitle}[/dim]"),
        border_style="bold blue",
        padding=(1, 4),
    ))
    console.print()


def print_rule(text: str):
    console.print(Rule(f"[bold blue]{text}[/bold blue]"))


def print_success(text: str):
    console.print(f"\n[bold green]✓[/bold green] {text}")


def print_info(text: str):
    console.print(f"[bold cyan]ℹ[/bold cyan] {text}")
