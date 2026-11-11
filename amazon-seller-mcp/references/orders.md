# Orders, shipments and buyer contact

Resolve the real order and item IDs first. Sending a message, review request, cancellation or shipment confirmation requires the seller’s request and the connector’s approval flow.

Each example is a JSON argument object. Replace placeholders and illustrative values with verified inputs. In the signature, `?` marks optional fields. Check the connected tool for its current contract.

## buyer_message_options

Shows which text message types Amazon allows you to send to the buyer of one order right now, each with its character limit, plus the buyer's preferred language. Use before buyer_message_send. Buyer messages can't be read through this server.

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

## buyer_message_send

Sends a text message to the buyer of one order, using a message type Amazon allows for that order (see buyer_message_options). Write in the buyer's language; no links, email addresses, phone numbers or review requests. The seller sees the exact text and must Approve, Decline or answer before anything is sent.

First obtain the allowed type, language and length from buyer_message_options. Only send the exact order-related text the seller approved.

Example arguments

```json
{
  "orderId": "<Amazon order ID>",
  "type": "confirmCustomizationDetails",
  "text": "<exact order-related text in buyer language>"
}
```

Accepted arguments

```ts
{
  orderId: string;
  // The exact message text (max 2000 characters; 800 for confirmCustomizationDetails).
  text: string;
  // Message type; must be allowed for the order.
  type: "confirmOrderDetails" | "confirmDeliveryDetails" | "confirmServiceDetails" | "unexpectedProblem" | "confirmCustomizationDetails";
}
```

## order_cancel

Cancels unshipped orders from the seller side with a reason (BuyerCanceled when the buyer asked; NoInventory etc. otherwise), via Amazon's order acknowledgement feed. Cancels every item of the order unless orderItemIds are given. Shipped or already cancelled orders are refused. The seller must approve; check the result with feeds_status.

Use BuyerCanceled only for an actual buyer request. Verify the item scope, then check the returned feedId.

Example arguments

```json
{
  "orders": [
    {
      "orderId": "<Amazon order ID>",
      "orderItemIds": [
        "<item ID to cancel>"
      ],
      "reason": "BuyerCanceled"
    }
  ]
}
```

Accepted arguments

```ts
{ orders: Array<{ orderId: string; orderItemIds?: Array<string>; reason: "NoInventory" | "BuyerCanceled" | "ShippingAddressUndeliverable" | "CustomerExchange" | "GeneralAdjustment" | "CarrierCreditDecision" | "RiskAssessmentInformationNotValid" | "CarrierCoverageFailure" | "CustomerReturn" | "MerchandiseNotReceived"; }>; }
```

## orders_confirm_shipment

Marks Self Ship orders as shipped with carrier and tracking number (several orders, one approval). Ships every unshipped item unless items are given. Easy Ship orders are refused (Amazon handles those). Known carriers: Delhivery, Blue Dart, DTDC, India Post, Ekart, Xpressbees, Ecom Express, Shadowfax, Shree Maruti, Professional Couriers, Gati, Amazon Shipping; others are sent as "Other" with the name. The seller must approve; each order's result is reported.

Verify Self Ship, carrier, tracking and the quantities shipped. Read the per-order results after approval.

Example arguments

```json
{
  "shipments": [
    {
      "orderId": "<Amazon order ID>",
      "carrier": "Delhivery",
      "trackingNumber": "<actual tracking number>",
      "items": [
        {
          "orderItemId": "<shipped item ID>",
          "quantity": 1
        }
      ]
    }
  ]
}
```

Accepted arguments

```ts
{ shipments: Array<{
  carrier: string;
  items?: Array<{ orderItemId: string; quantity: number; }>;
  orderId: string;
  // ISO time it shipped; default now.
  shipDate?: string;
  shippingMethod?: string;
  trackingNumber: string;
}>; }
```

## orders_get

Gets one order by its Amazon order ID (e.g. 403-1234567-1234567): items, quantities, prices, status, Easy Ship flag, ship-by date and packages.

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

