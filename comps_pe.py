#!/usr/bin/env python3
"""
Lab 07 - Comparable-company P/E policy and implied price range.

Case: Asbury Automotive (ABG) valued off franchised-vehicle-retail peers.
Retrospective training comparison: December 31, 2024 closing prices paired
with FY2024 total GAAP diluted EPS.

Equity-to-equity only. A P/E multiple is a share price divided by a per-share
earnings figure, so it is applied directly to the target's EPS. There is no
cash or debt bridge anywhere in this file, and none belongs in one.

Standard library only. No network access, no installs.
"""

# ----------------------------------------------------------------------
# EDITABLE INPUTS
# ----------------------------------------------------------------------
# price        = closing share price
# diluted_eps  = total GAAP diluted earnings per share for the matching year
# Use None (or any nonpositive number) for a missing / unusable figure.

TARGET = {
    "ticker": "ABG",
    "name": "Asbury Automotive Group",
    "price": 243.03,
    "diluted_eps": 21.50,
}

PEERS = [
    {"ticker": "AN", "name": "AutoNation", "price": 169.84, "diluted_eps": 16.92},
    {"ticker": "GPI", "name": "Group 1 Automotive", "price": 421.48, "diluted_eps": 36.81},
]

# ----------------------------------------------------------------------
# CONSTANTS
# ----------------------------------------------------------------------
NM = "not meaningful"
MULT_DP = 6      # multiples displayed to six decimals
PRICE_DP = 2     # prices displayed to cents
LINE = "-" * 68

# All arithmetic below runs on unrounded floats. Rounding happens only in
# the formatting helpers, at the moment of display.


# ----------------------------------------------------------------------
# HELPERS
# ----------------------------------------------------------------------
def is_usable(value):
    """A figure is usable only if it is a real, positive number."""
    if value is None or isinstance(value, bool):
        return False
    if not isinstance(value, (int, float)):
        return False
    if value != value:  # NaN
        return False
    return value > 0


def pe_ratio(price, eps):
    """Price-to-earnings, or None when either input is missing or nonpositive."""
    if is_usable(price) and is_usable(eps):
        return price / eps
    return None


def median(values):
    """Median of a nonempty list, retaining full precision."""
    ordered = sorted(values)
    n = len(ordered)
    mid = n // 2
    if n % 2 == 1:
        return ordered[mid]
    return (ordered[mid - 1] + ordered[mid]) / 2.0


def fmt_mult(value):
    return NM if value is None else "{:.{dp}f}x".format(value, dp=MULT_DP)


def fmt_price(value):
    return NM if value is None else "${:,.{dp}f}".format(value, dp=PRICE_DP)


def fmt_change(value):
    return NM if value is None else "{:+,.{dp}f}".format(value, dp=PRICE_DP)


def fmt_input(value):
    return "missing/nonpositive" if not is_usable(value) else "{:,.2f}".format(value)


def clean_peer_set(peers, target_ticker):
    """Deduplicate peers by ticker (first occurrence wins) and drop the target."""
    seen = set()
    kept = []
    dropped_dupes = []
    dropped_target = []
    for peer in peers:
        key = str(peer.get("ticker", "")).strip().upper()
        if key == str(target_ticker).strip().upper():
            dropped_target.append(peer)
            continue
        if key in seen:
            dropped_dupes.append(peer)
            continue
        seen.add(key)
        kept.append(peer)
    return kept, dropped_dupes, dropped_target


def implied_price(multiple, target_eps):
    """Implied share price = peer multiple x target EPS."""
    if multiple is None or not is_usable(target_eps):
        return None
    return multiple * target_eps


def median_implied(multiples, target_eps):
    """Median-implied price for a set of peer multiples, or None if empty."""
    if not multiples:
        return None
    return implied_price(median(multiples), target_eps)


