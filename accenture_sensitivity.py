"""One-at-a-time sensitivity runner for the existing Accenture Lab 10 model.

Run: python accenture_sensitivity.py ACN_Lab11_inputs.json

The input file records two student-chosen drivers, their year-by-year lower and
higher values, range reasons, and a prediction locked before changed runs.
Percent inputs in JSON use percentage units (3.0 means 3.0%, not 300%).
Financial statement amounts are USD millions; per-share values are USD/share.
"""

import argparse
import copy
import json
from contextlib import contextmanager
from math import isclose, isfinite
from pathlib import Path

import accenture_proforma as model


OPERATING_DRIVERS = {
    "growth": "percent",
    "gross_margin": "percent",
    "sga_ratio": "percent",
    "depreciation_ratio": "percent",
    "business_optimization": "USD millions",
    "capex_ratio": "percent",
    "receivable_days": "days",
    "deferred_revenue_ratio": "percent",
}
OUTPUTS = ("operating_income", "fcfe", "per_share")
OUTPUT_NAMES = {
    "operating_income": "Operating profit (USD millions)",
    "fcfe": "FCFE (USD millions)",
    "per_share": "Value (USD/share)",
}


@contextmanager
def independent_inputs(assumptions, opening):
    """Install fresh inputs for one complete run and restore model globals."""
    original_assumptions, original_opening = model.ASSUMPTIONS, model.OPENING
    model.ASSUMPTIONS = copy.deepcopy(assumptions)
    model.OPENING = copy.deepcopy(opening)
    try:
        yield
    finally:
        model.ASSUMPTIONS = original_assumptions
        model.OPENING = original_opening


def _values(driver, scenario):
    values = driver[scenario]
    if not isinstance(values, dict) or set(values) != {str(y) for y in driver["years"]}:
        raise ValueError(f"{driver['key']} {scenario}: provide one value for each selected FY year")
    converted = {}
    for year, value in values.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value):
            raise ValueError(f"{driver['key']} {scenario} FY{year}: value must be finite")
        converted[int(year)] = value / 100 if driver["unit"] == "percent" else value
    return converted


def validate_config(config, base_assumptions):
    if not isinstance(config, dict):
        raise ValueError("Input file must contain a JSON object")
    drivers = config.get("drivers")
    if not isinstance(drivers, list) or len(drivers) != 2:
        raise ValueError("Provide exactly two operating drivers")
    if len({d.get("key") for d in drivers if isinstance(d, dict)}) != 2:
        raise ValueError("The two drivers must be different")
    for driver in drivers:
        if not isinstance(driver, dict) or driver.get("key") not in OPERATING_DRIVERS:
            raise ValueError(f"Choose a listed operating assumption: {', '.join(OPERATING_DRIVERS)}")
        key = driver["key"]
        if driver.get("unit") != OPERATING_DRIVERS[key]:
            raise ValueError(f"{key} unit must be {OPERATING_DRIVERS[key]}")
        years = driver.get("years")
        if not isinstance(years, list) or not years or len(years) != len(set(years)):
            raise ValueError(f"{key}: list unique affected years")
        if any(isinstance(y, bool) or not isinstance(y, int) or y not in model.YEARS for y in years):
            raise ValueError(f"{key}: years must be FY2026-FY2030")
        if not isinstance(driver.get("range_reason"), str) or not driver["range_reason"].strip():
            raise ValueError(f"{key}: explain the lower/higher range")
        lower, higher = _values(driver, "lower"), _values(driver, "higher")
        for year in years:
            base = base_assumptions[key][model.YEARS.index(year)]
            if not lower[year] < base < higher[year]:
                raise ValueError(f"{key} FY{year}: require lower < base < higher")
    record = config.get("locked_prediction")
    required = ("timestamp", "input_change", "expected_direction_and_size", "reason")
    if not isinstance(record, dict) or any(
        not isinstance(record.get(k), str) or not record[k].strip() for k in required
    ):
        raise ValueError("Add a timestamped locked_prediction with input_change, expected_direction_and_size, and reason before running changed inputs")


