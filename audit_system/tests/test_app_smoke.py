"""End-to-end smoke tests: every section must render without raising.

app.py is a single Streamlit script, so the only way to know a refactor did not
break a section is to actually run the script for each one. Streamlit's AppTest
does that headlessly — no browser, no server, and (because every section is
exercised in static mode) no Anthropic API call.

The app refuses to start without ANTHROPIC_API_KEY, so a placeholder is set
here. Nothing in these tests reaches the network.

Runs with the standard library only (no pytest):  python3 -m unittest -v
"""

import ast
import builtins
import contextlib
import os
import pathlib
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = os.path.join(ROOT, "app.py")
sys.path.insert(0, ROOT)

os.environ.setdefault("ANTHROPIC_API_KEY", "sk-ant-smoke-test-placeholder")
os.environ.pop("AUDITIQ_PASSWORD", None)

from streamlit.testing.v1 import AppTest  # noqa: E402


def _module() -> ast.Module:
    with open(APP, encoding="utf-8") as fh:
        return ast.parse(fh.read(), filename="app.py")


def _literal(name: str):
    """Evaluate a module-level literal assignment from app.py without importing it."""
    for node in _module().body:
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == name for t in node.targets
        ):
            return ast.literal_eval(node.value)
    raise AssertionError(f"{name} not found at module level in app.py")


SECTIONS = _literal("_SECTIONS")


def _render(section_id: int) -> AppTest:
    at = AppTest.from_file(APP, default_timeout=180)
    at.session_state["signed_in"] = True
    at.session_state["active_tab"] = section_id
    at.run()
    return at


class TestSectionsRender(unittest.TestCase):
    """Every section renders clean — no traceback, no st.error on screen."""

    def test_every_section_renders(self):
        for section_id, section in enumerate(SECTIONS):
            with self.subTest(section=section["name"]):
                at = _render(section_id)
                self.assertEqual(
                    [e.message for e in at.exception], [],
                    f"{section['name']} raised",
                )
                self.assertEqual(
                    [e.value for e in at.error], [],
                    f"{section['name']} rendered an error",
                )
                self.assertGreater(len(at.markdown), 10, f"{section['name']} rendered almost nothing")

    def test_out_of_range_section_falls_back_to_dashboard(self):
        at = _render(len(SECTIONS) + 5)
        self.assertEqual([e.message for e in at.exception], [])
        self.assertEqual(at.session_state["active_tab"], 0)


class TestSectionRegistry(unittest.TestCase):
    """_SECTIONS is the single source of truth; everything must line up with it."""

    def test_help_covers_every_section(self):
        help_keys = set(_literal("_HELP"))
        self.assertEqual(
            help_keys, set(range(len(SECTIONS))),
            f"_HELP keys {sorted(help_keys)} do not match section ids",
        )

    def test_sections_carry_every_field(self):
        for section in SECTIONS:
            for field in ("group", "nav", "name", "Français", "English", "done_key"):
                self.assertIn(field, section, f"{section.get('name')} missing {field!r}")

    def test_navigation_targets_are_in_range(self):
        """No `active_tab = N` may point past the end of _SECTIONS.

        Renumbering sections used to leave stale integers behind in the
        "What's New" banner and the voice-command router; this catches that.
        """
        stale = [
            node.value.value
            for node in ast.walk(_module())
            if isinstance(node, ast.Assign)
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, int)
            and any(
                isinstance(t, ast.Subscript)
                and isinstance(t.slice, ast.Constant)
                and t.slice.value == "active_tab"
                for t in node.targets
            )
            and not 0 <= node.value.value < len(SECTIONS)
        ]
        self.assertEqual(stale, [], f"active_tab assigned out-of-range ids: {stale}")


class TestSignInGate(unittest.TestCase):
    """The gate must actually check the password when one is configured."""

    def _submit(self, configured, typed):
        if configured is None:
            os.environ.pop("AUDITIQ_PASSWORD", None)
        else:
            os.environ["AUDITIQ_PASSWORD"] = configured
        try:
            at = AppTest.from_file(APP, default_timeout=180)
            at.run()
            at.text_input(key="si_pwd").set_value(typed)
            at.button(key="si_submit").click().run()
            return at
        finally:
            os.environ.pop("AUDITIQ_PASSWORD", None)

    def test_wrong_password_is_refused(self):
        at = self._submit("correct-horse", "wrong")
        self.assertFalse(at.session_state["signed_in"])

    def test_correct_password_is_accepted(self):
        at = self._submit("correct-horse", "correct-horse")
        self.assertTrue(at.session_state["signed_in"])

    def test_sso_does_not_bypass_a_configured_password(self):
        os.environ["AUDITIQ_PASSWORD"] = "correct-horse"
        try:
            at = AppTest.from_file(APP, default_timeout=180)
            at.run()
            at.button(key="si_sso1").click().run()
            self.assertFalse(at.session_state["signed_in"])
        finally:
            os.environ.pop("AUDITIQ_PASSWORD", None)

    def test_open_demo_when_no_password_configured(self):
        at = self._submit(None, "")
        self.assertTrue(at.session_state["signed_in"])


