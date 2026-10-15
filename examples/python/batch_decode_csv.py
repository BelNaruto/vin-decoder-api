"""Batch-decode a CSV of VINs (50 per request) and write an enriched CSV.

Get your key: https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/vin-recognition-decoder
Support (fastest): Telegram @pintoflow

    pip install requests
    RAPIDAPI_KEY=xxx python batch_decode_csv.py vins.csv decoded.csv

Input CSV needs a column named "vin".
"""
import csv
import os
import sys

import requests

HOST = "vin-recognition-decoder.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"], "X-RapidAPI-Host": HOST}
BATCH = 50
FIELDS = ["vin", "ok", "make", "model", "modelYear", "trim", "bodyClass",
          "engine_cylinders", "engine_displacementL", "transmission_style",
          "plant_country", "decodeQuality", "error"]


def decode_batch(vins):
    r = requests.post(f"https://{HOST}/decode/batch", headers=HEADERS,
                      json={"vins": vins}, timeout=120)
    r.raise_for_status()
    return r.json()["data"]


def flatten(item, vin):
    if not item.get("success"):
        return {"vin": vin, "ok": False, "error": item.get("error", {}).get("code")}
    d = item["data"]
    eng, tr, pl = d.get("engine") or {}, d.get("transmission") or {}, d.get("plant") or {}
    return {
        "vin": d.get("vin", vin), "ok": True, "make": d.get("make"), "model": d.get("model"),
        "modelYear": d.get("modelYear"), "trim": d.get("trim"), "bodyClass": d.get("bodyClass"),
        "engine_cylinders": eng.get("cylinders"), "engine_displacementL": eng.get("displacementL"),
        "transmission_style": tr.get("style"), "plant_country": pl.get("country"),
        "decodeQuality": d.get("decodeQuality"), "error": "",
    }


def main(src, dst):
    with open(src, newline="") as f:
        vins = [row["vin"].strip() for row in csv.DictReader(f) if row.get("vin")]

    with open(dst, "w", newline="") as out:
        w = csv.DictWriter(out, fieldnames=FIELDS)
        w.writeheader()
        for i in range(0, len(vins), BATCH):
            chunk = vins[i:i + BATCH]
            results = decode_batch(chunk)
            items = results if isinstance(results, list) else results.get("results", [])
            for vin, item in zip(chunk, items):
                w.writerow(flatten(item, vin))
            print(f"decoded {min(i + BATCH, len(vins))}/{len(vins)}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "vins.csv",
         sys.argv[2] if len(sys.argv) > 2 else "decoded.csv")
