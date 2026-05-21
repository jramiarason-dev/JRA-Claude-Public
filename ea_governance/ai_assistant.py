"""
ai_assistant.py
Stub for Claude API integration — activate by setting ANTHROPIC_API_KEY env var.

When active, this module will:
  - Analyse submitted solution descriptions and pre-fill routing scores
  - Generate a draft architecture review pre-assessment
  - Suggest relevant standards and patterns based on submission text
  - Draft ADR context/rationale sections from free text
  - Flag potential standard violations before human review
"""
import os

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
AI_ENABLED = ANTHROPIC_API_KEY is not None


def analyse_submission(title: str, description: str, arch_type: str) -> dict:
    """
    Returns pre-filled routing scores and flagged risks.
    When AI_ENABLED=False, returns empty dict (manual scoring only).
    """
    if not AI_ENABLED:
        return {
            "ai_enabled": False,
            "message": "AI analysis not activated. Set ANTHROPIC_API_KEY to enable.",
        }
    # TODO: call Claude API with structured prompt
    # Model: claude-sonnet-4-6
    # Prompt: analyse the submission and return JSON with routing_score, risk_flags, suggested_standards[]
    pass


def generate_review_pre_assessment(request: dict) -> str:
    """
    Returns a draft pre-assessment text for the EA reviewer.
    When AI_ENABLED=False, returns empty string.
    """
    if not AI_ENABLED:
        return ""
    # TODO: call Claude API
    pass


def suggest_standards(description: str) -> list:
    """
    Returns list of STD-IDs likely relevant to the submission.
    """
    if not AI_ENABLED:
        return []
    # TODO: call Claude API
    pass


def draft_adr_sections(context_notes: str) -> dict:
    """
    Returns suggested Context, Decision, Rationale, Consequences sections.
    """
    if not AI_ENABLED:
        return {}
    # TODO: call Claude API
    pass
