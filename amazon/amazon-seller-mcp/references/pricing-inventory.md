# Pricing and inventory

Use INR for Amazon.in prices. Keep estimated fees, payout, seller costs and realised profit distinct. Local settings influence planning tools.

Each example is a JSON argument object. Replace placeholders and illustrative values with verified inputs. In the signature, `?` marks optional fields. Check the connected tool for its current contract.

## buybox_target_price

For one of your SKUs: who holds the Buy Box, the price Amazon expects would win it for you, and Amazon's fees and your payout (and profit, if you give costPrice) at your price and at that target. Only suggests; to change the price use listing_update_price (asks for approval).

Example arguments

```json
{
  "sku": "<seller SKU>"
}
```

Accepted arguments

```ts
{
  // Your cost per unit, INR, to show profit.
  costPrice?: number;
  sku: string;
}
```

## competitor_watch

Saves competitor ASINs per SKU on this PC (add/remove), and on each check shows what changed since the last check: Buy Box seller and price, lowest offer, number of offers, sales rank and title, next to your own price. Checks every watched SKU unless one is given. Star ratings and review counts aren't available from Amazon's API. Read only.

Example arguments

```json
{
  "sku": "<seller SKU>",
  "check": true
}
```

Accepted arguments

```ts
{
  add?: Array<string>;
  // Fetch current competitor data (false = only edit the list).
  check?: boolean;
  remove?: Array<string>;
  sku?: string;
}
```

## fees_estimate

Amazon's estimated fees (referral, closing, etc.) for one of your SKUs at a given INR price (FBM), what Amazon pays out, and—if you give your cost per unit—your margin.

Use the shipping field according to its declared meaning. Include the seller’s actual fulfilment and packing costs separately when estimating profit.

Example arguments

```json
{
  "sku": "<seller SKU>",
  "price": 499,
  "costPrice": 200
}
```

Accepted arguments

```ts
{
  // Your cost per unit, INR, to compute margin.
  costPrice?: number;
  // Selling price in INR, including tax.
  price: number;
  // Shipping charged to the buyer, INR.
  shipping?: number;
  sku: string;
}
```

## inventory_low_stock

Lists SKUs whose FBM quantity is at or below a threshold (default 5), lowest first, by scanning your listings.

Example arguments

```json
{
  "threshold": 5,
  "withSalesVelocity": true
}
```

Accepted arguments

```ts
{
  // Also include listings that aren't currently buyable.
  includeNotBuyable?: boolean;
  threshold?: number;
  // Also show units sold per day over the last 30 days and days of stock left, least cover first (checks the 20 lowest-stock SKUs).
  withSalesVelocity?: boolean;
}
```

## margin_scan

Amazon fees, payout, your cost (from sku_settings_set), profit and margin % for every listing at its current price, in batched Amazon calls, worst margin first. Also the break-even price and the lowest price that keeps your minimum margin. Lists SKUs with no saved cost so you can add them. Read only.

Example arguments

```json
{
  "skus": [
    "<seller SKU>"
  ]
}
```

Accepted arguments

```ts
{
  // Minimum margin used where a SKU has none saved.
  defaultMinMarginPercent?: number;
  // Also save the rows as a CSV file in the downloads folder (opens in Excel).
  exportCsv?: boolean;
  maxRows?: number;
  onlyLossMaking?: boolean;
  // Only these SKUs (default: every listing with a price).
  skus?: Array<string>;
}
```

## pricing_competitive

For one of your SKUs (or any ASIN): who holds the featured offer (Buy Box) and at what price, the lowest competing new offers, reference prices, and—for your SKU—the price Amazon expects would win the featured offer.

Example arguments

```json
{
  "sku": "<seller SKU>"
}
```

Accepted arguments

```ts
{ asin?: string; sku?: string; }
```

## reprice_plan

Works out a new price for many SKUs at once: win_buybox uses the price Amazon expects would win the Buy Box; match_lowest uses the lowest other seller's price minus undercutBy. Every price is kept inside your saved min/max price and minimum margin (sku_settings_set), and SKUs that already hold the Buy Box are left alone. Shows the plan with profit at each new price. With apply=true the changed SKUs are validated by Amazon and sent as ONE bulk update after ONE seller approval (check later with feeds_status).

Example arguments

```json
{
  "skus": [
    "<seller SKU>"
  ],
  "strategy": "win_buybox",
  "apply": false
}
```

Accepted arguments

```ts
{
  // Send the planned prices for approval as one bulk update.
  apply?: boolean;
  // Also reprice SKUs where you already hold the Buy Box.
  includeBuyBoxHolders?: boolean;
  // Default: every buyable listing with stock (first 100).
  skus?: Array<string>;
  strategy?: "win_buybox" | "match_lowest";
  // For match_lowest: go this many rupees under the lowest other offer.
  undercutBy?: number;
}
```

## restock_plan

For every listing: units sold in the last 7 and 30 days (from your orders), daily sales speed, days of stock left, the date it runs out, and how many to reorder to cover your supplier lead time plus cover days (saved per SKU with sku_settings_set; defaults 7 and 30 days). Most urgent first. Read only.

Example arguments

```json
{
  "onlyNeedingReorder": true
}
```

Accepted arguments

```ts
{
  defaultCoverDays?: number;
  defaultLeadTimeDays?: number;
  // Also save the rows as a CSV file in the downloads folder (opens in Excel).
  exportCsv?: boolean;
  maxRows?: number;
  // Hide SKUs that don't need a reorder yet.
  onlyNeedingReorder?: boolean;
}
```

## sku_settings_set

Saves per-SKU numbers on this PC once, so other tools never need to ask again: unit cost, packing and shipping cost, min/max price, minimum margin %, supplier lead time, reorder cover days. Used by margin_scan, reprice_plan, restock_plan, sku_360 and profit tools. Give rows (only the given fields change), a CSV (header sku plus any of unit_cost, packing_cost, shipping_cost, min_price, max_price, min_margin_percent, lead_time_days, reorder_cover_days, notes), or nothing to list what's saved. Nothing is sent to Amazon.

Call with {} to read current settings. The example writes local planning inputs that affect later recommendations.

Example arguments

```json
{
  "rows": [
    {
      "sku": "<seller SKU>",
      "unitCost": 200,
      "leadTimeDays": 7
    }
  ]
}
```

Accepted arguments

```ts
{
  // Path to a .csv file instead of rows.
  csvPath?: string;
  rows?: Array<{
  // Days from ordering stock to having it ready.
  leadTimeDays?: number;
  // Never price above this, INR.
  maxPrice?: number;
  // Lowest acceptable profit as % of the selling price.
  minMarginPercent?: number;
  // Never price below this, INR.
  minPrice?: number;
  notes?: string;
  // Box, tape, label per order, INR.
  packingCost?: number;
  // Delete all saved settings for this SKU.
  remove?: boolean;
  // Days of sales a reorder should cover (default 30).
  reorderCoverDays?: number;
  // Your shipping cost per order (Self Ship), INR.
  shippingCost?: number;
  sku: string;
  // What one unit costs you to buy or make, INR.
  unitCost?: number;
}>;
}
```
