# A+ content and media

A+ documents, uploaded images and media-library items use different identifiers. Carry each ID from the producing tool. Asset upload, draft save, submission and live placement are separate stages.

Each example is a JSON argument object. Replace placeholders and illustrative values with verified inputs. In the signature, `?` marks optional fields. Check the connected tool for its current contract.

## aplus_approval_tracker

Every A+ document that needs attention: in review (with days waiting), rejected (re-checked with Amazon's validation to show what's wrong now), drafts never submitted, and approved documents with ASINs that can't show them (e.g. brand not eligible). Each has the next step. Amazon's written rejection reason is only in Seller Central. Read only.

Example arguments

```json
{
  "olderThanDays": 7
}
```

Accepted arguments

```ts
{
  // Also check approved documents for blocked ASINs.
  includeApproved?: boolean;
  // Only documents last updated at least this many days ago.
  olderThanDays?: number;
}
```

## aplus_assets

Lists every image and video in one A+ document (or all, up to 100): upload/media ID, crop size and offset, alt text and module. Flags missing or too-long alt text, missing or zero crops, missing video thumbnails, and images reused in several places. Read only.

Example arguments

```json
{
  "contentReferenceKey": "<contentReferenceKey>"
}
```

Accepted arguments

```ts
{
  all?: boolean;
  contentReferenceKey?: string;
  // Also save the rows as a CSV file in the downloads folder (opens in Excel).
  exportCsv?: boolean;
}
```

## aplus_attach_asins

Attaches ASINs to an A+ document (adds to the existing ones by default). ASINs outside your brand or not in the catalog are left out with the reason. Warns when this would replace live A+ content. The seller must approve.

Use replace only when the seller intends the complete new association list.

Example arguments

```json
{
  "contentReferenceKey": "<contentReferenceKey>",
  "asins": [
    "<product ASIN>"
  ],
  "mode": "add"
}
```

Accepted arguments

```ts
{
  asins: Array<string>;
  contentReferenceKey: string;
  // add: keep current ASINs. replace: only these ASINs.
  mode?: "add" | "replace";
}
```

## aplus_build_from_outline

