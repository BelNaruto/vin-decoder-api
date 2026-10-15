"""Decode a VIN with the VIN Recognition/Decoder API.

Get your key: https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/vin-recognition-decoder
Support (fastest): Telegram @pintoflow

    pip install requests
    RAPIDAPI_KEY=xxx python decode_vin.py 1HGCM82633A004352
"""
import os
import sys
import time

import requests

HOST = "vin-recognition-decoder.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"], "X-RapidAPI-Host": HOST}


def call(path, params=None, method="GET", json=None):
    """Call the API; retry only 502/503/504 with backoff."""
    for delay in (2, 5, 15, None):
        r = requests.request(method, f"https://{HOST}{path}", headers=HEADERS,
                             params=params, json=json, timeout=60)
        body = r.json()
        if body.get("success"):
            return body
        if r.status_code in (502, 503, 504) and delay:
            time.sleep(int(r.headers.get("Retry-After", delay)))
            continue
        err = body.get("error", {})
        raise RuntimeError(f"{err.get('code')}: {err.get('message')} "
                           f"(requestId {body.get('meta', {}).get('requestId')})")


def main():
    vin = sys.argv[1] if len(sys.argv) > 1 else "1HGCM82633A004352"

    check = call("/validate", {"vin": vin})["data"]
    if not check["valid"]:
        print("Invalid VIN:", check["errors"], "suggestion:", check.get("suggestion"))
        sys.exit(1)

    res = call("/decode", {"vin": vin, "compact": "true"})
    car = res["data"]
    for w in res["meta"].get("warnings", []):
        print("WARNING:", w)

    print(f"{car['modelYear']} {car['make']} {car['model']} {car.get('trim') or ''}".strip())
    print("Body:        ", car.get("bodyClass"))
    print("Engine:      ", car.get("engine"))
    print("Transmission:", car.get("transmission"))
    print("Plant:       ", car.get("plant"))
    print("Quality:     ", car.get("decodeQuality"))


if __name__ == "__main__":
    main()
