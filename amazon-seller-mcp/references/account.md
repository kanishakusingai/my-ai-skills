# Account and connection

Start with server_info for connection details. Choose daily_briefing for an account overview or sku_360 for a seller item.

Each example is a JSON argument object. Replace placeholders and illustrative values with verified inputs. In the signature, `?` marks optional fields. Check the connected tool for its current contract.

## account_health

Seller Central's Account Health page as data (Seller Performance report): account status, Account Health Rating, order defect rate, late shipment, cancellation, valid tracking and on-time delivery rates against Amazon's targets, and policy violation counts. Metrics outside target are listed first. Read only; returns a reportId if Amazon is still building it.

If the response is pending, resume with its reportId.

Example arguments

```json
{
  "waitSeconds": 5
}
```

Accepted arguments

```ts
{
  reportId?: string;
  // Seconds to wait for Amazon to finish the report before returning its ID (call again later with reportId).
  waitSeconds?: number;
}
```

## audit_recent

Lists recent change decisions from the local audit log (newest first): what was proposed, whether the seller approved, declined or answered, and Amazon's result.

Example arguments

```json
{
  "limit": 10
}
```

Accepted arguments

```ts
{
  // How many entries to return.
  limit?: number;
  // Only entries from this tool, e.g. listing_update_price.
  tool?: string;
}
```

## changes_since

Compares the account with the last time this tool ran (a checkpoint saved on this PC) and lists only what's new: new and cancelled orders, orders that shipped, listings that became unbuyable or buyable, new listing errors, stock that hit zero, price changes, Buy Box won or lost (first 20 ASINs with stock), feeds that finished, and A+ documents approved or rejected. The first run saves a baseline. Read only.

Use saveCheckpoint=false when you want to inspect changes without advancing the comparison point.

Example arguments

```json
{
  "saveCheckpoint": false
}
```

Accepted arguments

```ts
{
  // Save the current state as the new checkpoint (false = peek without moving it).
  saveCheckpoint?: boolean;
}
```

## confirm_change

Resolves a change that is waiting for the seller's approval. ONLY call this after showing the seller the preview and getting their explicit answer in this conversation. Never approve on their behalf. decision: "approve" applies exactly the previewed change; "decline" cancels it; "answer" cancels it and records what the seller said instead.

The example is for a seller who explicitly chose Decline. For an answer, include the seller’s words. After a timeout, inspect the audit log and the affected resource before taking further action.

Example arguments

```json
{
  "confirmationId": "<ID from the displayed preview>",
  "decision": "decline"
}
```

Accepted arguments

```ts
{
  // The seller's own words, required for decision "answer".
  answer?: string;
  // The confirmationId from the change tool's preview.
  confirmationId: string;
  // The seller's decision.
  decision: "approve" | "decline" | "answer";
}
```

## daily_briefing

One morning check of the whole account (India time): today's sales vs yesterday, unshipped orders (overdue / due today / later), low stock, listings where another seller holds the Buy Box, and listings with errors or not buyable. Read only. A part that can't be read is listed under notChecked; the rest still shows.

Example arguments

```json
{
  "lowStockThreshold": 5
}
```

Accepted arguments

```ts
{
  // Units at or below this count as low stock.
  lowStockThreshold?: number;
}
```

## seller_get_account

Shows which Amazon marketplaces this seller account participates in, the store name, and whether any listings are suspended. Use it to check the connection works.

Use server_info first if the question is about currency, timezone or prompt support.

Example arguments

```json
{}
```

Accepted arguments

```ts
{ [key: string]: unknown; }
```

## server_info

Shows this Amazon seller MCP server's version, the marketplace it manages (Amazon.in), and whether the connected app can show approval prompts directly.

Example arguments

```json
{}
```

Accepted arguments

```ts
{ [key: string]: unknown; }
```

## sku_360

One call for the whole picture of a SKU (or the ASIN of one of your listings): status and issues, price, stock and handling time, Buy Box holder and the price to win it, Amazon fees, payout and profit (with costs saved by sku_settings_set), units sold in the last 7 and 30 days, days of stock left, unshipped orders, sales rank, image count, A+ status, saved versions, and suggested next tools. includeReports adds sessions/conversion and returns (slower, Amazon builds reports). Read only; a part that fails is listed under notChecked.

Preserve any notChecked sections when summarising results.

Example arguments

```json
{
  "sku": "<seller SKU>"
}
```

Accepted arguments

```ts
{
  asin?: string;
  // Also sessions, conversion, Buy Box % (last 30 days) and returns (needs report building).
  includeReports?: boolean;
  sku?: string;
  // Seconds to wait for Amazon to finish the report before returning its ID (call again later with reportId).
  waitSeconds?: number;
}
```
