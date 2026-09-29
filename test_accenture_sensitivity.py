"""Focused checks for Lab 11 scenario isolation and valuation gating."""

import copy
import json
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

import accenture_proforma as model
import accenture_sensitivity as sensitivity


class SensitivityTests(unittest.TestCase):
    def test_scenarios_are_independent_and_base_is_restored(self):
        original_assumptions = copy.deepcopy(model.ASSUMPTIONS)
        original_opening = copy.deepcopy(model.OPENING)
        config = json.loads(Path("ACN_Lab11_inputs.json").read_text(encoding="utf-8"))
        with redirect_stdout(StringIO()):
            results = sensitivity.analyze(config)
        self.assertEqual(model.ASSUMPTIONS, original_assumptions)
        self.assertEqual(model.OPENING, original_opening)
        base = results["base"]
        for driver in config["drivers"]:
            for scenario in ("lower", "base", "higher"):
                entry = results[driver["key"]][scenario]
                self.assertIsNone(entry["error"])
                for key, value in original_assumptions.items():
                    if key != driver["key"]:
                        self.assertEqual(entry["assumptions"][key], value)
                self.assertTrue(all(abs(row["balance_gap"]) < .05 for row in entry["result"]["rows"]))
                self.assertTrue(all(row["cash_minimum_met"] for row in entry["result"]["rows"]))
        self.assertAlmostEqual(base["per_share"], 182.00069750778502)
        higher = results["growth"]["higher"]["result"]
        self.assertAlmostEqual(higher["operating_income"] - base["operating_income"],
                               533.4, delta=0.1)
        self.assertAlmostEqual(higher["fcfe"] - base["fcfe"], 279.7, delta=0.1)
        self.assertAlmostEqual(higher["per_share"] - base["per_share"], 4.24, delta=0.01)

    def test_signed_negative_fcfe_kept_and_value_unavailable(self):
        original_assumptions = copy.deepcopy(model.ASSUMPTIONS)
        original_opening = copy.deepcopy(model.OPENING)
        stress = copy.deepcopy(original_assumptions)
        stress["business_optimization"] = [100_000.0] * 5
        result = sensitivity.run(stress, original_opening)
        self.assertLess(result["fcfe"], 0)
        self.assertIsNone(result["per_share"])
        self.assertIn("nonpositive", result["valuation_note"])
        self.assertEqual(model.ASSUMPTIONS, original_assumptions)
        self.assertEqual(model.OPENING, original_opening)


if __name__ == "__main__":
    unittest.main()
