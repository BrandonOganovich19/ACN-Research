# Accenture (NYSE: ACN) Reverse DCF Analysis

**Valuation date: September 10, 2026**  
**Latest completed market close used: September 9, 2026**  
**Currency: USD; financial-statement amounts are USD millions unless stated otherwise**

## Important Disclaimer

I am not a financial advisor. This analysis was prepared solely as an educational class project and is not financial, investment, legal, tax, or accounting advice. The information, assumptions, projections, and valuation results should not be relied upon to buy, sell, or hold any security or make any investment decision. The analysis has not been audited or reviewed by a licensed financial professional.

## Conclusion and Conditional Call

At the latest completed closing price of **$175.80**, Accenture's market value implies approximately **-7.69% annual revenue growth for ten years**, assuming an **8.69% WACC**, **3.0% terminal growth**, **14.49% EBIT margin**, and **17.48% FCFF margin**.

That negative implied growth is not automatically proof of undervaluation. The most distrusted input is the **17.48% TTM FCFF margin**, because recent cash flow can be elevated by working-capital timing and large noncash share-based compensation addbacks. Holding that conversion rate constant for ten years materially lowers the required growth rate.

**Conditional call - Watch-defer. Initiate further class-project analysis if Accenture sustains at least 3% revenue growth while normalized FCFF margin remains at or above 15%; otherwise continue to watch and defer. Monitor: operating margin in the next reported quarter.**

“Initiate” means advancing the company for additional class research. It is not an instruction to buy the shares.

## 1. Inputs and Sources

`Counsel-log.pdf` remains the historical primary source. The latest available Accenture Form 10-Q updates operations and balance-sheet inputs through May 31, 2026. The September 9, 2026 market close updates pricing.

| Input | Value | As-of date / period | Status and source |
|---|---:|---|---|
| Current reference price | $175.80 | September 9, 2026 close | External observation: StockAnalysis ACN history, accessed September 10, 2026 |
| Q3 diluted weighted-average shares | 615.593 million | Quarter ended May 31, 2026 | Extracted: Accenture Form 10-Q, Income Statements, lines 202-207 |
| Approximate ordinary shares outstanding | 612.4 million | Accessed September 10, 2026 | Accenture Investor FAQ estimate; cross-check only |
| Equity value used | $108,221.3 | Mixed September 9/May 31 dates | Calculated: $175.80 x 615.593 million |
| Cash and equivalents | $10,165.2 | May 31, 2026 | Form 10-Q Balance Sheet, lines 110-116 |
| Current debt and borrowings | $112.8 | May 31, 2026 | Form 10-Q Balance Sheet, lines 132-143 |
| Long-term debt | $5,029.4 | May 31, 2026 | Form 10-Q Balance Sheet, lines 142-149 |
| Net cash | $5,023.0 | May 31, 2026 | Calculated: cash less total debt |
| Enterprise value target | $103,198.3 | Mixed September 9/May 31 dates | Calculated: equity value + debt - cash |
| TTM revenue | $73,100.6 | Twelve months ended May 31, 2026 | Calculated from FY2025 PDF and 10-Q comparative periods |
| TTM EBIT | $10,592.2 | Twelve months ended May 31, 2026 | Calculated from FY2025 PDF and 10-Q comparative periods |
| TTM EBIT margin | 14.49% | Twelve months ended May 31, 2026 | Calculated: TTM EBIT / revenue |
| TTM operating cash flow | $13,182.1 | Twelve months ended May 31, 2026 | Calculated from FY2025 PDF and 10-Q Cash Flow Statement, lines 457-479 |
| TTM capex | $600.4 | Twelve months ended May 31, 2026 | Calculated from FY2025 PDF and 10-Q property-and-equipment purchases |
| TTM interest expense | $265.8 | Twelve months ended May 31, 2026 | Calculated from FY2025 PDF and 10-Q Income Statements, lines 181-198 |
| TTM effective tax rate | 25.45% | Twelve months ended May 31, 2026 | Calculated: tax expense / pretax income |
| TTM FCFF | $12,779.9 | Twelve months ended May 31, 2026 | CFO - capex + after-tax interest |
| TTM FCFF margin | 17.48% | Twelve months ended May 31, 2026 | Calculated; normalization risk flagged |
| FY2026 revenue guidance | 3%-4% local currency | FY ending August 31, 2026 | Management estimate: Q3 FY2026 earnings release, June 18, 2026 |
| FY2026 FCF guidance | $10.8-$11.5 billion | FY ending August 31, 2026 | Management estimate: Q3 FY2026 earnings release, June 18, 2026 |

