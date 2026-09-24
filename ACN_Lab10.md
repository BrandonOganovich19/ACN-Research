# Lab 10 — Pro-Forma: Accenture plc (NYSE: ACN)

**Question:** What are five years of Accenture's statements worth, built from assumptions I can defend?

**Answer:** $182.00 per share (model) against $177.41 (market close, Sept. 24, 2026), on the same 612 million shares.

Units: USD millions unless stated. Accenture's fiscal year ends **August 31**. Projection years FY2026E–FY2030E; opening balance sheet is FY2025A (Aug 31, 2025). Model file: `accenture\_proforma.py` (adapted from `proforma.py`).

**ABG baseline rerun:** `python proforma.py` ran successfully before the company-specific model, printed zero balance-sheet gaps and cash-floor passes for FY2026E–FY2030E, and reproduced the baseline value of $291.75 per share.

\---

## The line that makes Accenture different

**One sentence:** Accenture has no inventory and no floor plan — its working asset is receivables from clients, and the line that funds it is **deferred revenues** (clients paying in advance), so in my model the floor-plan row becomes deferred revenues at 40.5% of receivables and 0% interest.

**What it does to the model:** ABG's inventory (days of cost of sales) becomes receivables (days of revenue), and ABG's floor plan (a % of inventory, with an interest rate) becomes deferred revenues (a % of receivables, free). Each year receivables grow with revenue and use cash, and deferred revenues grow with receivables and give about 40% of that cash back — interest-free. Accenture itself treats the two as a pair: the DSO it reports nets deferred revenue against receivables (my calculation gives 41.7, 47.8 and 46.7 days for FY23–FY25, against the 42, 46 and 47 days the company reports).

\---

## R1 — History grid (three 10-Ks)

Figures are from the audited consolidated statements in Accenture's FY2023, FY2024, and FY2025 Forms 10-K. Earnings-release exhibits provide a cross-check. The two personal filing checks are recorded in the checked table below.

|Line|FY2023|FY2024|FY2025|Source|
|-|-:|-:|-:|-|
|Revenue|64,111.7|64,896.5|69,673.0|FY2023, FY2024, and FY2025 10-K Consolidated Income Statements; FY2025 and FY2024 also in FY2025 Note 17|
|Gross profit (revenue − cost of services)|20,731.6|21,162.3|22,235.4|Computed from the FY2023, FY2024, and FY2025 10-K Income Statements; cost of services 43,380.1 / 43,734.1 / 47,437.6|
|SG\&A (sales \& marketing + G\&A)|10,858.6|11,128.0|11,394.4|FY2023, FY2024, and FY2025 10-K Income Statements (S\&M 6,582.6 / 6,846.7 / 7,043.4; G\&A 4,275.9 / 4,281.3 / 4,351.0)|
|Net income (total, incl. NCI)|7,003.5|7,419.2|7,832.4|FY2023, FY2024, and FY2025 10-K Income Statements; FY2025 and FY2024 also in FY2025 Note 17|
|Net income attributable to Accenture plc|6,871.6|7,264.8|7,678.4|FY2023, FY2024, and FY2025 10-K Income Statements|
|Inventory|none|none|none|FY2023, FY2024, and FY2025 10-K Balance Sheets contain no inventory line; Accenture's working asset is below|
|Receivables \& contract assets (current)|12,227.2|13,664.8|14,985.1|FY2023, FY2024, and FY2025 10-K Consolidated Balance Sheets|
|PP\&E, net|1,530.0|1,521.1|1,566.4|FY2023, FY2024, and FY2025 10-K Balance Sheets and Note 5 (Property and Equipment)|
|Total shareholders' equity (incl. NCI)|26,458.6|29,168.2|32,241.0|FY2023, FY2024, and FY2025 10-K Balance Sheets (Accenture plc only: 25,692.8 / 28,288.6 / 31,195.4)|

Filing each column comes from: FY2025 column — FY2025 Form 10-K (filed Oct 2025); FY2024 column — FY2024 Form 10-K (also the comparative column of FY2025); FY2023 column — FY2023 Form 10-K (also the comparative column of FY2024).

**Checked by hand (me, in the filing):**

