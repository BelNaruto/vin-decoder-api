#!/usr/bin/env bash
# VIN Recognition/Decoder API – cURL examples for every endpoint
# Get your key: https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/vin-recognition-decoder
# Support (fastest): Telegram @pintoflow
set -euo pipefail
: "${RAPIDAPI_KEY:?Set RAPIDAPI_KEY first: export RAPIDAPI_KEY=your-key}"
HOST="vin-recognition-decoder.p.rapidapi.com"
VIN="${1:-1HGCM82633A004352}"
H=(-H "X-RapidAPI-Key: $RAPIDAPI_KEY" -H "X-RapidAPI-Host: $HOST")

echo "== Validate";            curl -s "${H[@]}" "https://$HOST/validate?vin=$VIN"; echo
echo "== Basic offline decode"; curl -s "${H[@]}" "https://$HOST/decode-basic?vin=$VIN"; echo
echo "== Full decode (compact)"; curl -s "${H[@]}" "https://$HOST/decode?vin=$VIN&compact=true"; echo
echo "== Batch decode"
curl -s "${H[@]}" -H "Content-Type: application/json" \
  -d '{"vins":["1HGCM82633A004352","5YJ3E1EA7KF317000"]}' "https://$HOST/decode/batch"; echo
echo "== Full report";         curl -s "${H[@]}" "https://$HOST/report?vin=$VIN"; echo
echo "== Recalls";             curl -s "${H[@]}" "https://$HOST/recalls?vin=$VIN"; echo
echo "== Recalls by make/model/year"; curl -s "${H[@]}" "https://$HOST/recalls?make=honda&model=accord&year=2003"; echo
echo "== Complaints (air bags)"; curl -s "${H[@]}" "https://$HOST/complaints?vin=$VIN&limit=5&component=AIR%20BAGS"; echo
echo "== Safety ratings";      curl -s "${H[@]}" "https://$HOST/safety-ratings?vin=$VIN"; echo
echo "== Fuel economy";        curl -s "${H[@]}" "https://$HOST/fuel-economy?vin=$VIN"; echo
echo "== History check";       curl -s "${H[@]}" "https://$HOST/history-check?vin=$VIN"; echo
echo "== WMI lookup";          curl -s "${H[@]}" "https://$HOST/wmi?code=${VIN:0:3}"; echo
echo "== Makes";               curl -s "${H[@]}" "https://$HOST/makes?type=car&search=hon"; echo
echo "== Models";              curl -s "${H[@]}" "https://$HOST/models?make=honda&year=2020&type=car"; echo

# Extract a VIN from a photo (uncomment and point to your image)
# curl -s "${H[@]}" -F "file=@door-sticker.jpg" "https://$HOST/extract-vin"
# curl -s "${H[@]}" -H "Content-Type: application/json" \
#   -d '{"image_url":"https://example.com/vin-plate.jpg"}' "https://$HOST/extract-vin?decode=true"
