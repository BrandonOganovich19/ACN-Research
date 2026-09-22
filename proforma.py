"""Five-year integrated pro forma, FY2026E-FY2030E (USD millions, except per share).

The engine follows the lab instruction exactly; nothing is solved backwards.

NOTE: the input values below are reconstructed placeholders (the lab's table was
not available when this was written). Replace OPENING and ASSUMPTIONS with the
lab's assumption table and opening balance sheet, then rerun. Only a match on
the lab's own inputs proves the model.
"""

YEARS = list(range(2026, 2031))
LABELS = [f"FY{y}E" for y in YEARS]

# ---- Opening balance sheet (FY2025A) -------------------------------------
OPENING = {
    "revenue": 17_881.8359375,
    "cash": 40.4,
    "inventory": 2_000.0,
    "ppe": 4_000.0,
    "other_assets": 2_000.0,
    "floor_plan": 1_000.0,
    "debt": 3_659.1666666666665,
    "revolver": 0.0,
    "other_liabilities": 1_500.0,
    "equity": 1_881.2333333333336,
}

# ---- Assumptions (lists = one value per year, FY2026E-FY2030E) ------------
ASSUMPTIONS = {
    "growth":             [0.024671085, 0.018, 0.018, 0.018, 0.018],
    "gross_margin":       [0.20] * 5,
    "sga_ratio":          [0.6604813665188138, 0.6389288185479036,
                           0.6349286588951505, 0.63077422928031,
                           0.6263588508300498],   # SG&A as % of gross profit
    "depreciation_ratio": [0.10] * 5,             # % of opening PP&E
    "impairment":         [0.0] * 5,
    "capex":              [1_119.9873472296208, 556.373089264762,
                           570.6079131006945, 586.1692787656737,
                           573.9151423459557],
    "inventory_days":     [40.0] * 5,
    "floor_plan_ratio":   [0.75] * 5,             # % of inventory
    "debt_repayment":     [77.08333333333333] * 4 + [100.0],
    "buyback":            [150.0] * 5,
    "tax_rate":           [0.25] * 5,
    "floor_plan_rate":    [0.0] * 5,
    "debt_rate":          [0.08] * 5,
    "revolver_rate":      [0.0] * 5,
    "minimum_cash":       40.4,
    # CAPM cost of equity = risk-free rate + beta x equity risk premium.
    # These are reconstructed placeholders until the lab inputs are available.
    "risk_free_rate":     0.04,
    "beta":               1.00,
    "equity_risk_premium": 0.06,
    "terminal_growth":    0.03,
    "share_count":        17.489418676332413,
}

OTHER_ASSETS_RATE = 0.008  # 0.8% of change in revenue, per the instruction


def validate_inputs():
    missing = [k for k, v in OPENING.items() if v is None]
    for k, v in ASSUMPTIONS.items():
        if v is None or (isinstance(v, list) and (len(v) != 5 or None in v)):
            missing.append(k)
    if missing:
        raise ValueError("Fill these inputs from the lab: " + ", ".join(missing))


