# Interpreting repeated return labels

Example: a returns report contains two different RMA/tracking IDs for the same order item, each listing a ₹92 seller-paid label. That establishes two issued label records with listed values totalling ₹184. It does not establish two physically returned units or ₹184 already deducted.

Keep these separate in the report:
- Every RMA, requested quantity and tracking number, with no automatic deletion.
- Distinct order-item count, explicitly not a physical return count.
- Return delivery dates and carrier evidence where available.
- Actual reverse-shipping debits found in financial transactions.
- Unbilled issued-label amounts, if relevant, as provisional exposure.

If the finance ledger contains one shipping debit, identify its event and distinguish forward versus reverse shipping before matching it to labels. Existing forward shipping on a refunded order remains part of original deductions; do not deduct it again. If a return summary says ₹249 refunded but financial principal and tax total ₹254, disclose the ₹5 discrepancy and reconcile money using the financial event without adding both amounts.

Conclude with what the evidence proves and what is unresolved. Avoid telling the seller they paid for all generated labels unless the debits support it.
