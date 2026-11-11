# Catalog and listing inspection

Use a catalog ASIN to inspect a product and a seller SKU to inspect its offer. For a listing issue, resolve the SKU first, then choose the narrowest diagnostic.

Each example is a JSON argument object. Replace placeholders and illustrative values with verified inputs. In the signature, `?` marks optional fields. Check the connected tool for its current contract.

## catalog_get

Amazon catalog details for any ASIN on Amazon.in: title, brand, product type, browse category, sales rank, images and key attributes.

Example arguments

```json
{
  "asin": "<product ASIN>",
  "includeAttributes": true
}
```

Accepted arguments

```ts
{ asin: string; includeAttributes?: boolean; }
```

## catalog_health_scan

Scans every listing and groups what's wrong, worst first, each group with the tool that fixes it: not buyable/suppressed, listing errors (by Amazon code), out of stock, no price, Buy Box lost (ASINs with stock), missing bullets/description/search terms, short titles, and (checkAplus) ASINs without A+ content. Read only.

Example arguments

```json
{
  "checkAplus": true
}
```

Accepted arguments

```ts
{
  // Check live A+ content per ASIN (one call each, up to 50).
  checkAplus?: boolean;
  // Check the Buy Box on up to 100 ASINs with stock.
  checkBuyBox?: boolean;
  // Also save the rows as a CSV file in the downloads folder (opens in Excel).
  exportCsv?: boolean;
}
```

## catalog_search

Searches the Amazon.in catalog by keywords (optionally limited to brands) or by identifiers (EAN, UPC, GTIN, ISBN, ASIN). Useful before creating a listing on an existing product.

Inspect candidate ASINs with catalog_get. Use listings_search to find the seller’s SKU for a catalog item.

Example arguments

```json
{
  "keywords": [
    "oil sprayer"
  ],
  "limit": 5
}
```

Accepted arguments

```ts
{ brandNames?: Array<string>; identifiers?: Array<string>; identifiersType?: "ASIN" | "EAN" | "GTIN" | "ISBN" | "JAN" | "UPC" | "SKU"; keywords?: Array<string>; limit?: number; }
```

## listings_search

Lists your Amazon.in listings with price, FBM quantity, status and issue count. Filter by SKUs, ASINs, status (BUYABLE / DISCOVERABLE / not buyable), listings with issues, or a word in the title.

Example arguments

```json
{
  "asins": [
    "<product ASIN>"
  ],
  "limit": 5
}
```

Accepted arguments

```ts
{
  asins?: Array<string>;
  limit?: number;
  skus?: Array<string>;
  sortBy?: "sku" | "createdDate" | "lastUpdatedDate";
  status?: "buyable" | "not_buyable" | "discoverable";
  // Case-insensitive word or phrase in the title.
  titleContains?: string;
  // Only listings with issues of this severity.
  withIssues?: "ERROR" | "WARNING";
}
```

## listings_get

One SKU in detail: ASIN, product type, title, status, price, FBM quantity, handling time, and every listing issue (including suppression reasons). Set includeAttributes=true for all listing attributes.

Example arguments

```json
{
  "sku": "<seller SKU>",
  "includeAttributes": true
}
```

Accepted arguments

```ts
{ includeAttributes?: boolean; sku: string; }
```

## listing_audit

Checks one of your listings (give its SKU or its ASIN) for what to improve: Amazon's listing issues and suppression, missing required/recommended fields, title and bullet lengths vs limits, empty search terms, image count, A+ content, Buy Box and price to win, and Brand Analytics search queries not used in the listing. Changes nothing; apply fixes with listing_patch (the seller approves each one).

Example arguments

```json
{
  "sku": "<seller SKU>"
}
```

Accepted arguments

```ts
{
  // Instead of sku: the ASIN of one of your listings.
  asin?: string;
  sku?: string;
}
```

## listing_compare

Puts your listing next to up to 10 competitor ASINs: title length, bullet count and length, description length, image count, Buy Box price, lowest offer, number of offers, sales rank and brand, then lists your gaps (fewer images, shorter bullets, higher price, worse rank) and words competitors use in titles that yours doesn't. Read only. Star ratings and review counts aren't available from Amazon's API.

Compare like products and distinguish factual gaps from suggestions.

Example arguments

```json
{
  "sku": "<seller SKU>",
  "competitors": [
    "<comparable ASIN>"
  ]
}
```

Accepted arguments

```ts
{
  // Instead of sku: the ASIN of one of your listings.
  asin?: string;
  competitors: Array<string>;
  sku?: string;
}
```

## listing_compliance_scan

