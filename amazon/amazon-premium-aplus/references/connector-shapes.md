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
| `keywords violate our community guidelines: warranty` | Historical validator rejection on this account | Remove the rejected claim. Do not evade the rejection with replacement-cover wording or invent coverage. Use verified facts and current content policy. |
| `unexpected property name: 'premiumHeaderImageText'` / `'premiumImageTextOverlay'` | Those modules are Standard only | Use PREMIUM_FULL_BACKGROUND_TEXT / PREMIUM_FULL_BACKGROUND_IMAGE |
| `unexpected property name: 'body', expected [description, headline]` | PREMIUM_TEXT uses `description` | Rename body → description |
| `unexpected property name: 'value', expected [textList]` | description is a paragraph list | Wrap it: `{"textList":[{"value":...}]}` |
| `techSpecs: size must be between 4 and 16` | Too few rows | Add rows up to 4–16 |
| `expected [techSpec]` then `expected [specKey, specValue]` | Each row needs a wrapper | `{"techSpec":{"specKey":{...},"specValue":{...}}}` |
| `500 InternalFailure` on validate with PREMIUM_TECH_SPECS | Amazon side, repeatable | Retry once. If it repeats, put specs in PREMIUM_TEXT |
| `image needs an uploadDestinationId` / `needs altText` | Image not uploaded, or no alt text | Upload with `aplus_upload_image`. Add `altText` |
| `module's content must be under "premiumX"` | Content key doesn't match the type | Key is the type in camelCase: PREMIUM_FOUR_COLUMN_IMAGES → premiumFourColumnImages |
