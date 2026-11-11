---
name: omshrim-product-listing
description: Inspect, draft, update or submit OMSHRIM Amazon.in product listings using verified product details, images and current listing requirements. Use for new products, offers on existing ASINs, corrections and listing drafts. PPC and A+ authoring have separate workflows.
---

# OMSHRIM product listings on Amazon.in

Use the sibling OMSHRIM seller context and product registry when available to find the likely product. Verify the current SKU, ASIN and requested action before preparing a change. The current Amazon connector and Seller Central form determine which fields and actions are available.

## Choose the listing task

| Seller's request | How to proceed |
| --- | --- |
| Inspect or correct an owned listing | Find the seller SKU with `listings_search`. Read `listings_get` with `includeAttributes: true`, then compare the offer with the catalog and gallery. For a correction, show the current and proposed values of the affected fields. |
| Add an offer on an existing ASIN | Inspect the candidate with `catalog_get`. Match the exact product, including brand, model, variant and pack contents, and check eligibility with `listing_restrictions_check`. Similar competitor photos alone cannot establish a match. Use the existing-ASIN offer route in `listing_create` once the identity is established and the seller requests creation. |
| List a new product | Use the verified product details to choose the category and product type. Look up the type with `product_type_search` and read `product_type_get` for required fields, accepted formats and allowed values. Prepare the new SKU and attributes for that product type. |
| Draft, save or submit | Draft the requested fields first. For a request to save a Seller Central draft, check whether the connected workflow can save that specific draft. If it cannot, deliver the prepared fields as a local draft and explain where they still need to be entered. Submit when the current request authorises submission. |

## Verify what is being sold

Read supplied details, seller confirmations and available account information. Inspect supplied photos and the current gallery. Compare the listing title, bullets, description, attributes and package contents with what the images actually show. Identify which claims are verified and which appear only in artwork. If sources conflict, draft the supported fields and ask one focused question about any consequential fact still required.

- **Product and package.** Check the silhouette, controls, ports, power source, manual or electric operation, functions, capacity, dimensions and included quantities. For example, a photo showing one mop and two heads establishes a reason to check the package contents before describing a two-pack. Compare measurements printed on the image with the attributes. Record the item weight and packed shipping weight in their respective fields.
- **Brand, origin and manufacturer.** Verify these for this product. Earlier confirmation of China as the country of origin or OMSHRIM as manufacturer applies only to the SKU it covered. A brand name added digitally to a photo cannot establish physical branding. Preserve the seller's actual product identity and use its own label.
- **Identifiers and tax details.** Verify any GTIN exemption for the current brand and product type in the listing flow. A previous SKU's exemption and the seller's GST registration or exemption are separate facts. Treat a suggested classification as provisional until supported. Use verified HSN, manufacturer or importer addresses, package weight, warranty, battery capacity and certification wherever required. Mark missing values explicitly.

## Prepare the requested fields and images

Use the current requirements for the chosen product type. A screenshot or cached schema can help locate a field, but check which fields are required for this listing. Include only the parts of the listing the seller asked for.

- **Product page.** Draft the title, bullets, description and backend search terms from verified facts. Include category, product type and the relevant attributes. For an update, check whether the tool replaces a whole field. If editing one bullet replaces the entire bullet list, carry the other current bullets into the proposed value.
- **Offer.** Identify the seller SKU and target ASIN where known. Show the proposed offer, price and stock separately so the seller can review exactly what will be sold.
- **Gallery.** Show the main image first, followed by the proposed supporting images. Apply the current listing main-image requirements. A+ design preferences belong to A+ placements. Inspect the gallery tool's accepted slots, URL hosts and upload mechanisms. For `listing_images_set`, supply the complete intended slot order. A repository upload establishes where a file is hosted. Check Amazon's result to establish gallery acceptance.
- **Files.** Keep local drafts and assets in an accessible current workspace. Before returning an old download link, check that its file exists. Retrieve moved or remote-only files as needed. To report a Drive backup or upload, verify the remote file in Drive.

## Apply and verify a change

Complete authorised preparation before requesting any approval required by the connector. Present the concrete change, including its SKU or ASIN, fields and proposed values. Reuse seller authorisation within the scope it covers and follow the current tool approval flow.

After writing, read back the affected SKU, price, stock, attributes or gallery. Report the actual state. A local draft, a saved Seller Central draft, a submitted change, an accepted change awaiting propagation and a published listing are different outcomes. If Amazon accepts an image update but the old main image still appears, report both observations. After a rejected irreversible write, establish the cause and a safe next action before another attempt.

If the seller cancels a draft, identify that exact draft and remove it through the supported draft mechanism, then verify the result. Keep unrelated images and live listings intact. The live SKU deletion tool removes a listing and does not serve as a draft-cancellation action. Resume a cancelled listing only on a fresh seller request.
