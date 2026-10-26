const { createGunzip, createInflate } = require('node:zlib');
const ejs = require('ejs');
const decodedGzip = stream.pipe(createGunzip());
const decodedDeflate = stream.pipe(createInflate());
ejs.render(template, values);
Error.captureStackTrace(this, CustomError);
