"""Agent 3 — Audit Report Generation.

Takes audit observations/findings and produces a formal Word audit report.
"""

import json
from rich.prompt import Prompt, Confirm
from rich.panel import Panel

from base_agent import (console, make_client, ask_for_files,
                         build_file_content_blocks, print_banner,
                         print_rule, print_success, print_info, MODEL)
from generators import generate_audit_report_docx

SYSTEM_PROMPT = """You are a Senior Internal Audit Manager with 20+ years of experience writing \
professional audit reports for regulated financial institutions (private banks, asset managers, \
wealth managers).

The institution is a Swiss private bank and asset manager with operations in Switzerland, \
Singapore, Hong Kong, Bahamas, European Union, and United Kingdom.

YOUR ROLE is to transform raw audit observations into a professional, formal audit report that:
1. Meets internal audit professional standards (IIA Standards)
2. Is appropriate for presentation to the Audit Committee and senior management
3. Is clear, concise, and evidence-based
4. Provides actionable recommendations with appropriate urgency
5. Reflects the multi-jurisdictional regulatory context

REPORT STRUCTURE:
- Executive Summary: overall opinion, count of findings by risk, key messages
- Scope & Methodology: what was reviewed, how, period covered
- Findings: each finding presented with: description, risk rating, impact, root cause,
  recommendation, management response placeholder, target date
- Conclusion: overall assessment and forward-looking statements
- Follow-up actions: key next steps

RISK RATINGS (IIA aligned):
- Critical: Immediate action required; significant regulatory, financial, or reputational risk
- High: Urgent attention required within 30-60 days; material control weakness
- Medium: Action required within 90 days; control improvement needed
- Low: Action within 6 months; best practice recommendation
- Informational: No action required; observation for awareness

OVERALL OPINION OPTIONS:
- Satisfactory: Controls are adequate and operating effectively
- Needs Improvement: Some controls require strengthening
- Unsatisfactory: Significant control weaknesses identified
- Critical: Fundamental control failures; immediate action required

STYLE REQUIREMENTS:
- Professional, objective, factual language
- Third person ("the team", "the bank", "management")
- No jargon without explanation
- Specific, measurable recommendations
- Regulatory implications highlighted where applicable"""


TOOLS = [
    {
        "name": "generate_audit_report",
        "description": (
            "Generate a formal audit report Word document from the structured findings. "
            "Call this once all findings are identified and structured."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "report_title": {
                    "type": "string",
                    "description": "Full title of the audit report"
                },
                "audit_period": {
                    "type": "string",
                    "description": "Audit period (e.g. 'Q1 2025', 'January – March 2025')"
                },
                "executive_summary": {
                    "type": "string",
                    "description": "2-4 paragraph executive summary for the Audit Committee"
                },
                "audit_scope": {
                    "type": "string",
                    "description": "What was in scope, jurisdictions covered, entities reviewed"
                },
                "methodology": {
                    "type": "string",
                    "description": "Audit approach, sampling methodology, standards applied"
                },
                "overall_opinion": {
                    "type": "string",
                    "enum": ["Satisfactory", "Needs Improvement", "Unsatisfactory", "Critical"],
                    "description": "Overall audit opinion"
                },
                "findings": {
                    "type": "array",
                    "description": "All findings in order of risk severity (highest first)",
                    "items": {
                        "type": "object",
                        "properties": {
                            "finding_ref": {
                                "type": "string",
                                "description": "Reference (e.g. F001, AML-01)"
                            },
                            "title": {
                                "type": "string",
                                "description": "Short, descriptive finding title"
                            },
                            "description": {
                                "type": "string",
                                "description": "Full description of the finding with specific evidence"
                            },
                            "risk_rating": {
                                "type": "string",
                                "enum": ["Critical", "High", "Medium", "Low", "Informational"]
                            },
                            "impact": {
                                "type": "string",
                                "description": "Actual or potential impact (financial, regulatory, operational)"
                            },
                            "root_cause": {
                                "type": "string",
                                "description": "Underlying root cause of the finding"
                            },
                            "recommendation": {
                                "type": "string",
                                "description": "Specific, actionable recommendation for management"
                            },
                            "management_response": {
                                "type": "string",
                                "description": "Placeholder for management response (e.g. 'Management agrees...')"
                            },
                            "due_date": {
                                "type": "string",
                                "description": "Target completion date based on risk rating"
                            },
                            "regulatory_implications": {
                                "type": "string",
                                "description": "Relevant regulatory requirements and potential breach implications"
                            }
                        },
                        "required": ["finding_ref", "title", "description",
                                     "risk_rating", "recommendation"]
                    }
                },
                "conclusion": {
                    "type": "string",
                    "description": "Concluding paragraph with overall assessment"
                },
                "follow_up_actions": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Key follow-up actions and next audit touchpoints"
                }
            },
            "required": ["report_title", "executive_summary", "findings",
                         "conclusion", "overall_opinion"]
        }
    }
]