|Item|Value I expect|Where I looked|Match?|
|-|-:|-|-|
|FY2025 revenue|69,672,977 (thousands)|FY2025 10-K, Consolidated Income Statement|☑|
|FY2023 total shareholders' equity|26,458,593 (thousands)|FY2023 10-K, Consolidated Balance Sheet|☑|

**Prior-year base confirmed:** FY2022 revenue was $61,594.305 million in the FY2023 10-K; it is used only to compute FY2023 reported growth.

\---

## R2 — Ratios (three years)

|Ratio|FY2023|FY2024|FY2025|Note|
|-|-:|-:|-:|-|
|Gross margin|32.3%|32.6%|31.9%|FY26 first nine months: 32.1%|
|SG\&A ÷ gross profit (as reported)|52.4%|52.6%|51.2%||
|Model expense proxy: (SG\&A − total depreciation) ÷ gross profit|49.4%|50.0%|48.4%|Analytical adjustment, not a reported SG\&A measure; see assumption table|
|Receivable days (receivables ÷ revenue × 365)|69.6|76.9|78.5|Replaces inventory days|
|Deferred revenues ÷ receivables|40.1%|37.9%|40.5%|Replaces floor plan ÷ inventory|
|Depreciation ÷ opening PP\&E|37.4%|35.8%|40.9%|Depreciation 620.7 / 547.9 / 622.5 divided by prior-year PP\&E of 1,659.1 / 1,530.0 / 1,521.1; matches the engine's opening-PP\&E convention|
|Effective tax rate|23.4%|23.5%|23.7%|Tax ÷ pretax income|
|Reported revenue growth (USD)|4.1%|1.2%|7.4%|Computed from 10-K revenue; FY2022 revenue was 61,594.3|
|Local-currency growth|8%|2%|7%|10-K MD\&A / earnings releases|
|Organic growth (ex-acquisitions)|not disclosed|not disclosed|about 4%|See note below|

**Capital spending — filing vs data provider:**

||FY2023|FY2024|FY2025|
|-|-:|-:|-:|
|Filing: "Purchases of property and equipment" (cash flow statement)|528.2|516.5|600.0|
|Data provider (StockAnalysis / S\&P Global, "Capital Expenditures")|528.17|516.51|600.04|
|Capex ÷ revenue|0.82%|0.80%|0.86%|

Capital spending is shown above as a positive outflow magnitude. The provider's cash-flow field displays negative signs: −528.17, −516.51, and −600.04. Source: [StockAnalysis cash-flow statement](https://stockanalysis.com/stocks/acn/financials/cash-flow-statement/).

The displayed capital-spending amounts match after rounding. **Unresolved provider reconciliation:** the previously captured operating-income field of 10,854 differs from the filing's 10,225.664 by 628.336; removing the 615.324 business-optimization charge alone gives 10,840.988, not 10,854. I do not claim that this charge fully explains the provider field, and I use the filing figures in the history grid. The provider's 7,678 net-income figure represents income attributable to Accenture plc, rather than consolidated net income of 7,832.4.

**Organic growth — how Accenture discloses it.** The 10-K MD\&A does not give an organic figure; it reports growth in U.S. dollars and in **local currency** (which strips out exchange rates but not acquisitions). The acquisition piece ("inorganic contribution") is given by management on the earnings calls: a bit more than 3% for FY2025 (so organic about 4% of the 7%), and about 1.5% expected for FY2026. So for Accenture, the "stores already owned" growth = local-currency growth − inorganic contribution.

\---

## R3 — Assumption set

Label key: **history** = taken from the three 10-Ks (or FY26 10-Q run-rate); **guidance** = management's FY2026 outlook; **judgment** = my call, with my reason.

