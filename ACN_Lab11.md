# Lab 11 — Accenture pro forma sensitivity

**Question:** Which assumptions drive Accenture's FY2026E–FY2030E forecast and value, and what explains their effects?

**Result, over these ranges:** FY2027E–FY2030E revenue growth has the larger span for FY2030E operating profit, FY2030E free cash flow to equity (FCFE), and value per share. This comparison depends on the selected range widths; it is not a universal ranking of economic importance or a probability forecast.

This analysis runs the existing [Lab 10 model](accenture_proforma.py) from [ACN\_Lab10.md](ACN_Lab10.md). Financial statement amounts are **USD millions**; share values are **USD per share**. Fiscal years end August 31. FY2025A is the opening balance sheet. FY2026E–FY2030E are model projections, including an unreported FY2026 at the time of this run (September 29, 2026).

## Base and independent assumptions

The original `python accenture\_proforma.py` run produced FY2030E operating profit of **$13,176.1 million**, FY2030E FCFE of **$9,728.6 million**, and model value of **$182.00/share**. All five projected years had balance-sheet gaps of $0.0 million at displayed precision and passed the $5,000 million minimum-cash check. The model's valuation uses a 10.56% cost of equity, 3.0% terminal growth, 1.9% minority-interest deduction, and 612 million shares, as documented in Lab 10. Valuation timing and terminal-value limitations are discussed there.

|Independent driver|Base input|Lower|Higher|Affected years|Range basis|
|-|-:|-:|-:|-|-|
|Revenue growth|3.0% each year|2.0% each year|4.0% each year|FY2027E–FY2030E|Analyst judgment anchored to Lab 10's approximate 2% FY2026 and 4% FY2025 organic-growth estimates. FY2026E growth stays at its 4.0% base. The shift is **−1/+1 percentage point**, with no acquisition spend added.|
|Gross margin|32.0% each year|31.9% each year|32.6% each year|FY2026E–FY2030E|The 31.9%–32.6% range observed across FY2023–FY2025 in Lab 10. Its distance from the base is asymmetric: −0.1/+0.6 percentage points.|

These are independent assumption-table inputs. Each scenario starts from a fresh copy of the complete base assumptions and FY2025A opening sheet. Only the named driver's values in the specified forecast years change. Revenue, expenses, receivables, deferred revenue, cash flow, and balance sheets recalculate through the entire model. The ranges are scenarios, not new company observations.

## Locked changed-input record

**Recorded before any changed-input run:** 2026-09-29 20:32:38 UTC. This is an analyst judgment prepared at the user's request; it is not represented as the student's own prediction.

**Change predicted:** FY2027E–FY2030E growth from 3.0% to 4.0% per year (+1.0 percentage point), leaving FY2026E at 4.0%. I expected FY2030E operating profit to rise by about **$500 million**, FCFE by about **$350 million**, and value by about **$5–$7/share**. The reason: compounding revenue adds gross profit and operating profit; tax, capex, and receivables net of deferred revenue reduce the cash-flow gain; higher terminal FCFE raises value. This is a rough pre-run estimate, not a result back-filled from the sensitivity table.

**Reconciliation after the run:** The actual high-growth case raised operating profit **$533.4 million**, FCFE **$279.7 million**, and value **$4.24/share**. The operating-profit direction and rough size matched. FCFE and value were below the predicted ranges. In FY2030E, the high-growth run has $84,767.8 million of revenue versus $81,554.3 million base, but $720.5 million of capex versus $693.2 million and a $701.2 million receivables increase versus $510.9 million base. Deferred revenue offsets some of that working-capital use ($284.0 million increase versus $206.9 million base); taxes also absorb part of the profit increase. These linked cash-flow effects explain why the final-year FCFE gain is smaller than the operating-profit gain. The resulting per-share change is therefore less than my estimate.

## One-at-a-time results

Signed changes equal the scenario output minus the **same** initial base output. FCFE is retained with its sign. Value is shown because all five annual FCFE figures remain positive in these runs and the existing model's valuation checks pass.

