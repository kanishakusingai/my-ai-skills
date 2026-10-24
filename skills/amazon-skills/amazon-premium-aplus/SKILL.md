---
name: amazon-premium-aplus
description: Build Amazon.in Premium A+ Content (EBC) for the seller's brand-registered ASINs. Use when the user asks to plan, write, draft, validate, save, fix, or submit Premium A+ content, pick A+ modules, or needs A+ image sizes, mobile/desktop image specs, image prompts, or character limits. Covers all 19 Premium modules with verified JSON shapes, the amazon-sp-mcp workflow, and fixes for known validator errors.
---

# Amazon.in Premium A+ Content

## Hard rules

- Maximum 7 modules per document. Never mix `STANDARD_*` and `PREMIUM_*` modules.
- `contentType: "EBC"`, `locale: "en-IN"`.
- Every write tool (`aplus_create`, `aplus_update`, `aplus_attach_asins`, `aplus_submit`) returns a preview. Show it to the seller and call `confirm_change` only after their explicit approval in this conversation.
- Copy must match the listing. Pull the facts with `listings_get` (`includeAttributes: true`) before writing, and don't claim anything the listing doesn't state.
- Banned in copy: "warranty", "guarantee", prices, discounts, shipping claims, phone numbers, emails, URLs, emojis, HTML, competitor names, "best seller" / "#1" claims, and customer review quotes.

## Workflow

1. **Facts.** Fetch with `listings_get` (`includeAttributes: true`). Note anything the seller hasn't confirmed.
2. **Plan.** Choose up to 7 modules using the blueprint below. Write copy to the limits in the quick-reference table.
3. **Images.** Give the seller a shot list with exact sizes and prompts (template below). Desktop and mobile are separate files where the table says so.
4. **Upload.** `aplus_upload_image` with the full Windows path. Keep `uploadDestinationId`. Use the returned crop unless the seller wants a different crop.
5. **Validate.** `aplus_validate` with `asins: [<ASIN>]`. Fix only the reported module and re-validate.
6. **Save.** `aplus_create` (new) or `aplus_update` (existing) → seller approves → `confirm_change`.
7. **Attach and submit.** `aplus_attach_asins` then `aplus_submit`, each with its own approval. Check status later with `aplus_get`, and the live document with `aplus_for_asin`.

Text-only drafts are fine to save early. Add image modules with `aplus_update` once images exist.

## Recommended 7-module blueprint

| # | Module | Job |
|---|--------|-----|
| 1 | PREMIUM_FULL_BACKGROUND_IMAGE | Hero: product plus one-line promise |
| 2 | PREMIUM_HOTSPOT_IMAGE_TEXT | Anatomy: tap points on key parts |
| 3 | PREMIUM_FOUR_COLUMN_IMAGES | Four core benefits |
| 4 | PREMIUM_IMAGE_CAROUSEL or PREMIUM_REGIMEN_CAROUSEL | Use cases, or how-to steps |
| 5 | PREMIUM_VIDEO_TEXT (if video) or PREMIUM_DUAL_IMAGE_TEXT | Demo, or what's in the box |
| 6 | PREMIUM_COMPARISON_SCROLLER (if 2–3 own ASINs) or PREMIUM_TEXT | Choose between your models, or specs as text |
| 7 | PREMIUM_FAQ | Remove purchase doubts |

Choose by buyer question: "What is it?" → hero. "How does it work?" → hotspot or video. "Will it suit me?" → carousel. "Which one?" → comparison. "What if…?" → FAQ.

## Quick reference: images and text

Image rules for all modules: JPG, PNG, or BMP. Maximum 2 MB (target under 500 KB). At least 72 dpi, RGB, no animated GIF. Sizes are minimum width x height in px. Every image needs `altText` (maximum 100 characters, describe the image, no keyword stuffing).

