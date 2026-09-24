"""Five-year integrated pro forma for Accenture plc (NYSE: ACN), FY2026E-FY2030E.

USD millions, except per-share values. Accenture's fiscal year ends August 31.

Adapted from proforma.py (ABG). SG&A is calibrated to margin guidance; cash is
calculated from cash flows, never plugged to balance the statements. Accenture's lines
are swapped in where ABG's do not exist:

  ABG line            Accenture line (and why)
  -----------------   ---------------------------------------------------------
  Inventory           Receivables and contract assets, in days of revenue.
                      Accenture sells people's time, so its working asset is
                      unbilled and billed work, not cars on a lot.
  Floor plan          Deferred revenues (clients paying in advance), as a % of
                      receivables, at 0% interest. It funds the receivables the
                      way floor plan funds ABG's inventory. Accenture itself nets
                      the two when it reports DSO (47 days at Aug 31, 2025).
  (none)              Interest income on opening cash (Accenture holds ~$11.5B).
  (none)              Business optimization: cash severance, not an add-back.
  (none)              Dividends. ABG pays none; Accenture pays ~$4B a year.

Opening balance sheet: Accenture FY2025 Form 10-K, balance sheet at Aug 31, 2025.
Every assumption is labelled (history / guidance / judgment) with its reason in
ACN_Lab10.md.

Run:  python accenture_proforma.py
Proof the check refuses:  python accenture_proforma.py --break-test
"""

import sys
from math import isfinite

YEARS = list(range(2026, 2031))
LABELS = [f"FY{y}E" for y in YEARS]

# ---- Opening balance sheet, FY2025A (Aug 31, 2025), FY2025 10-K -----------
TOTAL_ASSETS_FY25 = 65_394.897
TOTAL_LIABILITIES_FY25 = 20_352.097 + 12_801.833   # current + non-current

_cash = 11_478.729 + 5.945          # cash and equivalents + short-term investments
_receivables = 14_985.073           # receivables and contract assets (current)
_ppe = 1_566.374                    # property and equipment, net
_deferred_revenue = 6_073.170       # deferred revenues
_debt = 114.484 + 5_034.169         # current portion + long-term debt

OPENING = {
    "revenue": 69_672.977,
    "cash": _cash,
    "receivables": _receivables,
    "ppe": _ppe,
    # Goodwill 22,536.4, lease assets, other current and non-current assets
    "other_assets": TOTAL_ASSETS_FY25 - _cash - _receivables - _ppe,
    "deferred_revenue": _deferred_revenue,
    "debt": _debt,
    "revolver": 0.0,
    # Accounts payable, accrued payroll, lease liabilities, other liabilities
    "other_liabilities": TOTAL_LIABILITIES_FY25 - _deferred_revenue - _debt,
    # Total shareholders' equity, including noncontrolling interests
    "equity": 32_240.967,
}

# ---- Assumptions (lists = one value per year, FY2026E-FY2030E) ------------
ASSUMPTIONS = {
    "growth":                 [0.040, 0.030, 0.030, 0.030, 0.030],  # organic + FX, USD
    "gross_margin":           [0.320] * 5,
    "sga_ratio":              [0.482, 0.479, 0.476, 0.473, 0.470],  # SG&A ex-depreciation, % of GP
    "depreciation_ratio":     [0.39] * 5,                           # % of opening PP&E
    "impairment":             [0.0] * 5,
    "business_optimization":  [307.541, 0.0, 0.0, 0.0, 0.0],        # cash severance
    "capex_ratio":            [0.0095, 0.0085, 0.0085, 0.0085, 0.0085],  # % of revenue
    "receivable_days":        [78.5] * 5,                           # days of revenue
    "deferred_revenue_ratio": [0.405] * 5,                          # % of receivables
    "debt_repayment":         [0.0] * 5,                            # notes refinanced
    "dividends":              [round(4_008.0 * 1.07 ** i, 1) for i in range(5)],
    "buyback":                [2_000.0, 4_500.0, 4_500.0, 4_500.0, 4_500.0],
    "tax_rate":               [0.245] * 5,
    "deferred_revenue_rate":  [0.0] * 5,
    "debt_rate":              [0.052] * 5,
    "revolver_rate":          [0.055] * 5,
    "cash_yield":             [0.032] * 5,
    "other_wc_rate":          0.0,        # other assets / other liabilities held flat
    "minimum_cash":           5_000.0,
    # CAPM cost of equity = risk-free rate + beta x equity risk premium
    "risk_free_rate":         0.0511,     # U.S. Treasury 10-yr, Sep 23, 2026
    "beta":                   1.09,       # StockAnalysis, Sep 24, 2026
    "equity_risk_premium":    0.050,
    "terminal_growth":        0.030,
    "nci_share":              0.019,      # share of net income owed to minority holders (Avanade)
    "share_count":            612.0,      # millions, total shares outstanding at May 31, 2026
    "market_price":           177.41,     # USD closing price, Sep 24, 2026 (Yahoo Finance)
}


