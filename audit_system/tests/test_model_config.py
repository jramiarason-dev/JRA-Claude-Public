"""Regression tests for the Claude API model/config layer.

Guards the model ID and the cache-control wiring on system prompts so an
accidental downgrade or a malformed system block is caught before deploy.

Runs with the standard library only (no pytest):  python3 -m unittest -v
"""

import ast
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

import base_agent  # noqa: E402  (imports `anthropic`, available in the venv)


class TestModelId(unittest.TestCase):
    def test_model_is_current_opus(self):
        self.assertEqual(base_agent.MODEL, "claude-opus-4-8")

    def test_no_legacy_or_dated_model_ids(self):
        """No retired/dated model strings should linger in the agent modules."""
        banned = ("claude-opus-4-7", "claude-opus-4-6", "claude-3-")
        for fname in ("app.py", "base_agent.py", "agent1_regulatory.py",
                      "agent2_audit_plan.py", "agent3_report.py"):
            with open(os.path.join(ROOT, fname), encoding="utf-8") as fh:
                src = fh.read()
            for bad in banned:
                self.assertNotIn(bad, src, f"{fname} still references {bad!r}")


class TestCacheControlWiring(unittest.TestCase):
    """System prompts in the streaming helpers must be cacheable blocks.

    We assert on source text rather than importing app.py because app.py
    requires a Streamlit runtime that isn't present in the test environment.
    """

    def _source(self, fname):
        with open(os.path.join(ROOT, fname), encoding="utf-8") as fh:
            return fh.read()

    def test_base_agent_caches_system(self):
        self.assertIn('"cache_control": {"type": "ephemeral"}', self._source("base_agent.py"))

    def test_app_helpers_cache_system(self):
        src = self._source("app.py")
        # _call, _web_search_call and _agentic_loop should each wrap system in a
        # cacheable block — expect at least three breakpoints in the file.
        self.assertGreaterEqual(
            src.count('"cache_control": {"type": "ephemeral"}'), 3,
            "expected cache_control on every streaming helper's system prompt",
        )

    def test_app_helpers_use_streaming(self):
        src = self._source("app.py")
        self.assertIn("messages.stream(", src)
        self.assertIn("get_final_message()", src)


class TestAppSyntax(unittest.TestCase):
    """app.py can't be imported without Streamlit, but it must still parse."""

    def test_app_parses(self):
        for fname in ("app.py", "data.py", "base_agent.py", "generators.py"):
            with open(os.path.join(ROOT, fname), encoding="utf-8") as fh:
                ast.parse(fh.read(), filename=fname)


if __name__ == "__main__":
    unittest.main(verbosity=2)
