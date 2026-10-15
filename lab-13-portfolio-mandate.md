# Lab 13 — Portfolio Mandate Defense

Meridian Foundation Reserve (fictional) | FIN43900 | October 15, 2026

**Disclaimer (adapted from Agents.MD, Safety and Professional Boundaries):** I am not a financial advisor. This work is for educational purposes only. The clients, portfolios, and scenarios are fictional examples. This material does not constitute personalized investment advice or fiduciary, legal, tax, or accounting representation, and it provides no guarantee of performance. It is not certified, audited, or approved for a regulated filing. Consult a qualified professional before making real financial decisions.

**Authorship and AI-use disclosure:** ChatGPT was utilized as the AI agent to assist with preparing the written analysis and developing, explaining, and verifying the Python checker. These answers were prepared with AI assistance, including the sections the lab designates for independent work. No independent completion, attendance, partner exchange, or submission is claimed.

## Decision

A passes every static rule the assigned checker can evaluate; B fails the reserve, liquidity, and issuer tests; C fails the reserve test. This does not establish that A meets the entire mandate. The CIO must resolve the risk/return priority and specify the pilot's optimization objective before an optimizer is chosen. S9 remains **requires CIO clarification** for every candidate.

## S1–S10 classification and IPS mapping

| Statement | Type | Reason and IPS mapping |
|---|---|---|
| S1: Seven-year horizon; annual rebalancing | Hard constraint | The horizon guides asset suitability and annual rebalancing defines a governance schedule; neither is established by one allocation snapshot. |
| S2: CPI + 4% yearly, net of costs, over rolling five years | Objective | This is the real-return target and evaluation horizon, not a guaranteed outcome or a specified mathematical optimization function. |
| S3: $0.75m quarterly; twelve months in cash or daily-liquid government securities | Hard constraint | Spending and liquidity policy require $3m of eligible reserves, initially 3% of the $100m portfolio. |
| S4: 60% global equities / 40% U.S. investment-grade bonds benchmark | Preference | Within the supplied categories, this is a reference for evaluation, not a requirement to hold those exact weights; the IPS should record the benchmark. No tracking-error bound is stated. |
| S5: Long-only; no borrowing, short sales, or derivatives | Hard constraint | These are implementation prohibitions; nonnegative fully funded weights test only the representation supplied here, not hidden leverage or future trading. |
| S6: Single issuer at most 8% | Hard constraint | Concentration is limited at company level, combining that company's stock and bonds; the stated exemptions apply. |
| S7: Annual turnover at most 25% without approval | Hard constraint | A conditional trading restriction with a committee exception; trade history, the turnover convention, and approval records are needed to enforce it. |
| S8: At least 90% redeemable within five business days | Hard constraint | A measurable liquidity floor, separate from reserve eligibility. |
| S9: No calendar-year loss greater than 10% | Unverifiable promise | It expresses risk intolerance without an agreed measure or breach response; weights alone cannot verify or guarantee future losses. |
| S10: No sector, ESG, tax, or home-bias preference; optimizer unspecified | Missing | No extra preference should be invented; the pilot lacks an agreed optimization criterion and priority among conflicting goals. |

S4 is the most debatable label: a benchmark is properly a performance reference rather than an allocation preference. “Preference” is the closest available category, and it must not be converted into a 60/40 hard constraint.

## Checker and verification

Run from this folder:

```text
python mandate.py
python verify_mandate.py
```

The program uses only the Python standard library. All portfolio results are calculated from editable inputs; the separate verifier contains the lab's known answers as assertions. `verification.txt` records the actual run and the negative-weight probe.

Reserve floor = 4 × $0.75m / $100m × 100 = **3.0%**. The dollar reserve is $3m; its required percentage would change with portfolio value.

| Check | A | B | C | D |
|---|---:|---:|---:|---:|
| Total weight | 100.0 pass | 100.0 pass | 100.0 pass | 100.0 pass |
| Lowest weight | 0.0 pass | 0.0 pass | 0.0 pass | 0.0 pass |
| Reserve ≥ 3.0% | 14.0 pass | 1.0 FAIL | 2.0 FAIL | 100.0 pass |
| Liquid within 5 days ≥ 90% | 100.0 pass | 85.0 FAIL | 100.0 pass | 100.0 pass |
| Largest company ≤ 8% | 0.0 pass | 9.0 FAIL | 8.0 pass | 0.0 pass |
| Verdict | Passes checkable rules | Fails 3 | Fails 1 | Passes checkable rules |

All four receive “requires CIO clarification” for the calendar-year loss rule. Acme's 5% bonds plus 4% stock make B's exposure 9%. C's 8% is exactly on the permitted boundary. The supplied table explicitly treats the 10-year Treasury as reserve-eligible, so A's eligible total is 14%; daily liquidity does not eliminate interest-rate price risk.

Required probe: changing A's cash to −2 and equity fund to 64 preserves its 100% total. Its lowest weight becomes −2.0 and fails; its reserve remains 10.0%, liquidity 100.0%, and company exposure 0.0%, so exactly one rule fails. The verifier restores A afterward, and the saved `mandate.py` retains the original allocations.

## Attack portfolio D