Builds a ready A+ document from a simple outline, so no module JSON is written by hand: modules text, header_image_text (970×600), single_side_image (300×300), image_text_overlay (970×300), three_image_text (3 × 300×300), four_image_text (4 × 220×220), company_logo (600×180), or raw (a module already in Amazon's format, e.g. Premium). Each image is a local file path with alt text; images are uploaded (each path once), cropped from the centre to the module's shape, and checked for minimum size. The document is checked locally and by Amazon (optionally against ASINs). Uploading changes nothing live; publish with aplus_publish.

Example arguments

```json
{
  "name": "Product care",
  "asins": [
    "<product ASIN>"
  ],
  "modules": [
    {
      "type": "text",
      "headline": "Care instructions",
      "body": [
        "<verified care instruction>"
      ]
    }
  ]
}
```

Accepted arguments

```ts
{
  // Validate against these ASINs.
  asins?: Array<string>;
  modules: Array<{
  // Paragraphs.
  body: Array<string>;
  headline?: string;
  type: "text";
} | {
  // Paragraphs.
  body?: Array<string>;
  headline?: string;
  image: {
  // What the image shows (no keyword stuffing).
  altText: string;
  // Full path to a local PNG/JPEG, e.g. C:\Users\me\Pictures\hero.jpg
  path: string;
};
  imageHeadline?: string;
  type: "header_image_text";
} | {
  // Paragraphs.
  body?: Array<string>;
  headline?: string;
  image: {
  // What the image shows (no keyword stuffing).
  altText: string;
  // Full path to a local PNG/JPEG, e.g. C:\Users\me\Pictures\hero.jpg
  path: string;
};
  position?: "LEFT" | "RIGHT";
  type: "single_side_image";
} | {
  // Paragraphs.
  body?: Array<string>;
  headline?: string;
  image: {
  // What the image shows (no keyword stuffing).
  altText: string;
  // Full path to a local PNG/JPEG, e.g. C:\Users\me\Pictures\hero.jpg
  path: string;
};
  overlay?: "DARK" | "LIGHT";
  type: "image_text_overlay";
} | { blocks: Array<{
  // Paragraphs.
  body?: Array<string>;
  headline?: string;
  image: {
  // What the image shows (no keyword stuffing).
  altText: string;
  // Full path to a local PNG/JPEG, e.g. C:\Users\me\Pictures\hero.jpg
  path: string;
};
}>; headline?: string; type: "three_image_text"; } | { blocks: Array<{
  // Paragraphs.
  body?: Array<string>;
  headline?: string;
  image: {
  // What the image shows (no keyword stuffing).
  altText: string;
  // Full path to a local PNG/JPEG, e.g. C:\Users\me\Pictures\hero.jpg
  path: string;
};
}>; headline?: string; type: "four_image_text"; } | { image: {
  // What the image shows (no keyword stuffing).
  altText: string;
  // Full path to a local PNG/JPEG, e.g. C:\Users\me\Pictures\hero.jpg
  path: string;
}; type: "company_logo"; } | {
  // A module already in Amazon's format (e.g. a Premium module).
  module: { contentModuleType: string; [key: string]: unknown; };
  type: "raw";
}>;
  // Internal name, e.g. 'Diwali hamper A+ 2026'.
  name: string;
}
```

## aplus_coverage

For every ASIN in your listings: is A+ content (and Brand Story) live, in review, rejected, only a draft, or missing, and which document is live. Groups the gaps so you know what to build or fix. Checks several ASINs at a time; document data is cached for 10 minutes (refresh=true to reload). Read only.

Example arguments

```json
{
  "onlyMissing": true
}
```

Accepted arguments

```ts
{
  includeBrandStory?: boolean;
  // Only list ASINs where something isn't live.
  onlyMissing?: boolean;
  refresh?: boolean;
}
```

## aplus_create

Saves a new A+ document as a draft (nothing goes live). The document is checked first and the seller must approve. Then attach ASINs with aplus_attach_asins and submit with aplus_submit.

Save the returned content reference key for later editing or attachment.

Example arguments

```json
{
  "document": {
    "name": "Product care",
    "contentType": "EBC",
    "locale": "en-IN",
    "contentModuleList": [
      {
        "contentModuleType": "PREMIUM_TEXT",
        "premiumText": {
          "headline": {
            "value": "Care instructions"
          },
          "description": {
            "textList": [
              {
                "value": "<verified care instruction>"
              }
            ]
          }
        }
      }
    ]
  }
}
```

Accepted arguments

```ts
{
  // An A+ content document (A+ Content API 2020-11-01 format).
  document: {
  // Modules in Amazon's format, e.g. {"contentModuleType":"STANDARD_TEXT","standardText":{"headline":{"value":"..."},"body":{"textList":[{"value":"..."}]}}}.
  contentModuleList: Array<{ contentModuleType: string; [key: string]: unknown; }>;
  contentSubType?: string | null;
  // "EBC" for A+ content (Standard or Premium, incl. video modules), "BrandStory" for a Brand Story (BRAND_STORY_* modules only).
  contentType?: string;
  locale?: string;
  // Internal name, e.g. 'Car vacuum A+ (Diwali 2026)'.
  name: string;
};
}
```

## aplus_diff

Compares two A+ documents module by module (by position): modules added, removed or of another type, and every text, image ID, crop or alt text that changed. Each side is a contentReferenceKey or the full path to a .json file (e.g. an aplus_export backup), so you can see what changed since a backup. Read only.

Example arguments

```json
{
  "a": "<contentReferenceKey>",
  "b": "<second contentReferenceKey>"
}
```

Accepted arguments

```ts
{
  // Before: contentReferenceKey or full path to a .json file.
  a: string;
  // After: contentReferenceKey or full path to a .json file.
  b: string;
}
```

## aplus_export

Saves one A+ document (or all, up to 100) as JSON files on this PC in downloads\aplus-backups\<time>: the full document, status, badges and ASINs. Use it before edits; aplus_diff compares a backup with the live document and aplus_import_document turns one back into a draft. Image files aren't included (Amazon doesn't send them back), only their upload IDs. Read only.