### TTM Construction

```text
TTM value = FY2025 - nine months ended May 31, 2025
            + nine months ended May 31, 2026

TTM revenue = 69,672.977 - 52,076.717 + 55,504.334 = 73,100.594
TTM EBIT = 10,225.664 - 8,175.973 + 8,542.543 = 10,592.234
TTM CFO = 11,474.399 - 7,560.252 + 9,267.947 = 13,182.094
TTM capex = 600.039 - 492.124 + 492.491 = 600.406
TTM FCFF = 13,182.094 - 600.406 + 265.819 x (1 - 25.451%)
         = 12,779.853
```

## 2. Model Structure

- Explicit forecast horizon: **10 years**
- Terminal value: **Gordon Growth**, because no current peer exit multiple is introduced
- Solved variable: **constant annual revenue growth rate**
- Held fixed: **14.49% EBIT margin, 17.48% FCFF margin, 8.69% WACC, 3.0% terminal growth, and ten-year horizon**
- Target: **$103,198.3 million enterprise value**
- Goal Seek: PV of explicit FCFF plus PV of terminal value equals target EV

## 3. WACC

The updated filing does not supply all CAPM inputs. These remain visible placeholders, not sourced current market observations.

| Component | Value | Status |
|---|---:|---|
| Risk-free rate | 4.00% | Undated placeholder assumption |
| Beta | 1.10 | Undated placeholder; least reliable WACC input |
| Equity-risk premium | 4.50% | Undated placeholder assumption |
| Cost of equity | 8.95% | `4.00% + 1.10 x 4.50%` |
| Pretax cost of debt | 4.20% | Estimated from note coupons in `Counsel-log.pdf`, PDF p. 83 |
| Tax rate | 25.45% | TTM calculation |
| Equity weight | 95.46% | Updated equity value and debt |
| Debt weight | 4.54% | Updated equity value and debt |
| WACC | **8.69%** | Calculated estimate; not reported by Accenture |

```text
WACC = 95.46% x 8.95% + 4.54% x 4.20% x (1 - 25.45%) = 8.69%
```

## 4. Reverse DCF - Updated Company Run

USD millions. Revenue and FCFF change at the solved **-7.6882%** rate.

| Year | Revenue | EBIT | FCFF | Discount factor | PV of FCFF |
|---:|---:|---:|---:|---:|---:|
| 1 | $67,480.5 | $9,777.9 | $11,797.3 | 0.9201 | $10,854.5 |
| 2 | 62,292.4 | 9,026.1 | 10,890.3 | 0.8465 | 9,219.2 |
| 3 | 57,503.2 | 8,332.2 | 10,053.0 | 0.7789 | 7,830.3 |
| 4 | 53,082.2 | 7,691.6 | 9,280.1 | 0.7166 | 6,650.6 |
| 5 | 49,001.1 | 7,100.2 | 8,566.7 | 0.6594 | 5,648.6 |
| 6 | 45,233.8 | 6,554.4 | 7,908.0 | 0.6067 | 4,797.6 |
| 7 | 41,756.1 | 6,050.4 | 7,300.0 | 0.5582 | 4,074.8 |
| 8 | 38,545.8 | 5,585.3 | 6,738.8 | 0.5136 | 3,460.9 |
| 9 | 35,582.3 | 5,155.9 | 6,220.7 | 0.4725 | 2,939.5 |
| 10 | 32,846.7 | 4,759.5 | 5,742.4 | 0.4348 | 2,496.7 |

| Reconciliation | Value |
|---|---:|
| PV of explicit FCFF | $57,972.6 |
| Year-10 terminal value | $104,021.5 |
| PV of terminal value | $45,225.7 |
| Implied enterprise value | **$103,198.3** |
| Target enterprise value | **$103,198.3** |
| Difference | Approximately $0 |

At the **$175.80** reference price, the reverse DCF produces the same **$175.80 per-share value by construction** when explicit revenue growth is -7.69%. This is not evidence of mispricing.

## 5. Paste-Ready Excel Formulas

