"""Agent 2 — Audit Plan Creation.

Step 1 → Identifies audit subjects → exports PowerPoint
Step 2 → Generates detailed procedures for each subject → exports Excel
Each subject gets: procedures, test steps, sample sizes, evidence, risks.
"""

import json
from rich.prompt import Prompt, Confirm
from rich.panel import Panel

from base_agent import (console, make_client, ask_for_files,
                         build_file_content_blocks, print_banner,
                         print_rule, print_success, print_info, MODEL)
from generators import generate_audit_plan_ppt, generate_audit_procedures_excel

SYSTEM_PROMPT = """You are a Senior Internal Auditor with 20+ years of experience in financial \
services, specialising in risk-based audit planning for private banks and asset managers.

The institution is:
- A Swiss PRIVATE BANK and ASSET MANAGER with entities in Switzerland, Singapore, Hong Kong,
  Bahamas, European Union, and United Kingdom
- Regulated by FINMA, MAS, SFC, HKMA, SCB, various EU national regulators, FCA, and PRA

YOUR ROLE is to create a comprehensive, risk-based audit plan in two steps:

STEP 1 — AUDIT SUBJECTS (for PowerPoint):
Identify 6-12 distinct audit subjects/domains relevant to the topic. For each subject:
- Clear, specific subject name
- Concise description (what will be reviewed)
- Key audit objectives (3-5 bullet points)
- Risk level: Critical / High / Medium / Low
- Applicable jurisdictions
- Key regulatory references

STEP 2 — AUDIT PROCEDURES (for Excel):
For each subject, design 4-8 detailed audit procedures. Each procedure must include:
- Reference number (e.g. AML-001, MR-002)
- Specific objective
- Detailed procedure description
- Step-by-step test plan (3-6 numbered steps)
- Sample size with rationale
- Evidence to be requested/reviewed
- Associated risks (what could go wrong)
- Risk level: Critical / High / Medium / Low
- Control objective being tested
- Regulatory references

QUALITY STANDARDS:
- Procedures must be specific, actionable, and testable
- Risk assessments must be justified
- Sampling must be appropriate for the risk level
- All procedures must be feasible within a standard audit engagement"""

# ── Tool definitions ───────────────────────────────────────────────────────────

SUBJECT_SCHEMA = {
    "type": "object",
    "properties": {
        "subject_name": {"type": "string"},
        "description":  {"type": "string"},
        "key_objectives": {"type": "array", "items": {"type": "string"}},
        "risk_level": {"type": "string", "enum": ["Critical", "High", "Medium", "Low"]},
        "applicable_jurisdictions": {"type": "array", "items": {"type": "string"}},
        "regulatory_references": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["subject_name", "description", "key_objectives", "risk_level"]
}

PROCEDURE_SCHEMA = {
    "type": "object",
    "properties": {
        "ref":              {"type": "string"},
        "objective":        {"type": "string"},
        "procedure":        {"type": "string"},
        "test_steps":       {"type": "array", "items": {"type": "string"}},
        "sample_size":      {"type": "string"},
        "evidence_required":{"type": "string"},
        "associated_risks": {"type": "array", "items": {"type": "string"}},
        "risk_level":       {"type": "string", "enum": ["Critical", "High", "Medium", "Low"]},
        "control_objective":{"type": "string"},
        "regulatory_refs":  {"type": "array", "items": {"type": "string"}}
    },
    "required": ["ref", "objective", "procedure", "test_steps",
                 "evidence_required", "risk_level"]
}

TOOLS = [
    {
        "name": "generate_audit_plan_ppt",
        "description": (
            "Generate a PowerPoint presentation showing all audit subjects. "
            "Call this FIRST with the complete list of subjects before generating procedures."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "audit_title":  {"type": "string"},
                "audit_scope":  {"type": "string"},
                "objectives":   {"type": "array", "items": {"type": "string"}},
                "subjects":     {"type": "array", "items": SUBJECT_SCHEMA},
                "timeline":     {"type": "string"},
                "team":         {"type": "string"}
            },
            "required": ["audit_title", "subjects"]
        }
    },
    {
        "name": "generate_audit_procedures_excel",
        "description": (
            "Generate an Excel workbook with detailed audit procedures, test plans, and risks. "
            "Call this AFTER the PPT has been generated, with complete procedures for all subjects."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "audit_title": {"type": "string"},
                "subjects": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "subject_name": {"type": "string"},
                            "procedures":   {"type": "array", "items": PROCEDURE_SCHEMA}
                        },
                        "required": ["subject_name", "procedures"]
                    }
                }
            },
            "required": ["audit_title", "subjects"]
        }
    }
]