Example arguments

```json
{
  "contentReferenceKey": "<contentReferenceKey>"
}
```

Accepted arguments

```ts
{ all?: boolean; contentReferenceKey?: string; }
```

## aplus_for_asin

Shows which A+ document is live on each ASIN. Give ASINs, or set fromMyListings=true to check your listings (up to 100) and find the ones without A+ content.

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
{ asins?: Array<string>; fromMyListings?: boolean; }
```

## aplus_get

One A+ document: status, tier, modules (type, headline, text length, images), attached ASINs with badges. Set includeDocument=true for the full document (to edit it).

Example arguments

```json
{
  "contentReferenceKey": "<contentReferenceKey>",
  "includeDocument": true
}
```

Accepted arguments

```ts
{ contentReferenceKey: string; includeDocument?: boolean; }
```

## aplus_import_document

Creates a new A+ DRAFT from a .json file (an aplus_export backup, or a document edited by hand). Checked locally and by Amazon first; the seller must approve. It is NOT attached to ASINs or submitted: finish with aplus_attach_asins and aplus_submit. Images are reused by their upload IDs.

Example arguments

```json
{
  "filePath": "C:\\exports\\document.json"
}
```

Accepted arguments

```ts
{
  // Validate against these ASINs (they are not attached).
  asins?: Array<string>;
  // Full path to the .json file.
  filePath: string;
  // New internal name (default: the file's).
  name?: string;
}
```

## aplus_media_status

Shows the processing/review status of an A+ media item (video or image) in plain words, with any issues, plus its video pairings. Use after aplus_upload_video; a video is usable in A+ once it is AVAILABLE.

Example arguments

```json
{
  "mediaId": "<mediaId>"
}
```

Accepted arguments

```ts
{
  // Only this pairing (e.g. the thumbnail's imageMediaId).
  associatedMediaId?: string;
  mediaId: string;
}
```

## aplus_publish

Saves an A+ document, attaches ASINs and submits it for Amazon's approval with ONE seller approval. Give document (e.g. from aplus_build_from_outline) to create a new one, or contentReferenceKey + document to replace an existing one, or fromContentReferenceKey to copy an existing document onto new ASINs. Warns when it would replace live A+ content and leaves out ASINs that can't take your A+. submit=false stops after attaching (stays a draft).

The example copies an existing document and stops after attachment. Check status with aplus_get and live coverage with aplus_for_asin.

Example arguments

```json
{
  "asins": [
    "<product ASIN>"
  ],
  "fromContentReferenceKey": "<contentReferenceKey>",
  "submit": false
}
```

Accepted arguments

```ts
{
  asins: Array<string>;
  // Update this existing document instead of creating one.
  contentReferenceKey?: string;
  // An A+ document in Amazon's format, e.g. the document returned by aplus_build_from_outline.
  document?: { contentModuleList: Array<{ contentModuleType: string; [key: string]: unknown; }>; contentSubType?: string | null; contentType?: string; locale?: string; name: string; };
  // Copy this document's content into a new document.
  fromContentReferenceKey?: string;
  // Name for a copied document.
  name?: string;
  submit?: boolean;
}
```

## aplus_search

Lists your A+ content documents on Amazon.in with status (DRAFT, SUBMITTED, APPROVED, REJECTED), tier (Standard/Premium) and last update.

Use the selected content reference key with aplus_get to inspect one document.

Example arguments

```json
{
  "status": "DRAFT",
  "limit": 10
}
```

Accepted arguments

```ts
{ limit?: number; status?: "APPROVED" | "DRAFT" | "REJECTED" | "SUBMITTED"; }
```

## aplus_submit

Submits an A+ document to Amazon for approval so it can go live on its ASINs. Warns when it would replace live content. The seller must approve. Check the result later with aplus_get.

Example arguments

```json
{
  "contentReferenceKey": "<contentReferenceKey>"
}
```

Accepted arguments

```ts
{ contentReferenceKey: string; }
```

## aplus_suspend

Takes a live A+ or Brand Story document off its product pages. The document and its ASINs are kept, so you can submit it again later. The seller must approve.

Example arguments

```json
{
  "contentReferenceKey": "<contentReferenceKey>"
}
```

Accepted arguments

```ts
{ contentReferenceKey: string; }
```

## aplus_text_extract

Every headline, paragraph and image alt text of an A+ document in reading order, with module, field and character/word counts. exportCsv saves it for proofreading, translation or keyword checks. Read only.

Example arguments

```json
{
  "contentReferenceKey": "<contentReferenceKey>"
}
```

Accepted arguments

```ts
{
  contentReferenceKey: string;
  // Also save the rows as a CSV file in the downloads folder (opens in Excel).
  exportCsv?: boolean;
}
```

## aplus_update

Replaces the content of an existing A+ document. Updating an approved document sends it back to draft (the approved version stays live until the new one is approved). Checked first; the seller must approve.

Read the full existing document first. Removing modules from the replacement document can remove them from the draft.

Example arguments

```json
{
  "contentReferenceKey": "<contentReferenceKey>",
  "document": {
    "name": "Product care",
    "contentType": "EBC",
    "locale": "en-IN",
    "contentModuleList": [
      {
        "contentModuleType": "PREMIUM_TEXT",
        "premiumText": {
          "headline": {
            "value": "Care instructions"
          },
          "description": {
            "textList": [
              {
                "value": "<verified care instruction>"
              }
            ]
          }
        }
      }
    ]
  }
}
```

Accepted arguments

```ts
{
  contentReferenceKey: string;
  // An A+ content document (A+ Content API 2020-11-01 format).
  document: {
  // Modules in Amazon's format, e.g. {"contentModuleType":"STANDARD_TEXT","standardText":{"headline":{"value":"..."},"body":{"textList":[{"value":"..."}]}}}.
  contentModuleList: Array<{ contentModuleType: string; [key: string]: unknown; }>;
  contentSubType?: string | null;
  // "EBC" for A+ content (Standard or Premium, incl. video modules), "BrandStory" for a Brand Story (BRAND_STORY_* modules only).
  contentType?: string;
  locale?: string;
  // Internal name, e.g. 'Car vacuum A+ (Diwali 2026)'.
  name: string;
};
}
```

## aplus_upload_folder

Uploads every PNG/JPEG in a folder (full path) for A+ in one call and returns each file's upload ID, size, a full-image crop and which Standard modules it's big enough for. A file already uploaded in the last 24 hours (same bytes) is reused instead of sent again (force=true to send anyway); identical files in the folder are sent once. dryRun=true only checks the files. Only .png/.jpg/.jpeg files are read. Uploading changes nothing live.

Example arguments

```json
{
  "folder": "C:\\assets\\aplus",
  "dryRun": true
}
```

Accepted arguments

```ts
{
  dryRun?: boolean;
  // Full path, e.g. C:\Users\me\Pictures\aplus
  folder: string;
  force?: boolean;
  maxFiles?: number;
  // Also sub-folders (3 levels).
  recursive?: boolean;
}
```

## aplus_upload_image

Uploads a local PNG or JPEG (full Windows path) for use in A+ modules and returns its uploadDestinationId and pixel size, plus a full-image crop to start from. Uploading doesn't change anything live.

Place the uploadDestinationId and crop in the intended module. For a video poster, use aplus_upload_media_image.

Example arguments

```json
{
  "filePath": "C:\\assets\\hero.jpg"
}
```

Accepted arguments

```ts
{
  // Absolute path, e.g. C:\Users\me\Pictures\banner.jpg
  filePath: string;
}
```

## aplus_upload_media_image

Uploads a local PNG or JPEG (full Windows path, max 10 MB) to your A+ media library and returns its imageMediaId (used as a video thumbnail) with a full-image crop. Uploading doesn't change anything live.

Pass its imageMediaId to aplus_upload_video as thumbnailMediaId.

Example arguments

```json
{
  "filePath": "C:\\assets\\thumbnail.jpg"
}
```

Accepted arguments

```ts
{
  // Absolute path, e.g. C:\Users\me\Pictures\thumb.jpg
  filePath: string;
  // Title in the media library (defaults to the file name).
  title?: string;
}
```

## aplus_upload_urls

Downloads PNG/JPEG images from public https links (up to 10) and uploads them for A+, e.g. your own listing images from catalog_get. Only Amazon image hosts are allowed by default (media-amazon.com, ssl-images-amazon.com, images-amazon.com); add others with allowHosts only if you trust them. Links to private or local network addresses, more than 3 redirects, files over 10 MB and non-images are refused. Same-file uploads from the last 24 hours are reused. Uploading changes nothing live.

Example arguments

```json
{
  "urls": [
    "<verified public HTTPS Amazon image URL>"
  ]
}
```

Accepted arguments

```ts
{
  allowHosts?: Array<string>;
  force?: boolean;
  // File names for the uploads, in the same order as urls.
  names?: Array<string>;
  urls: Array<string>;
}
```

## aplus_upload_video

Uploads a local MP4 or MOV (max 500 MB) to your A+ media library with a thumbnail (a local image path or an existing imageMediaId), a title (at least 3 words, not all caps) and an English accessibility description. Returns videoMediaId, imageMediaId and imageCropSpecification for a Premium video module. Amazon then processes and reviews it; check with aplus_media_status. Uploading doesn't change anything live.

Pass the returned media ID to aplus_media_status. This is the A+ media library, separate from Seller Central’s product-video form.

Example arguments

```json
{
  "filePath": "C:\\assets\\demo.mp4",
  "thumbnailPath": "C:\\assets\\thumbnail.jpg",
  "title": "Product setup demonstration",
  "description": "<describe the actual action in English>"
}
```

Accepted arguments

```ts
{
  // Accessibility description of what the video shows (en-IN).
  description: string;
  // Absolute path to the .mp4 or .mov file.
  filePath: string;
  // Or: an imageMediaId already in your media library.
  thumbnailMediaId?: string;
  // Absolute path to a PNG/JPEG thumbnail.
  thumbnailPath?: string;
  // Video title shown with the video, e.g. 'Cordless car vacuum demo'.
  title: string;
}
```

## aplus_uploads_list

Images uploaded through this server (aplus_upload_image, aplus_upload_folder, aplus_upload_urls, aplus_build_from_outline), newest first: file, source, size, upload ID and time. Amazon has no call that lists uploads, so this is a register kept on this PC (last 500). withUsage=true also reads your A+ documents (up to 100) to show which use each upload.

Example arguments

```json
{
  "limit": 10,
  "withUsage": true
}
```

Accepted arguments

```ts
{
  limit?: number;
  // Only uploads whose file name or source contains this.
  search?: string;
  withUsage?: boolean;
}
```

## aplus_validate

Checks an A+ document without saving it: local rules (no Standard+Premium mix, max 7 Premium modules, module keys, images uploaded, en-IN locale) and then Amazon's own validation, optionally against ASINs.

Correct the reported field or module and validate against the intended ASINs again.

Example arguments

```json
{
  "asins": [
    "<product ASIN>"
  ],
  "document": {
    "name": "Product care",
    "contentType": "EBC",
    "locale": "en-IN",
    "contentModuleList": [
      {
        "contentModuleType": "PREMIUM_TEXT",
        "premiumText": {
          "headline": {
            "value": "Care instructions"
          },
          "description": {
            "textList": [
              {
                "value": "<verified care instruction>"
              }
            ]
          }
        }
      }
    ]
  }
}
```

Accepted arguments

```ts
{
  asins?: Array<string>;
  // An A+ content document (A+ Content API 2020-11-01 format).
  document: {
  // Modules in Amazon's format, e.g. {"contentModuleType":"STANDARD_TEXT","standardText":{"headline":{"value":"..."},"body":{"textList":[{"value":"..."}]}}}.
  contentModuleList: Array<{ contentModuleType: string; [key: string]: unknown; }>;
  contentSubType?: string | null;
  // "EBC" for A+ content (Standard or Premium, incl. video modules), "BrandStory" for a Brand Story (BRAND_STORY_* modules only).
  contentType?: string;
  locale?: string;
  // Internal name, e.g. 'Car vacuum A+ (Diwali 2026)'.
  name: string;
};
}
```