Checks every listing (up to 100, or chosen SKUs) for the product information Amazon.in and Indian law expect: MRP, country of origin, manufacturer / packer / importer name and address, net quantity, generic name, HSN/tax code, battery details and warranty, plus every field the product type marks required. Field names come from each product type's rules, so only fields that exist for it are checked. Lists what's missing with the value format, most common first. Read only; fill them with listing_set_fields (fields.extra) or listing_fix_issues.

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
{ skus?: Array<string>; }
```

## listing_content_lint

Checks listing text before it goes live, without changing anything: product-type length limits, the search-terms byte limit, banned promotional wording (best seller, free delivery, sale…), medical/eco claims, special characters, repeated words, keywords that repeat the title or brand, and how many top Brand Analytics search queries the text covers. Give a sku (checks the live listing), draft fields, or both (draft fields override the live text).

Example arguments

```json
{
  "sku": "<seller SKU>",
  "draft": {
    "title": "<proposed verified title>"
  }
}
```

Accepted arguments

```ts
{
  // Listing content as plain values. Only the fields given change.
  draft?: {
  brand?: string;
  // All bullet points, in order (replaces the current ones).
  bullets?: Array<string>;
  color?: string;
  description?: string;
  // Other attributes by Amazon name with plain values, e.g. {"item_type_name":"gift box","number_of_items":2}.
  extra?: { [key: string]: string | number | boolean | Array<string | number>; };
  // Search terms (backend keywords): one string or a list.
  keywords?: string | Array<string>;
  manufacturer?: string;
  material?: string;
  modelNumber?: string;
  size?: string;
  title?: string;
};
  // For limits when checking a draft without a sku.
  productType?: string;
  // Search queries to measure coverage; defaults to Brand Analytics data seen this session.
  searchQueries?: Array<{ query: string; volume?: number; }>;
  sku?: string;
}
```

## listing_images

The images buyers see for each listing (all, up to 100, or chosen SKUs): slot (MAIN, PT01…), pixel size and link, with problems: no main image, main image under 1000 px (no zoom), not square, fewer than 6 images, the same picture twice. Read only; reorder with listing_images_set.

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
{ skus?: Array<string>; }
```

## listing_restrictions_check

Checks whether your account may list each ASIN on Amazon.in (brand or category approval, not eligible, ASIN not found) and gives Amazon's approval link when approval is needed. Read only; use before listing_create on an existing ASIN.

Example arguments

```json
{
  "asins": [
    "<product ASIN>"
  ]
}
```

Accepted arguments

```ts
{ asins: Array<string>; conditionType?: "new_new" | "used_like_new" | "used_very_good" | "used_good" | "used_acceptable" | "refurbished_refurbished"; }
```

## product_type_get

Listing fields for an Amazon.in product type: view=required (default: the mandatory fields, each with its value format) or view=all (every field by group). Includes text length limits (title, bullet points). Pass fields=[...] for one field's exact value format and allowed values.

Example arguments

```json
{
  "productType": "<type from product_type_search>",
  "view": "required"
}
```

Accepted arguments

```ts
{
  fields?: Array<string>;
  productType: string;
  requirements?: "LISTING" | "LISTING_OFFER_ONLY" | "LISTING_PRODUCT_ONLY";
  // 'required' for the mandatory fields with their value formats, or 'all' for every field name by group.
  view?: "required" | "all";
}
```

## product_type_search

Finds Amazon.in product types (e.g. VACUUM_CLEANER, HOME_BED_AND_BATH) by keywords or by a product title.

Example arguments

```json
{
  "itemName": "Oil sprayer"
}
```

Accepted arguments

```ts
{
  // A product title; Amazon suggests matching product types.
  itemName?: string;
  keywords?: Array<string>;
}
```

## variation_family

For a SKU or any ASIN: its variation parent, theme (e.g. COLOR/SIZE), and every child with its theme values (colour, size…), your SKU, price, stock and whether it's buyable, plus theme combinations that have no child yet. Read only.

Example arguments

```json
{
  "sku": "<seller SKU>"
}
```

Accepted arguments

```ts
{ asin?: string; maxChildren?: number; sku?: string; }
```

## listing_diff

Shows, field by field, how a listing differs now from a backup (backupFile: listings.json from listings_export), from a saved version (version: from listing_history), or from another of your SKUs (otherSku). Price, stock and handling time are compared too. Read only.

Example arguments

```json
{
  "sku": "<seller SKU>",
  "version": 1
}
```

Accepted arguments

```ts
{ backupFile?: string; otherSku?: string; sku: string; version?: number; }
```

## listing_history

Past versions of one SKU: every approved change made through this server saves the listing just before it (price, stock, handling time and attributes; last 20). Shows each version, what differs from the live listing now, and the approval log entries for the SKU. Use listing_rollback to restore one.

Example arguments

```json
{
  "sku": "<seller SKU>"
}
```

Accepted arguments

```ts
{
  sku: string;
  // Show the full attribute differences for this version (0 = newest).
  version?: number;
}
```

## listings_export

Saves your listings (all, up to 2000, or chosen SKUs) on this PC in downloads\listing-backups\<time>: listings.json with each listing's own attributes, price, stock, handling time and issues (listing_diff compares against it), and a CSV with one row per SKU (title, bullets, description, search terms, price, MRP, stock) to open in Excel. Read only.

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
{ skus?: Array<string>; }
```
