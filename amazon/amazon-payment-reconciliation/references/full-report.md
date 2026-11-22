# Repeat the OMSHRIM financial report

When the seller asks for the same financial report or a full reconciliation through today, deliver the three files below in a fresh dated folder. A narrower request can use only the relevant part. Collect current Amazon.in records or use the supplied exports. For “till now”, start at the earliest verifiable activity, show the actual IST cutoff and any gaps by source. Previous outputs provide layout examples only.

Build all three outputs from one signed ledger in INR. Use integer paise or decimal currency, retain IDs as text, and count each underlying event once. For a historical cutoff, apply only releases known by that date. Mark unknown amounts and incomplete coverage explicitly. A deferred refund can affect the account ledger before settlement. Bank receipt requires bank evidence.

## Amazon-payment-reconciliation.xlsx

Keep the original ten sheets in this order.

| Sheet | Contents |
| --- | --- |
| Summary | Period, snapshot time, opening balance, net proceeds, successful payouts, remaining, immediately available, reserved and unexplained difference. State whether the bank confirms receipt. |
| SKU results | Quantities by evidence type, sales, fees, outward and reverse shipping, net proceeds and account-level offsets. |
| Orders | Order and package status, units, signed sale, refund, fees, credits, and net. Explain zero rows from actual offsets or missing finance events. |
| Fees | Base fee, fee GST, gross debits, credits and net cost by category, including closing fees, refund commission, shipping and advertising. Separate customer refunds and tax withholding. |
| Payouts and balances | Transfer IDs, dates, statuses, account type and amounts, available and reserved balances, and the settlement-to-balance reconciliation. |
| Returns | Order/item, reason, RMA, label payer and price, tracking, pickup and receipt evidence, matched finance events and unmatched returns/refunds. |
| Transactions | All source events with signed amount, date, status, identifiers, lifecycle links and inclusion decision. |
| Components | Signed leaf amounts, Amazon category/path, GST, parent transaction ID and inclusion flag. |
| Settlements | Settlement periods, group IDs, transfer references and statement breakdowns used to cross-check the ledger. |
| Audit and notes | Coverage, assumptions, missing evidence, open discrepancies, unresolved reimbursements and verification results. |

## OMSHRIM-finance-dashboard.html

Create a standalone offline file with the original six views covering overview, orders, deductions, returns, payouts and balances, and the transaction ledger. Include the balance bridge, monthly net proceeds, SKU results, category breakdown, order search, transaction drill-down, filtered CSV export and print. Compute every date, count, badge, caption and difference from this run, including a nonzero opening balance or incomplete coverage. Embed only the fields used by the views and escape embedded data.

## Return-charge-audit.md

In simple English, show how each return affects the seller's money. Match refunds to returns and returns to refunds. Check package tracking for RTOs even when the returns report has no entry. Separate customer returns, carrier RTOs and unresolved refunds. Record outbound delivery scans, buyer non-receipt claims, pickup attempts, carrier return delivery scans and seller-confirmed receipt separately. Count confirmed, failed and unknown pickups by stated unit of analysis. Missing tracking leaves the outcome unknown.

For each refunded order, show principal and product GST reversed, original shipping and credits, retained closing and other selling fees, refund commission with GST, confirmed reverse shipping, withholding changes, any posted reimbursement, net refund entry and net order proceeds. Show label amount and payer alongside the evidence for any matching charge. Retain reissued labels without counting order-level charges twice. Track pending claims separately from posted reimbursements. Show the reason, IDs, amounts and missing evidence for each exception.

Report total and average fees per refunded customer-return order. Divide the net service fees of matched distinct orders (including fee GST, after credits) by their distinct order count. Keep customer principal, product GST, withholding, inventory cost and provisional labels outside this average. State the denominator, any unallocated charges and any unmatched orders. With zero qualifying orders, show the average as unavailable. Report RTO fee outcomes separately.

## Verify the outputs

Reopen the workbook, check formula errors and tie the component, transaction, order and SKU figures to their controls, including account-level offsets. Reconcile opening balance plus proceeds less successful payouts to closing balance. Check the available/reserved split independently. Open the HTML offline and test navigation, search, drill-down and CSV export. Compare one refunded order across all three outputs when available. Confirm the dates, signs, summary amounts and disclosed gaps agree. A balanced ledger may still contain an individual fee or refund that warrants review.
