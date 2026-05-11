"""Agent 1 — Regulatory Framework Assembly.

Compiles all applicable regulations and frameworks for a given audit topic
across Switzerland, Singapore, Hong Kong, Bahamas, EU, and UK for a Swiss
private bank that is also an asset manager.
"""

import json
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.text import Text

from base_agent import (console, make_client, ask_for_files,
                         build_file_content_blocks, print_banner,
                         print_rule, print_success, print_info, MODEL)
from generators import generate_regulatory_framework_docx

SYSTEM_PROMPT = """You are an expert regulatory compliance specialist for financial institutions \
with 25+ years of experience covering banking, private banking, and asset management regulation \
across multiple jurisdictions.

The institution you support is:
- A Swiss PRIVATE BANK headquartered in Geneva/Zurich, regulated by FINMA
- Also authorised as an ASSET MANAGER (AIFM and/or UCITS manager)
- With licensed entities/branches in:
    • Singapore → regulated by MAS (CMS licence, fund management)
    • Hong Kong → regulated by SFC (Type 1, 4, 9 licences) and HKMA
    • Bahamas → regulated by SCB (bank and investment fund licences)
    • European Union → various national regulators (CSSF Luxembourg, BaFin, AMF…)
    • United Kingdom → regulated by FCA and PRA

YOUR ROLE is to compile a comprehensive, structured regulatory framework for a given audit topic. \
You MUST:
1. Cover ALL six jurisdictions above
2. Cite specific laws, regulations, circulars, and supervisory guidance (with exact names/numbers)
3. Highlight cross-jurisdictional differences and regulatory overlaps
4. Flag critical/high-priority requirements and upcoming changes
5. Structure the output clearly for use by an internal audit team

When ready to export, call the tool `save_regulatory_framework` with the full structured data.

IMPORTANT: Always include specific regulation names, article numbers, and regulator guidance \
documents. Do not be vague — auditors need precise references."""


TOOLS = [
    {
        "name": "save_regulatory_framework",
        "description": (
            "Export the compiled regulatory framework to a structured Word document. "
            "Call this once you have assembled the complete framework for all jurisdictions."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "audit_topic": {
                    "type": "string",
                    "description": "The audit topic (e.g. 'AML/KYC', 'Market Risk', 'GDPR')"
                },
                "institution_description": {
                    "type": "string",
                    "description": "Brief description of the institution and context"
                },
                "jurisdictions": {
                    "type": "array",
                    "description": "One entry per jurisdiction",
                    "items": {
                        "type": "object",
                        "properties": {
                            "jurisdiction": {"type": "string"},
                            "regulator": {"type": "string"},
                            "key_regulations": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "description": {"type": "string"},
                                        "key_requirements": {
                                            "type": "array",
                                            "items": {"type": "string"}
                                        },
                                        "applicability": {"type": "string"}
                                    },
                                    "required": ["name", "description", "key_requirements"]
                                }
                            },
                            "frameworks": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Industry standards / frameworks (e.g. BCBS, FATF, ISO)"
                            },
                            "recent_changes": {
                                "type": "string",
                                "description": "Upcoming or recent regulatory changes"
                            }
                        },
                        "required": ["jurisdiction", "regulator", "key_regulations"]
                    }
                },
                "cross_jurisdictional_considerations": {
                    "type": "string",
                    "description": "Key overlaps, conflicts, and multi-jurisdiction compliance considerations"
                },
                "priority_areas": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Top 5 priority areas for the audit based on regulatory risk"
                }
            },
            "required": ["audit_topic", "jurisdictions"]
        }
    }
]


