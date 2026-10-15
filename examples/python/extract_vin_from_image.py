"""Read a VIN from a photo (VIN OCR) – file upload, URL or base64.

Get your key: https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/vin-recognition-decoder
Support (fastest): Telegram @pintoflow

    pip install requests
    RAPIDAPI_KEY=xxx python extract_vin_from_image.py door-sticker.jpg
    RAPIDAPI_KEY=xxx python extract_vin_from_image.py https://example.com/vin-plate.jpg
"""
import os
import sys

import requests

HOST = "vin-recognition-decoder.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"], "X-RapidAPI-Host": HOST}
URL = f"https://{HOST}/extract-vin"


def extract(src):
    params = {"decode": "true"}
    if src.startswith(("http://", "https://")):
        r = requests.post(URL, headers=HEADERS, params=params, json={"image_url": src}, timeout=90)
    else:
        with open(src, "rb") as f:
            r = requests.post(URL, headers=HEADERS, params=params,
                              files={"file": (os.path.basename(src), f)}, timeout=90)
    return r.json()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Pass an image path or URL")
    out = extract(sys.argv[1])
    if not out.get("success"):
        sys.exit(f"{out['error']['code']}: {out['error']['message']}")

    d = out["data"]
    print("VIN:", d["vin"], "| check digit valid:", d.get("checkDigitValid"))
    if d.get("correctedFromOcr"):
        print("Look-alike characters were corrected (e.g. O -> 0)")
    if not d.get("checkDigitValid") and d.get("alternatives"):
        print("Please confirm one of:", d["alternatives"])
    v = d.get("vehicle")
    if v:
        print("Vehicle:", v.get("modelYear"), v.get("make"), v.get("model"))