# ----------------------------------------------------------------------
# REPORT
# ----------------------------------------------------------------------
def main():
    target_eps = TARGET.get("diluted_eps")
    target_ticker = TARGET.get("ticker", "TARGET")

    print(LINE)
    print("COMPARABLE-COMPANY P/E ANALYSIS")
    print(LINE)
    print("Target: {} ({})".format(TARGET.get("name", ""), target_ticker))
    print("  Price per share:    {}".format(fmt_input(TARGET.get("price"))))
    print("  Diluted EPS:        {}".format(fmt_input(target_eps)))
    target_pe = pe_ratio(TARGET.get("price"), target_eps)
    print("  Current P/E:        {}".format(fmt_mult(target_pe)))
    print()

    peers, dupes, self_refs = clean_peer_set(PEERS, target_ticker)
    for peer in self_refs:
        print("Excluded {}: target cannot be its own peer.".format(peer.get("ticker")))
    for peer in dupes:
        print("Excluded {}: duplicate peer entry.".format(peer.get("ticker")))
    if self_refs or dupes:
        print()

    print("PEER MULTIPLES")
    print(LINE)
    print("{:<6} {:<26} {:>10} {:>10} {:>12}".format(
        "Ticker", "Company", "Price", "EPS", "P/E"))
    usable = []   # list of (ticker, multiple)
    for peer in peers:
        multiple = pe_ratio(peer.get("price"), peer.get("diluted_eps"))
        if multiple is not None:
            usable.append((peer.get("ticker"), multiple))
        print("{:<6} {:<26} {:>10} {:>10} {:>12}".format(
            str(peer.get("ticker", "")),
            str(peer.get("name", ""))[:26],
            fmt_input(peer.get("price")),
            fmt_input(peer.get("diluted_eps")),
            fmt_mult(multiple)))
    print()

    multiples = [m for _, m in usable]

    if not multiples:
        print("No usable peers. Every peer has a missing or nonpositive price or EPS,")
        print("so no peer-implied price can be calculated.")
        print(LINE)
        return

    if not is_usable(target_eps):
        print("Target diluted EPS is missing or nonpositive, so every implied price is")
        print("{}. A negative or near-zero denominator gives a multiple no".format(NM))
        print("comparison can interpret.")
        print(LINE)
        return

    low = min(multiples)
    high = max(multiples)
    mid = median(multiples)
    full_median_price = implied_price(mid, target_eps)

    print("PEER MULTIPLE SUMMARY ({} usable peer{})".format(
        len(multiples), "" if len(multiples) == 1 else "s"))
    print(LINE)
    print("  Minimum P/E:        {}".format(fmt_mult(low)))
    print("  Median P/E:         {}".format(fmt_mult(mid)))
    print("  Maximum P/E:        {}".format(fmt_mult(high)))
    print()

    print("IMPLIED VALUE FOR {} (peer P/E x {} diluted EPS of {:,.2f})".format(
        target_ticker, target_ticker, target_eps))
    print(LINE)
    if len(multiples) == 1:
        only_ticker = usable[0][0]
        print("  Reference estimate: {}".format(fmt_price(full_median_price)))
        print()
        print("  One usable peer ({}) gives a single reference estimate, not a".format(only_ticker))
        print("  range. Minimum, median and maximum all collapse to the same")
        print("  number, so there is no spread to report.")
    else:
        print("  At minimum P/E:     {}".format(fmt_price(implied_price(low, target_eps))))
        print("  At median P/E:      {}".format(fmt_price(full_median_price)))
        print("  At maximum P/E:     {}".format(fmt_price(implied_price(high, target_eps))))
        print()
        print("  Implied range:      {} - {}".format(
            fmt_price(implied_price(low, target_eps)),
            fmt_price(implied_price(high, target_eps))))
    if is_usable(TARGET.get("price")):
        gap = full_median_price - TARGET["price"]
        print("  Vs. actual price:   {} ({} at median)".format(
            fmt_price(TARGET["price"]), fmt_change(gap)))
    print()

    print("LEAVE-ONE-PEER-OUT SENSITIVITY")
    print(LINE)
    print("Baseline median-implied price: {}".format(fmt_price(full_median_price)))
    print()
    print("{:<8} {:>22} {:>22}".format("Removed", "Median-implied", "Change vs. baseline"))
    for removed_ticker, _ in usable:
        remaining = [m for t, m in usable if t != removed_ticker]
        if not remaining:
            print("{:<8} {:>22} {:>22}".format(
                str(removed_ticker), "no estimate", NM))
            continue
        price = median_implied(remaining, target_eps)
        change = price - full_median_price  # unrounded on both sides
        note = ""
        if len(remaining) == 1:
            note = "  (reference estimate, no range)"
        print("{:<8} {:>22} {:>22}{}".format(
            str(removed_ticker), fmt_price(price), fmt_change(change), note))
    print(LINE)


if __name__ == "__main__":
    main()
