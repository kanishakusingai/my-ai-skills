# Reports and bulk feeds

A report retrieves data. A listings feed processes changes. Keep the correct ID for the matching status tool.

Each example is a JSON argument object. Replace placeholders and illustrative values with verified inputs. In the signature, `?` marks optional fields. Check the connected tool for its current contract.

## feeds_recent

Lists your recent listings feeds (bulk updates) on Amazon.in with their status, newest first. Use feeds_status for per-SKU results.

Example arguments

```json
{
  "max": 10
}
```

Accepted arguments

```ts
{ max?: number; }
```

## feeds_status

Checks a listings feed (e.g. from a bulk update) by its feed ID. Once Amazon has processed it, shows per-SKU results: accepted or rejected, with Amazon's error and warning messages.

A completed feed can contain rejected SKUs. Inspect each row before describing the update as complete.

Example arguments

```json
{
  "feedId": "<feedId>"
}
```

Accepted arguments

```ts
{ feedId: string; }
```

## reports_download

Downloads a finished report to the local downloads folder (decompressed) and returns its first rows. For tab-separated reports you can filter rows where a column contains some text. Large JSON reports return only the first items of each list.

Example arguments

```json
{
  "reportId": "<reportId>",
  "maxRows": 10
}
```

Accepted arguments

```ts
{ filterColumn?: string; filterContains?: string; maxRows?: number; reportId: string; }
```

## reports_request

Asks Amazon to build any SP-API report your roles allow (e.g. GET_MERCHANT_LISTINGS_ALL_DATA, GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL, GET_BRAND_ANALYTICS_* ) and waits briefly. When it's DONE, use reports_download. Brand Analytics has dedicated tools.

Keep the reportId even when the initial wait ends. Use reports_status to resume the same request.

Example arguments

```json
{
  "reportType": "GET_MERCHANT_LISTINGS_ALL_DATA",
  "waitSeconds": 5
}
```

Accepted arguments

```ts
{
  endDate?: string;
  reportOptions?: { [key: string]: string; };
  reportType: string;
  startDate?: string;
  // Seconds to wait for Amazon to finish the report before returning its ID (call again later with reportId).
  waitSeconds?: number;
}
```

## reports_status

Checks whether a report is ready (IN_QUEUE, IN_PROGRESS, DONE, CANCELLED or FATAL).

DONE → reports_download with reportId. IN_QUEUE or IN_PROGRESS → check later. CANCELLED or FATAL → inspect the reason.

Example arguments

```json
{
  "reportId": "<reportId>"
}
```

Accepted arguments

```ts
{ reportId: string; }
```
