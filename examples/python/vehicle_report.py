"""One-call vehicle report: decode + recalls + complaints + crash ratings + fuel economy + history counts.

Get your key: https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/vin-recognition-decoder
Support (fastest): Telegram @pintoflow

    pip install requests
    RAPIDAPI_KEY=xxx python vehicle_report.py 1HGCM82633A004352
"""
import json
import os
import sys

import requests

HOST = "vin-recognition-decoder.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"], "X-RapidAPI-Host": HOST}

vin = sys.argv[1] if len(sys.argv) > 1 else "1HGCM82633A004352"
res = requests.get(f"https://{HOST}/report", headers=HEADERS, params={"vin": vin}, timeout=90).json()

if not res.get("success"):
    sys.exit(f"{res['error']['code']}: {res['error']['message']}")

r = res["data"]
# A section is null if its data source was down; the reason is in meta.sectionErrors
for section, reason in (res["meta"].get("sectionErrors") or {}).items():
    print(f"[{section} unavailable: {reason}]")

v = r.get("vehicle") or {}
print(f"\n=== {v.get('modelYear')} {v.get('make')} {v.get('model')} {v.get('trim') or ''} ===")

recalls = r.get("recalls")
if recalls is not None:
    items = recalls if isinstance(recalls, list) else recalls.get("recalls", [])
    print(f"\nRecalls: {len(items)}")
    for rc in items[:5]:
        print(f" - {rc.get('campaignNumber')} | {rc.get('component')}"
              f"{'  ⚠ PARK IT' if rc.get('parkIt') else ''}")

if r.get("complaints"):
    print("\nComplaints summary:", json.dumps(r["complaints"].get("summary", r["complaints"]), indent=2)[:600])

if r.get("safetyRatings"):
    print("\nSafety ratings:", json.dumps(r["safetyRatings"], indent=2)[:600])

if r.get("fuelEconomy"):
    print("\nFuel economy:", json.dumps(r["fuelEconomy"], indent=2)[:600])

if r.get("history"):
    print("\nHistory record counts:", r["history"])
