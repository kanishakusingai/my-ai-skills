---
name: amazon-ad-campaign-designer
description: Design Amazon India Sponsored Products launch plans using the verified listing, Helium 10 exports or competitor research. Select targets, set bids and budgets, and prepare separate Exact and Phrase keyword worksheets and Auto settings where appropriate.
---

# Design an Amazon Sponsored Products campaign

For OMSHRIM, apply the sibling [seller context](../omshrim-seller-context/SKILL.md) for product lookup and seller preferences when available. For another seller, use their explicit marketplace and preferences. For diagnosis of an existing campaign, use the sibling `amazon-ad-performance-review` skill when available.

## Establish what the shopper would receive

Fetch the owned listing with attributes, gallery images, Featured Offer and advertising eligibility information. Read the title, product type and category and inspect every available gallery image before selecting targets. Establish how the product operates, its material, the quantity and what comes in the box.

Resolve differences that change search intent. For example, a USB cable in a photo could power a corded product or charge a cordless one. Check the model's operating details before targeting “cordless.” Apply the same care to manual versus electric operation, single items versus two-packs, and refill counts. Continue the draft with supported features, identify the specific listing correction or missing fact, and flag eligibility issues that affect launch. A campaign plan grants no authority to edit the live listing or start spending.

## Build the keyword evidence

1. **Use supplied exports first.** Keep the raw Helium 10 CSVs and their filenames. Run `python scripts/merge_xray.py file1.csv file2.csv` to skip byte-identical exports, normalise phrase identity and read exact metric-column names. Its ranked summary uses the maximum observed search volume across overlapping exports. Keep the source values available for inspection. The default output is the top 300 rows. Increase `--top` when the research question needs wider coverage.
2. **Fill gaps with connected research.** Select competitors that match the verified product and document the ASINs used. Discover current Helium 10 tools and follow their session, pagination, quota and notice instructions. Use only a session ID the tool issued. Join enrichment results by phrase, report partial coverage and label missing metrics. The merge script's `source_file_count` counts distinct exports. Establish distinct competitor coverage from identified ASINs.
3. **Select by shopper intent.** Keep terms that accurately describe the product, including useful misspellings seen in the data. Exclude wrong products, wrong materials, accessory-only searches and unsupported features from the positive list. Stop when the evidence runs out. A rejected candidate stays off the positive list without becoming a negative.
4. **Establish bid currency.** Rupee-marked exports indicate INR. If a connected field such as `suggested_bid_usd` conflicts with the marketplace, use documented response metadata or seller confirmation and explain the unit used. Leave an ambiguous suggestion out of INR calculations until resolved. Distinguish the source suggestion, the proposed or configured bid, and actual CPC.

## Choose campaigns and bids for this ASIN

Use the product, keyword evidence, available performance data and seller's budget to choose which campaigns to propose. When multiple targeting types serve distinct purposes, recommend separate campaigns so the seller can control their budgets.

| Campaign | When it helps | Settings to supply |
| --- | --- | --- |
| Manual Exact | The search phrase closely identifies the verified product or has relevant conversion evidence. | Selected terms and per-keyword bids. |
| Manual Phrase | A verified phrase can reach relevant longer searches worth testing. | Phrase targets, bids and the search intent to monitor. |
| Auto | The seller wants discovery and can fund a bounded test. | State and proposed bid for each available targeting group, including which groups are disabled. |

Give each proposed campaign a budget, dynamic bidding strategy and each placement adjustment. Explain the bid that can apply after adjustments. Dynamic bids down only and zero placement uplifts are conservative starting settings for this seller. Adapt them to the current objective and evidence.

Use landed cost, applicable fees, shipping, returns and taxes where available to estimate contribution before ads and break-even ad spend. Identify omitted costs, including shipping missing from fee quotes. If the seller wants a launch plan before costs are known, give a bounded test with a spend limit and review point. Mark profitability as unknown.

Set bids from relevance, current suggestions and observed results. An aggressive bid from a previous launch is specific to that launch. For an explicitly requested uplift, show the source suggestion, calculation, rounding and effective bid. Avoid promises of orders or organic ranking.

## Handle negatives only when requested

This seller prefers to launch without negatives unless requested. Select requested negatives from actual search intent and verified product capability. Treat ₹50 spent without a sale as a prompt for review only.

Check all positive targets across the plan against both negative lists. Negative Exact must not equal a relevant positive. Negative Phrase must not appear as a phrase within a relevant positive. Use one keyword per line in each input, run the checker, and resolve any reported overlap before handoff.

```text
python scripts/check_negatives.py --positives positives.txt --neg-exact neg-exact.txt --neg-phrase neg-phrase.txt
```

## Prepare the keyword files

Use the available spreadsheet-authoring skill. Prefer the seller's newly supplied template. Otherwise use [the bundled keyword template](assets/keyword_template.xlsx). Its `Data` sheet has explanatory rows 1–3, headers `Keyword | Match Type | Bid` in row 4, and data from row 5. Preserve the supplied layout. If the original is unavailable and a reference is used to reconstruct it, disclose the reconstruction.

For the bundled layout, use `scripts/fill_template.py` with a CSV containing `keyword,bid`. Run it once per selected manual match type with its own target list and output filename, for example:

```text
python scripts/fill_template.py --template assets/keyword_template.xlsx --match Exact --csv exact.csv --out exact.xlsx
python scripts/fill_template.py --template assets/keyword_template.xlsx --match Phrase --csv phrase.csv --out phrase.xlsx
```

Write numeric INR bids for Amazon.in and clear old target rows. Reopen each file and compare every keyword, match type and bid with the selected list. Check for duplicates within each match type, leftover rows, intact headers and explanatory text. Inspect the rendered output. Supply supporting metrics and selection reasons separately when useful. Describe these files as keyword import sheets. A full campaign bulk-upload workbook requires additional campaign settings and records.

## Handoff and review

Deliver the requested files and settings with the research scope, listing conflicts, bid limitations and next review point. When asked for an earlier file, verify that it exists and retrieve or recreate it before linking. Distinguish recommended, saved, submitted and live campaigns. Follow current connector approval requirements for any authorised account change.

After enough delivery and attribution time, inspect spend concentration, actual shopper searches and conversions before raising bids. Promote relevant converting searches to Exact when useful. Spend and click thresholds indicate when to inspect the evidence.
