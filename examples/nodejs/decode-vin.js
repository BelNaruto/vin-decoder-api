// Validate and decode a VIN with the VIN Recognition/Decoder API (Node.js 18+, no dependencies)
// Get your key: https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/vin-recognition-decoder
// Support (fastest): Telegram @pintoflow
//
// Usage: RAPIDAPI_KEY=xxx node decode-vin.js 1HGCM82633A004352

const HOST = 'vin-recognition-decoder.p.rapidapi.com';
const KEY = process.env.RAPIDAPI_KEY;
if (!KEY) throw new Error('Set RAPIDAPI_KEY');

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// Retry only 502/503/504 with backoff, as recommended in the docs.
async function call(path, { method = 'GET', body } = {}) {
  const delays = [2000, 5000, 15000];
  for (let attempt = 0; ; attempt++) {
    const res = await fetch(`https://${HOST}${path}`, {
      method,
      headers: {
        'X-RapidAPI-Key': KEY,
        'X-RapidAPI-Host': HOST,
        ...(body ? { 'Content-Type': 'application/json' } : {}),
      },
      body: body ? JSON.stringify(body) : undefined,
    });
    const json = await res.json();
    if (json.success) return json;
    if ([502, 503, 504].includes(res.status) && attempt < delays.length) {
      const retryAfter = Number(res.headers.get('retry-after')) * 1000;
      await sleep(retryAfter || delays[attempt]);
      continue;
    }
    const err = new Error(`${json.error?.code}: ${json.error?.message}`);
    err.code = json.error?.code;
    err.requestId = json.meta?.requestId;
    throw err;
  }
}

async function main() {
  const vin = process.argv[2] || '1HGCM82633A004352';

  // 1. Cheap validation first (always HTTP 200)
  const { data: v } = await call(`/validate?vin=${encodeURIComponent(vin)}`);
  if (!v.valid) {
    console.error('Invalid VIN:', v.errors, v.suggestion ? `Did you mean ${v.suggestion}?` : '');
    process.exit(1);
  }

  // 2. Full decode (compact summary)
  const { data: car, meta } = await call(`/decode?vin=${encodeURIComponent(vin)}&compact=true`);
  if (meta.warnings) console.warn('Warnings:', meta.warnings);

  console.log(`${car.modelYear} ${car.make} ${car.model} ${car.trim ?? ''}`.trim());
  console.log('Body:        ', car.bodyClass);
  console.log('Engine:      ', car.engine);
  console.log('Transmission:', car.transmission);
  console.log('Plant:       ', car.plant);
  console.log('Quality:     ', car.decodeQuality);
}

main().catch((e) => {
  console.error(e.message, e.requestId ? `(requestId ${e.requestId})` : '');
  process.exit(1);
});
