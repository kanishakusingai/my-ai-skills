---
name: amazon-seller-mcp
description: Use the Amazon seller MCP connector for Amazon.in FBM operations. Choose a tool, supply its arguments, interpret results, and follow reports, feeds and approved changes through verification. Includes per-tool examples for listings, orders, pricing, finance, analytics and A+ content.
---

# Amazon seller MCP

Use the connected Amazon plugin for the seller’s Amazon.in account. For a specialised task such as an A+ creative brief or a payment workbook, use the relevant seller skill for the deliverable and this guide for connector operations. The catalog covers the 105 tools exposed in the authoring session. Discover the current tool before calling it. A changed live declaration takes precedence over the saved example.

## Find and call a tool

1. Choose the guide matching the seller’s question. Each tool has its purpose, example JSON arguments and complete input declaration, including optional fields, nested arrays and allowed values. Replace every placeholder and illustrative amount with the seller’s actual information.
2. Resolve identifiers from the appropriate source. An ASIN identifies a catalog product. A seller SKU identifies an offer. If given only an ASIN for an offer change, look it up with `listings_search` and resolve ambiguity if several SKUs match. Use the actual order ID, order item ID, report ID, feed ID, A+ document key or media ID for its corresponding field.
3. In a host exposing the tools from this session, prefix the short name with `mcp__codex_apps__amazon_`. For example, `text(await tools.mcp__codex_apps__amazon_server_info({}))` shows the server version, marketplace and approval mode. In other clients, use the name the connected client exposes. The example JSON in each guide is the argument object for **one** call.
4. Check the tool result for errors, skipped rows, exclusions, partial coverage and pending work. Prefer structured output when available and inspect text blocks for additional warnings. Show dates in India time and amounts in INR. Use the exact period and scope returned. Preserve IDs needed for the next step.

| For this task | Guide | Tools |
| --- | --- | ---: |
| Account and connection | [account](references/account.md) | 8 |
| Catalog and listing inspection | [catalog](references/catalog.md) | 17 |
| Listing changes | [listing-changes](references/listing-changes.md) | 15 |
| Pricing and inventory | [pricing-inventory](references/pricing-inventory.md) | 9 |
| Orders, shipments and buyer contact | [orders](references/orders.md) | 11 |
| Payments and profit | [money](references/money.md) | 6 |
| Sales and Brand Analytics | [analytics](references/analytics.md) | 9 |
| Reports and bulk feeds | [reports-feeds](references/reports-feeds.md) | 5 |
| A+ content and media | [aplus](references/aplus.md) | 25 |

## Follow a task through to its result

**Listing corrections.** For a title change, fetch `listings_get` with attributes, confirm the product and current title, then use `listing_content_lint` on the draft. Submit the requested field with `listing_set_fields` and inspect the preview. After approval, re-read the SKU. For many SKUs, preview the affected rows and track the returned feed with `feeds_status`. Separate excluded rows, submitted rows, and rows Amazon subsequently rejected.

**Price and stock decisions.** Use `pricing_competitive` for the competing offer and `fees_estimate` or `buybox_target_price` for the economics. Identify missing seller costs. Use `reprice_plan` with `apply: false` to inspect the proposed prices. Use `inventory_low_stock` or `restock_plan` for inventory decisions. An estimate, plan, or saved local assumption is distinct from a live selling price or quantity.

**Orders and buyer contact.** Check the fulfilment channel, shipped state and item quantities in `orders_get` before a shipment or cancellation. For a buyer message, use `buyer_message_options` to obtain the permitted message type, length and language. Use only order-related text in the buyer’s language. Exclude links, emails, phone numbers, marketing and review requests. For a requested review invitation, check eligibility and use the standard `review_request_send` action at most once per order. Obtain approval for the exact send.

**Payout questions.** For “Where is my payment?”, identify whether the seller means a particular order, available balance or bank transfer. Use `finances_order`, `finances_balance` or `finances_payouts` accordingly. Compare settlement periods and transfer dates when reconciling against bank records. Preserve deferred balances, refunds and unattributed charges in any totals.

**A+ content.** Find the document with `aplus_search` or `aplus_for_asin`. Read its full content for an edit. Check assets, then validate the document for the target ASINs. For a draft request, save only when requested. For an authorised combined action, `aplus_publish` can save, attach and submit in one approval. For uploaded video, wait for the media status to become AVAILABLE. Verify submission using `aplus_get` and live placement using `aplus_for_asin`. Product-gallery video upload is a different Seller Central workflow.

**Reports and feeds.** Reuse the report ID when Amazon is still building data. Resume a dedicated analytics tool with the ID and its required filters, or check a general report with `reports_status`. Download after DONE. Investigate CANCELLED or FATAL before requesting another report. For a bulk change, keep the feed ID and inspect per-SKU results with `feeds_status`. On an uncertain write outcome, look up the feed, audit log or current resource before retrying.

## Seller approval

Read `server_info` when the approval mode matters. At authoring time, server version 0.1.0 reported `directPrompts: false`. A client supporting direct prompts can show its own approval controls. For a pending preview, display the exact change, affected items and any exclusions, then wait for the seller’s explicit decision. Use `confirm_change` with the returned confirmation ID and that decision only. The answer option records the seller’s words and cancels the pending change. A revised request needs a fresh preview. A successful preview, feed submission or A+ submission represents an intermediate state.

Some tools write a file, advance a local checkpoint, upload an asset, or save costs on the server PC. The individual guides describe these effects even when the live listing stays untouched. Use full paths accessible to the server for uploads and imports.

## Use the helper script

Run [amazon_tools.py](scripts/amazon_tools.py) with Python 3.9+ from the skill directory. It reads the same guides used by the skill. Searching, showing a tool and preparing a workflow run locally with the Python standard library.

```text
python scripts/amazon_tools.py search buy box
python scripts/amazon_tools.py show listing_set_fields
python scripts/amazon_tools.py workflow connection
python scripts/amazon_tools.py workflow sku-review --sku YOUR-SKU --emit-js
python scripts/amazon_tools.py workflow order-money --order-id YOUR-ORDER-ID --emit-js
python scripts/amazon_tools.py workflow feed-review --feed-id YOUR-FEED-ID --emit-js
python scripts/amazon_tools.py workflow report-watch --report-id YOUR-REPORT-ID --checks 3 --emit-js
```

Without `--emit-js`, the workflow command prints the planned calls and arguments for inspection. With it, the script emits a runnable JavaScript body for the connected Codex `functions.exec` host. Inspect the emitted calls, then execute that body in the host for an in-scope request. The host supplies the authenticated `tools` object and `text`; standalone Python only prepares the code. In a client with a different interface, use the JSON plan to invoke the same tools individually.

The SKU and order workflows run independent reads together and retain results and errors per tool. The report watcher uses the existing report ID and polls at ten-second intervals while pending, up to the selected check count. It stops on completion, terminal failure, tool error or an unrecognised status and preserves the response. Resume with the same ID if further monitoring is needed. Mutations and seller decisions use the individual connected tools and their normal approval flow.