def run(regulatory_context: str = ""):
    print_banner(
        "Agent 2 — Audit Plan",
        "Creates audit subjects (PPT) and detailed procedures (Excel)"
    )

    client     = make_client()
    output_dir = "outputs"

    # ── Topic ─────────────────────────────────────────────────────────────────
    topic = Prompt.ask("[bold]Audit topic[/bold]")
    if not topic.strip():
        console.print("[red]No topic entered. Exiting.[/red]")
        return None, None

    extra_context = ""
    if regulatory_context:
        print_info("Regulatory framework from Agent 1 will be used as context.")
        extra_context = f"\n\nREGULATORY CONTEXT (from Agent 1):\n{regulatory_context}"
    else:
        # Allow manual context input
        if Confirm.ask("Do you have a regulatory framework or context to include?", default=False):
            console.print("Paste your context (press Enter twice when done):")
            lines = []
            while True:
                line = input()
                if line == "" and lines and lines[-1] == "":
                    break
                lines.append(line)
            extra_context = "\n".join(lines[:-1]) if lines else ""

    # ── File uploads ──────────────────────────────────────────────────────────
    file_ids_mimes = ask_for_files(client)

    # ── Build messages ────────────────────────────────────────────────────────
    user_content: list[dict] = []

    if file_ids_mimes:
        user_content.extend(build_file_content_blocks(file_ids_mimes))

    user_content.append({
        "type": "text",
        "text": (
            f"Create a comprehensive, risk-based audit plan for the following:\n\n"
            f"**Audit Topic:** {topic}\n"
            f"**Institution:** Swiss private bank and asset manager (CH, SG, HK, Bahamas, EU, UK)\n"
            f"{extra_context}\n\n"
            f"**INSTRUCTIONS:**\n\n"
            f"1. First, identify 6-12 distinct audit subjects. Think about:\n"
            f"   - Key risk areas relevant to this topic\n"
            f"   - Regulatory requirements across all 6 jurisdictions\n"
            f"   - Operational, compliance, and financial risks\n"
            f"   - Governance and control framework requirements\n\n"
            f"2. Call `generate_audit_plan_ppt` with all subjects to produce the PowerPoint.\n\n"
            f"3. Then, for each subject, design 4-8 detailed audit procedures. Make them:\n"
            f"   - Specific and actionable\n"
            f"   - Risk-based (higher risk = more procedures)\n"
            f"   - Aligned to regulatory requirements\n\n"
            f"4. Call `generate_audit_procedures_excel` with all procedures to produce the Excel.\n\n"
            f"Be thorough and professional — this plan will be used by audit teams."
        )
    })

    messages = [{"role": "user", "content": user_content}]

    # ── Agentic loop ──────────────────────────────────────────────────────────
    print_rule("Generating Audit Plan")
    console.print()

    ppt_file   = None
    excel_file = None

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
                            console.print("[dim italic]Planning audit structure…[/dim italic]")
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

                if block.name == "generate_audit_plan_ppt":
                    print_rule("Generating PowerPoint")
                    try:
                        ppt_file = generate_audit_plan_ppt(block.input, output_dir)
                        print_success(f"PowerPoint saved: [bold]{ppt_file}[/bold]")
                        result = f"PPT generated: {ppt_file}. Now please generate the detailed procedures Excel."
                    except Exception as e:
                        result = f"Error: {e}"
                        console.print(f"[red]{result}[/red]")
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })

                elif block.name == "generate_audit_procedures_excel":
                    print_rule("Generating Excel Procedures")
                    try:
                        excel_file = generate_audit_procedures_excel(block.input, output_dir)
                        print_success(f"Excel saved: [bold]{excel_file}[/bold]")
                        result = f"Excel generated: {excel_file}. Audit plan complete."
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

    # ── Summary ───────────────────────────────────────────────────────────────
    console.print()
    files_info = []
    if ppt_file:
        files_info.append(f"[white]PowerPoint:[/white] {ppt_file}")
    if excel_file:
        files_info.append(f"[white]Excel:[/white]      {excel_file}")

    console.print(Panel(
        f"[bold green]Audit Plan Complete[/bold green]\n\n"
        f"[white]Topic:[/white] {topic}\n"
        + "\n".join(files_info),
        border_style="green",
        title="Agent 2 Output"
    ))
    console.print()
    return ppt_file, excel_file


if __name__ == "__main__":
    import dotenv; dotenv.load_dotenv()
    run()