def run(assumptions, opening):
    """Run the full model; retain statements and visible accounting results."""
    with independent_inputs(assumptions, opening):
        rows = model.project()
        model.assert_balanced(rows)
        last = rows[-1]
        result = {
            "rows": rows,
            "operating_income": last["operating_income"],
            "fcfe": last["fcfe"],
            "per_share": None,
            "valuation_note": "",
        }
        if any(row["fcfe"] <= 0 for row in rows):
            result["valuation_note"] = "Unavailable: at least one annual FCFE is nonpositive; signed FCFE is retained."
        elif last["fcfe"] + last["debt_repayment"] <= 0:
            result["valuation_note"] = "Unavailable: terminal cash flow is nonpositive."
        else:
            result["per_share"] = model.value(rows)["per_share"]
        return result


def changed_assumptions(base, driver, scenario):
    assumptions = copy.deepcopy(base)
    values = _values(driver, scenario)
    for year, value in values.items():
        assumptions[driver["key"]][model.YEARS.index(year)] = value
    # Verify the scenario changes only this independent operating assumption.
    for key in base:
        if key != driver["key"] and assumptions[key] != base[key]:
            raise AssertionError(f"Unexpected independent input change: {key}")
    return assumptions


def fmt(value, unit):
    if value is None:
        return "N/A"
    if unit == "percent":
        return f"{value * 100:.2f}%"
    if unit == "days":
        return f"{value:.1f} days"
    if unit == "USD millions":
        return f"${value:,.1f}m"
    return f"${value:,.2f}/share"


def input_path(assumptions, driver):
    key = driver["key"]
    return ", ".join(
        f"FY{year}E {fmt(assumptions[key][model.YEARS.index(year)], driver['unit'])}"
        for year in driver["years"]
    )