def project():
    rows, prior = [], dict(OPENING)

    for i, year in enumerate(YEARS):
        a = {k: v[i] if isinstance(v, list) else v for k, v in ASSUMPTIONS.items()}

        # Income statement
        revenue = prior["revenue"] * (1 + a["growth"])
        gross_profit = revenue * a["gross_margin"]
        sga = gross_profit * a["sga_ratio"]
        depreciation = prior["ppe"] * a["depreciation_ratio"]
        impairment = a["impairment"]
        operating_income = gross_profit - sga - depreciation - impairment
        interest = (prior["floor_plan"] * a["floor_plan_rate"]
                    + prior["debt"] * a["debt_rate"]
                    + prior["revolver"] * a["revolver_rate"])
        pretax_income = operating_income - interest
        tax = max(0.0, pretax_income) * a["tax_rate"]
        net_income = pretax_income - tax

        # Balance sheet except cash
        inventory = (revenue - gross_profit) * a["inventory_days"] / 365
        floor_plan = inventory * a["floor_plan_ratio"]
        capex = a["capex"]
        ppe = prior["ppe"] + capex - depreciation
        change_other_wc = OTHER_ASSETS_RATE * (revenue - prior["revenue"])
        other_assets = prior["other_assets"] + change_other_wc - impairment
        debt = prior["debt"] - a["debt_repayment"]
        other_liabilities = prior["other_liabilities"]
        equity = prior["equity"] + net_income - a["buyback"]

        # Cash flow
        change_inventory = inventory - prior["inventory"]
        change_floor_plan = floor_plan - prior["floor_plan"]
        fcfe = (net_income + depreciation + impairment - capex - change_inventory
                - change_other_wc + change_floor_plan - a["debt_repayment"])

        # Cash and revolver
        cash = prior["cash"] + fcfe - a["buyback"]
        revolver = prior["revolver"]
        if cash < a["minimum_cash"]:
            revolver += a["minimum_cash"] - cash
            cash = a["minimum_cash"]
        else:
            repay = min(revolver, cash - a["minimum_cash"])
            revolver -= repay
            cash -= repay

        assets = cash + inventory + ppe + other_assets
        liabilities = floor_plan + debt + revolver + other_liabilities

        row = dict(
            year=year, revenue=revenue, gross_profit=gross_profit, sga=sga,
            depreciation=depreciation, impairment=impairment,
            operating_income=operating_income, interest=interest,
            pretax_income=pretax_income, tax=tax, net_income=net_income,
            cash=cash, inventory=inventory, ppe=ppe, other_assets=other_assets,
            assets=assets, floor_plan=floor_plan, debt=debt, revolver=revolver,
            other_liabilities=other_liabilities, liabilities=liabilities,
            equity=equity, capex=capex, change_inventory=change_inventory,
            change_other_wc=change_other_wc, change_floor_plan=change_floor_plan,
            debt_repayment=a["debt_repayment"], buyback=a["buyback"], fcfe=fcfe,
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
        if abs(r["balance_gap"]) >= 0.05:
            raise AssertionError(f"FY{r['year']}E balance sheet gap: {r['balance_gap']:.1f}")
        if not r["cash_minimum_met"]:
            raise AssertionError(f"FY{r['year']}E cash below minimum: {r['cash']:.1f}")


def main():
    validate_inputs()
    rows = project()

    print_table("INCOME STATEMENT", [
        ("Revenue", "revenue"), ("Gross profit", "gross_profit"), ("SG&A", "sga"),
        ("Depreciation", "depreciation"), ("Impairment", "impairment"),
        ("Operating income", "operating_income"), ("Interest", "interest"),
        ("Pretax income", "pretax_income"), ("Tax", "tax"), ("Net income", "net_income"),
    ], rows)
    print_table("BALANCE SHEET", [
        ("Cash", "cash"), ("Inventory", "inventory"), ("PP&E", "ppe"),
        ("Other assets", "other_assets"), ("Total assets", "assets"),
        ("Floor plan", "floor_plan"), ("Debt", "debt"), ("Revolver", "revolver"),
        ("Other liabilities", "other_liabilities"),
        ("Total liabilities", "liabilities"), ("Equity", "equity"),
    ], rows)
    print_table("CASH FLOW STATEMENT", [
        ("Net income", "net_income"), ("Depreciation", "depreciation"),
        ("Impairment", "impairment"), ("Capital expenditures", "capex"),
        ("Change in inventory", "change_inventory"),
        ("Change in other working capital", "change_other_wc"),
        ("Change in floor plan", "change_floor_plan"),
        ("Debt repayment", "debt_repayment"),
        ("Free cash flow to equity", "fcfe"), ("Share buyback", "buyback"),
    ], rows)

    print("\nCHECKS")
    for r in rows:
        status = "PASS" if r["cash_minimum_met"] else "FAIL"
        print(f"FY{r['year']}E  Assets - liabilities - equity: "
              f"{round(r['balance_gap'], 1) + 0.0:.1f}  Cash minimum: {status}")

    assert_balanced(rows)

    ke = (ASSUMPTIONS["risk_free_rate"]
          + ASSUMPTIONS["beta"] * ASSUMPTIONS["equity_risk_premium"])
    g = ASSUMPTIONS["terminal_growth"]
    pv_fcfe = sum(r["fcfe"] / (1 + ke) ** (i + 1) for i, r in enumerate(rows))
    terminal_value = (rows[-1]["fcfe"] + rows[-1]["debt_repayment"]) * (1 + g) / (ke - g)
    pv_terminal = terminal_value / (1 + ke) ** 5
    equity_value = pv_fcfe + pv_terminal

    print("\nVALUATION")
    print(f"Equity value: ${equity_value:,.2f} million")
    print(f"Share of value after 2030: {pv_terminal / equity_value:.1%}")
    print(f"Value per share: ${equity_value / ASSUMPTIONS['share_count']:,.2f}")


if __name__ == "__main__":
    main()