def validate_inputs():
    missing = [k for k, v in OPENING.items() if v is None]
    for k, v in ASSUMPTIONS.items():
        if v is None or (isinstance(v, list) and (len(v) != 5 or None in v)):
            missing.append(k)
    if missing:
        raise ValueError("Fill these inputs: " + ", ".join(missing))
    for name, inputs in (("Opening", OPENING), ("Assumption", ASSUMPTIONS)):
        for key, item in inputs.items():
            values = item if isinstance(item, list) else [item]
            if any(isinstance(v, bool) or not isinstance(v, (int, float))
                   or not isfinite(v) for v in values):
                raise ValueError(f"{name} {key} must contain finite numbers")
    ke = ASSUMPTIONS["risk_free_rate"] + ASSUMPTIONS["beta"] * ASSUMPTIONS["equity_risk_premium"]
    if not -1 < ASSUMPTIONS["terminal_growth"] < ke or ke <= -1:
        raise ValueError("Require -100% < terminal growth < cost of equity")
    if ASSUMPTIONS["share_count"] <= 0:
        raise ValueError("Share count must be positive")
    if not 0 <= ASSUMPTIONS["nci_share"] < 1:
        raise ValueError("Minority share must be between zero and one (exclusive of one)")
    if ASSUMPTIONS["minimum_cash"] < 0:
        raise ValueError("Minimum cash cannot be negative")
    gap = (sum(OPENING[k] for k in ("cash", "receivables", "ppe", "other_assets"))
           - sum(OPENING[k] for k in ("deferred_revenue", "debt", "revolver",
                                      "other_liabilities", "equity")))
    if abs(gap) >= 0.05:
        raise ValueError(f"Opening balance sheet does not balance: gap {gap:.1f}")