def run():
    print_banner(
        "Agent 3 — Audit Report",
        "Generates a formal audit report from observations and findings"
    )

    client     = make_client()
    output_dir = "outputs"

    # ── Topic & observations ──────────────────────────────────────────────────
    topic = Prompt.ask("[bold]Audit topic / report title[/bold]")
    if not topic.strip():
        console.print("[red]No topic entered. Exiting.[/red]")
        return None

    audit_period = Prompt.ask("[bold]Audit period[/bold]", default="Q1 2025")

    console.print()
    print_info("Now enter your audit observations and findings.")
    print_info("You can type them directly, upload documents, or both.")
    console.print()

    # ── File uploads ──────────────────────────────────────────────────────────
    file_ids_mimes = ask_for_files(client)

    # ── Manual observations ───────────────────────────────────────────────────
    typed_observations = ""
    if Confirm.ask("Type/paste observations directly?", default=True):
        console.print(
            "[dim]Enter your observations below. Press Enter twice on an empty line to finish.[/dim]"
        )
        lines = []
        blank_count = 0
        while blank_count < 1:
            try:
                line = input()
                if line == "":
                    blank_count += 1
                    if blank_count < 1:
                        lines.append(line)
                else:
                    blank_count = 0
                    lines.append(line)
            except EOFError:
                break
        typed_observations = "\n".join(lines).strip()

    if not file_ids_mimes and not typed_observations:
        console.print("[yellow]No observations provided. Please provide at least some context.[/yellow]")
        typed_observations = Prompt.ask("Brief description of the audit findings")

    # ── Scope and context ─────────────────────────────────────────────────────
    console.print()
    scope = Prompt.ask(
        "[bold]Audit scope[/bold] (entities, jurisdictions reviewed)",
        default=f"Swiss private bank and asset manager — {topic} review covering all jurisdictions"
    )

    # ── Build messages ────────────────────────────────────────────────────────
    user_content: list[dict] = []

    if file_ids_mimes:
        user_content.extend(build_file_content_blocks(file_ids_mimes))
        user_content.append({
            "type": "text",
            "text": (
                f"I have uploaded {len(file_ids_mimes)} document(s) above containing "
                f"audit workpapers, observations, and evidence."
            )
        })

    observations_section = ""
    if typed_observations:
        observations_section = f"\n\n**Audit Observations / Findings:**\n{typed_observations}"

    user_content.append({
        "type": "text",
        "text": (
            f"Please draft a professional audit report for the following engagement:\n\n"
            f"**Report Title:** {topic}\n"
            f"**Audit Period:** {audit_period}\n"
            f"**Scope:** {scope}\n"
            f"{observations_section}\n\n"
            f"**INSTRUCTIONS:**\n\n"
            f"1. Analyse all observations provided (documents uploaded and/or text above)\n"
            f"2. Structure and enhance each finding with:\n"
            f"   - Clear, professional description\n"
            f"   - Appropriate risk rating (Critical/High/Medium/Low/Informational)\n"
            f"   - Quantified impact where possible\n"
            f"   - Root cause analysis\n"
            f"   - Specific, actionable recommendation\n"
            f"   - Regulatory implications (FINMA, FCA, MAS, SFC, etc.)\n"
            f"   - Target dates based on risk rating\n"
            f"3. Draft a compelling executive summary for the Audit Committee\n"
            f"4. Determine the overall audit opinion\n"
            f"5. Call `generate_audit_report` to produce the Word document\n\n"
            f"Ensure findings are ordered by risk severity (Critical first)."
        )
    })

    messages = [{"role": "user", "content": user_content}]

    # ── Agentic loop ──────────────────────────────────────────────────────────
    print_rule("Drafting Audit Report")
    console.print()

    output_file = None

    while True:
        kwargs = dict(
            model      = MODEL,
            max_tokens = 16000,
            thinking   = {"type": "adaptive"},
            system     = [{"type": "text", "text": SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}}],
            messages   = messages,
            tools      = TOOLS,
            betas      = ["files-api-2025-04-14"],
        )

        thinking_shown = False
        with client.beta.messages.stream(**kwargs) as stream:
            for event in stream:
                if hasattr(event, "type"):
                    if event.type == "content_block_start":
                        block = event.content_block
                        if block.type == "thinking" and not thinking_shown:
                            console.print("[dim italic]Structuring findings…[/dim italic]")
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

        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            break

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type != "tool_use":
                    continue
                if block.name == "generate_audit_report":
                    print_rule("Generating Audit Report Document")
                    try:
                        output_file = generate_audit_report_docx(block.input, output_dir)
                        print_success(f"Report saved: [bold]{output_file}[/bold]")
                        result = f"Audit report saved to: {output_file}"
                    except Exception as e:
                        result = f"Error: {e}"
                        console.print(f"[red]{result}[/red]")
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })

            if tool_results:
                messages.append({"role": "user", "content": tool_results})
            else:
                break
        else:
            break

    # ── Allow follow-up ───────────────────────────────────────────────────────
    while Confirm.ask("\nAsk a follow-up question or request revisions?", default=False):
        follow_up = Prompt.ask("Your question or revision request")
        if not follow_up.strip():
            break
        messages.append({"role": "user", "content": follow_up})

        kwargs = dict(
            model      = MODEL,
            max_tokens = 8192,
            thinking   = {"type": "adaptive"},
            system     = [{"type": "text", "text": SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}}],
            messages   = messages,
            tools      = TOOLS,
            betas      = ["files-api-2025-04-14"],
        )

        with client.beta.messages.stream(**kwargs) as stream:
            for event in stream:
                if hasattr(event, "type"):
                    if event.type == "content_block_delta":
                        if hasattr(event, "delta"):
                            d = event.delta
                            if hasattr(d, "type") and d.type == "text_delta":
                                console.print(d.text, end="", markup=False)
            console.print()
            response = stream.get_final_message()

        messages.append({"role": "assistant", "content": response.content})

        # Handle tool use in follow-up
        if response.stop_reason == "tool_use":
            for block in response.content:
                if block.type == "tool_use" and block.name == "generate_audit_report":
                    try:
                        output_file = generate_audit_report_docx(block.input, output_dir)
                        print_success(f"Updated report: [bold]{output_file}[/bold]")
                        messages.append({
                            "role": "user",
                            "content": [{"type": "tool_result", "tool_use_id": block.id,
                                         "content": f"Updated report saved: {output_file}"}]
                        })
                    except Exception as e:
                        console.print(f"[red]Error: {e}[/red]")

    # ── Summary ───────────────────────────────────────────────────────────────
    console.print()
    console.print(Panel(
        f"[bold green]Audit Report Complete[/bold green]\n\n"
        f"[white]Topic:[/white]  {topic}\n"
        f"[white]Period:[/white] {audit_period}\n"
        + (f"[white]File:[/white]   {output_file}" if output_file else ""),
        border_style="green",
        title="Agent 3 Output"
    ))
    console.print()
    return output_file


if __name__ == "__main__":
    import dotenv; dotenv.load_dotenv()
    run()
