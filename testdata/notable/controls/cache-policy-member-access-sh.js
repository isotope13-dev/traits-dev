// Benign control for the @storybook/core-server 7.6.10 false positive: the
// bundled http-cache-semantics policy object assigns `_isShared=obj.sh`, and
// unrelated bundled helpers create a local log write stream and pipe an HTTP
// response through a decompress chain. The bare `obj.sh` member access is a
// cache-policy flag, not a shell-script path, so the download-to-shell-script
// conviction must not fire; the ordinary stream-to-file capability stays
// notable.
const https = require("https");
const fs = require("fs-extra");
const zlib = require("zlib");

class CachePolicy {
  static fromObject(obj) {
    if (this._responseTime) throw Error("Reinitialized");
    if (!obj || obj.v !== 1) throw Error("Invalid serialization");
    this._responseTime = obj.t;
    this._isShared = obj.sh;
    this._cacheHeuristic = obj.ch;
    this._immutableMinTtl = obj.imm !== void 0 ? obj.imm : 24 * 3600 * 1e3;
    this._status = obj.st;
    this._resHeaders = obj.resh;
    this._rescc = obj.rescc;
    return new this(void 0, void 0, { _fromObject: obj });
  }
}

const createLogStream = async (logFileName = "storybook.log") => {
  const temporaryLogPath = temporary.file({ name: logFileName });
  const logStream = fs.createWriteStream(temporaryLogPath, { encoding: "utf8" });
  return new Promise((resolve, reject) => {
    logStream.once("open", () => resolve({ logStream }));
    logStream.once("error", reject);
  });
};

const decompressResponse = (response, checker) => {
  const finalStream = new PassThrough({ autoDestroy: false });
  const decompressStream = zlib.createUnzip();
  mimicResponse(response, finalStream);
  response.pipe(checker).pipe(decompressStream).pipe(finalStream);
  return finalStream;
};

https.get("https://registry.npmjs.org/@storybook/core-server", (res) => {
  decompressResponse(res, contentChecker);
});
