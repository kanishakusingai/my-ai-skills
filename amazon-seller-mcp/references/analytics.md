# Sales and Brand Analytics

Use matching India-time reporting windows. Preserve report IDs while results are pending. Distinguish organic Brand Analytics from advertising campaign metrics.

Each example is a JSON argument object. Replace placeholders and illustrative values with verified inputs. In the signature, `?` marks optional fields. Check the connected tool for its current contract.

## asin_traffic

Seller Central's Business Report for your ASINs (Sales and Traffic report): sessions, page views, Buy Box %, units ordered, sales (INR) and conversion (unit session %) per ASIN, most sessions first. Default: the last 30 full days in India time (Amazon has no data for today yet). Returns a reportId if Amazon is still building it.

Example arguments

```json
{
  "asins": [
    "<product ASIN>"
  ],
  "period": "last_7_days"
}
```

Accepted arguments

```ts
{
  asinGranularity?: "CHILD" | "PARENT";
  // Only these ASINs.
  asins?: Array<string>;
  // First day (YYYY-MM-DD, India time), inclusive.
  from?: string;
  maxRows?: number;
  // A preset range in India time. Ignored when from is given.
  period?: "today" | "yesterday" | "last_7_days" | "last_30_days" | "this_week" | "last_week" | "this_month" | "last_month";
  // Reuse a Sales and Traffic report requested earlier.
  reportId?: string;
  // Last day (YYYY-MM-DD, India time), inclusive. Defaults to today.
  to?: string;
  // Seconds to wait for Amazon to finish the report before returning its ID (call again later with reportId).
  waitSeconds?: number;
}
```

## brand_catalog_performance

For your brand's ASINs: how often they appeared in Amazon search, and the clicks, cart adds, purchases and search sales (INR) that came from it, with click rate and conversion (Brand Analytics Search Catalog Performance report). Periods are WEEK (Sunday–Saturday), MONTH or QUARTER; without a date you get the latest complete one. Returns a reportId if Amazon is still building it.

Example arguments

```json
{
  "asins": [
    "<product ASIN>"
  ],
  "period": "WEEK"
}
```

Accepted arguments

```ts
{
  // Only these ASINs.
  asins?: Array<string>;
  // Any date inside the wanted period.
  date?: string;
  maxRows?: number;
  period?: "WEEK" | "MONTH" | "QUARTER";
  reportId?: string;
  // Seconds to wait for Amazon to finish the report before returning its ID (call again later with reportId).
  waitSeconds?: number;
}
```

## brand_search_query_performance

For your brand's ASINs: which search queries bring impressions, clicks, add-to-carts and purchases, with your ASIN's share of each (Search Query Performance report). Periods are WEEK (Sunday–Saturday), MONTH or QUARTER; without a date you get the latest complete one. Returns a reportId if Amazon is still building it.

Use the same ASIN list and period when resuming a pending report. Compare like reporting windows.

Example arguments

```json
{
  "asins": [
    "<product ASIN>"
  ],
  "period": "WEEK"
}
```

Accepted arguments

```ts
{
  // Your ASINs (Amazon allows about 18 per report).
  asins: Array<string>;
  date?: string;
  maxRows?: number;
  period?: "WEEK" | "MONTH" | "QUARTER";
  reportId?: string;
  // Seconds to wait for Amazon to finish the report before returning its ID (call again later with reportId).
  waitSeconds?: number;
}
```

## brand_search_terms

Amazon.in's most searched terms with the top clicked ASINs, click share and conversion share (Brand Analytics Search Terms report). The report is huge, so give your ASINs and/or keywords to filter it. Weeks run Sunday–Saturday; without a date you get the latest complete period. Returns a reportId if Amazon is still building it.

Example arguments

```json
{
  "keywords": [
    "oil sprayer"
  ],
  "period": "WEEK",
  "maxRows": 10
}
```

Accepted arguments

```ts
{
  // Only rows where one of these ASINs is a top clicked ASIN.
  asins?: Array<string>;
  // Any date inside the wanted period.
  date?: string;
  // Only search terms containing any of these words.
  keywords?: Array<string>;
  maxRows?: number;
  period?: "DAY" | "WEEK" | "MONTH" | "QUARTER";
  // Reuse a report requested earlier.
  reportId?: string;
  // Seconds to wait for Amazon to finish the report before returning its ID (call again later with reportId).
  waitSeconds?: number;
}
```