|Driver and case|Input in affected years|FY2030E operating profit ($m)|Change ($m)|FY2030E FCFE ($m)|Change ($m)|Value ($/share)|Change ($/share)|Accounting|
|-|-|-:|-:|-:|-:|-:|-:|-|
|Growth, lower|2.0% FY27–FY30|12,658.2|−517.9|9,453.9|−274.7|177.83|−4.17|Pass|
|Growth, base|3.0% FY27–FY30|13,176.1|+0.0|9,728.6|+0.0|182.00|+0.00|Pass|
|Growth, higher|4.0% FY27–FY30|13,709.5|+533.4|10,008.3|+279.7|186.24|+4.24|Pass|
|Gross margin, lower|31.9% FY26–FY30|13,132.9|−43.2|9,693.0|−35.6|181.34|−0.66|Pass|
|Gross margin, base|32.0% FY26–FY30|13,176.1|+0.0|9,728.6|+0.0|182.00|+0.00|Pass|
|Gross margin, higher|32.6% FY26–FY30|13,435.4|+259.3|9,942.4|+213.8|185.96|+3.96|Pass|

|Output span: maximum minus minimum across lower/base/higher|Growth range|Gross-margin range|Larger span over these ranges|
|-|-:|-:|-|
|FY2030E operating profit ($m)|1,051.3|302.6|Growth|
|FY2030E FCFE ($m)|554.4|249.4|Growth|
|Value ($/share)|8.40|4.62|Growth|

Spans and signed changes are calculated from unrounded model values. Subtracting the displayed two-decimal value/share endpoints can differ by $0.01/share because each endpoint was rounded separately.

The growth range compounds over four years, affecting FY2030E revenue by $6,334.9 million between its endpoints. Higher revenue increases gross profit and SG\&A under the model's expense ratio, as well as capex and receivables. Gross margin changes gross profit and its linked SG\&A expense but leaves revenue unchanged. The spans also reflect that the growth path moves 2.0 percentage points from lower to higher in four years, while gross margin moves 0.7 percentage points in five years. Changing those widths could change the ranking.

## Check and valuation interpretation

All six lower/base/higher runs passed every projected year's balance-sheet and minimum-cash checks. The stored [terminal output](ACN_Lab11_output.txt) shows each input path, signed change, output span, and FY2030E income-statement, working-capital, cash-flow, and balance-sheet trace for changed runs. The base was rerun after all scenarios; independent inputs and linked results matched the first base within an absolute tolerance of **1e−8** in model units. No scenario used another scenario's changed assumptions.

**Analyst interpretation:** Growth deserves the next research effort: even the tested 2.0% path brings the model to $177.83/share, only $0.42 above the **historical** September 24, 2026 market close of $177.41 used in Lab 10. This does not establish a current buy/sell conclusion. Lab 10's value discounts from August 31, 2025 but uses later information and compares to a later quote; a contemporaneous valuation would need a roll-forward. The $182.00 base is also heavily dependent on terminal value (70.7% of its present value). Research should first test whether sustained organic growth near 2% or 4% and the no-acquisition spending assumption are defensible.

The surprising result in the locked comparison was the smaller FCFE and value gain: operating profit tracked the rough prediction, while additional working capital, capex, and tax reduced the cash available to shareholders. This sensitivity table assigns no probabilities to lower, base, or higher scenarios. It isolates one input at a time; correlated changes, such as pricing pressure affecting both growth and margin, are outside this analysis.

## Accenture results shared for the reciprocal partner check

My company is Accenture. The two independent drivers, actual yearly input paths, and range reasons are in the [Lab 11 inputs](ACN_Lab11_inputs.json); all unchanged independent assumptions and FY2025A opening balances are in the [Lab 10 model](accenture_proforma.py). Revenue growth is 4.0% in FY2026E for every run, then 2.0% / 3.0% base / 4.0% in each FY2027E–FY2030E year. Gross margin is 31.9% / 32.0% base / 32.6% in each FY2026E–FY2030E year. These are percentage-point paths. The [run output](ACN_Lab11_output.txt) contains each run's input path, five years of accounting checks, and the FY2030E statement trace. Statement outputs are USD millions; value is USD/share.

