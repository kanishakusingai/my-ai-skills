---
name: amazon-ad-campaign-designer
description: Design a complete Amazon India (Sponsored Products) ad campaign for a product - economics and break-even ACOS, keyword research from Helium 10 Xray/Cerebro CSVs or competitor data, Exact/Phrase/Auto campaign structure, bids, budgets, placements, negative keywords, and ready-to-upload keyword Excel files. Use this skill whenever the user asks to make ads, create a campaign, find keywords, set bids, build negative keywords, or "do PPC" for any Amazon listing or ASIN, even if they only upload competitor keyword CSVs or say "make ad for my product".
---

# Amazon Ad Campaign Designer

Builds a launch-ready Sponsored Products plan for one product. Default market: Amazon India (INR, marketplace A21TJRUUN4KGV). Keep replies short, direct, and plain: the user wants actions, not theory.

## Golden rules

1. **Only what the product really is.** Never put a feature, count, or spec in keywords or copy that the listing or images don't prove (e.g. "2-in-1", "3-in-1", number of batteries). If a feature is unclear, ask. Do not guess.
2. **Never block your own traffic.** Before giving negatives, run `scripts/check_negatives.py` against the positive keywords.
3. **State assumptions.** Cost, fees, and conversion rate are assumptions until the seller confirms them. Say so in one line.
4. **Nothing launches until the listing is right.** Title, bullets and images must match the product first.

## Workflow

### 1. Collect inputs
Ask only for what's missing: ASIN (or SKU), selling price, landed cost, and competitor keyword files (Helium 10 Xray/Cerebro CSVs). If Amazon tools are connected, read the listing (title, price, images, bullets) instead of asking. Helium 10 calls can be limited, so prefer CSVs the user already has and don't burn the last call.

### 2. Check the listing
Compare title, bullets and images with what the product does. Flag mismatches (wrong feature counts, other sellers' images, unverified specs) and fix or confirm them before ads. Changes to the live listing need the user's explicit approval.

### 3. Economics
- Profit per unit = price - landed cost - closing fee - referral fee - shipping - returns allowance - GST on fees (18%).
- Break-even ACOS = profit / price.
- Max affordable CPC = break-even ACOS x price x conversion rate (use 4-5% for a new listing).
- Show a one-line result: price, profit, break-even ACOS, max CPC.

### 4. Keyword analysis
Run `scripts/merge_xray.py <csv files...>` to merge competitor files: it dedupes keywords and reports search volume, suggested bid, competing products, and how many competitors rank for each.
Then filter by hand:
- Keep: terms that describe exactly this product (type, use, key feature). Terms that appear in several competitors are strongest.
- Drop: wrong product types, other brands, features the product doesn't have, very broad one-word terms for a new listing, blower-only or accessory-only terms when those don't match.
- Keep common misspellings customers really use (e.g. "vaccum", "vaccine cleaner") when they show volume.

### 5. Campaign structure
| Campaign | Keywords | Bid | Daily budget | Placement |
|---|---|---|---|---|
| Exact | 12-18 closest terms | slightly below suggested bid | 150-200 | Top of search +30% |
| Phrase | 10-18 broader terms | 1-3 below Exact | 100 | Top of search +30% |
| Auto | none (Amazon picks) | lowest | 100 | Dynamic bids down only, 0% other placements |
Optional later: product targeting on competitor ASINs (bid ~5, budget 100, 0% placements).
Rules: bids must stay under max CPC from step 3. Suggested bids from Helium 10 are a ceiling guide, not a target. Start lower for listings with no reviews.

### 6. Negative keywords
Give two copy-paste lists (one keyword per line), to be added to all campaigns:
- **Negative Exact:** bare generic or wrong-intent terms that would waste money only as exact searches (e.g. bare "vacuum", bare "blower" for a vacuum).
- **Negative Phrase:** any search containing wrong-product words (wet and dry, robot, mop, steam), competitor brands, and features the product lacks.
Safety checks:
- Run `scripts/check_negatives.py`: it fails if a negative phrase appears inside any positive keyword or if a negative exact equals one.
- Never negate terms real buyers of this product use (a past mistake: "car cleaner", "dust cleaner" for a car vacuum). If unsure, leave it out and let the Auto search-term report decide.
- Do not negate a feature the product has (e.g. "carpet" when the kit includes a carpet brush) unless the user says so. Mention such trade-offs in one line.

### 7. Deliver
- Fill the user's bulk template with `scripts/fill_template.py`. Template layout: sheet "Data", header row 4 = Keyword | Match Type | Bid, data from row 5. One file per match type (Exact, Phrase). Use the user's uploaded template if present.
- Save to /mnt/user-data/outputs and call present_files.
- In chat, show: economics line, campaign table (budget, bids, placements), negative lists in code blocks, and anything left out and why.

### 8. Optimization plan (always include)
- After ~7 days, read the Auto search-term report: move terms with sales into Exact; add terms with ₹50+ spend and no sale as negatives.
- If conversion is under 4% after 100 clicks, cut bids by ₹2 and check listing/price; consider a small coupon.
- Raise bids ₹1-2 only if impressions are very low and ACOS is under break-even.
- Review CTR (below ~0.3% usually means title/main image problem, with a small sample the cause may just be low data).

## Scripts
- `scripts/merge_xray.py` - merge Xray/Cerebro CSVs into one ranked keyword table.
- `scripts/fill_template.py` - write keywords, match type, bids into the bulk template.
- `scripts/check_negatives.py` - validate negatives against positive keywords.
Run with `python3 scripts/<name>.py --help`.
