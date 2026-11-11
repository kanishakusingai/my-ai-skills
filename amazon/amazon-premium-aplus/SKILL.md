---
name: amazon-premium-aplus
description: Plan, draft, create, validate, repair, or submit Amazon.in Premium A+ Content for the seller's ASINs. Use for module choice, image prompts and sizes, character limits, connector JSON, and account-specific validator errors.
---

# Amazon.in Premium A+ Content

Use this skill for the seller's brand-registered ASINs. For OMSHRIM products, read the sibling [seller context](../omshrim-seller-context/SKILL.md) and [A+ image preferences](../amazon-a-plus-content-image-preference/SKILL.md) when available. Inspect the current listing and gallery images before writing claims or planning visuals. Build product-specific compositions that answer buying questions. The seller likes useful image carousels when they help explain the product.

This skill contains a historical connector workflow and a module guide based on a May 2023 source. Inspect the current connected tool schemas and validate the chosen modules before use. Current schemas, validator responses, and supported combined save, attach, and submit actions take precedence where they differ.

## Match the requested stage

- **Plan or draft.** Fetch listing facts with listings_get and includeAttributes true. Use the listing title, product type, category, and gallery images to identify what shoppers need to understand about this ASIN. Choose the module type, count, and order around those questions. Use fewer than seven when the story is complete. Supply complete copy and a shot list with prompts and exact sizes from [the module guide](references/module-guide.md) and [the image prompt template](references/image-prompts.md). A draft-only request ends with the draft. If the request already authorises image generation, continue with generation.
- **Build or repair.** Inspect the current A+ document, available assets, and tool schemas. Reuse verified copy and uploaded images where appropriate. Make the requested change, validate the affected document, and resolve the reported errors. Read [connector shapes and troubleshooting](references/connector-shapes.md) for the historical field names and account-specific fixes.
- **Submit or check status.** Review the document and ASIN attachment, run the connector validation, follow the tool's approval flow for each account change, then verify the recorded submission status. Use aplus_get for document status and aplus_for_asin for the live association when available.

A text-only draft can be saved early when saving is authorised, then updated with image modules. Account writes such as aplus_create, aplus_update, aplus_attach_asins, and aplus_submit have historically returned previews requiring confirm_change. Present the actual tool preview and obtain the seller's explicit approval before confirming a change that requires it. Follow the current tool's approval mechanism for combined actions. The preference or draft instructions alone do not authorise an account write.

## Content boundaries

- Use no more than seven modules per document. Do not mix STANDARD_* and PREMIUM_* modules. Use contentType "EBC" and locale "en-IN".
- Match every factual statement to the current listing or a seller-confirmed fact. Note unresolved details. Do not transfer claims from another ASIN or an older draft.
- Exclude "warranty", "guarantee", prices, discounts, shipping claims, phone numbers, email addresses, URLs, emojis, HTML, competitor names, "best seller" or "#1" claims, and customer review quotes. Review current content policy and validator feedback before submission.
- Use a module only when its role is clear. A hero answers what it is. A hotspot or video explains operation. A carousel can show use cases or steps. A comparison helps choose between verified own ASINs. A FAQ addresses purchase questions. The [module guide](references/module-guide.md) contains the original seven-module example and the size, copy, and count tables for all 19 module types.
- Give every image accurate alt text and check each desktop/mobile placement. Use the product's real photographs to preserve its shape, colour, parts, and included items. AI can supply backgrounds and scenes without altering the product. Review the seller's A+ image preferences for composition and mobile clarity.

## Build and validate

The historical sequence below remains useful when the current connector exposes separate actions. Adapt it to the actual tools shown in the session.

1. Fetch facts with listings_get and includeAttributes true. Record claims that need confirmation.
2. Select up to seven modules and write within the character limits in [the module guide](references/module-guide.md). Prepare a separate file and prompt for desktop or mobile wherever its table requires one.
3. Upload assets with aplus_upload_image using a full Windows path. Retain each uploadDestinationId and the returned crop unless the seller asks for a different crop. Upload videos with aplus_upload_video where a video module is used.
4. Run aplus_validate with the intended ASIN in the asins array. Correct the reported module and revalidate. Use [connector shapes and troubleshooting](references/connector-shapes.md) for the known JSON wrappers and account errors.
5. Save a new document with aplus_create or revise an existing one with aplus_update, using the required approval flow. Attach the intended ASIN with aplus_attach_asins and submit with aplus_submit when authorised and supported. Verify the outcome rather than assuming a successful write from a preview.

## Before handoff

- [ ] Seven or fewer modules, all of the PREMIUM_* family.
- [ ] Every claim matches current facts and the copy excludes prohibited content.
- [ ] Each image meets the selected module's minimum size, has alt text, and has a mobile version where required.
- [ ] Mobile previews have readable text and safe crops in the A+ placement.
- [ ] aplus_validate reports VALID for the intended ASIN.
- [ ] Each required account-change approval was obtained and the final status was checked.
- [ ] The handoff distinguishes a draft, uploaded assets, saved content, submitted content, and live content.