| Module (API type) | Desktop image | Separate mobile image | Text limits | Count |
|---|---|---|---|---|
| FULL_BACKGROUND_IMAGE | 1464 x 600 | 600 x 450 | headline 80, body 300 | 1 |
| TEXT | none | none | headline 80, body 300 | 1 |
| FULL_BACKGROUND_TEXT | 1464 x 600 | 600 x 450 | subhead 40, headline 60, body 300 | 1 |
| FOUR_COLUMN_IMAGES | 300 x 225 each | no (desktop reused) | subhead 80, headline 30, body 150 | 4 |
| DUAL_IMAGE_TEXT | 650 x 350 each | no | subhead 50, headline 50, body 300 | 2 |
| IMAGE_TEXT | 800 x 600 | no | subhead 40, headline 80, body 500 | 1 |
| HERO_VIDEO | MP4 ≥ 960 x 540, ≤ 200 MB, ≤ 180 s, plus 1464 x 600 poster | no | headline 80, body 300 | 1 |
| VIDEO_TEXT | MP4 and poster ≥ 800 x 600, ≤ 200 MB, ≤ 180 s | no | subhead 40, headline 80, body 500, video title 50, video description 200 | 1 |
| COMPARISON_CAROUSEL | 200 x 225 per product | no | headline 80, image headline 25, feature 30, tooltip 150, detail 30 | 4–7 products, 5–12 features |
| COMPARISON_SCROLLER | 300 x 225 per product | no | headline 80, image headline 30, feature 30, body 80 | 2–3 products, 2–5 features |
| THREE_COLUMN_COMPARISON | 488 x 700 per panel | 600 x 450 per panel | chart headline 25, image headline 25, feature 20, text 20 | 2–4 products, 3–7 features |
| HOTSPOT_IMAGE | 1464 x 600 | 600 x 450 per hotspot | hotspot headline 50, body 200 | 2–6 hotspots |
| HOTSPOT_IMAGE_TEXT | 1464 x 600 | 600 x 450 per hotspot | headline 80, body 300, hotspot headline 50 | 2–6 hotspots |
| NAVIGATION_CAROUSEL | 1464 x 600 per panel | 600 x 450 per panel | nav text 25, subhead 25, headline 25, body 100 | 2–5 panels |
| REGIMEN_CAROUSEL | 1464 x 600 per panel | 600 x 450 per panel | headline 100, inset headline 20, inset body 100, nav 20 | 2–5 panels |
| IMAGE_CAROUSEL | 1464 x 600 per panel | 600 x 450 per panel | headline 50, body 200 | 2–6 panels |
| VIDEO_IMAGE_CAROUSEL | 800 x 600 images, MP4 ≥ 800 x 600 | no | headline 80, panel headline 50, subhead 80, body 500, video title 50, description 200 | 2–6 panels |
| FAQ | 1464 x 600 (if used) | no | question 120, answer 250 | 2–5 Q&As |
| TECH_SPECS | none | none | headline 80, label 30, value 500 | 4–16 rows |

Source: Amazon Premium A+ Module Guide v1.0 (May 2023), via Parker-Lambert. The API names are matched to the guide names. Confirm sizes in A+ Content Manager before final export. The validator is the final check.

Design rules:
- Mobile crops cut the sides. Keep the product and any baked-in text in the centre 60%.
- Baked-in text must be readable at 375 px wide (on 1464 px banners, headline text at least 60 px tall).
- Keep one consistent angle, lighting, and colour palette across all modules.
- Use real product photos. AI can make backgrounds and scenes only, and must not change the product's shape, colour, parts, or included items.

## Verified JSON shapes

These field names were confirmed against Amazon's validator. Text is `{"value": "..."}`. A paragraph is `{"textList": [{"value": "..."}]}`.

Image object (all image fields):
```json
{ "uploadDestinationId": "<from aplus_upload_image>", "altText": "Black cordless handheld vacuum on white", "imageCropSpecification": { "...": "use the crop returned by aplus_upload_image" } }
```

PREMIUM_TEXT (validated and saved in production):
```json
{ "contentModuleType": "PREMIUM_TEXT",
  "premiumText": {
    "headline": { "value": "One Vacuum. Two Jobs." },
    "description": { "textList": [ { "value": "Paragraph one." }, { "value": "Paragraph two." } ] } } }
```

Content object keys and inner fields:

