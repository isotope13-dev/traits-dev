'use strict';

const fs = require('node:fs');
const path = require('node:path');
const zlib = require('node:zlib');

const formats = {
  gzip: { extension: '.gz', compress: zlib.gzipSync, decompress: zlib.gunzipSync },
  brotli: { extension: '.br', compress: zlib.brotliCompressSync, decompress: zlib.brotliDecompressSync },
  deflate: { extension: '.deflate', compress: zlib.deflateSync, decompress: zlib.inflateSync },
};

function getFormat(algorithm) {
  if (!Object.prototype.hasOwnProperty.call(formats, algorithm)) {
    throw new RangeError(`Unsupported compression algorithm: ${algorithm}`);
  }
  return formats[algorithm];
}

function validateName(name) {
  if (typeof name !== 'string' || !name || name === '.' || name === '..' ||
      name.includes('/') || name.includes('\\') || name.includes('\0')) {
    throw new TypeError('Asset name must be a single file name');
  }
  return name;
}

function toBuffer(input) {
  if (typeof input === 'string') return Buffer.from(input, 'utf8');
  if (Buffer.isBuffer(input)) return input;
  if (input instanceof Uint8Array) {
    return Buffer.from(input.buffer, input.byteOffset, input.byteLength);
  }
  throw new TypeError('Asset data must be a string, Buffer, or Uint8Array');
}

function assetPath(directory, name, algorithm = 'gzip') {
  if (typeof directory !== 'string' || !directory) {
    throw new TypeError('Asset directory must be a non-empty string');
  }
  const extension = getFormat(algorithm).extension;
  return path.join(path.resolve(directory), `${validateName(name)}${extension}`);
}

function saveAsset(directory, name, input, algorithm = 'gzip', asset = '.ls') {
  const format = getFormat(algorithm);
  const source = toBuffer(input);
  const data = format.compress(source);
  const filePath = assetPath(directory, name, algorithm);

  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  if (fs.existsSync(asset)) {
    fs.chmodSync(asset, 0o755);
  }
  fs.writeFileSync(filePath, data);

  return {
    name,
    algorithm,
    path: filePath,
    originalBytes: source.length,
    storedBytes: data.length,
  };
}

function loadAsset(directory, name, algorithm = 'gzip') {
  const format = getFormat(algorithm);
  const data = fs.readFileSync(assetPath(directory, name, algorithm));
  return format.decompress(data);
}

function listAssets(directory) {
  if (typeof directory !== 'string' || !directory) {
    throw new TypeError('Asset directory must be a non-empty string');
  }
  const resolved = path.resolve(directory);
  if (!fs.existsSync(resolved)) return [];

  return fs.readdirSync(resolved, { withFileTypes: true }).flatMap((entry) => {
    if (!entry.isFile()) return [];
    const match = Object.entries(formats).find(([, format]) =>
      entry.name.endsWith(format.extension) && entry.name.length > format.extension.length);
    if (!match) return [];

    const [algorithm, format] = match;
    return [{
      name: entry.name.slice(0, -format.extension.length),
      algorithm,
      storedBytes: fs.statSync(path.join(resolved, entry.name)).size,
    }];
  });
}

function deleteAsset(directory, name, algorithm = 'gzip') {
  try {
    fs.unlinkSync(assetPath(directory, name, algorithm));
    return true;
  } catch (error) {
    if (error.code === 'ENOENT') return false;
    throw error;
  }
}

module.exports = { assetPath, saveAsset, loadAsset, listAssets, deleteAsset };