|Assumption|Value (FY26E → FY30E)|Label|Reason|
|-|-|-|-|
|Revenue growth, FY26|4.0%|guidance / judgment|Guidance is 3–4% local currency (June 2026); I take the 3.5% midpoint, subtract the \~1.5% that comes from acquisitions, and add the \~2% FX tailwind management guided. Removing acquisition growth because the model has no acquisition spending is my judgment.|
|Revenue growth, FY27–FY30|3.0%|judgment|Organic only, because my model spends nothing on acquisitions — taking bought growth without paying for it would overstate value. 3% sits between organic of \~4% in FY25 and \~2% in FY26, and AI can cut both ways on Accenture's hours.|
|Gross margin|32.0%|history|Three-year range 31.9–32.6%; the first nine months of FY26 ran 32.1%.|
|SG\&A expense proxy ÷ gross profit, FY26|48.2%|guidance / judgment|Calibrated to approximate management's 15.3% GAAP operating-margin guidance (model: 15.31%); 48.2% itself is not management guidance. I subtract total depreciation from reported SG\&A as a modelling convention and then deduct depreciation separately. This preserves aggregate operating income but is not a claim that all depreciation is reported in SG\&A; some may be in cost of services.|
|SG\&A ex-depreciation ÷ gross profit, FY27–FY30|47.9%, 47.6%, 47.3%, 47.0%|judgment|Falling 0.3 pt of gross profit a year = about 10 bps of margin a year, the low end of the 10–30 bps expansion Accenture has guided each year.|
|Depreciation ÷ opening PP\&E|39%|history / judgment|Three-year opening-PP\&E average is 38.0% (range 35.8–40.9%); I round to 39% because FY2025 was 40.9% and computers and software wear out quickly.|
|Impairment|0|judgment|The FY25 impairment ($271M, two divestitures) is already in the opening balance sheet; none is announced.|
|Business optimization (cash severance)|307.5 in FY26, then 0|history / judgment|FY26 figure is the actual Q1 FY26 charge from the 10-Q; the program was completed in Q1. It is cash severance, so it is expensed and **not** added back. Zero after is judgment — see the weakness I flag below.|
|Capex ÷ revenue|0.95% FY26; 0.85% after|guidance / history|FY26: management guides \~$0.7B of property and equipment additions. After: three-year history of 0.80–0.86%.|
|Receivable days (replaces inventory days)|78.5|history|FY2025 level (FY23 69.6, FY24 76.9); DSO rose again to 48 days by May 2026, so I do not assume it improves.|
|**Deferred revenues ÷ receivables (replaces floor plan)**|**40.5%, at 0% interest**|history|FY2025 level; three years 37.9–40.5%, and May 2026 was 40.7%. Clients prepay, so this funding costs nothing. This is my company-specific line.|
|Other assets / other liabilities|held flat (rate 0)|judgment|They hold goodwill, leases, payroll accruals and payables. With no acquisitions in the model, goodwill does not move; holding the rest flat is conservative (accrued payroll would actually grow with revenue and give cash). I did not copy ABG's 0.8% rule — that was ABG's instruction.|
|Debt|5,148.7 held; repayment 0|judgment|$5B of notes issued in FY2025; management said it expects to go back to the debt market, so I assume maturities are refinanced, not paid down.|
|Interest rate on debt|5.2%|history|FY26 nine-month interest expense (199.6) annualized ÷ debt.|
|Interest income on cash|3.2% of opening cash|history|FY26 nine-month interest income (259.8) annualized ÷ average cash. ABG's engine had no such line; Accenture's $11.5B of cash earns real income.|
|Revolver rate|5.5%|judgment|Scenario assumption 0.3 percentage points above the model's 5.2% existing-debt cost to allow for incremental borrowing costs; not a quoted facility rate. It has no effect in the base case because the revolver is never drawn.|
|Tax rate|24.5%|guidance|Midpoint of the 24–25% FY26 guidance; history was 23.4–23.7%, and I keep the higher guided rate after FY26 because the new global minimum tax is pushing it up.|
|Minimum cash|5,000|history|Accenture ran the business at $5.0B of cash at Aug 31, 2024, the low point of my three years.|
|Dividends|4,008 in FY26, +7% a year|guidance / judgment|FY26: $3,012.8 paid in nine months + Q4 dividend of $1.63 × \~611M shares. Growth: slower than the last 10% raise because the payout is already \~47% of earnings.|
|Share buyback (beyond employee-share offset)|2,000 in FY26; 4,500 after|guidance / judgment|I charge share-based pay as a real cost and do not add it back, so this line is only buybacks beyond those that cancel employee shares (history: 916 / 1,165 / 1,172 = purchases − issuance proceeds − share-based pay). FY26: $9.5B guided capital return − 4.0 dividends − \~1.4 share issuance − \~2.1 share-based pay. After FY26: the \~$3B a year Accenture would spend on acquisitions is not spent in my organic-only model, so it goes back to shareholders; this keeps cash near $13.4B instead of piling up.|
|Risk-free rate|5.11%|judgment|Official U.S. Treasury 10-year par yield, Sept. 23, 2026.|
|Beta|1.09|judgment|StockAnalysis, Sept 24, 2026 (Yahoo shows 1.07).|
|Equity risk premium|5.0%|judgment|Middle of the 4–6% range commonly used. Cost of equity = 5.11% + 1.09 × 5.0% = 10.56%.|
|Terminal growth|3.0%|judgment|Same as my organic growth and roughly long-run nominal GDP; well below the 10.56% cost of equity.|
|Minority interest (Avanade)|1.9% of equity value|history|FY25 net income to "noncontrolling interests – other" was 146.7 of 7,832.4. That slice of FCFE is not Accenture plc shareholders'.|
|Share count|612 million|history|Total shares outstanding at May 31, 2026 (Q3 FY26 release). Same count used for the market comparison.|

