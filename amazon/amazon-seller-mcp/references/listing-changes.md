# Listing changes

Examples with sample prices, quantities or replacement text illustrate the input shape. Use verified seller values and the connector’s approval flow before applying an account change.

Each example is a JSON argument object. Replace placeholders and illustrative values with verified inputs. In the signature, `?` marks optional fields. Check the connected tool for its current contract.

## listing_clone

Creates a new SKU from one of your listings. mode=offer: another offer on the same ASIN (e.g. a second SKU for a different price or stock). mode=product: a new product with all of the source's attributes copied and your changes applied (e.g. a new colour or size) — identifiers are dropped, so give a barcode in fields.extra (externally_assigned_product_identifier) or mark it exempt; set variationParentSku to make it a variation child. Missing required fields are listed. Amazon validates, then the seller approves.

Product mode needs the new product’s identifiers or exemption and verified variation details.

Example arguments

```json
{
  "sourceSku": "<seller SKU>",
  "newSku": "<new unique SKU>",
  "mode": "offer",
  "price": 499,
  "quantity": 3
}
```

Accepted arguments

```ts
{
  // For mode=product: what's different, e.g. {title, color, size}.
  fields?: {
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
  handlingDays?: number;
  mode?: "offer" | "product";
  newSku: string;
  // Default: the source's price.
  price?: number;
  quantity?: number;
  sourceSku: string;
  // Make the new product a variation child of this parent SKU.
  variationParentSku?: string;
  // Variation theme for the child, e.g. COLOR or SIZE/COLOR (default: the parent's).
  variationTheme?: string;
}
```

## listing_create