def report(config, base_assumptions, opening, results, restored):
    base = results["base"]
    print("ACCENTURE LAB 11 - ONE-AT-A-TIME SENSITIVITY")
    print("Fiscal years end August 31. Statement values: USD millions; per-share values: USD/share.")
    print("Source model: accenture_proforma.py; inputs and rationale: ACN_Lab10.md.")
    print("\nLOCKED PREDICTION (analyst judgment authorized by student before changed runs)")
    for key, label in (("timestamp", "Timestamp"), ("input_change", "Input old -> new"),
                       ("expected_direction_and_size", "Expected outputs"), ("reason", "Reason")):
        print(f"{label}: {config['locked_prediction'][key]}")
    print("\nBASE INPUTS")
    for d in config["drivers"]:
        print(f"{d['key']}: {input_path(base_assumptions, d)}")
    print("\nSENSITIVITY RESULTS (signed change from base)")
    print("Driver / case | Input path | FY2030E operating profit | Change | FY2030E FCFE | Change | Value/share | Change | Checks")
    print("---|---|---:|---:|---:|---:|---:|---:|---")
    for driver in config["drivers"]:
        key = driver["key"]
        print(f"\n{key} range: {driver['range_reason']}")
        cases = results[key]
        for scenario in ("lower", "base", "higher"):
            entry = cases[scenario]
            assumptions = entry["assumptions"]
            if entry["error"]:
                print(f"{key} / {scenario} | {input_path(assumptions, driver)} | N/A | N/A | N/A | N/A | N/A | N/A | INVALID: {entry['error']}")
                continue
            result = entry["result"]
            delta = lambda name: result[name] - base[name] if result[name] is not None and base[name] is not None else None
            op, fcfe, value = (result[name] for name in OUTPUTS)
            val_text = fmt(value, "USD/share") if value is not None else "N/A"
            print(f"{key} / {scenario} | {input_path(assumptions, driver)} | {op:,.1f} | {delta('operating_income'):+,.1f} | {fcfe:,.1f} | {delta('fcfe'):+,.1f} | {val_text} | {delta('per_share'):+,.2f} | PASS" if value is not None
                  else f"{key} / {scenario} | {input_path(assumptions, driver)} | {op:,.1f} | {delta('operating_income'):+,.1f} | {fcfe:,.1f} | {delta('fcfe'):+,.1f} | N/A | N/A | PASS; {result['valuation_note']}")
        if any(cases[s]["error"] for s in ("lower", "base", "higher")):
            print(f"{key} spans: unavailable because an accounting/model check failed")
        else:
            for name in OUTPUTS:
                valid = [cases[s]["result"][name] for s in ("lower", "base", "higher")
                         if cases[s]["result"][name] is not None]
                unit = "USD/share" if name == "per_share" else "USD millions"
                span = max(valid) - min(valid) if len(valid) >= 2 else None
                print(f"{key} span, {OUTPUT_NAMES[name]}: {fmt(span, unit)}")
    print("Spans and signed changes use unrounded model values; displayed rows can differ by $0.01/share after rounding.")
    print("\nACCOUNTING CHECKS BY RUN AND YEAR (balance gap in USD millions)")
    print("Driver / case | Year | Assets - liabilities - equity | Cash minimum | Revolver")
    print("---|---|---:|---|---")
    for driver in config["drivers"]:
        for scenario in ("lower", "base", "higher"):
            entry = results[driver["key"]][scenario]
            if entry["error"]:
                print(f"{driver['key']} / {scenario} | N/A | N/A | INVALID | {entry['error']}")
                continue
            for row in entry["result"]["rows"]:
                gap = round(row["balance_gap"], 1) + 0.0
                cash_status = "PASS" if row["cash_minimum_met"] else "FAIL"
                revolver_status = "drawn" if row["revolver"] > 0.05 else "not drawn"
                print(f"{driver['key']} / {scenario} | FY{row['year']}E | {gap:.1f} | {cash_status} | {revolver_status}")
    print("\nTRACE: FY2030E base and changed statement links")
    trace_keys = ("revenue", "gross_profit", "sga", "depreciation", "business_optimization",
                  "operating_income", "net_income", "capex", "change_receivables",
                  "change_deferred_revenue", "fcfe", "cash", "balance_gap")
    for driver in config["drivers"]:
        for scenario in ("lower", "higher"):
            entry = results[driver["key"]][scenario]
            if entry["error"]:
                continue
            row = entry["result"]["rows"][-1]
            print(f"{driver['key']} / {scenario}: " + "; ".join(f"{k}={row[k]:,.1f}" for k in trace_keys))
    print("\nRESTORED BASE CHECK")
    same_inputs = (model.ASSUMPTIONS == base_assumptions and model.OPENING == opening)
    same_outputs = all(isclose(restored[name], base[name], rel_tol=0, abs_tol=1e-8)
                       for name in OUTPUTS if base[name] is not None)
    same_rows = all(isclose(restored["rows"][i][name], base["rows"][i][name], rel_tol=0, abs_tol=1e-8)
                    for i in range(len(model.YEARS)) for name in ("revenue", "operating_income", "fcfe", "balance_gap"))
    print(f"Inputs: {'PASS' if same_inputs else 'FAIL'}; outputs and linked rows: {'PASS' if same_outputs and same_rows else 'FAIL'}; absolute tolerance 1e-8 USD millions or USD/share.")
    if not (same_inputs and same_outputs and same_rows):
        raise AssertionError("Restored base differs from the initial base")


def analyze(config):
    base_assumptions = copy.deepcopy(model.ASSUMPTIONS)
    opening = copy.deepcopy(model.OPENING)
    validate_config(config, base_assumptions)
    base = run(base_assumptions, opening)
    results = {"base": base}
    for driver in config["drivers"]:
        key = driver["key"]
        results[key] = {}
        for scenario in ("lower", "base", "higher"):
            assumptions = (copy.deepcopy(base_assumptions) if scenario == "base" else
                           changed_assumptions(base_assumptions, driver, scenario))
            try:
                result, error = run(assumptions, opening), None
            except (AssertionError, ValueError, ZeroDivisionError) as exc:
                result, error = None, str(exc)
            results[key][scenario] = {"assumptions": assumptions, "result": result, "error": error}
    restored = run(base_assumptions, opening)
    report(config, base_assumptions, opening, results, restored)
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_file", type=Path, help="JSON file with two drivers and locked prediction")
    args = parser.parse_args()
    analyze(json.loads(args.input_file.read_text(encoding="utf-8")))


if __name__ == "__main__":
    main()
