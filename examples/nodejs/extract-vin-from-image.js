// Read a VIN from a photo (VIN OCR) – Node.js 18+, no dependencies
// Get your key: https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/vin-recognition-decoder
// Support (fastest): Telegram @pintoflow
//
// Usage:
//   RAPIDAPI_KEY=xxx node extract-vin-from-image.js ./door-sticker.jpg
//   RAPIDAPI_KEY=xxx node extract-vin-from-image.js https://example.com/vin-plate.jpg

const fs = require('node:fs');
const path = require('node:path');

const HOST = 'vin-recognition-decoder.p.rapidapi.com';
const KEY = process.env.RAPIDAPI_KEY;
if (!KEY) throw new Error('Set RAPIDAPI_KEY');

async function extractVin(input) {
  const headers = { 'X-RapidAPI-Key': KEY, 'X-RapidAPI-Host': HOST };
  let body;

  if (/^https?:\/\//.test(input)) {
    headers['Content-Type'] = 'application/json';
    body = JSON.stringify({ image_url: input });
  } else {
    const form = new FormData();
    form.append('file', new Blob([fs.readFileSync(input)]), path.basename(input));
    body = form; // fetch sets the multipart boundary automatically
  }

  const res = await fetch(`https://${HOST}/extract-vin?decode=true`, { method: 'POST', headers, body });
  return res.json();
}

(async () => {
  const input = process.argv[2];
  if (!input) return console.error('Pass an image path or URL');

  const out = await extractVin(input);
  if (!out.success) {
    console.error(out.error.code, '-', out.error.message);
    if (out.error.code === 'VIN_NOT_FOUND_IN_IMAGE') {
      console.error('Tip: crop to the VIN, shoot straight on, avoid glare, VIN text ≥ 30px high.');
    }
    process.exit(1);
  }

  const { vin, checkDigitValid, correctedFromOcr, alternatives, vehicle } = out.data;
  console.log('VIN:', vin, checkDigitValid ? '(check digit OK)' : '(check digit FAILED)');
  if (correctedFromOcr) console.log('Note: look-alike characters were corrected (e.g. O→0).');
  if (!checkDigitValid && alternatives?.length) {
    console.log('Ask the user to confirm one of:', alternatives);
  }
  if (vehicle) console.log('Vehicle:', `${vehicle.modelYear} ${vehicle.make} ${vehicle.model}`);
})();