```text
B2  = 175.80                  Latest completed close
B3  = 615.593409              Diluted shares, millions
B4  = B2*B3                   Equity value
B5  = 5142.265                Total debt
B6  = 10165.245               Cash
B7  = B4+B5-B6                Target EV
B9  = 73100.594               TTM revenue
B10 = 10592.234               TTM EBIT
B11 = B10/B9                  EBIT margin
B12 = 25.451268%              Tax rate
B13 = 13182.094               TTM CFO
B14 = 600.406                 TTM capex
B15 = 265.819                 TTM interest
B16 = B13-B14+B15*(1-B12)     TTM FCFF
B17 = B16/B9                  FCFF margin
B19 = 4.00%                   Risk-free assumption
B20 = 1.10                    Beta assumption
B21 = 4.50%                   Equity-risk-premium assumption
B22 = B19+B20*B21             Cost of equity
B23 = 4.20%                   Pretax debt cost
B24 = B4/(B4+B5)              Equity weight
B25 = B5/(B4+B5)              Debt weight
B26 = B24*B22+B25*B23*(1-B12) WACC
B27 = 3.00%                   Terminal growth
B28 = -7.688232%              Goal Seek variable
```

Forecast beginning in row 32:

```excel
A32 = 1
A33 = A32+1
B32 = $B$9*(1+$B$28)
B33 = B32*(1+$B$28)
C32 = B32*$B$11
D32 = B32*$B$17
E32 = 1/(1+$B$26)^A32
F32 = D32*E32
```

Copy through Year 10, then:

```excel
D42 = D41*(1+$B$27)/($B$26-$B$27)
F42 = D42/(1+$B$26)^10
B44 = SUM(F32:F41)+F42
B45 = B44-$B$7
```

Goal Seek: set `B45` to zero by changing `B28`.

## 6. Sensitivity Grid

Each cell is the ten-year revenue growth rate required to match the updated enterprise value.

| WACC / Terminal growth | 2.0% | 3.0% | 4.0% |
|---:|---:|---:|---:|
| **7.69%** | -8.48% | -9.71% | -11.27% |
| **8.69%** | -6.68% | **-7.69%** | -8.93% |
| **9.69%** | -5.02% | -5.87% | -6.90% |

The base case is centered. Moving right to a higher terminal growth rate lowers required explicit growth; moving down to a higher WACC raises required explicit growth. The four-corner range is **-11.27% to -5.02%**, read directly from the grid.

## 7. Reasonableness Check

- PDF historical revenue CAGR, FY2023-FY2025: **4.25%**
- Latest Q3 FY2026 revenue growth: **6% USD / 3% local currency**
- Updated FY2026 guidance: **3%-4% local-currency revenue growth**
- Market-implied ten-year growth: **-7.69%**
- Sensitivity band: **-11.27% to -5.02%**

The implied decline is far below recent performance and management guidance. However, the gap is partly driven by the elevated 17.48% TTM FCFF margin. The appropriate interpretation is: **the price embeds substantial deterioration from current cash flow, or current cash conversion is not sustainable.** It is not proof of undervaluation.

## 8. Source Links

- Historical primary source: `Counsel-log.pdf`, Accenture FY2025 Form 10-K, in this folder.
- Accenture May 31, 2026 Form 10-Q: https://www.sec.gov/Archives/edgar/data/1467373/000146737326000032/acn-20260531.htm
- Accenture Q3 FY2026 earnings release: https://investor.accenture.com/~/media/Files/A/accenture-v4/investors/earnings-reports/2026/accenture-3q-fy26-earnings-release.pdf
- Accenture Investor FAQ: https://www.investor.accenture.com/investor-resources/investor-faqs
- ACN market-price history: https://stockanalysis.com/stocks/acn/history/

## 9. Unresolved Training-Shift Requirement

The course rubric requires the classroom training shift before the company run. Its original inputs and expected result were not included in the materials reviewed. It remains explicitly unresolved rather than fabricated.

## 10. After-Class Open Challenge

Normalize FCFF by separating recurring conversion from working-capital timing and share-based compensation, replace undated CAPM placeholders with dated instructor-approved inputs, and rerun a two-variable reverse DCF for combinations of revenue growth and FCFF margin.

## Educational-Use Reminder

This is a hypothetical class-project valuation exercise. It is not a recommendation regarding Accenture or any security, and no investment decision should be made based on this report.
