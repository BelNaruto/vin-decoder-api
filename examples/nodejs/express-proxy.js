// Minimal Express backend proxy: keep your RapidAPI key on the server, never in the browser/app.
// npm install express
// RAPIDAPI_KEY=xxx node express-proxy.js  ->  GET http://localhost:3000/api/vin/1HGCM82633A004352
//
// API: https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/vin-recognition-decoder
// Support (fastest): Telegram @pintoflow

const express = require('express');

const HOST = 'vin-recognition-decoder.p.rapidapi.com';
const KEY = process.env.RAPIDAPI_KEY;
const app = express();

// Simple in-memory cache: a VIN's specs never change.
const cache = new Map();

app.get('/api/vin/:vin', async (req, res) => {
  const vin = req.params.vin.toUpperCase().replace(/[\s.-]/g, '');
  if (cache.has(vin)) return res.json(cache.get(vin));

  const r = await fetch(`https://${HOST}/decode?vin=${encodeURIComponent(vin)}&compact=true`, {
    headers: { 'X-RapidAPI-Key': KEY, 'X-RapidAPI-Host': HOST },
  });
  const json = await r.json();
  if (json.success) cache.set(vin, json);
  res.status(r.status).json(json);
});

app.get('/api/vin/:vin/report', async (req, res) => {
  const r = await fetch(`https://${HOST}/report?vin=${encodeURIComponent(req.params.vin)}`, {
    headers: { 'X-RapidAPI-Key': KEY, 'X-RapidAPI-Host': HOST },
  });
  res.status(r.status).json(await r.json());
});

app.listen(3000, () => console.log('VIN proxy on http://localhost:3000'));
