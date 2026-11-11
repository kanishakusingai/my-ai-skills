---
name: amazon-payment-reconciliation
description: Reconcile Amazon.in seller proceeds, deductions, payouts, available and deferred balances, SKU units and return charges. Use for payment audits, Excel reconciliation reports, money still receivable, or explaining a particular charge.
---

# Reconcile Amazon.in seller payments

Use the sibling OMSHRIM seller context when available. State the reporting period, as-of date and currency (INR). Use India time for date boundaries. Account proceeds measure money posted to the seller account. Calculating profit also requires the seller's costs.

For a single charge, start with the order or transaction and explain the relevant line. For a payout question, match the settlement group and transfer status. For a full audit, build the ledger and workbook below. Distinguish what Amazon reports as transferred from what the seller's bank statement confirms as credited.

## Collect evidence for the requested period

Discover the current connector tools and check their limits before fetching data.

| Question | Source and how to use it |
| --- | --- |
| What is available or held? | Use `finances_balance`. Record the snapshot date, account type, total, available amount and reserve breakdown. Keep the relationship between totals and their components. |
| What posted, and why? | Use `finances_transactions` for the posted event population and control totals. Read `finances_order` for each relevant order's fee categories, fee GST, product GST, refunds, withholding and quantities. Match the order detail to its ledger event. |
| What did Amazon transfer? | Use `finances_payouts` for settlement groups and transfer outcomes, and `settlement_summary` or available settlement reports for period breakdowns. Retain posting date, settlement period and transfer date where they differ. A group opened before the requested period may transfer during it. |
| What happened to the units? | Use order records for quantities and fulfilment status. Use `returns_summary` for requests. Obtain the detailed returns file when the summary omits label cost, payer, RMA, order-item ID, tracking or return-delivery dates. Use the finance ledger for money posted. |

Track the requested dates, actual returned dates, counts, truncation and pending reports for each source. Historical observations included 180-day finance windows, 200 listed finance rows, 100 payout groups, 60-day return windows and 10 settlements. Use the current schema and actual response to establish coverage. A filename or a default date range cannot establish the reporting period.

Use non-overlapping windows for each date basis. Transaction totals can cover more rows than the connector displays. When that happens, narrow the windows or retrieve a detailed report before attributing the full total to orders or SKUs. Reuse a pending report ID with its original explicit dates. Describe any unretrievable history or unresolved coverage gap.

## Build one ledger of posted money

Keep the raw records and source identifiers. Use one authoritative monetary entry per event or component. Record the posted sign, date, transaction ID, order/item and SKU when available, lifecycle status, category, amount and inclusion decision. Log the reason for each exclusion. Parent transaction totals, order breakdowns and settlement summaries can describe the same money. Use the totals as cross-checks when the component rows drive the calculation.

- Separate customer principal, product GST and promotional rebates. If a discount on tax is already reflected in posted sales, count it once.
- Classify order fees, outward shipping, posted reverse-shipping debits, fee GST, billed advertising, cancellation fees, refund fees, customer refunds, TCS/TDS and adjustments. Keep unknown amounts visible. TCS/TDS is withholding and should be shown separately from Amazon service fees. If no withholding is separately identifiable, report that limitation without drawing a tax-liability conclusion.
- Use the advertising amount billed in the finance records. Campaign performance exports can cover different dates. Treat their spend as supporting detail when comparing charges.
- Match deferred and released records by transaction ID where available. Where IDs differ, check order item, transaction type, components and release evidence against the balances. Retain both lifecycle records and count the underlying proceeds once when supported. Equal amounts on the same order can be legitimate repeated fees. Flag uncertain matches for review.
- Classify transfers as payouts. Keep opening balances and settlement carry-forwards separate from period income and expenses. Total successful positive transfers separately from open groups, failed or unknown transfers and negative settlement balances.

## Prove the balance

For the same period and account scope, calculate:

```text
Expected closing balance = opening balance + net posted proceeds − successful payouts
Unexplained difference   = reported closing balance − expected closing balance
```

Net posted proceeds include the signed sales, refunds, fees, withholding and adjustments included in the ledger. Enter successful payouts as positive amounts in the subtraction. Establish the opening balance if activity predates the extract. For a historical cutoff, use a balance from that date or show a separate bridge of later proceeds and payouts to the current snapshot. If the opening balance or intervening activity is missing, label the tie-out incomplete and identify what is missing.

Separately tie available funds and offsets, deferred funds, and any account-level reserve to the reported total using the API's definitions. If a reserved subtotal already includes deferred funds, use either the subtotal or its components in the sum. Report any unexplained difference as a difference. Give a release date only when the evidence supports one.

## Reconcile SKU quantities and returns

Show ordered/unshipped, cancelled, shipped and financially posted units according to their source. Track units with posted refunds, requested return quantities and physically received returns separately. A one-unit request against a 25-unit order contributes one requested unit. Confirm physical receipt from delivery evidence.

Retain every authorisation, RMA and tracking number. Multiple records for one order item can represent multiple units, a replacement label or a repeated request. Report raw request count, distinct order-item count, requested quantities and confirmed receipts with clear labels.

For shipping, distinguish the original outward charge from a posted reverse-shipping debit. Include a reverse charge in confirmed deductions only when the finance event supports it. Show seller-paid labels awaiting a matching debit as provisional exposure, retaining their reported tax treatment and any reissue uncertainty. If a scenario would help the seller, label it separately from the confirmed balance. Use the [worked return example](references/return-evidence.md) for repeated ₹92 labels and a refund discrepancy between reports.

For each SKU, show units sold on the stated basis, refunded units, requested quantities, gross posted sales, item fees, outward shipping, refund impact, actual return shipping and net proceeds. Split released and deferred order proceeds. Carry account-level advertising and cancellation offsets below the SKU totals unless the seller requests an allocation with a supported basis.

## Deliver and verify

Use the available spreadsheet skill for a requested Excel report. Include a summary, SKU results, order detail, fees, payout status, balances, returns, source ledger and inclusion/exclusion log. Combine sheets where that aids review. Link summary figures to the authoritative rows with formulas. After export, reopen the workbook and verify order totals, fee subtotals, SKU totals with account-level offsets, successful payouts and both balance reconciliations.

Lead the handoff with **amount paid out, net seller balance remaining and amount immediately available** as of the stated date. Specify whether the payout figure is Amazon-confirmed or also bank-matched. Then show confirmed deductions, provisional return costs, recent unposted activity and any unexplained difference. For a charge question, cite the event and amount, explain what the line establishes, and identify any inference.