def project(broken_link=False):
    validate_inputs()
    rows, prior = [], dict(OPENING)

    for i, year in enumerate(YEARS):
        a = {k: v[i] if isinstance(v, list) else v for k, v in ASSUMPTIONS.items()}

        # Income statement
        revenue = prior["revenue"] * (1 + a["growth"])
        gross_profit = revenue * a["gross_margin"]
        sga = gross_profit * a["sga_ratio"]
        depreciation = prior["ppe"] * a["depreciation_ratio"]
        impairment = a["impairment"]
        business_optimization = a["business_optimization"]
        operating_income = (gross_profit - sga - depreciation - impairment
                            - business_optimization)
        interest_expense = (prior["deferred_revenue"] * a["deferred_revenue_rate"]
                            + prior["debt"] * a["debt_rate"]
                            + prior["revolver"] * a["revolver_rate"])
        interest_income = prior["cash"] * a["cash_yield"]
        pretax_income = operating_income - interest_expense + interest_income
        tax = max(0.0, pretax_income) * a["tax_rate"]
        net_income = pretax_income - tax

        # Balance sheet except cash
        receivables = revenue * a["receivable_days"] / 365
        deferred_revenue = receivables * a["deferred_revenue_ratio"]
        capex = revenue * a["capex_ratio"]
        ppe = prior["ppe"] + capex - depreciation
        change_other_wc = a["other_wc_rate"] * (revenue - prior["revenue"])
        other_assets = prior["other_assets"] + change_other_wc - impairment
        debt = prior["debt"] - a["debt_repayment"]
        other_liabilities = prior["other_liabilities"]
        equity = prior["equity"] + net_income - a["dividends"] - a["buyback"]

        # Cash flow
        change_receivables = receivables - prior["receivables"]
        change_deferred_revenue = deferred_revenue - prior["deferred_revenue"]
        if broken_link:          # --break-test only: drop one link on purpose
            change_deferred_revenue = 0.0
        fcfe = (net_income + depreciation + impairment - capex - change_receivables
                - change_other_wc + change_deferred_revenue - a["debt_repayment"])

        # Cash and revolver
        cash = prior["cash"] + fcfe - a["dividends"] - a["buyback"]
        revolver = prior["revolver"]
        if cash < a["minimum_cash"]:
            revolver += a["minimum_cash"] - cash
            cash = a["minimum_cash"]
        else:
            repay = min(revolver, cash - a["minimum_cash"])
            revolver -= repay
            cash -= repay

        assets = cash + receivables + ppe + other_assets
        liabilities = deferred_revenue + debt + revolver + other_liabilities

        row = dict(
            year=year, revenue=revenue, gross_profit=gross_profit, sga=sga,
            depreciation=depreciation, impairment=impairment,
            business_optimization=business_optimization,
            operating_income=operating_income, interest_expense=interest_expense,
            interest_income=interest_income, pretax_income=pretax_income, tax=tax,
            net_income=net_income, cash=cash, receivables=receivables, ppe=ppe,
            other_assets=other_assets, assets=assets,
            deferred_revenue=deferred_revenue, debt=debt, revolver=revolver,
            other_liabilities=other_liabilities, liabilities=liabilities,
            equity=equity, capex=capex, change_receivables=change_receivables,
            change_other_wc=change_other_wc,
            change_deferred_revenue=change_deferred_revenue,
            debt_repayment=a["debt_repayment"], dividends=a["dividends"],
            buyback=a["buyback"], fcfe=fcfe,
            opening_cash=prior["cash"],
            net_revolver_borrowing=revolver - prior["revolver"],
            change_cash=cash - prior["cash"],
            balance_gap=assets - liabilities - equity,
            cash_minimum_met=cash >= a["minimum_cash"] - 1e-9,
        )
        rows.append(row)
        prior = row

    return rows


def print_table(title, lines, rows):
    print(f"\n{title}")
    print(f"{'Line':<34}" + "".join(f"{l:>12}" for l in LABELS))
    print("-" * (34 + 12 * len(LABELS)))
    for label, key in lines:
        print(f"{label:<34}" + "".join(f"{round(r[key], 1) + 0.0:>12,.1f}" for r in rows))


def assert_balanced(rows):
    for r in rows:
        if any(not isfinite(v) for v in r.values() if isinstance(v, (int, float))):
            raise AssertionError(f"FY{r['year']}E contains a non-finite result")
        if abs(r["balance_gap"]) >= 0.05:
            raise AssertionError(f"FY{r['year']}E balance sheet gap: {r['balance_gap']:.1f}")
        if not r["cash_minimum_met"]:
            raise AssertionError(f"FY{r['year']}E cash below minimum: {r['cash']:.1f}")


def value(rows):
    """Lab convention: omit negative annual FCFE and any nonpositive terminal base."""
    validate_inputs()
    assert_balanced(rows)
    if len(rows) != len(YEARS):
        raise ValueError("Valuation requires all five projected years")
    a = ASSUMPTIONS
    ke = a["risk_free_rate"] + a["beta"] * a["equity_risk_premium"]
    g = a["terminal_growth"]
    negative = [r["year"] for r in rows if r["fcfe"] < 0]
    pv_fcfe = sum(max(r["fcfe"], 0.0) / (1 + ke) ** (i + 1) for i, r in enumerate(rows))
    terminal_base = rows[-1]["fcfe"] + rows[-1]["debt_repayment"]
    if rows[-1]["fcfe"] <= 0 or terminal_base <= 0:
        terminal_value = 0.0   # a perpetuity of a negative cash flow is not a value
    else:
        terminal_value = terminal_base * (1 + g) / (ke - g)
    pv_terminal = terminal_value / (1 + ke) ** len(rows)
    equity_value = (pv_fcfe + pv_terminal) * (1 - a["nci_share"])
    return dict(ke=ke, negative=negative, pv_fcfe=pv_fcfe, pv_terminal=pv_terminal,
                equity_value=equity_value, per_share=equity_value / a["share_count"])


