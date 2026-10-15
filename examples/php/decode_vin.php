<?php
// Decode a VIN with the VIN Recognition/Decoder API (PHP + cURL)
// Get your key: https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/vin-recognition-decoder
// Support (fastest): Telegram @pintoflow
//
// RAPIDAPI_KEY=xxx php decode_vin.php 1HGCM82633A004352

$host = 'vin-recognition-decoder.p.rapidapi.com';
$key  = getenv('RAPIDAPI_KEY') ?: die("Set RAPIDAPI_KEY\n");
$vin  = $argv[1] ?? '1HGCM82633A004352';

$ch = curl_init("https://$host/decode?" . http_build_query(['vin' => $vin, 'compact' => 'true']));
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_TIMEOUT        => 60,
    CURLOPT_HTTPHEADER     => ["X-RapidAPI-Key: $key", "X-RapidAPI-Host: $host"],
]);
$res = json_decode(curl_exec($ch), true);
curl_close($ch);

if (empty($res['success'])) {
    fwrite(STDERR, "{$res['error']['code']}: {$res['error']['message']}\n");
    exit(1);
}

$car = $res['data'];
printf("%s %s %s %s\n", $car['modelYear'], $car['make'], $car['model'], $car['trim'] ?? '');
printf("Engine: %s cyl, %s L\n", $car['engine']['cylinders'] ?? '?', $car['engine']['displacementL'] ?? '?');
printf("Plant:  %s\n", $car['plant']['country'] ?? '?');
