const zlib = require('zlib'); module.exports = { gzip: zlib.createGzip, gunzip: zlib.createGunzip };