def main():
    validate_inputs()

    if "--break-test" in sys.argv:
        print("BREAK TEST: change in deferred revenue removed from the cash flow.")
        assert_balanced(project(broken_link=True))   # expected to raise
        return

    rows = project()

    print("ACCENTURE PLC (NYSE: ACN) - PRO FORMA, USD MILLIONS, FISCAL YEARS END AUG 31")
    print_table("INCOME STATEMENT", [
        ("Revenue", "revenue"), ("Gross profit", "gross_profit"),
        ("SG&A (ex-depreciation)", "sga"), ("Depreciation", "depreciation"),
        ("Impairment", "impairment"),
        ("Business optimization", "business_optimization"),
        ("Operating income", "operating_income"),
        ("Interest expense", "interest_expense"),
        ("Interest income", "interest_income"),
        ("Pretax income", "pretax_income"), ("Tax", "tax"),
        ("Net income", "net_income"),
    ], rows)
    print_table("BALANCE SHEET", [
        ("Cash", "cash"), ("Receivables & contract assets", "receivables"),
        ("PP&E", "ppe"), ("Other assets", "other_assets"),
        ("Total assets", "assets"),
        ("Deferred revenues", "deferred_revenue"), ("Debt", "debt"),
        ("Revolver", "revolver"), ("Other liabilities", "other_liabilities"),
        ("Total liabilities", "liabilities"), ("Equity", "equity"),
    ], rows)
    print_table("CASH FLOW STATEMENT", [
        ("Net income", "net_income"), ("Depreciation", "depreciation"),
        ("Impairment", "impairment"), ("Capital expenditures", "capex"),
        ("Change in receivables", "change_receivables"),
        ("Change in other working capital", "change_other_wc"),
        ("Change in deferred revenues", "change_deferred_revenue"),
        ("Debt repayment", "debt_repayment"),
        ("Free cash flow to equity", "fcfe"), ("Dividends", "dividends"),
        ("Share buyback", "buyback"),
        ("Net revolver borrowing", "net_revolver_borrowing"),
        ("Change in cash", "change_cash"),
        ("Opening cash", "opening_cash"), ("Closing cash", "cash"),
    ], rows)

    print("\nCHECKS")
    for r in rows:
        status = "PASS" if r["cash_minimum_met"] else "FAIL"
        revolver = "drawn" if r["revolver"] > 0.05 else "not drawn"
        print(f"FY{r['year']}E  Assets - liabilities - equity: "
              f"{round(r['balance_gap'], 1) + 0.0:.1f}  Cash minimum: {status}  "
              f"Revolver: {revolver}")

    assert_balanced(rows)

    v = value(rows)
    a = ASSUMPTIONS
    print("\nVALUATION")
    if v["negative"]:
        print("Negative FCFE in: " + ", ".join(f"FY{y}E" for y in v["negative"]))
    print(f"Cost of equity: {v['ke']:.2%}  Terminal growth: {a['terminal_growth']:.1%}")
    print(f"Equity value to Accenture plc holders: ${v['equity_value']:,.2f} million")
    total_pv = v['pv_fcfe'] + v['pv_terminal']
    terminal_share = f"{v['pv_terminal'] / total_pv:.1%}" if total_pv else "N/A (zero value)"
    print(f"Share of value after 2030: {terminal_share}")
    print(f"Value per share: ${v['per_share']:,.2f}  "
          f"(market ${a['market_price']:,.2f}, same {a['share_count']:,.0f}M shares)")


if __name__ == "__main__":
    main()
# Disclaimer: I am not a financial professional. The information and opinions
# presented here are for educational purposes only and should not be used to
# make financial decisions. This project was created using Codex.
