function decompress(data) { return zlib.gunzipSync(data); }
var text = decompress(fs.readFileSync("payload.dat")).decode(); console.log(text);