## orders_search

Finds FBM orders created in a date range (India time), optionally filtered by status (e.g. UNSHIPPED) and shipping type (Easy Ship or Self Ship). Returns a compact list with items, totals and ship-by dates. No buyer names or addresses.

Example arguments

```json
{
  "period": "last_7_days",
  "statuses": [
    "UNSHIPPED"
  ],
  "shipping": "self_ship"
}
```

Accepted arguments

```ts
{
  // First day (YYYY-MM-DD, India time), inclusive.
  from?: string;
  // Maximum orders to return.
  limit?: number;
  // A preset range in India time. Ignored when from is given.
  period?: "today" | "yesterday" | "last_7_days" | "last_30_days" | "this_week" | "last_week" | "this_month" | "last_month";
  // Easy Ship, Self Ship, or any.
  shipping?: "any" | "easy_ship" | "self_ship";
  // Only these fulfillment statuses.
  statuses?: Array<"PENDING_AVAILABILITY" | "PENDING" | "UNSHIPPED" | "PARTIALLY_SHIPPED" | "SHIPPED" | "CANCELLED" | "UNFULFILLABLE">;
  // Last day (YYYY-MM-DD, India time), inclusive. Defaults to today.
  to?: string;
}
```

## pick_list

All unshipped FBM orders (last 30 days) as a pick list: units to pick per SKU, and every order sorted by ship-by time with overdue / today / later and Easy Ship flags. Can save a printable HTML page or a CSV in the downloads folder. No buyer names or addresses. Read only.

Example arguments

```json
{
  "shipping": "self_ship",
  "format": "none"
}
```

Accepted arguments

```ts
{
  // Also save a printable HTML page or a CSV.
  format?: "none" | "html" | "csv";
  shipping?: "any" | "easy_ship" | "self_ship";
}
```

## review_request_candidates

Checks your recent shipped orders (last 35 days, newest first, up to `limit` orders checked one by one to respect Amazon's rate limit) and lists the ones where Amazon currently offers 'Request a Review'. Use review_request_send to send one.

Example arguments

```json
{
  "limit": 5
}
```

Accepted arguments

```ts
{
  // Most orders to check (each check is one Amazon call, about 1 per second).
  limit?: number;
}
```

## review_request_send

Sends Amazon's standard 'Request a Review' email (product review + seller feedback) to the buyer of one order. Amazon writes the email; you can't add text. Only possible once per order, 5–30 days after delivery. The seller must Approve, Decline or answer before anything is sent.

Check eligibility first. Use the standard Amazon request and record the result for that order.

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

## returns_summary

Your FBM returns requested in a date range (India time, up to 60 days; default last 30 days), grouped by SKU and by return reason, with units, refunded amount and the latest returns. Read only. Returns a reportId if Amazon is still building the report.

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
  // How many individual returns to list, newest first.
  maxRecent?: number;
  // A preset range in India time. Ignored when from is given.
  period?: "today" | "yesterday" | "last_7_days" | "last_30_days" | "this_week" | "last_week" | "this_month" | "last_month";
  // Reuse a returns report requested earlier.
  reportId?: string;
  // Last day (YYYY-MM-DD, India time), inclusive. Defaults to today.
  to?: string;
  // Seconds to wait for Amazon to finish the report before returning its ID (call again later with reportId).
  waitSeconds?: number;
}
```

## seller_feedback_summary

Your seller feedback (ratings 1–5 buyers left about you, not product reviews) for a period (default last 90 days): average rating, count per star, percent negative (1–2 stars), and the negative and neutral ones with order ID, date and comment so you can respond or ask Amazon to remove them. Buyer e-mails are never shown. Read only.

Example arguments

```json
{
  "days": 30,
  "maxComments": 5
}
```

Accepted arguments

```ts
{
  days?: number;
  maxComments?: number;
  // Seconds to wait for Amazon to finish the report before returning its ID (call again later with reportId).
  waitSeconds?: number;
}
```
