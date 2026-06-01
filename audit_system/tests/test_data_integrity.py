"""Regression tests for the audit reference-data layer (data.py).

These guard against the most common source of silent breakage in this app:
drift between the three theme-keyed dictionaries and the template→theme mapping.
A theme present in one dict but missing from another causes empty exports,
KeyErrors, or blank tabs at runtime — none of which surface until a user picks
the affected template.

Runs with the standard library only (no pytest):  python3 -m unittest -v
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import data  # noqa: E402


class TestThemeDictConsistency(unittest.TestCase):
    """The three theme-keyed dicts must cover exactly the same set of themes."""

    def setUp(self):
        self.ri = set(data.RISK_INDICATORS)
        self.at = set(data.AUDIT_TESTS_LIBRARY)
        self.da = set(data.DATA_ANALYTICS_SCENARIOS)

    def test_risk_indicators_match_audit_tests(self):
        self.assertEqual(
            self.ri, self.at,
            f"RISK_INDICATORS vs AUDIT_TESTS_LIBRARY drift: {self.ri ^ self.at}",
        )

    def test_risk_indicators_match_data_analytics(self):
        self.assertEqual(
            self.ri, self.da,
            f"RISK_INDICATORS vs DATA_ANALYTICS_SCENARIOS drift: {self.ri ^ self.da}",
        )

    def test_all_three_dicts_identical_keys(self):
        self.assertTrue(self.ri == self.at == self.da)

    def test_no_empty_theme_entries(self):
        for name in ("RISK_INDICATORS", "AUDIT_TESTS_LIBRARY", "DATA_ANALYTICS_SCENARIOS"):
            d = getattr(data, name)
            for theme, entries in d.items():
                self.assertTrue(entries, f"{name}[{theme!r}] is empty")


class TestTopicKeyMapping(unittest.TestCase):
    """Every template→theme mapping must resolve to a real theme key."""

    def test_mapped_themes_exist(self):
        valid = set(data.RISK_INDICATORS)
        missing = [
            (label, theme)
            for label, themes in data.TOPIC_KEY_MAPPING.items()
            for theme in themes
            if theme not in valid
        ]
        self.assertEqual(missing, [], f"TOPIC_KEY_MAPPING points to unknown themes: {missing}")

    def test_mapping_values_are_lists(self):
        for label, themes in data.TOPIC_KEY_MAPPING.items():
            self.assertIsInstance(themes, list, f"{label!r} mapping is not a list")
            self.assertTrue(themes, f"{label!r} maps to an empty theme list")


class TestAuditTestSchema(unittest.TestCase):
    """Every audit test entry must carry the fields the exporters read."""

    REQUIRED = {"id", "level", "objective", "procedure", "failure_criteria"}
    VALID_LEVELS = {"Critical", "High", "Moderate", "Low"}

    def test_entries_have_required_fields(self):
        for theme, tests in data.AUDIT_TESTS_LIBRARY.items():
            for t in tests:
                missing = self.REQUIRED - set(t)
                self.assertEqual(missing, set(), f"{theme} test {t.get('id')} missing {missing}")

    def test_levels_are_valid(self):
        for theme, tests in data.AUDIT_TESTS_LIBRARY.items():
            for t in tests:
                self.assertIn(
                    t["level"], self.VALID_LEVELS,
                    f"{theme} test {t['id']} has invalid level {t['level']!r}",
                )

    def test_test_ids_are_unique(self):
        ids = [t["id"] for tests in data.AUDIT_TESTS_LIBRARY.values() for t in tests]
        dupes = {i for i in ids if ids.count(i) > 1}
        self.assertEqual(dupes, set(), f"Duplicate audit-test ids: {dupes}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