|Accenture case|FY2030E operating profit ($m)|FY2030E FCFE ($m)|Value ($/share)|
|-|-:|-:|-:|
|Base|13,176.1|9,728.6|182.00|
|Growth 2.0%, FY27–FY30|12,658.2|9,453.9|177.83|
|Growth 4.0%, FY27–FY30|13,709.5|10,008.3|186.24|
|Gross margin 31.9%, FY26–FY30|13,132.9|9,693.0|181.34|
|Gross margin 32.6%, FY26–FY30|13,435.4|9,942.4|185.96|

My timestamped, analyst-assisted prediction before the changed runs was that raising FY2027E–FY2030E growth from 3.0% to 4.0% would lift FY2030E operating profit by about $500m, FCFE by about $350m, and value by about $5–$7/share. The actual changes were **+$533.4m, +$279.7m, and +$4.24/share**. All scenario years passed the balance-sheet and cash-floor checks, and the restored base matched. For the reciprocal review, my partner can recompute one of these differences, check the unchanged inputs in the linked files, and ask me to trace it through the statements.

## Partner exchange record

My partner modeled KKR. The checks below are recomputed from the KKR results my partner supplied. No KKR model file or complete assumption tables were available to me, so input-by-input claims rest on my partner's description.

### Exchange 1 — predict, then question

**Question I received from my partner:** "Is your range a percentage-point shift or a percent change? Which currency and scale are the money figures in—thousands or millions?"

**My answer:** Both are **percentage-point** shifts, not relative percent changes. Revenue growth moves from 3.0% base to 2.0% or 4.0% in each FY2027E–FY2030E year (−1/+1 pt), with FY2026E held at 4.0%. Gross margin moves from 32.0% base to 31.9% or 32.6% in each FY2026E–FY2030E year (−0.1/+0.6 pt). Statement amounts are **USD millions**, not thousands, so +$533.4m operating profit means $533.4 million. Value is **USD per share** on 612 million shares.

**Question I asked my partner:** "Is your range a percentage-point shift or a percent change? Which currency and scale are the money figures in (thousands, millions)?" I also asked which historical fee series and years support the 5%–15% range, and whether the growth rate applies to recurring fees only.

**Partner's answer:** Both KKR ranges are percentage-point shifts applied to each FY2026E–FY2030E year, and all money figures are USD millions. Fee growth runs 5% / 10% base / 15%, a range my partner said is informed by KKR's historical fee growth. The compensation ratio runs 55.116% / 60.116% base / 65.116%; the base is FY2025's actual ratio and the ±5-point width is a judgment. **Gap noted:** the specific fee series and years behind 5%–15%, and whether the rate covers recurring fees only, were not identified.

**My unit/range check on partner's model:** KKR fee growth is 5%, 10% base, and 15% in each FY2026E–FY2030E year, a −5/+5 **percentage-point** shift. Compensation divided by asset-management revenue is 55.116%, 60.116% base, and 65.116%, also −5/+5 percentage points. Output scale is USD millions. The compensation range is a stated judgment, not an observed historical range.

### Exchange 2 — check each other's evidence

**Partner's recomputed difference on my model:** My partner recomputed the FY2030E 4.0% revenue-growth case minus the base: operating profit **+$533.4m** ($13,709.5m − $13,176.1m), FCFE **+$279.7m** ($10,008.3m − $9,728.6m), and value **+$4.24/share** ($186.24 − $182.00). All three match my table.

**Question I received from my partner:** "Did the balance sheet balance and the cash checks pass in every year of every run?"