**Weakest judgment I would expect to be attacked:** business optimization at zero after FY26 — Accenture has booked a "one-time" program in FY23 (1,063), FY24 (438), FY25 (615) and FY26 (308).

\---

## Opening balance sheet (FY2025A, Aug 31, 2025, FY2025 10-K)

|Engine line|Value|Built from|
|-|-:|-|
|Cash|11,484.7|Cash and equivalents 11,478.7 + short-term investments 5.9|
|Receivables \& contract assets|14,985.1|Current receivables and contract assets|
|PP\&E|1,566.4|Property and equipment, net|
|Other assets|37,358.8|Total assets 65,394.9 less the three lines above (goodwill 22,536.4, leases, other)|
|**Total assets**|**65,394.9**||
|Deferred revenues|6,073.2|Deferred revenues|
|Debt|5,148.7|Current portion 114.5 + long-term debt 5,034.2|
|Revolver|0.0||
|Other liabilities|21,932.1|Total liabilities 33,153.9 less deferred revenues and debt|
|Equity|32,241.0|Total shareholders' equity incl. noncontrolling interests|
|**Total liabilities + equity**|**65,394.9**||

The model refuses to run if this opening sheet does not balance.

The separate deferred-revenue line models **current** deferred revenue only. FY2025 non-current deferred revenue of $642.361 million remains within other liabilities and is held flat; this is why the model ratio uses $6,073.170 million rather than total deferred revenue.

\---

## I / V — Output and check block

`python accenture\_proforma.py`

||FY2026E|FY2027E|FY2028E|FY2029E|FY2030E|
|-|-:|-:|-:|-:|-:|
|Revenue|72,459.9|74,633.7|76,872.7|79,178.9|81,554.3|
|Operating income|11,092.5|11,801.8|12,251.5|12,708.4|13,176.1|
|Net income|8,450.2|9,034.1|9,373.0|9,717.6|10,070.3|
|Free cash flow to equity|8,012.2|8,762.7|9,071.6|9,393.7|9,728.6|
|Cash|13,488.9|13,463.0|13,445.8|13,429.5|13,404.4|
|Total assets|68,075.4|68,510.3|68,989.5|69,498.0|70,021.4|

```
CHECKS
FY2026E  Assets - liabilities - equity: 0.0  Cash minimum: PASS  Revolver: not drawn
FY2027E  Assets - liabilities - equity: 0.0  Cash minimum: PASS  Revolver: not drawn
FY2028E  Assets - liabilities - equity: 0.0  Cash minimum: PASS  Revolver: not drawn
FY2029E  Assets - liabilities - equity: 0.0  Cash minimum: PASS  Revolver: not drawn
FY2030E  Assets - liabilities - equity: 0.0  Cash minimum: PASS  Revolver: not drawn

VALUATION
Cost of equity: 10.56%  Terminal growth: 3.0%
Equity value to Accenture plc holders: $111,384.43 million
Share of value after 2030: 70.7%
Value per share: $182.00  (market $177.41, same 612M shares)
```

The check block reads zero every year, cash never falls below the $5.0B floor, and **no year draws the revolver**. FCFE is positive in every year, so no year is marked "negative FCFE" (the code would flag it, value only positive years, and refuse to put a terminal value on a negative cash flow, because a perpetuity of losses is not a price anyone pays).