class TestOutputEscaping(unittest.TestCase):
    """User and model text reaches the page through unsafe_allow_html blocks."""

    def test_free_text_is_escaped_before_rendering(self):
        at = _render(0)
        at.session_state["last_voice_transcript"] = "<img src=x onerror=alert(1)>"
        at.run()
        rendered = "\n".join(m.value for m in at.markdown)
        self.assertNotIn("<img src=x onerror=alert(1)>", rendered)
        self.assertIn("&lt;img src=x onerror=alert(1)&gt;", rendered)

    def test_no_raw_link_interpolation_left(self):
        """href attributes must go through _safe_link, never a bare field."""
        with open(APP, encoding="utf-8") as fh:
            src = fh.read()
        self.assertNotIn('href="{link}"', src)
        self.assertIn("def _safe_link(", src)


class TestExportStaging(unittest.TestCase):
    """Generated reports must not survive on disk in a shared directory."""

    def _export_bytes(self):
        """Compile _export_bytes out of app.py — importing app.py needs Streamlit."""
        for node in _module().body:
            if isinstance(node, ast.FunctionDef) and node.name == "_export_bytes":
                ns = {"tempfile": tempfile, "Path": pathlib.Path}
                exec(compile(ast.Module([node], []), "app.py", "exec"), ns)
                return ns["_export_bytes"]
        raise AssertionError("_export_bytes not found in app.py")

    def test_returns_bytes_and_removes_the_staging_directory(self):
        seen = {}

        def fake_generator(payload, outdir):
            seen["outdir"] = outdir
            target = pathlib.Path(outdir) / "report.docx"
            target.write_bytes(b"PK\x03\x04" + payload["name"].encode())
            return str(target)

        out = self._export_bytes()(fake_generator, {"name": "audit"})
        self.assertEqual(out, b"PK\x03\x04audit")
        self.assertFalse(
            pathlib.Path(seen["outdir"]).exists(),
            "staging directory outlived the export",
        )

    def test_staging_directory_is_not_inside_the_project(self):
        seen = {}

        def fake_generator(payload, outdir):
            seen["outdir"] = outdir
            target = pathlib.Path(outdir) / "r.xlsx"
            target.write_bytes(b"x")
            return str(target)

        self._export_bytes()(fake_generator, {})
        self.assertNotIn(
            pathlib.Path(ROOT).resolve(), pathlib.Path(seen["outdir"]).resolve().parents,
            "exports are staged inside the repository",
        )

    def test_no_shared_output_directory(self):
        with open(APP, encoding="utf-8") as fh:
            src = fh.read()
        self.assertNotIn("OUTPUT_DIR", src, "app.py still uses a process-wide output directory")
        self.assertNotIn(
            '_path"]', src,
            "an export still travels as a filesystem path rather than bytes",
        )


class TestDegradesWithoutOptionalPackages(unittest.TestCase):
    """The app must still run where anthropic and rich are not installable.

    That is the Streamlit-in-Snowflake warehouse runtime: packages resolve
    against the Snowflake Anaconda channel only, and outbound network access is
    off until an administrator enables it. The static reference library needs
    neither, so every section has to render anyway — with the AI buttons
    disabled, not with a stopped app.
    """

    @contextlib.contextmanager
    def _without(self, *blocked_roots):
        real_import = builtins.__import__

        def guard(name, *args, **kwargs):
            root = name.split(".")[0]
            if root in blocked_roots:
                raise ImportError(f"No module named {name!r} (simulated)")
            return real_import(name, *args, **kwargs)

        evicted = {k: v for k, v in sys.modules.items() if k.split(".")[0] in blocked_roots}
        for k in evicted:
            del sys.modules[k]
        builtins.__import__ = guard
        try:
            yield
        finally:
            builtins.__import__ = real_import
            sys.modules.update(evicted)

    def test_every_section_renders_without_anthropic_or_rich(self):
        key = os.environ.pop("ANTHROPIC_API_KEY", None)
        try:
            with self._without("anthropic", "rich"):
                for section_id, section in enumerate(SECTIONS):
                    with self.subTest(section=section["name"]):
                        at = _render(section_id)
                        self.assertEqual(
                            [e.message for e in at.exception], [],
                            f"{section['name']} raised in static mode",
                        )
                        self.assertEqual(
                            [e.value for e in at.error], [],
                            f"{section['name']} errored in static mode",
                        )
                        self.assertGreater(len(at.markdown), 10)
        finally:
            if key is not None:
                os.environ["ANTHROPIC_API_KEY"] = key

    def test_static_mode_is_announced_not_fatal(self):
        key = os.environ.pop("ANTHROPIC_API_KEY", None)
        try:
            at = _render(0)
            self.assertIn(
                "Static reference mode", " ".join(i.value for i in at.info),
                "no banner explaining why the AI buttons are disabled",
            )
        finally:
            if key is not None:
                os.environ["ANTHROPIC_API_KEY"] = key


class TestDocumentAnalyserRemoved(unittest.TestCase):
    """The Document Analyser was removed; nothing may reference it again."""

    def test_no_references_left(self):
        with open(APP, encoding="utf-8") as fh:
            src = fh.read()
        for needle in ("Document Analyser", "analyze_document_static", "extract_text_from_file"):
            self.assertNotIn(needle, src, f"app.py still references {needle!r}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
