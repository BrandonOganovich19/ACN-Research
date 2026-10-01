# ACN valuation – Lab 12 notes

USD billions unless noted. FY ends Aug 31.

## As presenter

## 1\. Selection

* Picked ACN to test whether AI grows demand for its work or squeezes pricing/margins.
* Enough public data (filings, bookings, service mix) for a driver-based model.
* Sept 3 memo: watch-defer (weak Q3 bookings, unclear organic growth).
* Sources: ACN-2026-09-03.md, Project1\_EditionA\_ACN.md

## 2\. Company and evidence

* Consulting + managed services. FY2026A revenue $74.18 (Consulting $36.88, Managed Services $37.30), bookings $84.54.
* Revenue: FY23 $64.11, FY24 $64.90, FY25 $69.67, FY26 $74.18.
* FY23–25 from 10-Ks; FY26 from Oct 1 release (unaudited). Filings in thousands, model in millions.
* Q3 bookings −2%, book-to-bill \~1.03 → Q4 bookings +4% to $22.17, book-to-bill 1.2.
* FY27 guidance: 3–6% local-currency growth (includes acquisitions), 15.9–16.1% op margin.
* Sources: ACN\_Lab10.md, FY2026 earnings release, Counsel-log.pdf (FY25 10-K)

## 3\. Pro-forma

* Opens at FY2025A, forecasts FY26E–FY30E.
* Growth 4% FY26, then 3%/yr (organic judgment, no acquisitions). Gross margin 32% (hist. 31.9–32.6%).
* Receivables 78.5 days; deferred revenue 40.5% of receivables; capex 0.95% → 0.85%; tax 24.5%.
* Key judgments: no acquisition spend, zero optimization costs after FY26.
* FY30E: revenue $81.55, op income $13.18, FCFE $9.73.
* Checks: balance sheet balances every year, cash > $5.0 floor, revolver undrawn, 9 tests pass.
* Sources: ACN\_Lab10.md, accenture\_proforma.py

## 4\. Valuation

* FCFE DCF: 10.56% cost of equity (5.11% + 1.09 × 5.0%), 3.0% terminal growth.
* $111.38 equity value / 612M shares = **$182.00/share** vs. **$177.41** (Sept 24, 2026) → \~2.6% above market. TV = 70.7% of value.
* Equity DCF, so no EV bridge. Limitation: model dated Aug 31, 2025 vs. Sept 2026 price.
* Peers (Oct 10, 2025): CTSH + EPAM P/E → $177.27–$220.65 vs. ACN $240.94. Different method, stale, not averaged.
* Reverse DCF: $177.41 implies \~1.90% FY27–30 growth vs. 3.0% base (everything else held fixed).
* Sources: ACN\_Lab10.md, accenture\_comps.md, comps\_pe.py

## 5\. Sensitivity (Lab 11)

* Growth 2% / 3% / 4% → $177.83 / $182.00 / $186.24 (span $8.40).
* Gross margin 31.9% / 32.0% / 32.6% → $181.34 / $182.00 / $185.96 (span $4.62).
* Trace (3% → 4% growth): +$533.4M FY30 op profit → +$279.7M FCFE → +$4.24/share. Less than predicted because expenses, tax, capex, and receivables rise too.
* Ranking only holds for these ranges; not a probability. Growth + margin together not tested.
* Sources: ACN\_Lab11.md, ACN\_Lab11\_output.txt, accenture\_sensitivity.py

## 6\. Interpretation

* Still watch-defer. Q4 helped, but the $4.59/share gap is smaller than the uncertainty.
* $600M/yr optimization costs → $173.44/share.
* FY26 actuals beat model (revenue $74.18 vs. $72.46, op income $11.41 vs. $11.09); shares \~596M vs. 612M. Need to roll the model forward.
* Would get more positive: organic Consulting growth, book-to-bill > \~1.1. More negative: book-to-bill \~1.0, recurring costs.
* Next: FY27 acquisition contribution, updated share count, AI and revenue per employee.

\---

## As reviewer – Halozyme (HALO)

Partner's case: DCF $117.46 vs. $111.56 (5.3% premium), TV 75.5% of EV, royalty growth main driver ($99.74–$137.90), watch/defer.

Questions to ask:

1. Selection/evidence: Royalties are \~62% of revenue, mostly DARZALEX SC, VYVGART Hytrulo, and Phesgo. What share is the top product, and where in the 10-K does it show that? (If no page, open the 10-K together = evidence check.)
2. Model/valuation: Reverse DCF rates (27.726%, 17.726%...) are 2.274 pts below 30/20/15/10/5, but the current base is 32.5/22.5/17.5/12.5/7.5. Which base did it use, and does the $107 result still apply?
3. Sensitivity/interpretation: Royalty tested ±5 pts vs. SG\&A ±2 pts. Would royalties still rank first with comparable ranges, and what evidence would move you off watch/defer?
* Follow up any thin answer with "what supports that?" and record gaps.

## 

\*\*Disclosure\*\* This material was prepared for a college course for educational purposes only. I am not a financial advisor, and nothing herein constitutes investment advice.