**The model refuses when broken.** `python accenture\_proforma.py --break-test` removes the change in deferred revenues from the cash flow (one broken link) and the model stops with:

```
AssertionError: FY2026E balance sheet gap: -238.3
```

The gap is exactly the FY26 change in deferred revenues — the check names the year and the link. The check is never silenced.

Additional verification: `python -m unittest -v test\_accenture\_proforma` passes seven tests covering the base valuation and cash reconciliation, broken cash-flow link, opening balance-sheet gap, invalid valuation inputs, revolver drawing and repayment, all-negative FCFE, and the partner sensitivity. The base case remains $182.00 per share.

**Price sentence:** The model says **$182.00** per share; the market says **$177.41** at the Sept. 24, 2026 close, on the same 612 million shares — so what is the market assuming about AI's effect on Accenture's hours and pricing that my 3% organic growth is not? (FY2026 actual results are released Oct. 1, 2026; FY2026E should be re-checked against them.)

\---

## E — Partner review

*Review partner: Claude (AI), acting as my partner for this section.*

**Completion status:** This is disclosed AI practice feedback. The lab describes a reciprocal class-partner review; acceptance of an AI substitute has not been established. My attack on my KKR partner's table and their answer are recorded below.

**Partner's attack on my judgment label:** *"Why that number, and what would change it?"* — on: **Business optimization = 0 in FY2027E–FY2030E (judgment)**