## keyword_gap

For one of your SKUs: which Brand Analytics search queries (Search Query Performance) use words that are missing from the listing's title, bullet points, description and search terms, most searched first, plus the missing words ranked by search volume. Read only; to edit the listing use listing_patch (asks for approval). Returns a reportId if Amazon is still building the report.

Example arguments

```json
{
  "sku": "<seller SKU>",
  "period": "WEEK",
  "maxQueries": 20
}
```

Accepted arguments

```ts
{
  // Any date inside the wanted period; default is the latest complete one.
  date?: string;
  maxQueries?: number;
  period?: "WEEK" | "MONTH" | "QUARTER";
  // Reuse a Search Query Performance report requested earlier.
  reportId?: string;
  sku: string;
  // Seconds to wait for Amazon to finish the report before returning its ID (call again later with reportId).
  waitSeconds?: number;
}
```

## market_basket

Brand Analytics Market Basket: for each of your ASINs, the products buyers most often bought in the same order and how often (%), marking which of those are your own ASINs, with bundle and cross-sell ideas. Read only; returns a reportId if Amazon is still building it.

Example arguments

```json
{
  "asins": [
    "<product ASIN>"
  ],
  "period": "MONTH"
}
```

Accepted arguments

```ts
{
  // Only these ASINs.
  asins?: Array<string>;
  // Any date inside the wanted period.
  date?: string;
  period?: "WEEK" | "MONTH" | "QUARTER";
  reportId?: string;
  // Seconds to wait for Amazon to finish the report before returning its ID (call again later with reportId).
  waitSeconds?: number;
}
```

## repeat_purchase

Brand Analytics Repeat Purchase: per ASIN, orders, unique customers, % of customers who bought again, and repeat sales (INR and % of sales), best repeat rate first, with brand totals. Read only; returns a reportId if Amazon is still building it.

Example arguments

```json
{
  "asins": [
    "<product ASIN>"
  ],
  "period": "MONTH"
}
```

Accepted arguments

```ts
{
  // Only these ASINs.
  asins?: Array<string>;
  // Any date inside the wanted period.
  date?: string;
  period?: "WEEK" | "MONTH" | "QUARTER";
  reportId?: string;
  // Seconds to wait for Amazon to finish the report before returning its ID (call again later with reportId).
  waitSeconds?: number;
}
```

## sales_anomalies

Compares the last 7 full days with the 7 days before (or the days you choose) per ASIN — sessions, conversion, Buy Box %, units and sales — and lists ASINs with a real drop (or spike), each with the likely cause from the listing now: not buyable, out of stock, price change since the earlier period, or Buy Box loss. Read only; uses the Sales and Traffic report (cached).

Example arguments

```json
{
  "days": 7,
  "minSessions": 20
}
```

Accepted arguments

```ts
{
  days?: number;
  includeSpikes?: boolean;
  minDropPercent?: number;
  // Ignore ASINs with fewer sessions than this in the earlier period.
  minSessions?: number;
  // Seconds to wait for Amazon to finish the report before returning its ID (call again later with reportId).
  waitSeconds?: number;
}
```

## sales_get_metrics

Units sold, order count and sales (INR) for a period in India time, grouped by hour/day/week/month or as one total, optionally for one ASIN or SKU. Set compare=true to also get the previous period of the same length and the change.

Example arguments

```json
{
  "sku": "<seller SKU>",
  "period": "last_7_days",
  "granularity": "day",
  "compare": true
}
```

Accepted arguments

```ts
{
  asin?: string;
  // Also return the previous period and the difference.
  compare?: boolean;
  // First day (YYYY-MM-DD, India time), inclusive.
  from?: string;
  granularity?: "hour" | "day" | "week" | "month" | "total";
  // A preset range in India time. Ignored when from is given.
  period?: "today" | "yesterday" | "last_7_days" | "last_30_days" | "this_week" | "last_week" | "this_month" | "last_month";
  sku?: string;
  // Last day (YYYY-MM-DD, India time), inclusive. Defaults to today.
  to?: string;
}
```
