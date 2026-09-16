# Wildcat Capital Loan Portfolio — EDA Findings Summary

**Dataset:** `wildcat_loans_clean.csv` | **Prepared by:** Tyler Tobin | **Course:** MIS3060, Business Intelligence with AI

## Dataset Overview

The loan portfolio file contains 2,340 individual loans, each described by 12 attributes: loan amount, interest rate, term, credit score, debt-to-income ratio, annual income, loan purpose, loan status, state, and identifiers. This is the full population analyzed in this EDA — no rows were dropped during loading.

## Data Quality Issues

Two issues surfaced during inspection that should be addressed before any downstream reporting or modeling:

1. **Missing credit scores are not randomly distributed.** 47 loans (2.0%) are missing `credit_score`. Comparing loan status among those rows to the full dataset shows Delinquent loans are more than twice as common (23.4% vs. 10.6%) and Default loans are more than double (10.6% vs. 4.5%) among the missing-score rows, while Current loans are under-represented (36.2% vs. 62.1%). This means the missingness is *not* random — it's concentrated in riskier loans, likely because higher-risk borrowers are less consistently credit-checked or reported. Simply dropping these 47 rows in a credit-risk analysis would understate risk in the remaining population; this should be reported explicitly rather than silently excluded.
2. **`state` contains duplicate categories from inconsistent entry.** The column shows 27 unique values, but seven states are split across both an abbreviation and a full name (PA/Pennsylvania, NJ/New Jersey, NY/New York, FL/Florida, CA/California, IL/Illinois, TX/Texas). Any state-level grouping run before cleaning this would undercount those states. This needs to be standardized (e.g., map full names to their abbreviations) before geographic analysis.
3. **`origination_date`** loads as text rather than a date type, as expected — converted successfully to `datetime64` in Step 2 with no formatting failures.

## Key Distributions

The typical loan is modest, but the portfolio's average is pulled well above the median: mean loan amount is about $68,400 against a median of about $40,700. The histogram shows why — most loans cluster under $100K, but there's a second, flatter band of loans spread fairly evenly from roughly $150K to $500K rather than a smoothly tapering tail. That shape looks less like ordinary right-skew and more like two distinct loan populations mixed together (e.g., a "typical consumer loan" group and a separate, much larger "large loan" group) — worth investigating by segment before treating the portfolio as one distribution.

Annual income is similarly right-skewed (mean far above median), consistent with a small number of high-income borrowers. Interest rates average about 11.9% with no negative or implausible values (range roughly 4.5%–21%). Credit scores average about 674, within the valid 500–850 range.

## Categorical Breakdown

Loan purpose splits across five categories: Home Improvement (30.9%), Auto (25.8%), Personal (20.3%), Business (14.0%), and Education (9.0%) — no unexpected categories once case and spelling are accounted for.

Loan status: Current (62.1%), Paid Off (22.7%), Delinquent (10.6%), Default (4.5%). The 4.5% default rate plus the 10.6% delinquent (past due, not yet defaulted) means roughly 15% of the portfolio is in some stage of distress — worth flagging as a headline risk metric.

## Notable Relationships

Grouping by loan status shows a consistent, monotonic risk gradient: as status moves from Current → Paid Off → Delinquent → Default, mean interest rate rises (11.35% → 12.21% → 13.36% → 14.23%) and mean credit score falls (684.7 → 670.3 → 645.6 → 617.1). Home Improvement loans have the highest default rate by purpose (6.49%), followed by Personal (4.84%); Education has the lowest (2.38%).

The strongest correlation in the dataset is between credit score and interest rate (r = −0.84), a stronger relationship than typically expected. The scatter plot shows why the number is so strong: rates don't decline smoothly with credit score — they step down in four distinct bands (roughly 500–650, 650–700, 700–750, 750–850), suggesting Wildcat prices loans off a discrete risk-tier table rather than a continuous formula. This is a good example of why the tutorial insists on checking the scatter plot alongside the correlation coefficient — a single number would have hidden this stepped structure. Loan amount and annual income showed essentially no linear correlation (r = 0.02), which is worth a second look given the bimodal-looking loan amount distribution noted above.

## Open Questions and Next Steps

- Should the two apparent loan-amount subpopulations be analyzed separately (e.g., by an amount threshold or by purpose), since averaging across both may misrepresent either group?
- What process produces the missing credit scores, and should the concentration among Delinquent/Default loans change how risk models handle imputation versus exclusion?
- After standardizing the `state` duplicates, does default rate or loan volume show meaningful geographic concentration?
- The discrete rate-tier pattern is a hypothesis based on the scatter plot alone — worth confirming against Wildcat's actual pricing policy if available, since EDA findings here are exploratory, not conclusive.

## Section 12 Checklist Verification

| Check | Expected Value | Actual Value | Confirmed? |
|---|---|---|---|
| Shape | (2,340 rows, 12 columns) | (2,340 rows, 12 columns) | Yes |
| Null credit_score | 47 | 47 | Yes |
| Most common loan purpose | Home Improvement (724) | Home Improvement (724) | Yes |
| origination_date type | Should be datetime, not text | Converted to datetime64[us] in Step 2 | Yes |

All four checklist benchmarks match exactly, confirming the file loaded correctly with no row loss and every downstream script ran against the correct data. Note that some Section 6/8 benchmarks in the tutorial text itself (e.g., "~$12,400" average loan, "~625" average credit score, a positive loan_amount/annual_income correlation) do **not** match this dataset's actual values, even though the four structural checks above line up exactly. This is most likely because this is a simulated dataset and each student's copy may be independently generated with different underlying values — but that's worth confirming with your instructor rather than assuming, since it could also indicate a different file version. Either way, trust the numbers your own scripts produce over the tutorial's example figures.

---

*Note: This summary was drafted from the script output as a starting point. Since interpreting findings and forming your own analytical judgment is the actual learning objective of this exercise (see Section 1.2 of the tutorial), review each claim against the script output yourself, and rewrite anything in your own words before submitting.*