def run():
    print_banner(
        "Agent 1 — Regulatory Framework",
        "Assembles applicable regulations & frameworks for a Swiss private bank / asset manager"
    )

    client = make_client()
    output_dir = "outputs"

    # ── Topic input ───────────────────────────────────────────────────────────
    print_info("Jurisdictions covered: Switzerland · Singapore · Hong Kong · Bahamas · EU · UK")
    console.print()
    topic = Prompt.ask("[bold]Audit topic[/bold] (e.g. 'AML/KYC', 'Market Risk', 'MiFID II')")
    if not topic.strip():
        console.print("[red]No topic entered. Exiting.[/red]")
        return

    # ── File uploads ──────────────────────────────────────────────────────────
    file_ids_mimes = ask_for_files(client)

    # ── Build messages ────────────────────────────────────────────────────────
    user_content: list[dict] = []

    if file_ids_mimes:
        user_content.extend(build_file_content_blocks(file_ids_mimes))
        user_content.append({
            "type": "text",
            "text": (
                f"I have uploaded {len(file_ids_mimes)} document(s) above for context. "
                f"Please incorporate them into your analysis."
            )
        })

    user_content.append({
        "type": "text",
        "text": (
            f"Please compile a comprehensive regulatory framework for the following audit topic:\n\n"
            f"**Audit Topic:** {topic}\n\n"
            f"**Institution:** Swiss private bank and asset manager with operations in Switzerland, "
            f"Singapore, Hong Kong, Bahamas, European Union, and United Kingdom.\n\n"
            f"For EACH jurisdiction:\n"
            f"1. Identify the primary regulator and applicable regulatory body\n"
            f"2. List all key regulations, laws, circulars, and guidance with precise citations\n"
            f"3. Describe key requirements relevant to this audit topic\n"
            f"4. Note any upcoming or recent regulatory changes\n"
            f"5. Identify applicable industry frameworks (FATF, BCBS, IOSCO, etc.)\n\n"
            f"Then highlight cross-jurisdictional considerations and your top 5 priority areas "
            f"for the audit based on regulatory risk.\n\n"
            f"Once you have compiled the full framework, call `save_regulatory_framework` to export it."
        )
    })

    messages = [{"role": "user", "content": user_content}]

    # ── Agentic loop ──────────────────────────────────────────────────────────
    print_rule("Regulatory Analysis")
    console.print()
    output_file = None

    while True:
        kwargs = dict(
            model      = MODEL,
            max_tokens = 16000,
            thinking   = {"type": "adaptive"},
            system     = SYSTEM_PROMPT,
            messages   = messages,
            tools      = TOOLS,
            betas      = ["files-api-2025-04-14"],
        )
        if file_ids_mimes:
            kwargs["betas"] = ["files-api-2025-04-14"]

        thinking_shown = False
        with client.beta.messages.stream(**kwargs) as stream:
            for event in stream:
                if hasattr(event, "type"):
                    if event.type == "content_block_start":
                        block = event.content_block
                        if block.type == "thinking" and not thinking_shown:
                            console.print("[dim italic]Analysing regulations…[/dim italic]")
                            thinking_shown = True
                        elif block.type == "text" and thinking_shown:
                            console.print()
                            thinking_shown = False
                    elif event.type == "content_block_delta":
                        if hasattr(event, "delta"):
                            d = event.delta
                            if hasattr(d, "type") and d.type == "text_delta":
                                console.print(d.text, end="", markup=False)
            console.print()
            response = stream.get_final_message()

        # Append assistant response to history
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            break

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type != "tool_use":
                    continue
                if block.name == "save_regulatory_framework":
                    print_rule("Generating Regulatory Framework Document")
                    try:
                        output_file = generate_regulatory_framework_docx(block.input, output_dir)
                        print_success(f"Saved: [bold]{output_file}[/bold]")
                        result_text = f"Framework document saved to: {output_file}"
                    except Exception as e:
                        result_text = f"Error saving document: {e}"
                        console.print(f"[red]{result_text}[/red]")

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result_text
                    })

            if tool_results:
                messages.append({"role": "user", "content": tool_results})
            else:
                break
        else:
            break

    # ── Summary ───────────────────────────────────────────────────────────────
    console.print()
    if output_file:
        console.print(Panel(
            f"[bold green]Regulatory Framework Complete[/bold green]\n\n"
            f"[white]Topic:[/white] {topic}\n"
            f"[white]Document:[/white] {output_file}",
            border_style="green",
            title="Agent 1 Output"
        ))
    else:
        console.print(Panel(
            "[bold yellow]Analysis complete (no document generated).[/bold yellow]\n"
            "Ask a follow-up question or re-run to generate the export.",
            border_style="yellow"
        ))

    console.print()
    return output_file


if __name__ == "__main__":
    import dotenv; dotenv.load_dotenv()
    run()