| Module | Content key | Fields | List item wrapper → item fields |
|---|---|---|---|
| PREMIUM_TEXT | premiumText | headline, description | – |
| PREMIUM_IMAGE_TEXT | premiumImageText | positionType, headline, subheadline, bodyText, image | – |
| PREMIUM_FULL_BACKGROUND_IMAGE | premiumFullBackgroundImage | headline, footer, desktopImage, mobileImage | – |
| PREMIUM_FULL_BACKGROUND_TEXT | premiumFullBackgroundText | headline, subheadline, description, positionType, colorType, desktopImage, mobileImage | – |
| PREMIUM_DUAL_IMAGE_TEXT | premiumDualImageText | headline, columns | `{"imageColumn": {...}}` → position, image, headline, description |
| PREMIUM_FOUR_COLUMN_IMAGES | premiumFourColumnImages | headline, columns | `{"imageColumn": {...}}` → position, image, headline, description |
| PREMIUM_IMAGE_CAROUSEL | premiumImageCarousel | headline, footer, carouselCards | `{"imagePanel": {...}}` → title, description, desktopImage, mobileImage, position, asin, buttonText |
| PREMIUM_NAVIGATION_CAROUSEL | premiumNavigationCarousel | carouselCards | likely the same panel shape. Validate first |
| PREMIUM_REGIMEN_CAROUSEL | premiumRegimenCarousel | headline, carouselCards | likely the same panel shape. Validate first |
| PREMIUM_VIDEO_IMAGE_CAROUSEL | premiumVideoImageCarousel | headline, carouselCards | validate first |
| PREMIUM_HOTSPOT_IMAGE | premiumHotspotImage | desktopImage, hotSpots | `{"imageHotSpot": {...}}` → title, description, xCoordinate, yCoordinate, mobileImage |
| PREMIUM_HOTSPOT_IMAGE_TEXT | premiumHotspotImageText | headline, mainDescription, desktopImage, hotSpots | same as above |
| PREMIUM_FAQ | premiumFaq | colorType, faqs | `{"faq": {...}}` → question, answer |
| PREMIUM_TECH_SPECS | premiumTechSpecs | headline, techSpecs (4–16) | `{"techSpec": {...}}` → specKey, specValue |
| PREMIUM_COMPARISON_SCROLLER | premiumComparisonScroller | headline, comparisonProducts, comparisonRows, showATC, showPrices, showReviews | validate first |
| PREMIUM_COMPARISON_CAROUSEL | premiumComparisonCarousel | headline, comparisonProducts, comparisonMetrics | validate first |
| PREMIUM_THREE_COLUMN_COMPARISON | premiumThreeColumnComparison | headline, comparisonProducts, comparisonRows | validate first |
| PREMIUM_HERO_VIDEO | premiumHeroVideo | headline, footer, heroVideo | video asset via `aplus_upload_video` |
| PREMIUM_VIDEO_TEXT | premiumVideoText | title, positionType, headline, description, video | video asset via `aplus_upload_video` |

Discover unknown shapes safely: put `{"probe": true}` at the unknown level and run `aplus_validate`. Amazon's 400 error lists the expected property names. Validation never saves anything.

## Troubleshooting (errors seen on this account)

| Error | Cause | Fix |
|---|---|---|
| `keywords violate our community guidelines: warranty` | Banned word | Remove it. Write "6-month replacement cover for manufacturing defects" |
| `unexpected property name: 'premiumHeaderImageText'` / `'premiumImageTextOverlay'` | Those modules are Standard only | Use PREMIUM_FULL_BACKGROUND_TEXT / PREMIUM_FULL_BACKGROUND_IMAGE |
| `unexpected property name: 'body', expected [description, headline]` | PREMIUM_TEXT uses `description` | Rename body → description |
| `unexpected property name: 'value', expected [textList]` | description is a paragraph list | Wrap it: `{"textList":[{"value":...}]}` |
| `techSpecs: size must be between 4 and 16` | Too few rows | Add rows up to 4–16 |
| `expected [techSpec]` then `expected [specKey, specValue]` | Each row needs a wrapper | `{"techSpec":{"specKey":{...},"specValue":{...}}}` |
| `500 InternalFailure` on validate with PREMIUM_TECH_SPECS | Amazon side, repeatable | Retry once. If it repeats, put specs in PREMIUM_TEXT |
| `image needs an uploadDestinationId` / `needs altText` | Image not uploaded, or no alt text | Upload with `aplus_upload_image`. Add `altText` |
| `module's content must be under "premiumX"` | Content key doesn't match the type | Key is the type in camelCase: PREMIUM_FOUR_COLUMN_IMAGES → premiumFourColumnImages |

## Image prompt template

Give the seller one prompt per image file:

```
[Module #, slot, desktop|mobile, W x H px]
Subject: <exact product, colour, parts visible. Reference the real product photo>
Scene: <background / setting / props>
Composition: <product position; empty space for text on left|right; keep centre 60% for mobile>
Light and style: <studio soft light | natural daylight>, photorealistic, ecommerce
Text on image: <none | exact words, large and high contrast>
Do not: change product shape or colour, add parts not in the box, add logos of other brands
```

## Pre-submit checklist

- [ ] 7 modules or fewer, all `PREMIUM_*`
- [ ] Every claim matches the listing facts. No banned words
- [ ] Every image is uploaded, at or above its minimum size, has alt text, and has a mobile version where required
- [ ] Mobile preview checked in A+ Content Manager
- [ ] `aplus_validate` returns VALID with the ASIN
- [ ] Seller approved the create/update, the attach, and the submit