> Attack (partner's words): "You call business optimization a one-time cost and set it to zero after FY2026, but Accenture has booked it four years running — $1,063M in FY23, $438M in FY24, $615M in FY25 and $308M in FY26. That is closer to a recurring cost of about $600M a year. Why is zero the right number, and how much of your $182 comes from assuming it stops?"

**My answer (two sentences):**

1. I set it to zero because management says the program that began in Q4 FY25 was completed in Q1 FY26 and no new program has been announced, and I would rather not invent a charge the company has not disclosed.
2. If I retain FY2026's $307.541M charge and assume $600M in each of FY2027–FY2030, the model falls by $8.56 per share to $173.44, below the quoted $177.41 market price; a new announced program would therefore lead me to revise the zero-cost assumption using its disclosed timing and cost.

**My attack on my partner's table** (company: **KKR \& Co. Inc. (NYSE: KKR)**, line: **Revenue growth**):

> "Your revenue growth of 10% is applied to a revenue line that is not a steady business: KKR's GAAP revenues went from $14,499M in 2023 to $21,879M in 2024 (+51%) and back to $19,464M in 2025 (−11%), and the 2024 jump came largely from net premiums of $7,899M, which the 10-K ties to one large block reinsurance transaction at Global Atlantic. Why that number, when a single growth rate on total revenue carries one-off reinsurance deals and investment gains forward as if they recur — and what would change it: would you get a different value if you grew fee-paying AUM or management fees instead?"

**Their answer:** "The sensitivity is now calculated: applying the historical 18.47% management-fee growth rate to the existing fee line raises the value from $10.38 to $12.68. Your response also clarifies that the current model does not apply 10% growth to total revenue, while accepting the remaining weakness in its insurance-premium forecast."

\---

## Organic growth — learn on your own

1. **What it is:** growth from the business a company already owned a year ago — same stores, same clients, same practices — excluding what it bought. It shows whether the core business is growing, apart from money spent on acquisitions.
2. **How Accenture discloses it:** not as "same-store" or "organic" in the 10-K. The MD\&A reports local-currency growth; management gives the inorganic contribution on the earnings calls (a bit more than 3% in FY25, \~1.5% expected in FY26). Organic = local-currency growth − inorganic.
3. **Why the video carries 1.8% for ABG when reported growth was 4.7%:** the gap is mostly dealerships ABG bought. The model never spends money on acquisitions, so it can only carry the growth of the stores ABG already owns; taking 4.7% would give free revenue from stores the cash flow never paid for. I do the same thing for Accenture — organic growth, no acquisition spend.

## Reflect (talking points for my partner)

1. **Label I'd defend the longest:** deferred revenues at 40.5% of receivables — three years of history (37.9–40.5%), May 2026 at 40.7%, and Accenture's own DSO nets the two lines, so it is the company's own view of how its working capital works.
2. **The number that surprised me:** in FY2024 Accenture spent $6.6B buying businesses and only $0.5B on property and equipment — its "capex" is acquisitions. (Runner-up: the data provider's FY25 operating income, 10,854, is not the 10-K's 10,225.7.)

## Limitations

* Timing: discount periods 1–5 are measured from the Aug. 31, 2025 opening balance sheet. The $182.00 output uses that classroom timing convention with later information and is not a valuation rebased to Sept. 24, 2026; the market comparison therefore has a date mismatch. A current-date valuation would require rolling forward the statements and excluding cash flows already realized.
* The expense proxy retains amortization within operating costs without a separate add-back or intangible-asset roll-forward. Other assets are held flat. These are simplified statements, not a full GAAP forecast.
* Valuation uses year-end discounting, a 365-day receivables convention, no tax benefit for forecast losses, and the lab's rule that negative annual FCFE is omitted. Ignoring cash deficits is a classroom rule, not a general valuation principle.
* FCFE is shown before revolver draws or repayments. Those financing movements are shown separately in the cash reconciliation; the base case needs none. No revolver capacity limit is modelled.
* The 1.9% minority deduction is a rounded earnings-share proxy for value, not an independently valued minority stake; the 612 million shares are a fixed May 2026 reference count, not a September count or a forecast after buybacks.
* FY2026E is a year that has already ended but not been reported; actual results (Oct 1, 2026) will replace it.
* Share-based pay (\~$2.1B a year) is treated as a real cost, which lowers FCFE versus the "free cash flow" Accenture reports ($10.9B in FY25).
* Excess cash above the $5B floor (\~$6.5B) is valued only through its interest income, not added separately — conservative.
* Educational projection, not investment advice.

## Sources

* Accenture Q4 FY25 results (8-K Ex. 99, Sept 25, 2025; separate from the 10-K): https://www.sec.gov/Archives/edgar/data/1467373/000146737325000213/q4fy25earnings8-kexhibit.htm
* Accenture Q4 FY24 results (8-K Ex. 99, Sept 26, 2024), FY24 and FY23 statements: https://www.sec.gov/Archives/edgar/data/1467373/000146737324000266/fy24q4plc8-kexhibit.htm
* Accenture FY2025 Form 10-K (Notes 5 and 17): https://www.sec.gov/Archives/edgar/data/1467373/000146737325000217/acn-20250831.htm
* Accenture FY2024 Form 10-K (Note 5, depreciation): https://www.sec.gov/Archives/edgar/data/1467373/000146737324000278/acn-20240831.htm
* Accenture FY2023 Form 10-K: https://www.sec.gov/Archives/edgar/data/1467373/000146737323000324/acn-20230831.htm
* Accenture Q3 FY26 results and FY26 outlook (8-K Ex. 99, June 18, 2026): https://www.sec.gov/Archives/edgar/data/1467373/000146737326000031/q3fy26earnings8-kexhibit.htm
* Q4 FY25 call (FY26 inorganic \~1.5%, \~$3B acquisitions): https://investor.accenture.com/\~/media/Files/A/accenture-v4/investors/earnings-reports/2025/accenture-fourth-quarter-fiscal-2025-conference-call-transcript-updated-10-8-2025.pdf
* Q2 FY25 call (FY25 inorganic a bit more than 3%): https://investor.accenture.com/\~/media/Files/A/Accenture-IR-V3/quarterly-earnings/2025/q2fy25/accenture-second-quarter-fiscal-2025-conference-call-transcript.pdf
* Share price (Sept. 24, 2026 close): https://finance.yahoo.com/quote/ACN/ ; beta and provider capex: https://stockanalysis.com/stocks/acn/ and https://stockanalysis.com/stocks/acn/financials/
* Official U.S. Treasury daily par yield curve rates (10-year yield, Sept. 23, 2026): https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily\_treasury\_yield\_curve\&field\_tdr\_date\_value=2026




> \*\*Disclaimer:\*\* I am not a financial professional. The information and opinions presented here are for educational purposes only and should not be used to make financial decisions. This project was created using Codex.

