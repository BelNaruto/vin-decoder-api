# VIN Decoder API & VIN OCR — Decode VINs, Read VINs from Photos, Recalls, Safety Ratings, Fuel Economy

[![RapidAPI](https://img.shields.io/badge/RapidAPI-Subscribe-0055DA?logo=rapid&logoColor=white)](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/vin-recognition-decoder)
[![Telegram](https://img.shields.io/badge/Support-@pintoflow-26A5E4?logo=telegram&logoColor=white)](https://t.me/pintoflow)
![Endpoints](https://img.shields.io/badge/endpoints-17-success)
![License](https://img.shields.io/badge/license-MIT-blue)

> 🚗 **Get your API key:** **[VIN Recognition/Decoder API on RapidAPI](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/vin-recognition-decoder)**.
>
> 💬 **Support on Telegram: [@pintoflow](https://t.me/pintoflow)** — message us for the fastest response (questions, bugs, custom plans or new features).

A **VIN decoder API** and **VIN OCR API** for developers. Decode any 17-character **Vehicle Identification Number** into make, model, year, trim, engine and 100+ specs, **extract a VIN from an image** (door-jamb sticker, dashboard plate, registration document), and get **NHTSA recalls, owner complaints, 5-star crash ratings, EPA fuel economy** and **vehicle history counts** — all from one REST API with ready-to-run examples in **Node.js, Python, PHP and cURL**.

## Table of contents

- [Use cases](#use-cases)
- [Examples in this repo](#examples-in-this-repo)
- [Quick start](#quick-start)
- [Response format](#response-format)
- [Endpoints](#endpoints)
- [Error codes](#error-codes)
- [Do's and don'ts](#dos-and-donts)
- [Data coverage and accuracy](#data-coverage-and-accuracy)
- [FAQ](#faq)
- [Support](#support)

## Use cases

- **Car dealership & marketplace listings** — auto-fill make, model, year, trim and engine from a VIN.
- **Insurance & fleet apps** — scan the VIN sticker with the phone camera instead of typing 17 characters.
- **Used-car checks** — show open recalls, owner complaints, crash-test ratings and history record counts.
- **Parts & service shops** — identify the exact engine/transmission before ordering parts.
- **Data cleaning** — validate VIN check digits and batch-decode up to 50 VINs per call.

## Examples in this repo

| Language | File | What it does |
|---|---|---|
| cURL | [`examples/curl/examples.sh`](examples/curl/examples.sh) | Every endpoint in one script |
| Node.js | [`examples/nodejs/decode-vin.js`](examples/nodejs/decode-vin.js) | Validate → decode a VIN with retry on 502/503/504 |
| Node.js | [`examples/nodejs/extract-vin-from-image.js`](examples/nodejs/extract-vin-from-image.js) | Read a VIN from a photo (file upload or URL) |
| Node.js | [`examples/nodejs/express-proxy.js`](examples/nodejs/express-proxy.js) | Backend proxy so your RapidAPI key is never exposed |
| Python | [`examples/python/decode_vin.py`](examples/python/decode_vin.py) | Decode a VIN and print a summary |
| Python | [`examples/python/batch_decode_csv.py`](examples/python/batch_decode_csv.py) | Batch-decode a CSV of VINs into an enriched CSV |
| Python | [`examples/python/vehicle_report.py`](examples/python/vehicle_report.py) | Full report: recalls, complaints, ratings, MPG |
| Python | [`examples/python/extract_vin_from_image.py`](examples/python/extract_vin_from_image.py) | VIN OCR from a photo with alternatives |
| PHP | [`examples/php/decode_vin.php`](examples/php/decode_vin.php) | Decode a VIN with PHP cURL |

Set your key once and run any example:

```bash
export RAPIDAPI_KEY="your-key-from-rapidapi"
```

Turn a **Vehicle Identification Number** (typed or photographed) into vehicle data:

- **Decode** a VIN into make, model, model year, trim, body, engine, transmission, plant and 100+ specs.
- **Read a VIN from a photo** of a door-jamb sticker, dashboard plate, windscreen tag or registration document.
- **Recalls, owner complaints, NHTSA crash-test ratings and EPA fuel economy** for the vehicle.
- **Validate** VINs (length, illegal characters, check digit) without spending time on a full decode.
- **Batch decode** up to 50 VINs in one call.
- **One-call vehicle report** that combines all of the above.

---

## Quick start

All requests go through RapidAPI. Send your key in the usual headers:

```bash
curl --request GET \
  --url 'https://vin-recognition-decoder.p.rapidapi.com/decode?vin=1HGCM82633A004352&compact=true' \
  --header 'X-RapidAPI-Key: <YOUR_KEY>' \
  --header 'X-RapidAPI-Host: vin-recognition-decoder.p.rapidapi.com'
```

```json
{
  "success": true,
  "data": {
    "vin": "1HGCM82633A004352",
    "make": "Honda",
    "model": "Accord",
    "modelYear": 2003,
    "trim": "EX-V6",
    "bodyClass": "Coupe",
    "engine": { "cylinders": 6, "displacementL": 3, "horsepower": 240, "configuration": "V-Shaped" },
    "transmission": { "style": "Automatic", "speeds": 5 },
    "plant": { "city": "Marysville", "state": "Ohio", "country": "United States (USA)" },
    "decodeQuality": "complete"
  },
  "meta": { "requestId": "c1f0…", "tookMs": 412 }
}
```

---

## Response format

Every response has the same envelope, so you can handle all endpoints with the same code.

**Success** (HTTP 200)

```json
{ "success": true, "data": { … }, "meta": { "requestId": "…", "tookMs": 123, "warnings": ["…"] } }
```

`meta.warnings` is only present when there is something you should know (for example a check-digit mismatch). Always read it.

**Error** (HTTP 4xx / 5xx)

```json
{
  "success": false,
  "error": { "code": "INVALID_VIN", "message": "VIN must be exactly 17 characters, got 16.", "details": { … } },
  "meta": { "requestId": "…" }
}
```

- `error.code` is stable. Build your logic on it.
- `error.message` is human-readable and may change wording.
- `error.details` is optional extra context, such as a corrected VIN suggestion.
- Quote `meta.requestId` when you contact support.

---

## Endpoints

VIN parameters are case-insensitive. Spaces, dashes and dots are ignored, so `1hg-cm826 33a004352` works. `/decode`, `/decode-basic`, `/validate`, `/report` and `/history-check` also accept the VIN as a path segment, for example `/decode/1HGCM82633A004352`.

### `GET /decode`: full decode

| Parameter | Required | Description |
|---|---|---|
| `vin` | yes | 17-character VIN |
| `compact` | no | `true` returns only the summary, without the long `specs` object |
| `modelYear` | no | Helps when position 10 is ambiguous (rare) |
| `strict` | no | `true` rejects VINs whose check digit is wrong (422 instead of a warning) |

Returns the summary fields shown above plus:

- `specs`: every non-empty field NHTSA has, such as airbags, ADAS features, GVWR, wheelbase, battery and seat belts.
- `decodeQuality`: one of the values below.
  - `complete`: decoded cleanly.
  - `partial`: some positions could not be decoded. Read `decodeNotes`.
  - `not_found`: only the data encoded in the VIN itself is available.
- `possibleModelYears`: model-year codes repeat every 30 years, so this lists every candidate.
- `origin`: region, country and WMI.

Aliases kept for older integrations: `/get-vin`, `/get-vin2`.

### `GET /decode-basic`: instant offline decode

Uses no external data source, so it is the fastest and most reliable call. It returns region, country, manufacturer, WMI/VDS/VIS sections, model-year candidates, plant code and serial number. It works for VINs from any country. Alias: `/simple-vin`.

### `GET /validate`

Returns `valid`, `structurallyValid`, `checkDigit { required, actual, expected, valid }`, `errors[]`, `warnings[]`, and a `suggestion` when the VIN contains I, O or Q, which are never used in VINs. It always returns HTTP 200, even for an invalid VIN, because the validation result is the answer.

### `POST /decode/batch`

```json
{ "vins": ["1HGCM82633A004352", "5YJ3E1EA7KF317000"] }
```

You can send up to **50 VINs**. Each item has its own `success` flag and either `data` or `error`, so one bad VIN does not fail the whole batch. Add `?full=true` to include `specs`.

### `POST /extract-vin`: read a VIN from an image

Send the image in **one** of these ways:

| Method | How |
|---|---|
| File upload | `multipart/form-data`, field name **`file`** (or `image`) |
| Base64 | JSON `{ "image_base64": "<base64 or data:image/...;base64,...>" }` |
| Public URL | JSON `{ "image_url": "https://…/photo.jpg" }` |

| Query parameter | Description |
|---|---|
| `decode` | Defaults to `true`, which also decodes the VIN that was found. Use `false` for a faster OCR-only result. |
| `include_text` | `true` also returns the raw OCR text |

Supported formats are JPEG, PNG, WEBP, BMP, GIF and TIFF, up to **8 MB**.

```bash
curl -X POST 'https://vin-recognition-decoder.p.rapidapi.com/extract-vin' \
  -H 'X-RapidAPI-Key: <YOUR_KEY>' -H 'X-RapidAPI-Host: vin-recognition-decoder.p.rapidapi.com' \
  -F 'file=@door-sticker.jpg'
```

The response includes:

- `vin`: the best candidate.
- `checkDigitValid`.
- `correctedFromOcr`: `true` when look-alike characters were fixed, for example an O read as 0.
- `alternatives[]`: other candidates found in the image.
- `vehicle`: the decoded summary.

Alias: `/extract-vin34`.

### `GET /report`: everything in one call

`?vin=…` returns the following sections:

- `vehicle`: full decode.
- `recalls`.
- `complaints`: a summary.
- `safetyRatings`.
- `fuelEconomy`.
- `history`: counts of history records.

The sections are fetched in parallel. If one source is down, that section is `null` and the reason appears in `meta.sectionErrors`, while the rest of the report is still returned.

### `GET /recalls`

Takes either `vin`, or `make` + `model` + `year`. It returns NHTSA safety recalls with the following fields:

- `campaignNumber`
- `component`
- `summary`
- `consequence`
- `remedy`
- `reportReceivedDate`
- `parkIt`
- `parkOutside`
- `overTheAirUpdate`

The newest recalls come first.

### `GET /complaints`

Takes either `vin`, or `make` + `model` + `year`. Optional parameters:

| Parameter | Description |
|---|---|
| `limit` | Default 20, maximum 100 |
| `offset` | Defaults to 0 |
| `component` | Filter by component, for example `AIR BAGS` |

The response has a `summary` with the total, crashes, fires, injuries, deaths and the top 10 components, plus a page of complaints with the newest first.

### `GET /safety-ratings`

Takes either `vin`, or `make` + `model` + `year`. It returns NHTSA 5-star ratings (overall, frontal, side, pole and rollover), the safety technology, and links to crash-test photos for each body style.

### `GET /fuel-economy`

Takes either `vin`, or `make` + `model` + `year`. It returns EPA data for each variant:

- City, highway and combined MPG.
- For electric vehicles: kWh per 100 miles and range.
- CO₂ in grams per mile.
- Annual fuel cost and EPA scores.

When the request uses a VIN, the variant whose engine matches the decoded engine is flagged with `bestMatch: true`.

### `GET /history-check`

`?vin=…` returns how many history records exist for the VIN (`damages`, `odometerReadings`, `events` and `photos`) plus `hasDamageRecords`. It only gives counts. It does not return the records themselves.

### `GET /wmi`

`?code=1HG` takes the first 3 characters of a VIN and returns the manufacturer, region and country.

### `GET /makes` and `GET /models`

- `/makes?type=car&search=hon`: `type` is optional. Examples are `car`, `truck`, `motorcycle`, `bus` and `multipurpose passenger vehicle (mpv)`.
- `/models?make=honda&year=2020&type=car`: `year` and `type` are optional.

### `GET /health`

Liveness check.

---

## Error codes

| HTTP | `error.code` | Meaning / what to do |
|---|---|---|
| 400 | `MISSING_VIN` | Add `?vin=` |
| 400 | `INVALID_VIN` | Wrong length or characters. See `details.errors` and `details.suggestion`. |
| 422 | `CHECK_DIGIT_MISMATCH` | Only returned with `strict=true`. The VIN is probably mistyped. |
| 422 | `VEHICLE_NOT_IDENTIFIED` | Make, model or year could not be decoded, so model-level data is unavailable. Pass `make`, `model` and `year` instead. |
| 400 | `MISSING_VEHICLE` | Pass `vin`, or all of `make`, `model` and `year`. |
| 400 | `INVALID_YEAR`, `INVALID_LIMIT`, `INVALID_OFFSET`, `INVALID_WMI`, `MISSING_MAKE` | Fix the parameter |
| 400 | `MISSING_VINS` | The batch body must be `{"vins": [...]}`. |
| 413 | `TOO_MANY_VINS` | Send no more than 50 VINs per batch. |
| 400 | `INVALID_JSON` | The body is not valid JSON. |
| 400 | `MISSING_IMAGE`, `INVALID_UPLOAD`, `INVALID_BASE64`, `INVALID_IMAGE_URL`, `IMAGE_DOWNLOAD_FAILED`, `EMPTY_IMAGE` | Fix the image input. |
| 413 | `IMAGE_TOO_LARGE`, `PAYLOAD_TOO_LARGE` | Images must be 8 MB or smaller. |
| 415 | `UNSUPPORTED_IMAGE_TYPE` | Send JPEG, PNG, WEBP, BMP, GIF or TIFF. |
| 422 | `VIN_NOT_FOUND_IN_IMAGE` | No VIN was readable. Retake the photo (see the tips below). |
| 404 | `WMI_NOT_FOUND`, `ROUTE_NOT_FOUND` | Unknown WMI or endpoint |
| 503 | `BUSY` | Too many images are being processed. Retry after the `Retry-After` header. |
| 502 | `UPSTREAM_UNAVAILABLE` | A data source is temporarily down. Retry later. |
| 504 | `UPSTREAM_TIMEOUT`, `OCR_TIMEOUT` | Retry. For OCR, send a smaller and sharper image. |
| 500 | `INTERNAL_ERROR` | Retry. If it persists, contact support with the `requestId`. |

**Retry only 502, 503 and 504**, with backoff (for example 2 s, then 5 s, then 15 s). Retrying a 4xx gives the same answer every time and still counts against your quota.

---

## Do's and don'ts

### Do

- **Validate first** with `/validate` or `/decode-basic` when the VINs come from user input. These calls are instant and catch typos before you spend a full decode.
- **Use `compact=true`** on `/decode` when you only need the main fields. The response is about half the size.
- **Use `/decode/batch`** for lists of VINs instead of many single calls.
- **Use `/report`** when you need several data sets for one VIN. It is one request instead of five.
- **Check `meta.warnings` and `decodeQuality`** before trusting a result blindly.
- **Cache results on your side.** A VIN's specs never change. Recalls and complaints change slowly, so refreshing them daily is plenty.
- **For photos**, follow these tips:
  - Crop to the VIN area.
  - Shoot straight on, in good light, without glare.
  - Make sure the VIN text is at least about 30 px high.
  - Door-jamb stickers and registration documents read best. Stamped chassis numbers are the hardest.
- **Show `alternatives` to your user** when `checkDigitValid` is `false` on an OCR result. Let them confirm the VIN.
- **Handle errors by `error.code`**, not by HTTP status alone or by the message text.

### Don't

- **Don't send pre-1981 or non-standard IDs** (fewer than 17 characters, or chassis or frame numbers). They are rejected with `INVALID_VIN`.
- **Don't "fix" I, O or Q yourself.** They never appear in VINs. `/validate` returns a `suggestion` for you.
- **Don't expect full detail for every country.** See the coverage section below.
- **Don't treat `/recalls` as proof that a specific car still needs a repair.** Recalls are listed per make, model and year. Whether a particular vehicle has been repaired is only known by the manufacturer, or by the VIN lookup at nhtsa.gov/recalls.
- **Don't treat `/history-check` as a full history report.** It tells you how many records exist, not what they say.
- **Don't send huge images or PDFs.** Resize photos to about 1500–2500 px on the long side. That is faster and usually more accurate.
- **Don't retry 4xx errors in a loop.** You will burn your quota on the same answer.
- **Don't call the API directly from a public web page or mobile app with your RapidAPI key embedded.** Proxy it through your backend so your key can't be stolen.
- **Don't use this data to make legal, insurance or safety-critical decisions on its own.** Confirm against official documents.

---

## Data coverage and accuracy

| Data | Source | Coverage |
|---|---|---|
| Specs (`/decode`) | NHTSA vPIC | **Best for vehicles sold in the USA and Canada.** For European and Asian-market VINs you usually get make, manufacturer, plant country and model year, but often not the model or engine. |
| Offline decode (`/decode-basic`, `/validate`, `/wmi`) | ISO 3779 and the WMI registry | Worldwide |
| Recalls, complaints, crash ratings | NHTSA | US-market vehicles |
| Fuel economy | US EPA (fueleconomy.gov) | US-market vehicles, model year 1984 and later |
| History counts | Third-party vehicle-history index | Varies by vehicle; strongest for vehicles sold in the US and Europe |

**Model year:**

- In North America, position 10 of the VIN plus position 7 gives a single year.
- Elsewhere, position 10 can mean two years 30 years apart, for example `E` = 2014 or 1984. The API returns the most recent plausible year and lists every candidate in `possibleModelYears`.
- Some manufacturers outside North America do not encode the year at all.

**Check digit:** position 9 is mandatory in North America and China. Elsewhere it is often just a filler, so a mismatch there is only a warning.

---

## FAQ

**Why is `model` null for my European VIN?**
The US government database only has full data for vehicles sold in North America. You still get make, manufacturer, country and year. Use `/decode-basic` for the structural data.

**Why does `/recalls?vin=…` return 422 `VEHICLE_NOT_IDENTIFIED`?**
The VIN could not be resolved to a model. Call `/recalls?make=…&model=…&year=…` instead.

**Why do I get several fuel-economy variants?**
EPA lists each engine and transmission separately. When you query by VIN, the variant matching the decoded engine is flagged with `bestMatch: true`.

**Is the image stored?**
No. Images are processed in memory and discarded as soon as the response is sent.

---

## Support

💬 **Need help? Contact us on Telegram: [@pintoflow](https://t.me/pintoflow)** for the fastest response. Please include the `meta.requestId` from the response when reporting an issue.

**Subscribe / get your key:** [https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/vin-recognition-decoder](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/vin-recognition-decoder)

## Keywords

VIN decoder API, VIN lookup API, VIN OCR, VIN scanner, extract VIN from image, vehicle identification number decoder, NHTSA vPIC API, car recall API, vehicle safety ratings API, EPA fuel economy API, WMI lookup, vehicle history check, Node.js VIN decoder, Python VIN decoder.

## License

The example code in this repository is MIT licensed. Use of the API is subject to the [RapidAPI terms](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/vin-recognition-decoder).
