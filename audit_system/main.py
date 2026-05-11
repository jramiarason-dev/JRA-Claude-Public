#!/usr/bin/env python3
"""
Audit Agent System — Main Entry Point

Three specialised agents for Swiss private bank / asset manager internal audit:

  Agent 1  →  Regulatory Framework (Word document)
  Agent 2  →  Audit Plan: subjects (PPT) + procedures (Excel)
  Agent 3  →  Audit Report from observations (Word document)

Usage:
    python main.py          # interactive menu
    python main.py --agent 1
    python main.py --agent 2
    python main.py --agent 3
"""

import os
import sys
import argparse
from pathlib import Path

try:
    import dotenv
    dotenv.load_dotenv()
except ImportError:
    pass

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.table import Table

console = Console()


BANNER = """
╔══════════════════════════════════════════════════════════════════════╗
║              INTERNAL AUDIT AGENT SYSTEM                            ║
║              Swiss Private Bank & Asset Manager                     ║
║              CH · SG · HK · Bahamas · EU · UK                      ║
╚══════════════════════════════════════════════════════════════════════╝
"""

AGENTS = {
    "1": {
        "name":    "Regulatory Framework Agent",
        "module":  "agent1_regulatory",
        "desc":    "Compiles applicable regulations & frameworks for a given audit topic",
        "outputs": ["Word document (.docx)"],
    },
    "2": {
        "name":    "Audit Plan Agent",
        "module":  "agent2_audit_plan",
        "desc":    "Creates audit subjects (PPT) and detailed procedures with risks (Excel)",
        "outputs": ["PowerPoint (.pptx)", "Excel workbook (.xlsx)"],
    },
    "3": {
        "name":    "Audit Report Agent",
        "module":  "agent3_report",
        "desc":    "Drafts a formal audit report from observations and findings",
        "outputs": ["Word document (.docx)"],
    },
}


def check_dependencies():
    missing = []
    for pkg, import_name in [
        ("anthropic",    "anthropic"),
        ("python-pptx",  "pptx"),
        ("openpyxl",     "openpyxl"),
        ("python-docx",  "docx"),
        ("rich",         "rich"),
    ]:
        try:
            __import__(import_name)
        except ImportError:
            missing.append(pkg)

    if missing:
        console.print(
            f"[bold red]Missing dependencies:[/bold red] {', '.join(missing)}\n"
            f"Run: [bold]pip install -r requirements.txt[/bold]"
        )
        sys.exit(1)

    if not os.environ.get("ANTHROPIC_API_KEY"):
        console.print(
            "[bold red]Error:[/bold red] ANTHROPIC_API_KEY is not set.\n"
            "Create a .env file from .env.example or export the variable."
        )
        sys.exit(1)

    Path("outputs").mkdir(exist_ok=True)


def print_banner():
    console.print(BANNER, style="bold blue")


def print_menu():
    table = Table(show_header=True, header_style="bold white on navy_blue",
                  border_style="blue", box=None)
    table.add_column("No.", style="bold cyan", width=4)
    table.add_column("Agent", style="bold white", min_width=30)
    table.add_column("Description", style="dim", min_width=45)
    table.add_column("Outputs", style="green")

    for key, info in AGENTS.items():
        table.add_row(
            key,
            info["name"],
            info["desc"],
            "\n".join(info["outputs"])
        )
    table.add_row("0", "Exit", "Quit the application", "")
    console.print(table)
    console.print()


def run_agent(agent_key: str, prev_output: dict | None = None):
    """Launch the requested agent. Returns output paths dict."""
    info = AGENTS.get(agent_key)
    if not info:
        console.print(f"[red]Unknown agent: {agent_key}[/red]")
        return None

    console.print()
    console.print(Panel(
        f"[bold white]{info['name']}[/bold white]\n[dim]{info['desc']}[/dim]",
        border_style="bold blue",
        padding=(0, 2)
    ))
    console.print()

    # Dynamically import the agent module
    module = __import__(info["module"])

    result = None
    if agent_key == "1":
        result = module.run()
    elif agent_key == "2":
        # Optionally pass regulatory context from Agent 1
        regulatory_context = ""
        if prev_output and prev_output.get("regulatory_doc"):
            doc_path = prev_output["regulatory_doc"]
            if Confirm.ask(f"Use regulatory framework from Agent 1 ({doc_path})?", default=True):
                try:
                    from docx import Document
                    doc = Document(doc_path)
                    regulatory_context = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
                except Exception:
                    pass
        ppt, xlsx = module.run(regulatory_context=regulatory_context)
        result = {"ppt": ppt, "excel": xlsx}
    elif agent_key == "3":
        result = module.run()

    return result


def main():
    parser = argparse.ArgumentParser(description="Audit Agent System")
    parser.add_argument("--agent", choices=["1", "2", "3"], help="Run a specific agent directly")
    args = parser.parse_args()

    check_dependencies()
    print_banner()

    if args.agent:
        run_agent(args.agent)
        return

    # ── Interactive menu ──────────────────────────────────────────────────────
    session_outputs: dict = {}

    while True:
        print_menu()
        choice = Prompt.ask("[bold]Select agent[/bold]", choices=["0", "1", "2", "3"], default="1")

        if choice == "0":
            console.print("\n[bold blue]Goodbye.[/bold blue]\n")
            break

        result = run_agent(choice, prev_output=session_outputs)

        # Store outputs for cross-agent use
        if choice == "1" and isinstance(result, str):
            session_outputs["regulatory_doc"] = result
        elif choice == "2" and isinstance(result, dict):
            session_outputs.update(result)
        elif choice == "3" and isinstance(result, str):
            session_outputs["report_doc"] = result

        console.print()
        if not Confirm.ask("Return to main menu?", default=True):
            console.print("\n[bold blue]Goodbye.[/bold blue]\n")
            break


if __name__ == "__main__":
    main()