**My answer:** Yes. All six lower/base/higher runs passed the balance-sheet and $5,000m minimum-cash checks in all five forecast years (30 scenario-year checks). Every balance-sheet gap displays as $0.0m, and the model rejects any gap of $0.05m or more. The restored base matched the first base within a 1e−8 tolerance. The per-run, per-year evidence is in `ACN\_Lab11\_output.txt`.

**Question I asked my partner:** "Did the balance sheet balance and the cash checks pass in every year of every run?"

**Partner's answer:** My partner reported that all runs passed the accounting checks and that the restored base matched the original. I did not see their check output, so this rests on their report.

**My check on partner's KKR result:** The 15% fee-growth case minus the 10% base is **$3,265.972m − $2,613.741m = +$652.231m operating profit** and **$867.711m − $719.669m = +$148.042m common FCFE**, close to their locked prediction of about +$650m and +$150m. My partner states that only fee growth changed and the compensation ratio stayed at 60.116%; higher compensation **expense** as revenue rises is a linked result, not a change in the independent **ratio**. This is consistent with a one-input-at-a-time run, but I could not audit the full input set or check output without their files.

### Exchange 3 — explain and compare

**Partner's range-width question to me:** "Your revenue-growth range covers 2 percentage points, while your gross-margin range covers only 0.7 points and is asymmetric around the base. Growth changes for four years, while margin changes for five. Could your larger growth span partly reflect those choices rather than growth being inherently more important?"

**My answer:** Yes. Growth produces the larger output span over my tested ranges, but the ranges have different widths, timing and economic effects. Revenue growth compounds, whereas gross margin changes the share of revenue retained after direct costs. A wider margin range or narrower growth range could change the ranking, so I cannot conclude that growth is always more important.

**Question I asked my partner:** "Why might your company's main driver differ from Accenture's, where growth leads over the tested ranges? Consider the business model, margins, capital intensity, and working capital."

**Partner's answer:** Our results identify growth as the larger driver in both companies over our chosen ranges: fee growth for KKR and revenue growth for Accenture. What differs is how growth reaches cash flow. In the KKR model, compensation absorbs part of additional fees, and taxes, outside-investor allocations and insurance capital retention further reduce common FCFE. In the Accenture model, additional revenue increases operating profit, but receivables, taxes and capex absorb part of the cash benefit, partly offset by deferred revenue. We also tested different second drivers (KKR compensation intensity versus Accenture gross margin), so the rankings are not directly equivalent.

**Comparison of the two companies' driver mechanisms:** Growth leads for Accenture over my ranges: consulting revenue earns about a 32% gross margin, capex is under 1% of revenue, and deferred revenue finances about 40.5% of receivables, so extra revenue compounds into operating profit and FCFE after receivables, capex, and taxes absorb part of it. For KKR, the fee-growth span is **$1,196.253m operating profit and $271.801m common FCFE** versus **$1,142.928m and $205.106m** for the compensation ratio (recomputed from their endpoints). Fee growth leads **over these ranges**, but only by $53.325m in operating profit, so a modest change in range width could reverse it. KKR's common FCFE is also shaped by outside-investor and insurance-capital allocations, which leave its value per share unavailable. Raw dollar spans should not be ranked across the two companies.

## Reproduce

From the project folder:

```powershell
python accenture\_proforma.py
python accenture\_sensitivity.py ACN\_Lab11\_inputs.json
python -m unittest -v test\_accenture\_proforma test\_accenture\_sensitivity
```

The inputs and pre-run record are in [ACN\_Lab11\_inputs.json](ACN_Lab11_inputs.json); the added runner is [accenture\_sensitivity.py](accenture_sensitivity.py). The original Lab 10 model is preserved. The runner marks a scenario invalid if its model or accounting checks fail and omits per-share value if any projected annual FCFE is nonpositive, retaining signed FCFE for analysis.

Lab instructions: [Lab 11 — Pro Forma Sensitivity](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-06/lab-11-proforma-what-if.md).

**Disclosure:** This lab was completed with Codex and Claude. I am not a financial advisor. This analysis is for educational purposes and should not be used as personalized financial advice.

