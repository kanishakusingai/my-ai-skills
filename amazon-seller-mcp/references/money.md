# Payments and profit

Use account balance for available funds, payout groups for transfers, settlement reports for period breakdowns and order transactions for order-level money movement.

Each example is a JSON argument object. Replace placeholders and illustrative values with verified inputs. In the signature, `?` marks optional fields. Check the connected tool for its current contract.

## finances_balance

Your current Amazon seller balance in INR per account type: total, available (to be paid out), reserved, and its deferred and account-level reserve parts.

Example arguments

```json
{}
```

Accepted arguments

```ts
{ [key: string]: unknown; }
```

## finances_order

The full money breakdown of one order (e.g. 403-1234567-1234567) from Amazon's financial transactions: sale, each Amazon fee, tax, refunds and the net amount, in INR with India-time dates.

Example arguments

```json
{
  "orderId": "<Amazon order ID>"
}
```

Accepted arguments

```ts
{ orderId: string; }
```

## finances_payouts

Amazon payouts (settlement groups) opened in a date range (India time, up to 180 days), newest first: status (Open/Closed), transfer status, period, amount in INR and transfer date, to match against your bank.

Use transfer dates and amounts for bank matching. Group-level status alone does not establish a bank credit.

Example arguments

```json
{
  "period": "last_30_days"
}
```

Accepted arguments

```ts
{
  // First day (YYYY-MM-DD, India time), inclusive.
  from?: string;
  // Maximum payouts to return.
  limit?: number;
  // A preset range in India time. Ignored when from is given.
  period?: "today" | "yesterday" | "last_7_days" | "last_30_days" | "this_week" | "last_week" | "this_month" | "last_month";
  // Last day (YYYY-MM-DD, India time), inclusive. Defaults to today.
  to?: string;
}
```

## finances_transactions

Amazon financial transactions (order payments, refunds, service fees, adjustments...) posted in a date range (India time, up to 180 days), with totals in INR per transaction type and per breakdown type (Sales, Expenses, Tax...). Totals cover every fetched transaction; only the first `limit` rows are listed.

The displayed row limit and the aggregate totals can cover different numbers of rows.

Example arguments

```json
{
  "period": "last_7_days",
  "limit": 20
}
```

Accepted arguments

```ts
{
  // First day (YYYY-MM-DD, India time), inclusive.
  from?: string;
  // Maximum transaction rows to list (totals still cover all).
  limit?: number;
  // A preset range in India time. Ignored when from is given.
  period?: "today" | "yesterday" | "last_7_days" | "last_30_days" | "this_week" | "last_week" | "this_month" | "last_month";
  // Last day (YYYY-MM-DD, India time), inclusive. Defaults to today.
  to?: string;
  // Only this transaction type, e.g. Shipment, Refund, ServiceFee, Adjustment (case-insensitive).
  type?: string;
}
```

## profit_by_sku

Profit per SKU for a date range (India time, up to 180 days) from Amazon's financial transactions: units, sales, Amazon fees, refunds and net proceeds in INR. Pass unitCosts (SKU → your cost per unit in INR) to also get cost, profit and margin. Fees not tied to a SKU (subscription, ads) are shown separately as unattributed.

Supply actual per-unit costs and carry unattributed charges separately.

Example arguments

```json
{
  "period": "last_30_days",
  "unitCosts": {
    "<seller SKU>": 200
  }
}
```

Accepted arguments

```ts
{
  // First day (YYYY-MM-DD, India time), inclusive.
  from?: string;
  // A preset range in India time. Ignored when from is given.
  period?: "today" | "yesterday" | "last_7_days" | "last_30_days" | "this_week" | "last_week" | "this_month" | "last_month";
  // Last day (YYYY-MM-DD, India time), inclusive. Defaults to today.
  to?: string;
  // Your cost per unit in INR per SKU, e.g. {"GIFT-1": 250}.
  unitCosts?: { [key: string]: number; };
}
```

## settlement_summary

Amazon's settlement reports (made automatically every settlement period, kept for 90 days), newest first: period, deposit date and total paid, split into sales, Amazon fees, refunds, tax withheld (TCS/TDS) and other charges, with the biggest lines. Read only. For bank transfer status use finances_payouts.

Example arguments

```json
{
  "count": 3
}
```

Accepted arguments

```ts
{
  // How many recent settlements to show.
  count?: number;
}
```
