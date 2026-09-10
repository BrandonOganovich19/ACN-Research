"""Five-year FCFF discounted cash flow valuation (USD millions)."""

import sys


# Editable inputs (USD millions except rates and per-share value)
STARTING_FCFF = 100.0
GROWTH_RATES = [0.08, 0.06, 0.05, 0.04, 0.03]
WACC = 0.10
TERMINAL_GROWTH = 0.03
NON_OPERATING_CASH = 50.0
DEBT = 300.0
DILUTED_SHARES = 50.0


def main():
    if TERMINAL_GROWTH >= WACC:
        sys.exit("Error: terminal growth must be less than WACC.")
    if len(GROWTH_RATES) != 5:
        sys.exit("Error: enter exactly five yearly growth rates.")
    if DILUTED_SHARES <= 0:
        sys.exit("Error: diluted shares must be greater than zero.")

    fcff_by_year = []
    fcff = STARTING_FCFF
    for growth_rate in GROWTH_RATES:
        fcff *= 1.0 + growth_rate
        fcff_by_year.append(fcff)

    pv_explicit_fcff = sum(
        yearly_fcff / (1.0 + WACC) ** year
        for year, yearly_fcff in enumerate(fcff_by_year, start=1)
    )
    terminal_value_year_5 = (
        fcff_by_year[-1] * (1.0 + TERMINAL_GROWTH)
        / (WACC - TERMINAL_GROWTH)
    )
    pv_terminal_value = terminal_value_year_5 / (1.0 + WACC) ** 5
    enterprise_value = pv_explicit_fcff + pv_terminal_value
    equity_value = enterprise_value + NON_OPERATING_CASH - DEBT
    value_per_diluted_share = equity_value / DILUTED_SHARES
    terminal_value_share = pv_terminal_value / enterprise_value

    for year, yearly_fcff in enumerate(fcff_by_year, start=1):
        print(f"FCFF Year {year} (USD millions): {yearly_fcff:.4f}")
    print(f"Present value of five explicit FCFF (USD millions): {pv_explicit_fcff:.4f}")
    print(f"Terminal value at Year 5 (USD millions): {terminal_value_year_5:.4f}")
    print(f"Present value of terminal value (USD millions): {pv_terminal_value:.4f}")
    print(f"Enterprise value (USD millions): {enterprise_value:.4f}")
    print(f"Equity value (USD millions): {equity_value:.4f}")
    print(f"Value per diluted share (USD): {value_per_diluted_share:.4f}")
    print(f"PV of terminal value as share of enterprise value: {terminal_value_share:.4f}")


if __name__ == "__main__":
    main()