Creates a new listing under a new SKU. Either offer on an existing ASIN (give offerOnAsin with price and quantity; product type is looked up) or create a full product (give productType and attributes in Amazon's format; use product_type_get first). Amazon validates first, missing required fields are listed, and the seller must approve.

The example adds an offer to an existing ASIN. For a new product, get its type schema and construct the required attributes.

Example arguments

```json
{
  "sku": "<seller SKU>",
  "offerOnAsin": {
    "asin": "<product ASIN>",
    "price": 499,
    "quantity": 3
  }
}
```

Accepted arguments

```ts
{ attributes?: { [key: string]: Array<{ [key: string]: unknown; }>; }; offerOnAsin?: { asin: string; condition?: "new_new" | "new_open_box" | "refurbished_refurbished" | "used_like_new" | "used_very_good" | "used_good" | "used_acceptable"; handlingDays?: number; price: number; quantity: number; }; productType?: string; sku: string; }
```

## listing_delete

Deletes one of your SKUs from Amazon.in. This removes the listing. Amazon has no preview for deletes; the seller sees the listing's details and must approve.

Read the current SKU and its offer before presenting the deletion. Confirm the exact seller SKU.

Example arguments

```json
{
  "sku": "<seller SKU>"
}
```

Accepted arguments

```ts
{ sku: string; }
```

## listing_fix_issues

Every listing error and warning Amazon reports (all listings or chosen SKUs, up to 100 with issues), each explained in plain words, with a proposed fix where it's safe: the value the product page already has, or the one value your other listings of the same product type use. Fields that need your knowledge are listed with their format; give them in fixes. With apply=true the proposed fixes (useSuggestions) and your fixes are validated by Amazon and sent as ONE bulk update after ONE seller approval. Price, stock and identifier fields are left to their own tools.

Start in proposal mode. Inspect exclusions and confirm which fixes have seller evidence before apply=true.

Example arguments

```json
{
  "skus": [
    "<seller SKU>"
  ],
  "apply": false
}
```

Accepted arguments

```ts
{
  apply?: boolean;
  // Your values in plain form, e.g. [{"sku":"GIFT-1","field":"country_of_origin","value":"IN"}].
  fixes?: Array<{ field: string; sku: string; value: string | number | boolean | Array<string | number>; }>;
  skus?: Array<string>;
  // With apply: also send the proposed fixes.
  useSuggestions?: boolean;
}
```

## listing_images_set

Sets a listing's images in a new order (first = main image, up to 9). Each image is a slot of its current images (MAIN, PT01…PT08, see listing_images) or an https link on Amazon's image hosts (media-amazon.com, ssl-images-amazon.com, images-amazon.com), e.g. an image of another of your products; Amazon downloads the image itself, so other links can't be used. Amazon validates first, then the seller approves; the listing is saved first so listing_rollback can undo it.

The example represents the complete intended order. Use only real current slots or allowed image URLs.

Example arguments

```json
{
  "sku": "<seller SKU>",
  "images": [
    "<verified main slot>",
    "<verified second slot>"
  ]
}
```

Accepted arguments

```ts
{
  // New order, e.g. ["PT02","MAIN","PT01"].
  images: Array<string>;
  sku: string;
}
```

## listing_patch

Edits any attributes of one of your listings with JSON Patch operations on /attributes/<name> (title item_name, bullet_point, product_description, generic_keyword, images, etc.). Values use Amazon's attribute format, e.g. {"op":"replace","path":"/attributes/item_name","value":[{"value":"New title","language_tag":"en_IN","marketplace_id":"A21TJRUUN4KGV"}]}. Use product_type_get for field names and limits. Amazon validates first; the seller must approve.

Inspect product_type_get and existing attributes before constructing a patch. The example illustrates the format for one title.

Example arguments

```json
{
  "sku": "<seller SKU>",
  "patches": [
    {
      "op": "replace",
      "path": "/attributes/item_name",
      "value": [
        {
          "value": "<verified title>",
          "language_tag": "en_IN",
          "marketplace_id": "A21TJRUUN4KGV"
        }
      ]
    }
  ]
}
```

Accepted arguments

```ts
{
  patches: Array<{ op: "add" | "replace" | "merge" | "delete"; path: string; value?: Array<{ [key: string]: unknown; }>; }>;
  // Why, shown to the seller (e.g. 'add missing keywords').
  reason?: string;
  sku: string;
}
```

## listing_rollback

Restores a SKU to a version saved by listing_history (default the newest): every attribute that differs is set back, and attributes added since are removed (except offer, stock, condition and identifiers). Choose fields to restore only some. Amazon validates, the seller approves, and the current listing is saved first so the rollback can be undone too.

Look up the version in listing_history and inspect listing_diff before requesting a restore.

Example arguments

```json
{
  "sku": "<seller SKU>",
  "version": 1,
  "fields": [
    "item_name"
  ]
}
```

Accepted arguments

```ts
{
  // Only these attributes, e.g. ["item_name","purchasable_offer"].
  fields?: Array<string>;
  sku: string;
  version?: number;
}
```

## listing_search_terms_build

Builds a listing's backend search terms within the product type's limit: your words first, then words from Brand Analytics search queries seen in this chat (run keyword_gap or brand_search_query_performance first), then the current terms. New words already in the title, bullets or brand are left out (dropTitleWords also removes them from the current terms), as are plural repeats, ASINs and words Amazon doesn't allow (best, sale, free…). Shows the proposal; apply=true sends it for approval (the listing is saved first, so listing_rollback can undo it).

Example arguments

```json
{
  "sku": "<seller SKU>",
  "words": [
    "<relevant term>"
  ],
  "apply": false
}
```

Accepted arguments

```ts
{
  apply?: boolean;
  // Also remove current words that are already in the title, bullets or brand (Amazon indexes those anyway).
  dropTitleWords?: boolean;
  // Keep current search-term words that still fit.
  keepCurrent?: boolean;
  sku: string;
  useSearchQueries?: boolean;
  // Your own words or phrases, most important first.
  words?: Array<string>;
}
```

## listing_set_fields

Changes a listing's title, bullet points, description, search terms, brand, colour, size, material, model number or any other attribute using plain values; the server builds Amazon's attribute format (marketplace and language tags) from the product type. The text is checked first (length limits, banned promotional/medical words, keyword bytes) and problems appear as warnings. Amazon validates, then the seller approves. The listing is saved first so listing_rollback can undo it.

A supplied bullet list replaces the existing list. Read all bullets before preparing the edit.

Example arguments

```json
{
  "sku": "<seller SKU>",
  "fields": {
    "title": "<verified title>"
  }
}
```

Accepted arguments

```ts
{
  // Listing content as plain values. Only the fields given change.
  fields: {
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
  reason?: string;
  sku: string;
}
```

## listing_update_handling_time

Sets how many days you need to ship (handling time) for one of your SKUs. Asks the seller to approve first.

Example arguments

```json
{
  "sku": "<seller SKU>",
  "days": 2
}
```

Accepted arguments

```ts
{ days: number; sku: string; }
```

## listing_update_price

Changes the selling price (INR, including tax) of one of your SKUs. Amazon validates the change first, then the seller is asked to Approve, Decline or answer. Nothing changes without approval.

Example arguments

```json
{
  "sku": "<seller SKU>",
  "price": 499
}
```

Accepted arguments

```ts
{
  // New price in INR, including tax.
  price: number;
  sku: string;
}
```

## listing_update_quantity

Sets the FBM (merchant-fulfilled) stock quantity of one of your SKUs. Asks the seller to approve first.

Example arguments

```json
{
  "sku": "<seller SKU>",
  "quantity": 3
}
```

Accepted arguments

```ts
{ quantity: number; sku: string; }
```

## listings_bulk_update

Changes price, FBM stock, handling time and/or attributes of up to 100 SKUs with ONE approval. Each SKU is validated by Amazon first; SKUs that fail or don't exist are excluded and listed. On approval the valid ones are sent as one Amazon listings feed; check it with feeds_status.

Retain excluded SKUs and the feedId. Report accepted and rejected rows separately after feeds_status.

Example arguments

```json
{
  "rows": [
    {
      "sku": "<seller SKU>",
      "quantity": 3
    }
  ]
}
```

Accepted arguments

```ts
{
  // Instead of rows: path to a UTF-8 CSV with header sku plus any of price,quantity,handling_days (blank cell = no change).
  csvPath?: string;
  // One row per SKU; each SKU at most once.
  rows?: Array<{
  // New handling time in days.
  handlingDays?: number;
  // Extra attribute patches, same format as listing_patch.
  patches?: Array<{ op: "add" | "replace" | "merge" | "delete"; path: string; value?: Array<{ [key: string]: unknown; }>; }>;
  // New price in INR, including tax.
  price?: number;
  // New FBM stock.
  quantity?: number;
  sku: string;
}>;
}
```

## listings_find_replace

Replaces a word or phrase in titles, bullets, descriptions and/or search terms across your listings (all or chosen SKUs, up to 100 changed), e.g. "Diwali" → "Christmas". The text is matched literally (whole words by default). Each changed listing is checked (length limits, banned words); listings whose new text breaks a limit are left out. Shows every change; apply=true validates with Amazon and sends ONE bulk update after ONE seller approval. Brand and identifiers are never touched.

Example arguments

```json
{
  "skus": [
    "<seller SKU>"
  ],
  "fields": [
    "description"
  ],
  "find": "<old wording>",
  "replace": "<approved wording>",
  "apply": false
}
```

Accepted arguments

```ts
{ apply?: boolean; fields?: Array<"title" | "bullets" | "description" | "keywords">; find: string; matchCase?: boolean; replace: string; skus?: Array<string>; wholeWord?: boolean; }
```

## listing_offer_set

Sets offer details the price tools don't: a sale price with start and end dates (or removeSale), the MRP, the Amazon Business (B2B) price and quantity discounts (e.g. 5+ units at ₹450), and the shipping template. Checks MRP against your price and the sale against your saved minimum price (sku_settings_set). Amazon validates first, then the seller approves; the listing is saved first so listing_rollback can undo it.

Use the seller’s actual offer values and review the price tier or sale window in the preview.

Example arguments

```json
{
  "sku": "<seller SKU>",
  "businessPrice": 449
}
```

Accepted arguments

```ts
{
  businessPrice?: number;
  // Maximum retail price, INR.
  mrp?: number;
  // Amazon Business quantity discounts; [] removes them.
  quantityTiers?: Array<{ minQuantity: number; price: number; }>;
  removeSale?: boolean;
  // Sale price (INR incl. tax) and IST dates, inclusive.
  salePrice?: { from: string; price: number; to: string; };
  // Shipping template ID, as in your other listings' merchant_shipping_group.
  shippingTemplate?: string;
  sku: string;
}
```