D holds **100% Cash and 0% of every other listed holding**. It is a counterexample, not an optimized recommendation. Its measured reserve and liquid weights are both 100%, and exempt cash creates no company concentration.

**Two-sentence judgment:** The objection holds as a suitability concern because an all-cash portfolio provides no demonstrated basis for meeting the net CPI + 4% rolling five-year target, even though it satisfies all static tests. S2 supports the objection, while S10 exposes the missing optimization priority; the inputs do not prove that cash will necessarily miss the target.

**Sceptical-colleague role:** I would cite S2 against D: the allocation needs a supported case for achieving CPI + 4% net of costs over rolling five-year periods. Holding only cash meets the reserve and liquidity floors but does not establish that return case. I would not declare a hard breach of S4 merely because D differs from 60/40, because a benchmark alone does not require matching weights. This is the lab's solo role-play, not a claim of a partner exchange.

## One question for the CIO

**When CPI + 4% and the stated loss tolerance conflict, should the pilot minimize downside risk subject to an agreed expected real-return target, or maximize expected real return subject to a precisely defined downside-risk limit?**

An answer prioritizing downside protection would shift the design toward cash and short government securities and may require revising the return objective. An answer prioritizing expected real return within a probabilistic risk budget would permit more growth exposure, subject to the hard constraints. These are conditional design consequences, not optimized weights. Before encoding S9, document the return measure, horizon, probability or scenario convention, and breach action; do not silently substitute volatility or a guarantee.

## Investment policy statement

An IPS documents the investor's purpose, return objectives, risk tolerance, constraints, responsibilities, and review procedures. It gives decision makers a stable basis for selecting and monitoring investments and responding when circumstances or limits change.

Objectives define desired outcomes; constraints delimit allowable decisions; governance assigns authority and responses. For Meridian, S2 supplies the return objective, S1 the horizon and rebalancing schedule, S3/S8 the liquidity requirements, S5/S6/S7 the implementation restrictions, S4 the evaluation reference, S9 the unresolved risk policy, and S10 the absent optimization instruction. An IPS must distinguish a target from a promise and identify conflicts before implementation.

This interpretation follows the assigned [CFA Institute IPS reading](https://rpc.cfainstitute.org/sites/default/files/-/media/documents/article/position-paper/investment-policy-statement-institutional-investors.pdf), Introduction and Section 3.

## Reflection

1. A checker can establish compliance with numeric allocation limits without showing that the client can reach its goals. D passes but has no supported return case for S2; A also lacks evidence on future returns, annual turnover, rebalancing implementation, and the unresolved loss requirement. Passing is necessary for the tested restrictions, not sufficient for suitability or full mandate approval.
2. S4 is the classification I would examine most carefully: a benchmark describes how performance is compared, but it does not state a binding allocation. S9 also requires care because forceful wording does not make an undefined future-loss promise testable.

## Code-comprehension checkpoint

**Question:** In `companies[holding["issuer"]] += weight`, why must the key be the issuer rather than the holding name, and what incorrect verdict could result for B if those were reversed?

**Answer:** The 8% limit applies to the total exposure to one company, so all securities issued by that company must be added together. Using the issuer as the dictionary key groups Acme's bonds and stock into the same running total. In B, the 5% bond allocation plus the 4% stock allocation equals 9%, which exceeds 8% and fails. If the holding name were used instead, the checker would keep the two positions separate, report a largest position of 5%, and incorrectly pass the issuer test. B would then appear to fail only two rules instead of three. `defaultdict(float)` starts each new issuer's total at 0.0, and `+= weight` adds each position to it.

This is an AI-assisted explanation; it does not document a student answering before receiving an explanation.

## Project 2 mandate — fictional client

The following mandate uses an illustrative fictional client because no existing Project 2 client information was supplied. Its figures are assumptions for the exercise, not verified facts about a real client.

**Client:** Campus Access Scholarship Reserve, $2m, ten-year horizon.

**Objective:** Seek CPI + 3% annualized net of costs over rolling five-year periods while funding quarterly $15,000 scholarships.

**Hard constraints:** Long-only and fully funded; no borrowing, shorting, or derivatives. Hold at least $60,000 in cash or daily-liquid government securities for twelve months of payouts. Keep at least 90% redeemable in five business days. Aggregate each company's stock and bonds under an 8% issuer cap; exempt cash, U.S. Treasuries, and diversified funds. Rebalance annually and keep annual turnover at or below 25% without committee approval.

**One client question:** If the return target conflicts with reliably funding scholarships, should the pilot prioritize payout protection or expected real growth? A payout-protection answer would support a larger reserve and less growth exposure; a growth-priority answer would support more equity risk subject to a subsequently agreed risk policy. No portfolio is optimized here.

## Submission status

Locally prepared: `mandate.py`, this Markdown file, `verify_mandate.py`, and `verification.txt`. All written questions have answers, including the code-comprehension checkpoint and a fictional Project 2 mandate. The authorship note identifies AI assistance in the independent-work sections. Upload the Markdown and Python files to your course GitHub repository and paste their individual links into the Lab 13 quiz; the verifier and output may accompany them as evidence. No GitHub upload or quiz submission has been performed.

Source: [Lab 13 — Portfolio Mandate Defense](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-08/lab-13-portfolio-mandate.md).
