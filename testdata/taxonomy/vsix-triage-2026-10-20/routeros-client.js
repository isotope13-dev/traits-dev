var __defProp = Object.defineProperty;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __moduleCache = /* @__PURE__ */ new WeakMap;
var __toCommonJS = (from) => {
  var entry = __moduleCache.get(from), desc;
  if (entry)
    return entry;
  entry = __defProp({}, "__esModule", { value: true });
  if (from && typeof from === "object" || typeof from === "function")
    __getOwnPropNames(from).map((key) => !__hasOwnProp.call(entry, key) && __defProp(entry, key, {
      get: () => from[key],
      enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable
    }));
  __moduleCache.set(from, entry);
  return entry;
};
var __commonJS = (cb, mod) => () => (mod || cb((mod = { exports: {} }).exports, mod), mod.exports);
var __export = (target, all) => {
  for (var name in all)
    __defProp(target, name, {
      get: all[name],
      enumerable: true,
      configurable: true,
      set: (newValue) => all[name] = () => newValue
    });
};
var __esm = (fn, res) => () => (fn && (res = fn(fn = 0)), res);

// node:util
var exports_util = {};
__export(exports_util, {
  types: () => types,
  promisify: () => promisify,
  log: () => log2,
  isUndefined: () => isUndefined2,
  isSymbol: () => isSymbol,
  isString: () => isString2,
  isRegExp: () => isRegExp2,
  isPrimitive: () => isPrimitive,
  isObject: () => isObject2,
  isNumber: () => isNumber2,
  isNullOrUndefined: () => isNullOrUndefined,
  isNull: () => isNull,
  isFunction: () => isFunction3,
  isError: () => isError,
  isDate: () => isDate2,
  isBuffer: () => isBuffer2,
  isBoolean: () => isBoolean2,
  isArray: () => isArray2,
  inspect: () => inspect,
  inherits: () => inherits2,
  format: () => format,
  deprecate: () => deprecate,
  default: () => util_default,
  debuglog: () => debuglog,
  callbackifyOnRejected: () => callbackifyOnRejected,
  callbackify: () => callbackify,
  _extend: () => _extend,
  TextEncoder: () => TextEncoder3,
  TextDecoder: () => TextDecoder2
});
function format(f, ...args) {
  if (!isString2(f)) {
    var objects = [f];
    for (var i = 0;i < args.length; i++)
      objects.push(inspect(args[i]));
    return objects.join(" ");
  }
  var i = 0, len = args.length, str = String(f).replace(formatRegExp, function(x2) {
    if (x2 === "%%")
      return "%";
    if (i >= len)
      return x2;
    switch (x2) {
      case "%s":
        return String(args[i++]);
      case "%d":
        return Number(args[i++]);
      case "%j":
        try {
          return JSON.stringify(args[i++]);
        } catch (_) {
          return "[Circular]";
        }
      default:
        return x2;
    }
  });
  for (var x = args[i];i < len; x = args[++i])
    if (isNull(x) || !isObject2(x))
      str += " " + x;
    else
      str += " " + inspect(x);
  return str;
}
function deprecate(fn, msg) {
  if (typeof process > "u" || process?.noDeprecation === true)
    return fn;
  var warned = false;
  function deprecated(...args) {
    if (!warned) {
      if (process.throwDeprecation)
        throw Error(msg);
      else if (process.traceDeprecation)
        console.trace(msg);
      else
        console.error(msg);
      warned = true;
    }
    return fn.apply(this, ...args);
  }
  return deprecated;
}
function stylizeWithColor(str, styleType) {
  var style = inspect.styles[styleType];
  if (style)
    return "\x1B[" + inspect.colors[style][0] + "m" + str + "\x1B[" + inspect.colors[style][1] + "m";
  else
    return str;
}
function stylizeNoColor(str, styleType) {
  return str;
}
function arrayToHash(array) {
  var hash = {};
  return array.forEach(function(val, idx) {
    hash[val] = true;
  }), hash;
}
function formatValue(ctx, value, recurseTimes) {
  if (ctx.customInspect && value && isFunction3(value.inspect) && value.inspect !== inspect && !(value.constructor && value.constructor.prototype === value)) {
    var ret = value.inspect(recurseTimes, ctx);
    if (!isString2(ret))
      ret = formatValue(ctx, ret, recurseTimes);
    return ret;
  }
  var primitive = formatPrimitive(ctx, value);
  if (primitive)
    return primitive;
  var keys = Object.keys(value), visibleKeys = arrayToHash(keys);
  if (ctx.showHidden)
    keys = Object.getOwnPropertyNames(value);
  if (isError(value) && (keys.indexOf("message") >= 0 || keys.indexOf("description") >= 0))
    return formatError(value);
  if (keys.length === 0) {
    if (isFunction3(value)) {
      var name = value.name ? ": " + value.name : "";
      return ctx.stylize("[Function" + name + "]", "special");
    }
    if (isRegExp2(value))
      return ctx.stylize(RegExp.prototype.toString.call(value), "regexp");
    if (isDate2(value))
      return ctx.stylize(Date.prototype.toString.call(value), "date");
    if (isError(value))
      return formatError(value);
  }
  var base = "", array = false, braces = ["{", "}"];
  if (isArray2(value))
    array = true, braces = ["[", "]"];
  if (isFunction3(value)) {
    var n = value.name ? ": " + value.name : "";
    base = " [Function" + n + "]";
  }
  if (isRegExp2(value))
    base = " " + RegExp.prototype.toString.call(value);
  if (isDate2(value))
    base = " " + Date.prototype.toUTCString.call(value);
  if (isError(value))
    base = " " + formatError(value);
  if (keys.length === 0 && (!array || value.length == 0))
    return braces[0] + base + braces[1];
  if (recurseTimes < 0)
    if (isRegExp2(value))
      return ctx.stylize(RegExp.prototype.toString.call(value), "regexp");
    else
      return ctx.stylize("[Object]", "special");
  ctx.seen.push(value);
  var output;
  if (array)
    output = formatArray(ctx, value, recurseTimes, visibleKeys, keys);
  else
    output = keys.map(function(key) {
      return formatProperty(ctx, value, recurseTimes, visibleKeys, key, array);
    });
  return ctx.seen.pop(), reduceToSingleString(output, base, braces);
}
function formatPrimitive(ctx, value) {
  if (isUndefined2(value))
    return ctx.stylize("undefined", "undefined");
  if (isString2(value)) {
    var simple = "'" + JSON.stringify(value).replace(/^"|"$/g, "").replace(/'/g, "\\'").replace(/\\"/g, '"') + "'";
    return ctx.stylize(simple, "string");
  }
  if (isNumber2(value))
    return ctx.stylize("" + value, "number");
  if (isBoolean2(value))
    return ctx.stylize("" + value, "boolean");
  if (isNull(value))
    return ctx.stylize("null", "null");
}
function formatError(value) {
  return "[" + Error.prototype.toString.call(value) + "]";
}
function formatArray(ctx, value, recurseTimes, visibleKeys, keys) {
  var output = [];
  for (var i = 0, l = value.length;i < l; ++i)
    if (hasOwnProperty2(value, String(i)))
      output.push(formatProperty(ctx, value, recurseTimes, visibleKeys, String(i), true));
    else
      output.push("");
  return keys.forEach(function(key) {
    if (!key.match(/^\d+$/))
      output.push(formatProperty(ctx, value, recurseTimes, visibleKeys, key, true));
  }), output;
}
function formatProperty(ctx, value, recurseTimes, visibleKeys, key, array) {
  var name, str, desc;
  if (desc = Object.getOwnPropertyDescriptor(value, key) || { value: value[key] }, desc.get)
    if (desc.set)
      str = ctx.stylize("[Getter/Setter]", "special");
    else
      str = ctx.stylize("[Getter]", "special");
  else if (desc.set)
    str = ctx.stylize("[Setter]", "special");
  if (!hasOwnProperty2(visibleKeys, key))
    name = "[" + key + "]";
  if (!str)
    if (ctx.seen.indexOf(desc.value) < 0) {
      if (isNull(recurseTimes))
        str = formatValue(ctx, desc.value, null);
      else
        str = formatValue(ctx, desc.value, recurseTimes - 1);
      if (str.indexOf(`
`) > -1)
        if (array)
          str = str.split(`
`).map(function(line) {
            return "  " + line;
          }).join(`
`).slice(2);
        else
          str = `
` + str.split(`
`).map(function(line) {
            return "   " + line;
          }).join(`
`);
    } else
      str = ctx.stylize("[Circular]", "special");
  if (isUndefined2(name)) {
    if (array && key.match(/^\d+$/))
      return str;
    if (name = JSON.stringify("" + key), name.match(/^"([a-zA-Z_][a-zA-Z_0-9]*)"$/))
      name = name.slice(1, -1), name = ctx.stylize(name, "name");
    else
      name = name.replace(/'/g, "\\'").replace(/\\"/g, '"').replace(/(^"|"$)/g, "'"), name = ctx.stylize(name, "string");
  }
  return name + ": " + str;
}
function reduceToSingleString(output, base, braces) {
  var numLinesEst = 0, length = output.reduce(function(prev, cur) {
    if (numLinesEst++, cur.indexOf(`
`) >= 0)
      numLinesEst++;
    return prev + cur.replace(/\u001b\[\d\d?m/g, "").length + 1;
  }, 0);
  if (length > 60)
    return braces[0] + (base === "" ? "" : base + `
 `) + " " + output.join(`,
  `) + " " + braces[1];
  return braces[0] + base + " " + output.join(", ") + " " + braces[1];
}
function isArray2(ar) {
  return Array.isArray(ar);
}
function isBoolean2(arg) {
  return typeof arg === "boolean";
}
function isNull(arg) {
  return arg === null;
}
function isNullOrUndefined(arg) {
  return arg == null;
}
function isNumber2(arg) {
  return typeof arg === "number";
}
function isString2(arg) {
  return typeof arg === "string";
}
function isSymbol(arg) {
  return typeof arg === "symbol";
}
function isUndefined2(arg) {
  return arg === undefined;
}
function isRegExp2(re) {
  return isObject2(re) && objectToString(re) === "[object RegExp]";
}
function isObject2(arg) {
  return typeof arg === "object" && arg !== null;
}
function isDate2(d) {
  return isObject2(d) && objectToString(d) === "[object Date]";
}
function isError(e) {
  return isObject2(e) && (objectToString(e) === "[object Error]" || e instanceof Error);
}
function isFunction3(arg) {
  return typeof arg === "function";
}
function isPrimitive(arg) {
  return arg === null || typeof arg === "boolean" || typeof arg === "number" || typeof arg === "string" || typeof arg === "symbol" || typeof arg > "u";
}
function isBuffer2(arg) {
  return arg instanceof Buffer;
}
function objectToString(o) {
  return Object.prototype.toString.call(o);
}
function pad(n) {
  return n < 10 ? "0" + n.toString(10) : n.toString(10);
}
function timestamp() {
  var d = new Date, time = [pad(d.getHours()), pad(d.getMinutes()), pad(d.getSeconds())].join(":");
  return [d.getDate(), months[d.getMonth()], time].join(" ");
}
function log2(...args) {
  console.log("%s - %s", timestamp(), format.apply(null, args));
}
function inherits2(ctor, superCtor) {
  if (superCtor)
    ctor.super_ = superCtor, ctor.prototype = Object.create(superCtor.prototype, { constructor: { value: ctor, enumerable: false, writable: true, configurable: true } });
}
function _extend(origin2, add) {
  if (!add || !isObject2(add))
    return origin2;
  var keys = Object.keys(add), i = keys.length;
  while (i--)
    origin2[keys[i]] = add[keys[i]];
  return origin2;
}
function hasOwnProperty2(obj, prop) {
  return Object.prototype.hasOwnProperty.call(obj, prop);
}
function callbackifyOnRejected(reason, cb) {
  if (!reason) {
    var newReason = Error("Promise was rejected with a falsy value");
    newReason.reason = reason, reason = newReason;
  }
  return cb(reason);
}
function callbackify(original) {
  if (typeof original !== "function")
    throw TypeError('The "original" argument must be of type Function');
  function callbackified(...args) {
    var maybeCb = args.pop();
    if (typeof maybeCb !== "function")
      throw TypeError("The last argument must be of type Function");
    var self2 = this, cb = function(...args2) {
      return maybeCb.apply(self2, ...args2);
    };
    original.apply(this, args).then(function(ret) {
      process.nextTick(cb.bind(null, null, ret));
    }, function(rej) {
      process.nextTick(callbackifyOnRejected.bind(null, rej, cb));
    });
  }
  return Object.setPrototypeOf(callbackified, Object.getPrototypeOf(original)), Object.defineProperties(callbackified, Object.getOwnPropertyDescriptors(original)), callbackified;
}
var formatRegExp, debuglog, inspect, types = () => {}, months, promisify, TextEncoder3, TextDecoder2, util_default;
var init_util = __esm(() => {
  formatRegExp = /%[sdj%]/g;
  debuglog = ((debugs = {}, debugEnvRegex = {}, debugEnv) => ((debugEnv = typeof process < "u" && false) && (debugEnv = debugEnv.replace(/[|\\{}()[\]^$+?.]/g, "\\$&").replace(/\*/g, ".*").replace(/,/g, "$|^").toUpperCase()), debugEnvRegex = new RegExp("^" + debugEnv + "$", "i"), (set) => {
    if (set = set.toUpperCase(), !debugs[set])
      if (debugEnvRegex.test(set))
        debugs[set] = function(...args) {
          console.error("%s: %s", set, pid, format.apply(null, ...args));
        };
      else
        debugs[set] = function() {};
    return debugs[set];
  }))();
  inspect = ((i) => (i.colors = { bold: [1, 22], italic: [3, 23], underline: [4, 24], inverse: [7, 27], white: [37, 39], grey: [90, 39], black: [30, 39], blue: [34, 39], cyan: [36, 39], green: [32, 39], magenta: [35, 39], red: [31, 39], yellow: [33, 39] }, i.styles = { special: "cyan", number: "yellow", boolean: "yellow", undefined: "grey", null: "bold", string: "green", date: "magenta", regexp: "red" }, i.custom = Symbol.for("nodejs.util.inspect.custom"), i))(function(obj, opts, ...rest) {
    var ctx = { seen: [], stylize: stylizeNoColor };
    if (rest.length >= 1)
      ctx.depth = rest[0];
    if (rest.length >= 2)
      ctx.colors = rest[1];
    if (isBoolean2(opts))
      ctx.showHidden = opts;
    else if (opts)
      _extend(ctx, opts);
    if (isUndefined2(ctx.showHidden))
      ctx.showHidden = false;
    if (isUndefined2(ctx.depth))
      ctx.depth = 2;
    if (isUndefined2(ctx.colors))
      ctx.colors = false;
    if (ctx.colors)
      ctx.stylize = stylizeWithColor;
    return formatValue(ctx, obj, ctx.depth);
  });
  months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  promisify = ((x) => (x.custom = Symbol.for("nodejs.util.promisify.custom"), x))(function(original) {
    if (typeof original !== "function")
      throw TypeError('The "original" argument must be of type Function');
    if (kCustomPromisifiedSymbol && original[kCustomPromisifiedSymbol]) {
      var fn = original[kCustomPromisifiedSymbol];
      if (typeof fn !== "function")
        throw TypeError('The "nodejs.util.promisify.custom" argument must be of type Function');
      return Object.defineProperty(fn, kCustomPromisifiedSymbol, { value: fn, enumerable: false, writable: false, configurable: true }), fn;
    }
    function fn(...args) {
      var promiseResolve, promiseReject, promise = new Promise(function(resolve, reject) {
        promiseResolve = resolve, promiseReject = reject;
      });
      args.push(function(err, value) {
        if (err)
          promiseReject(err);
        else
          promiseResolve(value);
      });
      try {
        original.apply(this, args);
      } catch (err) {
        promiseReject(err);
      }
      return promise;
    }
    if (Object.setPrototypeOf(fn, Object.getPrototypeOf(original)), kCustomPromisifiedSymbol)
      Object.defineProperty(fn, kCustomPromisifiedSymbol, { value: fn, enumerable: false, writable: false, configurable: true });
    return Object.defineProperties(fn, Object.getOwnPropertyDescriptors(original));
  });
  ({ TextEncoder: TextEncoder3, TextDecoder: TextDecoder2 } = globalThis);
  util_default = { TextEncoder: TextEncoder3, TextDecoder: TextDecoder2, promisify, log: log2, inherits: inherits2, _extend, callbackifyOnRejected, callbackify };
});

// node:buffer
var exports_buffer = {};
__export(exports_buffer, {
  transcode: () => transcode,
  resolveObjectURL: () => resolveObjectURL,
  kStringMaxLength: () => kStringMaxLength,
  kMaxLength: () => kMaxLength,
  isUtf8: () => isUtf8,
  isAscii: () => isAscii,
  default: () => buffer_default,
  constants: () => constants,
  btoa: () => btoa2,
  atob: () => atob,
  INSPECT_MAX_BYTES: () => INSPECT_MAX_BYTES,
  File: () => File,
  Buffer: () => Buffer2,
  Blob: () => Blob2
});
function getLens(b64) {
  var len2 = b64.length;
  if (len2 % 4 > 0)
    throw Error("Invalid string. Length must be a multiple of 4");
  var validLen = b64.indexOf("=");
  if (validLen === -1)
    validLen = len2;
  var placeHoldersLen = validLen === len2 ? 0 : 4 - validLen % 4;
  return [validLen, placeHoldersLen];
}
function _byteLength(validLen, placeHoldersLen) {
  return (validLen + placeHoldersLen) * 3 / 4 - placeHoldersLen;
}
function toByteArray(b64) {
  var tmp, lens = getLens(b64), validLen = lens[0], placeHoldersLen = lens[1], arr = new Uint8Array(_byteLength(validLen, placeHoldersLen)), curByte = 0, len2 = placeHoldersLen > 0 ? validLen - 4 : validLen, i2;
  for (i2 = 0;i2 < len2; i2 += 4)
    tmp = revLookup[b64.charCodeAt(i2)] << 18 | revLookup[b64.charCodeAt(i2 + 1)] << 12 | revLookup[b64.charCodeAt(i2 + 2)] << 6 | revLookup[b64.charCodeAt(i2 + 3)], arr[curByte++] = tmp >> 16 & 255, arr[curByte++] = tmp >> 8 & 255, arr[curByte++] = tmp & 255;
  if (placeHoldersLen === 2)
    tmp = revLookup[b64.charCodeAt(i2)] << 2 | revLookup[b64.charCodeAt(i2 + 1)] >> 4, arr[curByte++] = tmp & 255;
  if (placeHoldersLen === 1)
    tmp = revLookup[b64.charCodeAt(i2)] << 10 | revLookup[b64.charCodeAt(i2 + 1)] << 4 | revLookup[b64.charCodeAt(i2 + 2)] >> 2, arr[curByte++] = tmp >> 8 & 255, arr[curByte++] = tmp & 255;
  return arr;
}
function tripletToBase64(num) {
  return lookup[num >> 18 & 63] + lookup[num >> 12 & 63] + lookup[num >> 6 & 63] + lookup[num & 63];
}
function encodeChunk(uint8, start, end) {
  var tmp, output = [];
  for (var i2 = start;i2 < end; i2 += 3)
    tmp = (uint8[i2] << 16 & 16711680) + (uint8[i2 + 1] << 8 & 65280) + (uint8[i2 + 2] & 255), output.push(tripletToBase64(tmp));
  return output.join("");
}
function fromByteArray(uint8) {
  var tmp, len2 = uint8.length, extraBytes = len2 % 3, parts = [], maxChunkLength = 16383;
  for (var i2 = 0, len22 = len2 - extraBytes;i2 < len22; i2 += maxChunkLength)
    parts.push(encodeChunk(uint8, i2, i2 + maxChunkLength > len22 ? len22 : i2 + maxChunkLength));
  if (extraBytes === 1)
    tmp = uint8[len2 - 1], parts.push(lookup[tmp >> 2] + lookup[tmp << 4 & 63] + "==");
  else if (extraBytes === 2)
    tmp = (uint8[len2 - 2] << 8) + uint8[len2 - 1], parts.push(lookup[tmp >> 10] + lookup[tmp >> 4 & 63] + lookup[tmp << 2 & 63] + "=");
  return parts.join("");
}
function read(buffer, offset, isLE, mLen, nBytes) {
  var e, m, eLen = nBytes * 8 - mLen - 1, eMax = (1 << eLen) - 1, eBias = eMax >> 1, nBits = -7, i2 = isLE ? nBytes - 1 : 0, d = isLE ? -1 : 1, s = buffer[offset + i2];
  i2 += d, e = s & (1 << -nBits) - 1, s >>= -nBits, nBits += eLen;
  for (;nBits > 0; e = e * 256 + buffer[offset + i2], i2 += d, nBits -= 8)
    ;
  m = e & (1 << -nBits) - 1, e >>= -nBits, nBits += mLen;
  for (;nBits > 0; m = m * 256 + buffer[offset + i2], i2 += d, nBits -= 8)
    ;
  if (e === 0)
    e = 1 - eBias;
  else if (e === eMax)
    return m ? NaN : (s ? -1 : 1) * (1 / 0);
  else
    m = m + Math.pow(2, mLen), e = e - eBias;
  return (s ? -1 : 1) * m * Math.pow(2, e - mLen);
}
function write(buffer, value, offset, isLE, mLen, nBytes) {
  var e, m, c, eLen = nBytes * 8 - mLen - 1, eMax = (1 << eLen) - 1, eBias = eMax >> 1, rt = mLen === 23 ? Math.pow(2, -24) - Math.pow(2, -77) : 0, i2 = isLE ? 0 : nBytes - 1, d = isLE ? 1 : -1, s = value < 0 || value === 0 && 1 / value < 0 ? 1 : 0;
  if (value = Math.abs(value), isNaN(value) || value === 1 / 0)
    m = isNaN(value) ? 1 : 0, e = eMax;
  else {
    if (e = Math.floor(Math.log(value) / Math.LN2), value * (c = Math.pow(2, -e)) < 1)
      e--, c *= 2;
    if (e + eBias >= 1)
      value += rt / c;
    else
      value += rt * Math.pow(2, 1 - eBias);
    if (value * c >= 2)
      e++, c /= 2;
    if (e + eBias >= eMax)
      m = 0, e = eMax;
    else if (e + eBias >= 1)
      m = (value * c - 1) * Math.pow(2, mLen), e = e + eBias;
    else
      m = value * Math.pow(2, eBias - 1) * Math.pow(2, mLen), e = 0;
  }
  for (;mLen >= 8; buffer[offset + i2] = m & 255, i2 += d, m /= 256, mLen -= 8)
    ;
  e = e << mLen | m, eLen += mLen;
  for (;eLen > 0; buffer[offset + i2] = e & 255, i2 += d, e /= 256, eLen -= 8)
    ;
  buffer[offset + i2 - d] |= s * 128;
}
function createBuffer(length) {
  if (length > kMaxLength)
    throw RangeError('The value "' + length + '" is invalid for option "size"');
  let buf = new Uint8Array(length);
  return Object.setPrototypeOf(buf, Buffer2.prototype), buf;
}
function E(sym, getMessage, Base) {
  return class extends Base {
    constructor() {
      super();
      Object.defineProperty(this, "message", { value: getMessage.apply(this, arguments), writable: true, configurable: true }), this.name = `${this.name} [${sym}]`, this.stack, delete this.name;
    }
    get code() {
      return sym;
    }
    set code(value) {
      Object.defineProperty(this, "code", { configurable: true, enumerable: true, value, writable: true });
    }
    toString() {
      return `${this.name} [${sym}]: ${this.message}`;
    }
  };
}
function Buffer2(arg, encodingOrOffset, length) {
  if (typeof arg === "number") {
    if (typeof encodingOrOffset === "string")
      throw TypeError('The "string" argument must be of type string. Received type number');
    return allocUnsafe(arg);
  }
  return from(arg, encodingOrOffset, length);
}
function from(value, encodingOrOffset, length) {
  if (typeof value === "string")
    return fromString(value, encodingOrOffset);
  if (ArrayBuffer.isView(value))
    return fromArrayView(value);
  if (value == null)
    throw TypeError("The first argument must be one of type string, Buffer, ArrayBuffer, Array, or Array-like Object. Received type " + typeof value);
  if (isInstance(value, ArrayBuffer) || value && isInstance(value.buffer, ArrayBuffer))
    return fromArrayBuffer(value, encodingOrOffset, length);
  if (typeof SharedArrayBuffer < "u" && (isInstance(value, SharedArrayBuffer) || value && isInstance(value.buffer, SharedArrayBuffer)))
    return fromArrayBuffer(value, encodingOrOffset, length);
  if (typeof value === "number")
    throw TypeError('The "value" argument must not be of type number. Received type number');
  let valueOf = value.valueOf && value.valueOf();
  if (valueOf != null && valueOf !== value)
    return Buffer2.from(valueOf, encodingOrOffset, length);
  let b = fromObject(value);
  if (b)
    return b;
  if (typeof Symbol < "u" && Symbol.toPrimitive != null && typeof value[Symbol.toPrimitive] === "function")
    return Buffer2.from(value[Symbol.toPrimitive]("string"), encodingOrOffset, length);
  throw TypeError("The first argument must be one of type string, Buffer, ArrayBuffer, Array, or Array-like Object. Received type " + typeof value);
}
function assertSize(size) {
  if (typeof size !== "number")
    throw TypeError('"size" argument must be of type number');
  else if (size < 0)
    throw RangeError('The value "' + size + '" is invalid for option "size"');
}
function alloc(size, fill, encoding) {
  if (assertSize(size), size <= 0)
    return createBuffer(size);
  if (fill !== undefined)
    return typeof encoding === "string" ? createBuffer(size).fill(fill, encoding) : createBuffer(size).fill(fill);
  return createBuffer(size);
}
function allocUnsafe(size) {
  return assertSize(size), createBuffer(size < 0 ? 0 : checked(size) | 0);
}
function fromString(string, encoding) {
  if (typeof encoding !== "string" || encoding === "")
    encoding = "utf8";
  if (!Buffer2.isEncoding(encoding))
    throw TypeError("Unknown encoding: " + encoding);
  let length = byteLength(string, encoding) | 0, buf = createBuffer(length), actual = buf.write(string, encoding);
  if (actual !== length)
    buf = buf.slice(0, actual);
  return buf;
}
function fromArrayLike(array) {
  let length = array.length < 0 ? 0 : checked(array.length) | 0, buf = createBuffer(length);
  for (let i2 = 0;i2 < length; i2 += 1)
    buf[i2] = array[i2] & 255;
  return buf;
}
function fromArrayView(arrayView) {
  if (isInstance(arrayView, Uint8Array)) {
    let copy = new Uint8Array(arrayView);
    return fromArrayBuffer(copy.buffer, copy.byteOffset, copy.byteLength);
  }
  return fromArrayLike(arrayView);
}
function fromArrayBuffer(array, byteOffset, length) {
  if (byteOffset < 0 || array.byteLength < byteOffset)
    throw RangeError('"offset" is outside of buffer bounds');
  if (array.byteLength < byteOffset + (length || 0))
    throw RangeError('"length" is outside of buffer bounds');
  let buf;
  if (byteOffset === undefined && length === undefined)
    buf = new Uint8Array(array);
  else if (length === undefined)
    buf = new Uint8Array(array, byteOffset);
  else
    buf = new Uint8Array(array, byteOffset, length);
  return Object.setPrototypeOf(buf, Buffer2.prototype), buf;
}
function fromObject(obj) {
  if (Buffer2.isBuffer(obj)) {
    let len2 = checked(obj.length) | 0, buf = createBuffer(len2);
    if (buf.length === 0)
      return buf;
    return obj.copy(buf, 0, 0, len2), buf;
  }
  if (obj.length !== undefined) {
    if (typeof obj.length !== "number" || Number.isNaN(obj.length))
      return createBuffer(0);
    return fromArrayLike(obj);
  }
  if (obj.type === "Buffer" && Array.isArray(obj.data))
    return fromArrayLike(obj.data);
}
function checked(length) {
  if (length >= kMaxLength)
    throw RangeError("Attempt to allocate Buffer larger than maximum size: 0x" + kMaxLength.toString(16) + " bytes");
  return length | 0;
}
function byteLength(string, encoding) {
  if (Buffer2.isBuffer(string))
    return string.length;
  if (ArrayBuffer.isView(string) || isInstance(string, ArrayBuffer))
    return string.byteLength;
  if (typeof string !== "string")
    throw TypeError('The "string" argument must be one of type string, Buffer, or ArrayBuffer. Received type ' + typeof string);
  let len2 = string.length, mustMatch = arguments.length > 2 && arguments[2] === true;
  if (!mustMatch && len2 === 0)
    return 0;
  let loweredCase = false;
  for (;; )
    switch (encoding) {
      case "ascii":
      case "latin1":
      case "binary":
        return len2;
      case "utf8":
      case "utf-8":
        return utf8ToBytes(string).length;
      case "ucs2":
      case "ucs-2":
      case "utf16le":
      case "utf-16le":
        return len2 * 2;
      case "hex":
        return len2 >>> 1;
      case "base64":
        return base64ToBytes(string).length;
      default:
        if (loweredCase)
          return mustMatch ? -1 : utf8ToBytes(string).length;
        encoding = ("" + encoding).toLowerCase(), loweredCase = true;
    }
}
function slowToString(encoding, start, end) {
  let loweredCase = false;
  if (start === undefined || start < 0)
    start = 0;
  if (start > this.length)
    return "";
  if (end === undefined || end > this.length)
    end = this.length;
  if (end <= 0)
    return "";
  if (end >>>= 0, start >>>= 0, end <= start)
    return "";
  if (!encoding)
    encoding = "utf8";
  while (true)
    switch (encoding) {
      case "hex":
        return hexSlice(this, start, end);
      case "utf8":
      case "utf-8":
        return utf8Slice(this, start, end);
      case "ascii":
        return asciiSlice(this, start, end);
      case "latin1":
      case "binary":
        return latin1Slice(this, start, end);
      case "base64":
        return base64Slice(this, start, end);
      case "ucs2":
      case "ucs-2":
      case "utf16le":
      case "utf-16le":
        return utf16leSlice(this, start, end);
      default:
        if (loweredCase)
          throw TypeError("Unknown encoding: " + encoding);
        encoding = (encoding + "").toLowerCase(), loweredCase = true;
    }
}
function swap(b, n, m) {
  let i2 = b[n];
  b[n] = b[m], b[m] = i2;
}
function bidirectionalIndexOf(buffer, val, byteOffset, encoding, dir) {
  if (buffer.length === 0)
    return -1;
  if (typeof byteOffset === "string")
    encoding = byteOffset, byteOffset = 0;
  else if (byteOffset > 2147483647)
    byteOffset = 2147483647;
  else if (byteOffset < -2147483648)
    byteOffset = -2147483648;
  if (byteOffset = +byteOffset, Number.isNaN(byteOffset))
    byteOffset = dir ? 0 : buffer.length - 1;
  if (byteOffset < 0)
    byteOffset = buffer.length + byteOffset;
  if (byteOffset >= buffer.length)
    if (dir)
      return -1;
    else
      byteOffset = buffer.length - 1;
  else if (byteOffset < 0)
    if (dir)
      byteOffset = 0;
    else
      return -1;
  if (typeof val === "string")
    val = Buffer2.from(val, encoding);
  if (Buffer2.isBuffer(val)) {
    if (val.length === 0)
      return -1;
    return arrayIndexOf(buffer, val, byteOffset, encoding, dir);
  } else if (typeof val === "number") {
    if (val = val & 255, typeof Uint8Array.prototype.indexOf === "function")
      if (dir)
        return Uint8Array.prototype.indexOf.call(buffer, val, byteOffset);
      else
        return Uint8Array.prototype.lastIndexOf.call(buffer, val, byteOffset);
    return arrayIndexOf(buffer, [val], byteOffset, encoding, dir);
  }
  throw TypeError("val must be string, number or Buffer");
}
function arrayIndexOf(arr, val, byteOffset, encoding, dir) {
  let indexSize = 1, arrLength = arr.length, valLength = val.length;
  if (encoding !== undefined) {
    if (encoding = String(encoding).toLowerCase(), encoding === "ucs2" || encoding === "ucs-2" || encoding === "utf16le" || encoding === "utf-16le") {
      if (arr.length < 2 || val.length < 2)
        return -1;
      indexSize = 2, arrLength /= 2, valLength /= 2, byteOffset /= 2;
    }
  }
  function read2(buf, i3) {
    if (indexSize === 1)
      return buf[i3];
    else
      return buf.readUInt16BE(i3 * indexSize);
  }
  let i2;
  if (dir) {
    let foundIndex = -1;
    for (i2 = byteOffset;i2 < arrLength; i2++)
      if (read2(arr, i2) === read2(val, foundIndex === -1 ? 0 : i2 - foundIndex)) {
        if (foundIndex === -1)
          foundIndex = i2;
        if (i2 - foundIndex + 1 === valLength)
          return foundIndex * indexSize;
      } else {
        if (foundIndex !== -1)
          i2 -= i2 - foundIndex;
        foundIndex = -1;
      }
  } else {
    if (byteOffset + valLength > arrLength)
      byteOffset = arrLength - valLength;
    for (i2 = byteOffset;i2 >= 0; i2--) {
      let found = true;
      for (let j = 0;j < valLength; j++)
        if (read2(arr, i2 + j) !== read2(val, j)) {
          found = false;
          break;
        }
      if (found)
        return i2;
    }
  }
  return -1;
}
function hexWrite(buf, string, offset, length) {
  offset = Number(offset) || 0;
  let remaining = buf.length - offset;
  if (!length)
    length = remaining;
  else if (length = Number(length), length > remaining)
    length = remaining;
  let strLen = string.length;
  if (length > strLen / 2)
    length = strLen / 2;
  let i2;
  for (i2 = 0;i2 < length; ++i2) {
    let parsed = parseInt(string.substr(i2 * 2, 2), 16);
    if (Number.isNaN(parsed))
      return i2;
    buf[offset + i2] = parsed;
  }
  return i2;
}
function utf8Write(buf, string, offset, length) {
  return blitBuffer(utf8ToBytes(string, buf.length - offset), buf, offset, length);
}
function asciiWrite(buf, string, offset, length) {
  return blitBuffer(asciiToBytes(string), buf, offset, length);
}
function base64Write(buf, string, offset, length) {
  return blitBuffer(base64ToBytes(string), buf, offset, length);
}
function ucs2Write(buf, string, offset, length) {
  return blitBuffer(utf16leToBytes(string, buf.length - offset), buf, offset, length);
}
function base64Slice(buf, start, end) {
  if (start === 0 && end === buf.length)
    return fromByteArray(buf);
  else
    return fromByteArray(buf.slice(start, end));
}
function utf8Slice(buf, start, end) {
  end = Math.min(buf.length, end);
  let res = [], i2 = start;
  while (i2 < end) {
    let firstByte = buf[i2], codePoint = null, bytesPerSequence = firstByte > 239 ? 4 : firstByte > 223 ? 3 : firstByte > 191 ? 2 : 1;
    if (i2 + bytesPerSequence <= end) {
      let secondByte, thirdByte, fourthByte, tempCodePoint;
      switch (bytesPerSequence) {
        case 1:
          if (firstByte < 128)
            codePoint = firstByte;
          break;
        case 2:
          if (secondByte = buf[i2 + 1], (secondByte & 192) === 128) {
            if (tempCodePoint = (firstByte & 31) << 6 | secondByte & 63, tempCodePoint > 127)
              codePoint = tempCodePoint;
          }
          break;
        case 3:
          if (secondByte = buf[i2 + 1], thirdByte = buf[i2 + 2], (secondByte & 192) === 128 && (thirdByte & 192) === 128) {
            if (tempCodePoint = (firstByte & 15) << 12 | (secondByte & 63) << 6 | thirdByte & 63, tempCodePoint > 2047 && (tempCodePoint < 55296 || tempCodePoint > 57343))
              codePoint = tempCodePoint;
          }
          break;
        case 4:
          if (secondByte = buf[i2 + 1], thirdByte = buf[i2 + 2], fourthByte = buf[i2 + 3], (secondByte & 192) === 128 && (thirdByte & 192) === 128 && (fourthByte & 192) === 128) {
            if (tempCodePoint = (firstByte & 15) << 18 | (secondByte & 63) << 12 | (thirdByte & 63) << 6 | fourthByte & 63, tempCodePoint > 65535 && tempCodePoint < 1114112)
              codePoint = tempCodePoint;
          }
      }
    }
    if (codePoint === null)
      codePoint = 65533, bytesPerSequence = 1;
    else if (codePoint > 65535)
      codePoint -= 65536, res.push(codePoint >>> 10 & 1023 | 55296), codePoint = 56320 | codePoint & 1023;
    res.push(codePoint), i2 += bytesPerSequence;
  }
  return decodeCodePointsArray(res);
}
function decodeCodePointsArray(codePoints) {
  let len2 = codePoints.length;
  if (len2 <= MAX_ARGUMENTS_LENGTH)
    return String.fromCharCode.apply(String, codePoints);
  let res = "", i2 = 0;
  while (i2 < len2)
    res += String.fromCharCode.apply(String, codePoints.slice(i2, i2 += MAX_ARGUMENTS_LENGTH));
  return res;
}
function asciiSlice(buf, start, end) {
  let ret = "";
  end = Math.min(buf.length, end);
  for (let i2 = start;i2 < end; ++i2)
    ret += String.fromCharCode(buf[i2] & 127);
  return ret;
}
function latin1Slice(buf, start, end) {
  let ret = "";
  end = Math.min(buf.length, end);
  for (let i2 = start;i2 < end; ++i2)
    ret += String.fromCharCode(buf[i2]);
  return ret;
}
function hexSlice(buf, start, end) {
  let len2 = buf.length;
  if (!start || start < 0)
    start = 0;
  if (!end || end < 0 || end > len2)
    end = len2;
  let out = "";
  for (let i2 = start;i2 < end; ++i2)
    out += hexSliceLookupTable[buf[i2]];
  return out;
}
function utf16leSlice(buf, start, end) {
  let bytes = buf.slice(start, end), res = "";
  for (let i2 = 0;i2 < bytes.length - 1; i2 += 2)
    res += String.fromCharCode(bytes[i2] + bytes[i2 + 1] * 256);
  return res;
}
function checkOffset(offset, ext, length) {
  if (offset % 1 !== 0 || offset < 0)
    throw RangeError("offset is not uint");
  if (offset + ext > length)
    throw RangeError("Trying to access beyond buffer length");
}
function checkInt(buf, value, offset, ext, max, min) {
  if (!Buffer2.isBuffer(buf))
    throw TypeError('"buffer" argument must be a Buffer instance');
  if (value > max || value < min)
    throw RangeError('"value" argument is out of bounds');
  if (offset + ext > buf.length)
    throw RangeError("Index out of range");
}
function wrtBigUInt64LE(buf, value, offset, min, max) {
  checkIntBI(value, min, max, buf, offset, 7);
  let lo = Number(value & BigInt(4294967295));
  buf[offset++] = lo, lo = lo >> 8, buf[offset++] = lo, lo = lo >> 8, buf[offset++] = lo, lo = lo >> 8, buf[offset++] = lo;
  let hi = Number(value >> BigInt(32) & BigInt(4294967295));
  return buf[offset++] = hi, hi = hi >> 8, buf[offset++] = hi, hi = hi >> 8, buf[offset++] = hi, hi = hi >> 8, buf[offset++] = hi, offset;
}
function wrtBigUInt64BE(buf, value, offset, min, max) {
  checkIntBI(value, min, max, buf, offset, 7);
  let lo = Number(value & BigInt(4294967295));
  buf[offset + 7] = lo, lo = lo >> 8, buf[offset + 6] = lo, lo = lo >> 8, buf[offset + 5] = lo, lo = lo >> 8, buf[offset + 4] = lo;
  let hi = Number(value >> BigInt(32) & BigInt(4294967295));
  return buf[offset + 3] = hi, hi = hi >> 8, buf[offset + 2] = hi, hi = hi >> 8, buf[offset + 1] = hi, hi = hi >> 8, buf[offset] = hi, offset + 8;
}
function checkIEEE754(buf, value, offset, ext, max, min) {
  if (offset + ext > buf.length)
    throw RangeError("Index out of range");
  if (offset < 0)
    throw RangeError("Index out of range");
}
function writeFloat(buf, value, offset, littleEndian, noAssert) {
  if (value = +value, offset = offset >>> 0, !noAssert)
    checkIEEE754(buf, value, offset, 4, 340282346638528860000000000000000000000, -340282346638528860000000000000000000000);
  return write(buf, value, offset, littleEndian, 23, 4), offset + 4;
}
function writeDouble(buf, value, offset, littleEndian, noAssert) {
  if (value = +value, offset = offset >>> 0, !noAssert)
    checkIEEE754(buf, value, offset, 8, 179769313486231570000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000, -179769313486231570000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000);
  return write(buf, value, offset, littleEndian, 52, 8), offset + 8;
}
function addNumericalSeparator(val) {
  let res = "", i2 = val.length, start = val[0] === "-" ? 1 : 0;
  for (;i2 >= start + 4; i2 -= 3)
    res = `_${val.slice(i2 - 3, i2)}${res}`;
  return `${val.slice(0, i2)}${res}`;
}
function checkBounds(buf, offset, byteLength2) {
  if (validateNumber(offset, "offset"), buf[offset] === undefined || buf[offset + byteLength2] === undefined)
    boundsError(offset, buf.length - (byteLength2 + 1));
}
function checkIntBI(value, min, max, buf, offset, byteLength2) {
  if (value > max || value < min) {
    let n = typeof min === "bigint" ? "n" : "", range;
    if (byteLength2 > 3)
      if (min === 0 || min === BigInt(0))
        range = `>= 0${n} and < 2${n} ** ${(byteLength2 + 1) * 8}${n}`;
      else
        range = `>= -(2${n} ** ${(byteLength2 + 1) * 8 - 1}${n}) and < 2 ** ${(byteLength2 + 1) * 8 - 1}${n}`;
    else
      range = `>= ${min}${n} and <= ${max}${n}`;
    throw new ERR_OUT_OF_RANGE("value", range, value);
  }
  checkBounds(buf, offset, byteLength2);
}
function validateNumber(value, name) {
  if (typeof value !== "number")
    throw new ERR_INVALID_ARG_TYPE(name, "number", value);
}
function boundsError(value, length, type) {
  if (Math.floor(value) !== value)
    throw validateNumber(value, type), new ERR_OUT_OF_RANGE(type || "offset", "an integer", value);
  if (length < 0)
    throw new ERR_BUFFER_OUT_OF_BOUNDS;
  throw new ERR_OUT_OF_RANGE(type || "offset", `>= ${type ? 1 : 0} and <= ${length}`, value);
}
function base64clean(str) {
  if (str = str.split("=")[0], str = str.trim().replace(INVALID_BASE64_RE, ""), str.length < 2)
    return "";
  while (str.length % 4 !== 0)
    str = str + "=";
  return str;
}
function utf8ToBytes(string, units) {
  units = units || 1 / 0;
  let codePoint, length = string.length, leadSurrogate = null, bytes = [];
  for (let i2 = 0;i2 < length; ++i2) {
    if (codePoint = string.charCodeAt(i2), codePoint > 55295 && codePoint < 57344) {
      if (!leadSurrogate) {
        if (codePoint > 56319) {
          if ((units -= 3) > -1)
            bytes.push(239, 191, 189);
          continue;
        } else if (i2 + 1 === length) {
          if ((units -= 3) > -1)
            bytes.push(239, 191, 189);
          continue;
        }
        leadSurrogate = codePoint;
        continue;
      }
      if (codePoint < 56320) {
        if ((units -= 3) > -1)
          bytes.push(239, 191, 189);
        leadSurrogate = codePoint;
        continue;
      }
      codePoint = (leadSurrogate - 55296 << 10 | codePoint - 56320) + 65536;
    } else if (leadSurrogate) {
      if ((units -= 3) > -1)
        bytes.push(239, 191, 189);
    }
    if (leadSurrogate = null, codePoint < 128) {
      if ((units -= 1) < 0)
        break;
      bytes.push(codePoint);
    } else if (codePoint < 2048) {
      if ((units -= 2) < 0)
        break;
      bytes.push(codePoint >> 6 | 192, codePoint & 63 | 128);
    } else if (codePoint < 65536) {
      if ((units -= 3) < 0)
        break;
      bytes.push(codePoint >> 12 | 224, codePoint >> 6 & 63 | 128, codePoint & 63 | 128);
    } else if (codePoint < 1114112) {
      if ((units -= 4) < 0)
        break;
      bytes.push(codePoint >> 18 | 240, codePoint >> 12 & 63 | 128, codePoint >> 6 & 63 | 128, codePoint & 63 | 128);
    } else
      throw Error("Invalid code point");
  }
  return bytes;
}
function asciiToBytes(str) {
  let byteArray = [];
  for (let i2 = 0;i2 < str.length; ++i2)
    byteArray.push(str.charCodeAt(i2) & 255);
  return byteArray;
}
function utf16leToBytes(str, units) {
  let c, hi, lo, byteArray = [];
  for (let i2 = 0;i2 < str.length; ++i2) {
    if ((units -= 2) < 0)
      break;
    c = str.charCodeAt(i2), hi = c >> 8, lo = c % 256, byteArray.push(lo), byteArray.push(hi);
  }
  return byteArray;
}
function base64ToBytes(str) {
  return toByteArray(base64clean(str));
}
function blitBuffer(src, dst, offset, length) {
  let i2;
  for (i2 = 0;i2 < length; ++i2) {
    if (i2 + offset >= dst.length || i2 >= src.length)
      break;
    dst[i2 + offset] = src[i2];
  }
  return i2;
}
function isInstance(obj, type) {
  return obj instanceof type || obj != null && obj.constructor != null && obj.constructor.name != null && obj.constructor.name === type.name;
}
function defineBigIntMethod(fn) {
  return typeof BigInt > "u" ? BufferBigIntNotDefined : fn;
}
function BufferBigIntNotDefined() {
  throw Error("BigInt not supported");
}
function notimpl(name) {
  return () => {
    throw Error(name + " is not implemented for node:buffer browser polyfill");
  };
}
var lookup, revLookup, code = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/", i, len, customInspectSymbol, INSPECT_MAX_BYTES = 50, kMaxLength = 2147483647, kStringMaxLength = 536870888, btoa2, atob, File, Blob2, constants, ERR_BUFFER_OUT_OF_BOUNDS, ERR_INVALID_ARG_TYPE, ERR_OUT_OF_RANGE, MAX_ARGUMENTS_LENGTH = 4096, INVALID_BASE64_RE, hexSliceLookupTable, resolveObjectURL, isUtf8, isAscii = (str) => {
  for (let char of str)
    if (char.charCodeAt(0) > 127)
      return false;
  return true;
}, transcode, buffer_default;
var init_buffer = __esm(() => {
  lookup = [];
  revLookup = [];
  for (i = 0, len = code.length;i < len; ++i)
    lookup[i] = code[i], revLookup[code.charCodeAt(i)] = i;
  revLookup[45] = 62;
  revLookup[95] = 63;
  customInspectSymbol = typeof Symbol === "function" && typeof Symbol.for === "function" ? Symbol.for("nodejs.util.inspect.custom") : null;
  btoa2 = globalThis.btoa;
  atob = globalThis.atob;
  File = globalThis.File;
  Blob2 = globalThis.Blob;
  constants = { MAX_LENGTH: kMaxLength, MAX_STRING_LENGTH: kStringMaxLength };
  ERR_BUFFER_OUT_OF_BOUNDS = E("ERR_BUFFER_OUT_OF_BOUNDS", function(name) {
    if (name)
      return `${name} is outside of buffer bounds`;
    return "Attempt to access memory outside buffer bounds";
  }, RangeError);
  ERR_INVALID_ARG_TYPE = E("ERR_INVALID_ARG_TYPE", function(name, actual) {
    return `The "${name}" argument must be of type number. Received type ${typeof actual}`;
  }, TypeError);
  ERR_OUT_OF_RANGE = E("ERR_OUT_OF_RANGE", function(str, range, input) {
    let msg = `The value of "${str}" is out of range.`, received = input;
    if (Number.isInteger(input) && Math.abs(input) > 4294967296)
      received = addNumericalSeparator(String(input));
    else if (typeof input === "bigint") {
      if (received = String(input), input > BigInt(2) ** BigInt(32) || input < -(BigInt(2) ** BigInt(32)))
        received = addNumericalSeparator(received);
      received += "n";
    }
    return msg += ` It must be ${range}. Received ${received}`, msg;
  }, RangeError);
  Object.defineProperty(Buffer2.prototype, "parent", { enumerable: true, get: function() {
    if (!Buffer2.isBuffer(this))
      return;
    return this.buffer;
  } });
  Object.defineProperty(Buffer2.prototype, "offset", { enumerable: true, get: function() {
    if (!Buffer2.isBuffer(this))
      return;
    return this.byteOffset;
  } });
  Buffer2.poolSize = 8192;
  Buffer2.from = function(value, encodingOrOffset, length) {
    return from(value, encodingOrOffset, length);
  };
  Object.setPrototypeOf(Buffer2.prototype, Uint8Array.prototype);
  Object.setPrototypeOf(Buffer2, Uint8Array);
  Buffer2.alloc = function(size, fill, encoding) {
    return alloc(size, fill, encoding);
  };
  Buffer2.allocUnsafe = function(size) {
    return allocUnsafe(size);
  };
  Buffer2.allocUnsafeSlow = function(size) {
    return allocUnsafe(size);
  };
  Buffer2.isBuffer = function(b) {
    return b != null && b._isBuffer === true && b !== Buffer2.prototype;
  };
  Buffer2.compare = function(a, b) {
    if (isInstance(a, Uint8Array))
      a = Buffer2.from(a, a.offset, a.byteLength);
    if (isInstance(b, Uint8Array))
      b = Buffer2.from(b, b.offset, b.byteLength);
    if (!Buffer2.isBuffer(a) || !Buffer2.isBuffer(b))
      throw TypeError('The "buf1", "buf2" arguments must be one of type Buffer or Uint8Array');
    if (a === b)
      return 0;
    let x = a.length, y = b.length;
    for (let i2 = 0, len2 = Math.min(x, y);i2 < len2; ++i2)
      if (a[i2] !== b[i2]) {
        x = a[i2], y = b[i2];
        break;
      }
    if (x < y)
      return -1;
    if (y < x)
      return 1;
    return 0;
  };
  Buffer2.isEncoding = function(encoding) {
    switch (String(encoding).toLowerCase()) {
      case "hex":
      case "utf8":
      case "utf-8":
      case "ascii":
      case "latin1":
      case "binary":
      case "base64":
      case "ucs2":
      case "ucs-2":
      case "utf16le":
      case "utf-16le":
        return true;
      default:
        return false;
    }
  };
  Buffer2.concat = function(list, length) {
    if (!Array.isArray(list))
      throw TypeError('"list" argument must be an Array of Buffers');
    if (list.length === 0)
      return Buffer2.alloc(0);
    let i2;
    if (length === undefined) {
      length = 0;
      for (i2 = 0;i2 < list.length; ++i2)
        length += list[i2].length;
    }
    let buffer = Buffer2.allocUnsafe(length), pos = 0;
    for (i2 = 0;i2 < list.length; ++i2) {
      let buf = list[i2];
      if (isInstance(buf, Uint8Array))
        if (pos + buf.length > buffer.length) {
          if (!Buffer2.isBuffer(buf))
            buf = Buffer2.from(buf);
          buf.copy(buffer, pos);
        } else
          Uint8Array.prototype.set.call(buffer, buf, pos);
      else if (!Buffer2.isBuffer(buf))
        throw TypeError('"list" argument must be an Array of Buffers');
      else
        buf.copy(buffer, pos);
      pos += buf.length;
    }
    return buffer;
  };
  Buffer2.byteLength = byteLength;
  Buffer2.prototype._isBuffer = true;
  Buffer2.prototype.swap16 = function() {
    let len2 = this.length;
    if (len2 % 2 !== 0)
      throw RangeError("Buffer size must be a multiple of 16-bits");
    for (let i2 = 0;i2 < len2; i2 += 2)
      swap(this, i2, i2 + 1);
    return this;
  };
  Buffer2.prototype.swap32 = function() {
    let len2 = this.length;
    if (len2 % 4 !== 0)
      throw RangeError("Buffer size must be a multiple of 32-bits");
    for (let i2 = 0;i2 < len2; i2 += 4)
      swap(this, i2, i2 + 3), swap(this, i2 + 1, i2 + 2);
    return this;
  };
  Buffer2.prototype.swap64 = function() {
    let len2 = this.length;
    if (len2 % 8 !== 0)
      throw RangeError("Buffer size must be a multiple of 64-bits");
    for (let i2 = 0;i2 < len2; i2 += 8)
      swap(this, i2, i2 + 7), swap(this, i2 + 1, i2 + 6), swap(this, i2 + 2, i2 + 5), swap(this, i2 + 3, i2 + 4);
    return this;
  };
  Buffer2.prototype.toString = function() {
    let length = this.length;
    if (length === 0)
      return "";
    if (arguments.length === 0)
      return utf8Slice(this, 0, length);
    return slowToString.apply(this, arguments);
  };
  Buffer2.prototype.toLocaleString = Buffer2.prototype.toString;
  Buffer2.prototype.equals = function(b) {
    if (!Buffer2.isBuffer(b))
      throw TypeError("Argument must be a Buffer");
    if (this === b)
      return true;
    return Buffer2.compare(this, b) === 0;
  };
  Buffer2.prototype.inspect = function() {
    let str = "", max = INSPECT_MAX_BYTES;
    if (str = this.toString("hex", 0, max).replace(/(.{2})/g, "$1 ").trim(), this.length > max)
      str += " ... ";
    return "<Buffer " + str + ">";
  };
  if (customInspectSymbol)
    Buffer2.prototype[customInspectSymbol] = Buffer2.prototype.inspect;
  Buffer2.prototype.compare = function(target, start, end, thisStart, thisEnd) {
    if (isInstance(target, Uint8Array))
      target = Buffer2.from(target, target.offset, target.byteLength);
    if (!Buffer2.isBuffer(target))
      throw TypeError('The "target" argument must be one of type Buffer or Uint8Array. Received type ' + typeof target);
    if (start === undefined)
      start = 0;
    if (end === undefined)
      end = target ? target.length : 0;
    if (thisStart === undefined)
      thisStart = 0;
    if (thisEnd === undefined)
      thisEnd = this.length;
    if (start < 0 || end > target.length || thisStart < 0 || thisEnd > this.length)
      throw RangeError("out of range index");
    if (thisStart >= thisEnd && start >= end)
      return 0;
    if (thisStart >= thisEnd)
      return -1;
    if (start >= end)
      return 1;
    if (start >>>= 0, end >>>= 0, thisStart >>>= 0, thisEnd >>>= 0, this === target)
      return 0;
    let x = thisEnd - thisStart, y = end - start, len2 = Math.min(x, y), thisCopy = this.slice(thisStart, thisEnd), targetCopy = target.slice(start, end);
    for (let i2 = 0;i2 < len2; ++i2)
      if (thisCopy[i2] !== targetCopy[i2]) {
        x = thisCopy[i2], y = targetCopy[i2];
        break;
      }
    if (x < y)
      return -1;
    if (y < x)
      return 1;
    return 0;
  };
  Buffer2.prototype.includes = function(val, byteOffset, encoding) {
    return this.indexOf(val, byteOffset, encoding) !== -1;
  };
  Buffer2.prototype.indexOf = function(val, byteOffset, encoding) {
    return bidirectionalIndexOf(this, val, byteOffset, encoding, true);
  };
  Buffer2.prototype.lastIndexOf = function(val, byteOffset, encoding) {
    return bidirectionalIndexOf(this, val, byteOffset, encoding, false);
  };
  Buffer2.prototype.write = function(string, offset, length, encoding) {
    if (offset === undefined)
      encoding = "utf8", length = this.length, offset = 0;
    else if (length === undefined && typeof offset === "string")
      encoding = offset, length = this.length, offset = 0;
    else if (isFinite(offset))
      if (offset = offset >>> 0, isFinite(length)) {
        if (length = length >>> 0, encoding === undefined)
          encoding = "utf8";
      } else
        encoding = length, length = undefined;
    else
      throw Error("Buffer.write(string, encoding, offset[, length]) is no longer supported");
    let remaining = this.length - offset;
    if (length === undefined || length > remaining)
      length = remaining;
    if (string.length > 0 && (length < 0 || offset < 0) || offset > this.length)
      throw RangeError("Attempt to write outside buffer bounds");
    if (!encoding)
      encoding = "utf8";
    let loweredCase = false;
    for (;; )
      switch (encoding) {
        case "hex":
          return hexWrite(this, string, offset, length);
        case "utf8":
        case "utf-8":
          return utf8Write(this, string, offset, length);
        case "ascii":
        case "latin1":
        case "binary":
          return asciiWrite(this, string, offset, length);
        case "base64":
          return base64Write(this, string, offset, length);
        case "ucs2":
        case "ucs-2":
        case "utf16le":
        case "utf-16le":
          return ucs2Write(this, string, offset, length);
        default:
          if (loweredCase)
            throw TypeError("Unknown encoding: " + encoding);
          encoding = ("" + encoding).toLowerCase(), loweredCase = true;
      }
  };
  Buffer2.prototype.toJSON = function() {
    return { type: "Buffer", data: Array.prototype.slice.call(this._arr || this, 0) };
  };
  Buffer2.prototype.slice = function(start, end) {
    let len2 = this.length;
    if (start = ~~start, end = end === undefined ? len2 : ~~end, start < 0) {
      if (start += len2, start < 0)
        start = 0;
    } else if (start > len2)
      start = len2;
    if (end < 0) {
      if (end += len2, end < 0)
        end = 0;
    } else if (end > len2)
      end = len2;
    if (end < start)
      end = start;
    let newBuf = this.subarray(start, end);
    return Object.setPrototypeOf(newBuf, Buffer2.prototype), newBuf;
  };
  Buffer2.prototype.readUintLE = Buffer2.prototype.readUIntLE = function(offset, byteLength2, noAssert) {
    if (offset = offset >>> 0, byteLength2 = byteLength2 >>> 0, !noAssert)
      checkOffset(offset, byteLength2, this.length);
    let val = this[offset], mul = 1, i2 = 0;
    while (++i2 < byteLength2 && (mul *= 256))
      val += this[offset + i2] * mul;
    return val;
  };
  Buffer2.prototype.readUintBE = Buffer2.prototype.readUIntBE = function(offset, byteLength2, noAssert) {
    if (offset = offset >>> 0, byteLength2 = byteLength2 >>> 0, !noAssert)
      checkOffset(offset, byteLength2, this.length);
    let val = this[offset + --byteLength2], mul = 1;
    while (byteLength2 > 0 && (mul *= 256))
      val += this[offset + --byteLength2] * mul;
    return val;
  };
  Buffer2.prototype.readUint8 = Buffer2.prototype.readUInt8 = function(offset, noAssert) {
    if (offset = offset >>> 0, !noAssert)
      checkOffset(offset, 1, this.length);
    return this[offset];
  };
  Buffer2.prototype.readUint16LE = Buffer2.prototype.readUInt16LE = function(offset, noAssert) {
    if (offset = offset >>> 0, !noAssert)
      checkOffset(offset, 2, this.length);
    return this[offset] | this[offset + 1] << 8;
  };
  Buffer2.prototype.readUint16BE = Buffer2.prototype.readUInt16BE = function(offset, noAssert) {
    if (offset = offset >>> 0, !noAssert)
      checkOffset(offset, 2, this.length);
    return this[offset] << 8 | this[offset + 1];
  };
  Buffer2.prototype.readUint32LE = Buffer2.prototype.readUInt32LE = function(offset, noAssert) {
    if (offset = offset >>> 0, !noAssert)
      checkOffset(offset, 4, this.length);
    return (this[offset] | this[offset + 1] << 8 | this[offset + 2] << 16) + this[offset + 3] * 16777216;
  };
  Buffer2.prototype.readUint32BE = Buffer2.prototype.readUInt32BE = function(offset, noAssert) {
    if (offset = offset >>> 0, !noAssert)
      checkOffset(offset, 4, this.length);
    return this[offset] * 16777216 + (this[offset + 1] << 16 | this[offset + 2] << 8 | this[offset + 3]);
  };
  Buffer2.prototype.readBigUInt64LE = defineBigIntMethod(function(offset) {
    offset = offset >>> 0, validateNumber(offset, "offset");
    let first = this[offset], last = this[offset + 7];
    if (first === undefined || last === undefined)
      boundsError(offset, this.length - 8);
    let lo = first + this[++offset] * 256 + this[++offset] * 65536 + this[++offset] * 16777216, hi = this[++offset] + this[++offset] * 256 + this[++offset] * 65536 + last * 16777216;
    return BigInt(lo) + (BigInt(hi) << BigInt(32));
  });
  Buffer2.prototype.readBigUInt64BE = defineBigIntMethod(function(offset) {
    offset = offset >>> 0, validateNumber(offset, "offset");
    let first = this[offset], last = this[offset + 7];
    if (first === undefined || last === undefined)
      boundsError(offset, this.length - 8);
    let hi = first * 16777216 + this[++offset] * 65536 + this[++offset] * 256 + this[++offset], lo = this[++offset] * 16777216 + this[++offset] * 65536 + this[++offset] * 256 + last;
    return (BigInt(hi) << BigInt(32)) + BigInt(lo);
  });
  Buffer2.prototype.readIntLE = function(offset, byteLength2, noAssert) {
    if (offset = offset >>> 0, byteLength2 = byteLength2 >>> 0, !noAssert)
      checkOffset(offset, byteLength2, this.length);
    let val = this[offset], mul = 1, i2 = 0;
    while (++i2 < byteLength2 && (mul *= 256))
      val += this[offset + i2] * mul;
    if (mul *= 128, val >= mul)
      val -= Math.pow(2, 8 * byteLength2);
    return val;
  };
  Buffer2.prototype.readIntBE = function(offset, byteLength2, noAssert) {
    if (offset = offset >>> 0, byteLength2 = byteLength2 >>> 0, !noAssert)
      checkOffset(offset, byteLength2, this.length);
    let i2 = byteLength2, mul = 1, val = this[offset + --i2];
    while (i2 > 0 && (mul *= 256))
      val += this[offset + --i2] * mul;
    if (mul *= 128, val >= mul)
      val -= Math.pow(2, 8 * byteLength2);
    return val;
  };
  Buffer2.prototype.readInt8 = function(offset, noAssert) {
    if (offset = offset >>> 0, !noAssert)
      checkOffset(offset, 1, this.length);
    if (!(this[offset] & 128))
      return this[offset];
    return (255 - this[offset] + 1) * -1;
  };
  Buffer2.prototype.readInt16LE = function(offset, noAssert) {
    if (offset = offset >>> 0, !noAssert)
      checkOffset(offset, 2, this.length);
    let val = this[offset] | this[offset + 1] << 8;
    return val & 32768 ? val | 4294901760 : val;
  };
  Buffer2.prototype.readInt16BE = function(offset, noAssert) {
    if (offset = offset >>> 0, !noAssert)
      checkOffset(offset, 2, this.length);
    let val = this[offset + 1] | this[offset] << 8;
    return val & 32768 ? val | 4294901760 : val;
  };
  Buffer2.prototype.readInt32LE = function(offset, noAssert) {
    if (offset = offset >>> 0, !noAssert)
      checkOffset(offset, 4, this.length);
    return this[offset] | this[offset + 1] << 8 | this[offset + 2] << 16 | this[offset + 3] << 24;
  };
  Buffer2.prototype.readInt32BE = function(offset, noAssert) {
    if (offset = offset >>> 0, !noAssert)
      checkOffset(offset, 4, this.length);
    return this[offset] << 24 | this[offset + 1] << 16 | this[offset + 2] << 8 | this[offset + 3];
  };
  Buffer2.prototype.readBigInt64LE = defineBigIntMethod(function(offset) {
    offset = offset >>> 0, validateNumber(offset, "offset");
    let first = this[offset], last = this[offset + 7];
    if (first === undefined || last === undefined)
      boundsError(offset, this.length - 8);
    let val = this[offset + 4] + this[offset + 5] * 256 + this[offset + 6] * 65536 + (last << 24);
    return (BigInt(val) << BigInt(32)) + BigInt(first + this[++offset] * 256 + this[++offset] * 65536 + this[++offset] * 16777216);
  });
  Buffer2.prototype.readBigInt64BE = defineBigIntMethod(function(offset) {
    offset = offset >>> 0, validateNumber(offset, "offset");
    let first = this[offset], last = this[offset + 7];
    if (first === undefined || last === undefined)
      boundsError(offset, this.length - 8);
    let val = (first << 24) + this[++offset] * 65536 + this[++offset] * 256 + this[++offset];
    return (BigInt(val) << BigInt(32)) + BigInt(this[++offset] * 16777216 + this[++offset] * 65536 + this[++offset] * 256 + last);
  });
  Buffer2.prototype.readFloatLE = function(offset, noAssert) {
    if (offset = offset >>> 0, !noAssert)
      checkOffset(offset, 4, this.length);
    return read(this, offset, true, 23, 4);
  };
  Buffer2.prototype.readFloatBE = function(offset, noAssert) {
    if (offset = offset >>> 0, !noAssert)
      checkOffset(offset, 4, this.length);
    return read(this, offset, false, 23, 4);
  };
  Buffer2.prototype.readDoubleLE = function(offset, noAssert) {
    if (offset = offset >>> 0, !noAssert)
      checkOffset(offset, 8, this.length);
    return read(this, offset, true, 52, 8);
  };
  Buffer2.prototype.readDoubleBE = function(offset, noAssert) {
    if (offset = offset >>> 0, !noAssert)
      checkOffset(offset, 8, this.length);
    return read(this, offset, false, 52, 8);
  };
  Buffer2.prototype.writeUintLE = Buffer2.prototype.writeUIntLE = function(value, offset, byteLength2, noAssert) {
    if (value = +value, offset = offset >>> 0, byteLength2 = byteLength2 >>> 0, !noAssert) {
      let maxBytes = Math.pow(2, 8 * byteLength2) - 1;
      checkInt(this, value, offset, byteLength2, maxBytes, 0);
    }
    let mul = 1, i2 = 0;
    this[offset] = value & 255;
    while (++i2 < byteLength2 && (mul *= 256))
      this[offset + i2] = value / mul & 255;
    return offset + byteLength2;
  };
  Buffer2.prototype.writeUintBE = Buffer2.prototype.writeUIntBE = function(value, offset, byteLength2, noAssert) {
    if (value = +value, offset = offset >>> 0, byteLength2 = byteLength2 >>> 0, !noAssert) {
      let maxBytes = Math.pow(2, 8 * byteLength2) - 1;
      checkInt(this, value, offset, byteLength2, maxBytes, 0);
    }
    let i2 = byteLength2 - 1, mul = 1;
    this[offset + i2] = value & 255;
    while (--i2 >= 0 && (mul *= 256))
      this[offset + i2] = value / mul & 255;
    return offset + byteLength2;
  };
  Buffer2.prototype.writeUint8 = Buffer2.prototype.writeUInt8 = function(value, offset, noAssert) {
    if (value = +value, offset = offset >>> 0, !noAssert)
      checkInt(this, value, offset, 1, 255, 0);
    return this[offset] = value & 255, offset + 1;
  };
  Buffer2.prototype.writeUint16LE = Buffer2.prototype.writeUInt16LE = function(value, offset, noAssert) {
    if (value = +value, offset = offset >>> 0, !noAssert)
      checkInt(this, value, offset, 2, 65535, 0);
    return this[offset] = value & 255, this[offset + 1] = value >>> 8, offset + 2;
  };
  Buffer2.prototype.writeUint16BE = Buffer2.prototype.writeUInt16BE = function(value, offset, noAssert) {
    if (value = +value, offset = offset >>> 0, !noAssert)
      checkInt(this, value, offset, 2, 65535, 0);
    return this[offset] = value >>> 8, this[offset + 1] = value & 255, offset + 2;
  };
  Buffer2.prototype.writeUint32LE = Buffer2.prototype.writeUInt32LE = function(value, offset, noAssert) {
    if (value = +value, offset = offset >>> 0, !noAssert)
      checkInt(this, value, offset, 4, 4294967295, 0);
    return this[offset + 3] = value >>> 24, this[offset + 2] = value >>> 16, this[offset + 1] = value >>> 8, this[offset] = value & 255, offset + 4;
  };
  Buffer2.prototype.writeUint32BE = Buffer2.prototype.writeUInt32BE = function(value, offset, noAssert) {
    if (value = +value, offset = offset >>> 0, !noAssert)
      checkInt(this, value, offset, 4, 4294967295, 0);
    return this[offset] = value >>> 24, this[offset + 1] = value >>> 16, this[offset + 2] = value >>> 8, this[offset + 3] = value & 255, offset + 4;
  };
  Buffer2.prototype.writeBigUInt64LE = defineBigIntMethod(function(value, offset = 0) {
    return wrtBigUInt64LE(this, value, offset, BigInt(0), BigInt("0xffffffffffffffff"));
  });
  Buffer2.prototype.writeBigUInt64BE = defineBigIntMethod(function(value, offset = 0) {
    return wrtBigUInt64BE(this, value, offset, BigInt(0), BigInt("0xffffffffffffffff"));
  });
  Buffer2.prototype.writeIntLE = function(value, offset, byteLength2, noAssert) {
    if (value = +value, offset = offset >>> 0, !noAssert) {
      let limit = Math.pow(2, 8 * byteLength2 - 1);
      checkInt(this, value, offset, byteLength2, limit - 1, -limit);
    }
    let i2 = 0, mul = 1, sub = 0;
    this[offset] = value & 255;
    while (++i2 < byteLength2 && (mul *= 256)) {
      if (value < 0 && sub === 0 && this[offset + i2 - 1] !== 0)
        sub = 1;
      this[offset + i2] = (value / mul >> 0) - sub & 255;
    }
    return offset + byteLength2;
  };
  Buffer2.prototype.writeIntBE = function(value, offset, byteLength2, noAssert) {
    if (value = +value, offset = offset >>> 0, !noAssert) {
      let limit = Math.pow(2, 8 * byteLength2 - 1);
      checkInt(this, value, offset, byteLength2, limit - 1, -limit);
    }
    let i2 = byteLength2 - 1, mul = 1, sub = 0;
    this[offset + i2] = value & 255;
    while (--i2 >= 0 && (mul *= 256)) {
      if (value < 0 && sub === 0 && this[offset + i2 + 1] !== 0)
        sub = 1;
      this[offset + i2] = (value / mul >> 0) - sub & 255;
    }
    return offset + byteLength2;
  };
  Buffer2.prototype.writeInt8 = function(value, offset, noAssert) {
    if (value = +value, offset = offset >>> 0, !noAssert)
      checkInt(this, value, offset, 1, 127, -128);
    if (value < 0)
      value = 255 + value + 1;
    return this[offset] = value & 255, offset + 1;
  };
  Buffer2.prototype.writeInt16LE = function(value, offset, noAssert) {
    if (value = +value, offset = offset >>> 0, !noAssert)
      checkInt(this, value, offset, 2, 32767, -32768);
    return this[offset] = value & 255, this[offset + 1] = value >>> 8, offset + 2;
  };
  Buffer2.prototype.writeInt16BE = function(value, offset, noAssert) {
    if (value = +value, offset = offset >>> 0, !noAssert)
      checkInt(this, value, offset, 2, 32767, -32768);
    return this[offset] = value >>> 8, this[offset + 1] = value & 255, offset + 2;
  };
  Buffer2.prototype.writeInt32LE = function(value, offset, noAssert) {
    if (value = +value, offset = offset >>> 0, !noAssert)
      checkInt(this, value, offset, 4, 2147483647, -2147483648);
    return this[offset] = value & 255, this[offset + 1] = value >>> 8, this[offset + 2] = value >>> 16, this[offset + 3] = value >>> 24, offset + 4;
  };
  Buffer2.prototype.writeInt32BE = function(value, offset, noAssert) {
    if (value = +value, offset = offset >>> 0, !noAssert)
      checkInt(this, value, offset, 4, 2147483647, -2147483648);
    if (value < 0)
      value = 4294967295 + value + 1;
    return this[offset] = value >>> 24, this[offset + 1] = value >>> 16, this[offset + 2] = value >>> 8, this[offset + 3] = value & 255, offset + 4;
  };
  Buffer2.prototype.writeBigInt64LE = defineBigIntMethod(function(value, offset = 0) {
    return wrtBigUInt64LE(this, value, offset, -BigInt("0x8000000000000000"), BigInt("0x7fffffffffffffff"));
  });
  Buffer2.prototype.writeBigInt64BE = defineBigIntMethod(function(value, offset = 0) {
    return wrtBigUInt64BE(this, value, offset, -BigInt("0x8000000000000000"), BigInt("0x7fffffffffffffff"));
  });
  Buffer2.prototype.writeFloatLE = function(value, offset, noAssert) {
    return writeFloat(this, value, offset, true, noAssert);
  };
  Buffer2.prototype.writeFloatBE = function(value, offset, noAssert) {
    return writeFloat(this, value, offset, false, noAssert);
  };
  Buffer2.prototype.writeDoubleLE = function(value, offset, noAssert) {
    return writeDouble(this, value, offset, true, noAssert);
  };
  Buffer2.prototype.writeDoubleBE = function(value, offset, noAssert) {
    return writeDouble(this, value, offset, false, noAssert);
  };
  Buffer2.prototype.copy = function(target, targetStart, start, end) {
    if (!Buffer2.isBuffer(target))
      throw TypeError("argument should be a Buffer");
    if (!start)
      start = 0;
    if (!end && end !== 0)
      end = this.length;
    if (targetStart >= target.length)
      targetStart = target.length;
    if (!targetStart)
      targetStart = 0;
    if (end > 0 && end < start)
      end = start;
    if (end === start)
      return 0;
    if (target.length === 0 || this.length === 0)
      return 0;
    if (targetStart < 0)
      throw RangeError("targetStart out of bounds");
    if (start < 0 || start >= this.length)
      throw RangeError("Index out of range");
    if (end < 0)
      throw RangeError("sourceEnd out of bounds");
    if (end > this.length)
      end = this.length;
    if (target.length - targetStart < end - start)
      end = target.length - targetStart + start;
    let len2 = end - start;
    if (this === target && typeof Uint8Array.prototype.copyWithin === "function")
      this.copyWithin(targetStart, start, end);
    else
      Uint8Array.prototype.set.call(target, this.subarray(start, end), targetStart);
    return len2;
  };
  Buffer2.prototype.fill = function(val, start, end, encoding) {
    if (typeof val === "string") {
      if (typeof start === "string")
        encoding = start, start = 0, end = this.length;
      else if (typeof end === "string")
        encoding = end, end = this.length;
      if (encoding !== undefined && typeof encoding !== "string")
        throw TypeError("encoding must be a string");
      if (typeof encoding === "string" && !Buffer2.isEncoding(encoding))
        throw TypeError("Unknown encoding: " + encoding);
      if (val.length === 1) {
        let code2 = val.charCodeAt(0);
        if (encoding === "utf8" && code2 < 128 || encoding === "latin1")
          val = code2;
      }
    } else if (typeof val === "number")
      val = val & 255;
    else if (typeof val === "boolean")
      val = Number(val);
    if (start < 0 || this.length < start || this.length < end)
      throw RangeError("Out of range index");
    if (end <= start)
      return this;
    if (start = start >>> 0, end = end === undefined ? this.length : end >>> 0, !val)
      val = 0;
    let i2;
    if (typeof val === "number")
      for (i2 = start;i2 < end; ++i2)
        this[i2] = val;
    else {
      let bytes = Buffer2.isBuffer(val) ? val : Buffer2.from(val, encoding), len2 = bytes.length;
      if (len2 === 0)
        throw TypeError('The value "' + val + '" is invalid for argument "value"');
      for (i2 = 0;i2 < end - start; ++i2)
        this[i2 + start] = bytes[i2 % len2];
    }
    return this;
  };
  INVALID_BASE64_RE = /[^+/0-9A-Za-z-_]/g;
  hexSliceLookupTable = function() {
    let table = Array(256);
    for (let i2 = 0;i2 < 16; ++i2) {
      let i16 = i2 * 16;
      for (let j = 0;j < 16; ++j)
        table[i16 + j] = "0123456789abcdef"[i2] + "0123456789abcdef"[j];
    }
    return table;
  }();
  resolveObjectURL = notimpl("resolveObjectURL");
  isUtf8 = notimpl("isUtf8");
  transcode = notimpl("transcode");
  buffer_default = Buffer2;
});

// node:events
var exports_events = {};
__export(exports_events, {
  setMaxListeners: () => setMaxListeners2,
  once: () => once2,
  listenerCount: () => listenerCount2,
  init: () => EventEmitter2,
  getMaxListeners: () => getMaxListeners2,
  getEventListeners: () => getEventListeners,
  default: () => events_default,
  captureRejectionSymbol: () => captureRejectionSymbol,
  addAbortListener: () => addAbortListener,
  EventEmitter: () => EventEmitter2
});
function emitError(emitter, args) {
  var { _events: events } = emitter;
  if (args[0] ??= Error("Unhandled error."), !events)
    throw args[0];
  var errorMonitor = events[kErrorMonitor];
  if (errorMonitor)
    for (var handler of ArrayPrototypeSlice.call(errorMonitor))
      handler.apply(emitter, args);
  var handlers = events.error;
  if (!handlers)
    throw args[0];
  for (var handler of ArrayPrototypeSlice.call(handlers))
    handler.apply(emitter, args);
  return true;
}
function addCatch(emitter, promise, type, args) {
  promise.then(undefined, function(err) {
    queueMicrotask(() => emitUnhandledRejectionOrErr(emitter, err, type, args));
  });
}
function emitUnhandledRejectionOrErr(emitter, err, type, args) {
  if (typeof emitter[kRejection] === "function")
    emitter[kRejection](err, type, ...args);
  else
    try {
      emitter[kCapture] = false, emitter.emit("error", err);
    } finally {
      emitter[kCapture] = true;
    }
}
function overflowWarning(emitter, type, handlers) {
  handlers.warned = true;
  let warn = Error(`Possible EventEmitter memory leak detected. ${handlers.length} ${String(type)} listeners added to [${emitter.constructor.name}]. Use emitter.setMaxListeners() to increase limit`);
  warn.name = "MaxListenersExceededWarning", warn.emitter = emitter, warn.type = type, warn.count = handlers.length, console.warn(warn);
}
function onceWrapper(type, listener, ...args) {
  this.removeListener(type, listener), listener.apply(this, args);
}
function once2(emitter, type, options) {
  var signal = options?.signal;
  if (validateAbortSignal(signal, "options.signal"), signal?.aborted)
    throw new AbortError(undefined, { cause: signal?.reason });
  let { resolve, reject, promise } = $newPromiseCapability(Promise), errorListener = (err) => {
    if (emitter.removeListener(type, resolver), signal != null)
      eventTargetAgnosticRemoveListener(signal, "abort", abortListener);
    reject(err);
  }, resolver = (...args) => {
    if (typeof emitter.removeListener === "function")
      emitter.removeListener("error", errorListener);
    if (signal != null)
      eventTargetAgnosticRemoveListener(signal, "abort", abortListener);
    resolve(args);
  };
  if (eventTargetAgnosticAddListener(emitter, type, resolver, { once: true }), type !== "error" && typeof emitter.once === "function")
    emitter.once("error", errorListener);
  function abortListener() {
    eventTargetAgnosticRemoveListener(emitter, type, resolver), eventTargetAgnosticRemoveListener(emitter, "error", errorListener), reject(new AbortError(undefined, { cause: signal?.reason }));
  }
  if (signal != null)
    eventTargetAgnosticAddListener(signal, "abort", abortListener, { once: true });
  return promise;
}
function getEventListeners(emitter, type) {
  return emitter.listeners(type);
}
function setMaxListeners2(n, ...eventTargets) {
  validateNumber2(n, "setMaxListeners", 0);
  var length;
  if (eventTargets && (length = eventTargets.length))
    for (let i2 = 0;i2 < length; i2++)
      eventTargets[i2].setMaxListeners(n);
  else
    defaultMaxListeners = n;
}
function listenerCount2(emitter, type) {
  return emitter.listenerCount(type);
}
function eventTargetAgnosticRemoveListener(emitter, name, listener, flags) {
  if (typeof emitter.removeListener === "function")
    emitter.removeListener(name, listener);
  else
    emitter.removeEventListener(name, listener, flags);
}
function eventTargetAgnosticAddListener(emitter, name, listener, flags) {
  if (typeof emitter.on === "function")
    if (flags.once)
      emitter.once(name, listener);
    else
      emitter.on(name, listener);
  else
    emitter.addEventListener(name, listener, flags);
}
function ERR_INVALID_ARG_TYPE2(name, type, value) {
  let err = TypeError(`The "${name}" argument must be of type ${type}. Received ${value}`);
  return err.code = "ERR_INVALID_ARG_TYPE", err;
}
function ERR_OUT_OF_RANGE2(name, range, value) {
  let err = RangeError(`The "${name}" argument is out of range. It must be ${range}. Received ${value}`);
  return err.code = "ERR_OUT_OF_RANGE", err;
}
function validateAbortSignal(signal, name) {
  if (signal !== undefined && (signal === null || typeof signal !== "object" || !("aborted" in signal)))
    throw ERR_INVALID_ARG_TYPE2(name, "AbortSignal", signal);
}
function validateNumber2(value, name, min, max) {
  if (typeof value !== "number")
    throw ERR_INVALID_ARG_TYPE2(name, "number", value);
  if (min != null && value < min || max != null && value > max || (min != null || max != null) && Number.isNaN(value))
    throw ERR_OUT_OF_RANGE2(name, `${min != null ? `>= ${min}` : ""}${min != null && max != null ? " && " : ""}${max != null ? `<= ${max}` : ""}`, value);
}
function checkListener(listener) {
  if (typeof listener !== "function")
    throw TypeError("The listener must be a function");
}
function validateBoolean(value, name) {
  if (typeof value !== "boolean")
    throw ERR_INVALID_ARG_TYPE2(name, "boolean", value);
}
function getMaxListeners2(emitterOrTarget) {
  return emitterOrTarget?._maxListeners ?? defaultMaxListeners;
}
function addAbortListener(signal, listener) {
  if (signal === undefined)
    throw ERR_INVALID_ARG_TYPE2("signal", "AbortSignal", signal);
  if (validateAbortSignal(signal, "signal"), typeof listener !== "function")
    throw ERR_INVALID_ARG_TYPE2("listener", "function", listener);
  let removeEventListener;
  if (signal.aborted)
    queueMicrotask(() => listener());
  else
    signal.addEventListener("abort", listener, { __proto__: null, once: true }), removeEventListener = () => {
      signal.removeEventListener("abort", listener);
    };
  return { __proto__: null, [Symbol.dispose]() {
    removeEventListener?.();
  } };
}
var SymbolFor, kCapture, kErrorMonitor, kMaxEventTargetListeners, kMaxEventTargetListenersWarned, kRejection, captureRejectionSymbol, ArrayPrototypeSlice, defaultMaxListeners = 10, EventEmitter2 = function(opts) {
  if (this._events === undefined || this._events === this.__proto__._events)
    this._events = { __proto__: null }, this._eventsCount = 0;
  if (this._maxListeners ??= undefined, this[kCapture] = opts?.captureRejections ? Boolean(opts?.captureRejections) : EventEmitterPrototype[kCapture])
    this.emit = emitWithRejectionCapture;
}, EventEmitterPrototype, emitWithoutRejectionCapture = function(type, ...args) {
  if (type === "error")
    return emitError(this, args);
  var { _events: events } = this;
  if (events === undefined)
    return false;
  var handlers = events[type];
  if (handlers === undefined)
    return false;
  let maybeClonedHandlers = handlers.length > 1 ? handlers.slice() : handlers;
  for (let i2 = 0, { length } = maybeClonedHandlers;i2 < length; i2++) {
    let handler = maybeClonedHandlers[i2];
    switch (args.length) {
      case 0:
        handler.call(this);
        break;
      case 1:
        handler.call(this, args[0]);
        break;
      case 2:
        handler.call(this, args[0], args[1]);
        break;
      case 3:
        handler.call(this, args[0], args[1], args[2]);
        break;
      default:
        handler.apply(this, args);
        break;
    }
  }
  return true;
}, emitWithRejectionCapture = function(type, ...args) {
  if (type === "error")
    return emitError(this, args);
  var { _events: events } = this;
  if (events === undefined)
    return false;
  var handlers = events[type];
  if (handlers === undefined)
    return false;
  let maybeClonedHandlers = handlers.length > 1 ? handlers.slice() : handlers;
  for (let i2 = 0, { length } = maybeClonedHandlers;i2 < length; i2++) {
    let handler = maybeClonedHandlers[i2], result;
    switch (args.length) {
      case 0:
        result = handler.call(this);
        break;
      case 1:
        result = handler.call(this, args[0]);
        break;
      case 2:
        result = handler.call(this, args[0], args[1]);
        break;
      case 3:
        result = handler.call(this, args[0], args[1], args[2]);
        break;
      default:
        result = handler.apply(this, args);
        break;
    }
    if (result !== undefined && typeof result?.then === "function" && result.then === Promise.prototype.then)
      addCatch(this, result, type, args);
  }
  return true;
}, AbortError, events_default;
var init_events = __esm(() => {
  SymbolFor = Symbol.for;
  kCapture = Symbol("kCapture");
  kErrorMonitor = SymbolFor("events.errorMonitor");
  kMaxEventTargetListeners = Symbol("events.maxEventTargetListeners");
  kMaxEventTargetListenersWarned = Symbol("events.maxEventTargetListenersWarned");
  kRejection = SymbolFor("nodejs.rejection");
  captureRejectionSymbol = SymbolFor("nodejs.rejection");
  ArrayPrototypeSlice = Array.prototype.slice;
  EventEmitterPrototype = EventEmitter2.prototype = {};
  EventEmitterPrototype._events = undefined;
  EventEmitterPrototype._eventsCount = 0;
  EventEmitterPrototype._maxListeners = undefined;
  EventEmitterPrototype.setMaxListeners = function(n) {
    return validateNumber2(n, "setMaxListeners", 0), this._maxListeners = n, this;
  };
  EventEmitterPrototype.constructor = EventEmitter2;
  EventEmitterPrototype.getMaxListeners = function() {
    return this?._maxListeners ?? defaultMaxListeners;
  };
  EventEmitterPrototype.emit = emitWithoutRejectionCapture;
  EventEmitterPrototype.addListener = function(type, fn) {
    checkListener(fn);
    var events = this._events;
    if (!events)
      events = this._events = { __proto__: null }, this._eventsCount = 0;
    else if (events.newListener)
      this.emit("newListener", type, fn.listener ?? fn);
    var handlers = events[type];
    if (!handlers)
      events[type] = [fn], this._eventsCount++;
    else {
      handlers.push(fn);
      var m = this._maxListeners ?? defaultMaxListeners;
      if (m > 0 && handlers.length > m && !handlers.warned)
        overflowWarning(this, type, handlers);
    }
    return this;
  };
  EventEmitterPrototype.on = EventEmitterPrototype.addListener;
  EventEmitterPrototype.prependListener = function(type, fn) {
    checkListener(fn);
    var events = this._events;
    if (!events)
      events = this._events = { __proto__: null }, this._eventsCount = 0;
    else if (events.newListener)
      this.emit("newListener", type, fn.listener ?? fn);
    var handlers = events[type];
    if (!handlers)
      events[type] = [fn], this._eventsCount++;
    else {
      handlers.unshift(fn);
      var m = this._maxListeners ?? defaultMaxListeners;
      if (m > 0 && handlers.length > m && !handlers.warned)
        overflowWarning(this, type, handlers);
    }
    return this;
  };
  EventEmitterPrototype.once = function(type, fn) {
    checkListener(fn);
    let bound = onceWrapper.bind(this, type, fn);
    return bound.listener = fn, this.addListener(type, bound), this;
  };
  EventEmitterPrototype.prependOnceListener = function(type, fn) {
    checkListener(fn);
    let bound = onceWrapper.bind(this, type, fn);
    return bound.listener = fn, this.prependListener(type, bound), this;
  };
  EventEmitterPrototype.removeListener = function(type, fn) {
    checkListener(fn);
    var { _events: events } = this;
    if (!events)
      return this;
    var handlers = events[type];
    if (!handlers)
      return this;
    var length = handlers.length;
    let position = -1;
    for (let i2 = length - 1;i2 >= 0; i2--)
      if (handlers[i2] === fn || handlers[i2].listener === fn) {
        position = i2;
        break;
      }
    if (position < 0)
      return this;
    if (position === 0)
      handlers.shift();
    else
      handlers.splice(position, 1);
    if (handlers.length === 0)
      delete events[type], this._eventsCount--;
    return this;
  };
  EventEmitterPrototype.off = EventEmitterPrototype.removeListener;
  EventEmitterPrototype.removeAllListeners = function(type) {
    var { _events: events } = this;
    if (type && events) {
      if (events[type])
        delete events[type], this._eventsCount--;
    } else
      this._events = { __proto__: null };
    return this;
  };
  EventEmitterPrototype.listeners = function(type) {
    var { _events: events } = this;
    if (!events)
      return [];
    var handlers = events[type];
    if (!handlers)
      return [];
    return handlers.map((x) => x.listener ?? x);
  };
  EventEmitterPrototype.rawListeners = function(type) {
    var { _events } = this;
    if (!_events)
      return [];
    var handlers = _events[type];
    if (!handlers)
      return [];
    return handlers.slice();
  };
  EventEmitterPrototype.listenerCount = function(type) {
    var { _events: events } = this;
    if (!events)
      return 0;
    return events[type]?.length ?? 0;
  };
  EventEmitterPrototype.eventNames = function() {
    return this._eventsCount > 0 ? Reflect.ownKeys(this._events) : [];
  };
  EventEmitterPrototype[kCapture] = false;
  AbortError = class AbortError extends Error {
    constructor(message = "The operation was aborted", options = undefined) {
      if (options !== undefined && typeof options !== "object")
        throw ERR_INVALID_ARG_TYPE2("options", "Object", options);
      super(message, options);
      this.code = "ABORT_ERR", this.name = "AbortError";
    }
  };
  Object.defineProperties(EventEmitter2, { captureRejections: { get() {
    return EventEmitterPrototype[kCapture];
  }, set(value) {
    validateBoolean(value, "EventEmitter.captureRejections"), EventEmitterPrototype[kCapture] = value;
  }, enumerable: true }, defaultMaxListeners: { enumerable: true, get: () => {
    return defaultMaxListeners;
  }, set: (arg) => {
    validateNumber2(arg, "defaultMaxListeners", 0), defaultMaxListeners = arg;
  } }, kMaxEventTargetListeners: { value: kMaxEventTargetListeners, enumerable: false, configurable: false, writable: false }, kMaxEventTargetListenersWarned: { value: kMaxEventTargetListenersWarned, enumerable: false, configurable: false, writable: false } });
  Object.assign(EventEmitter2, { once: once2, getEventListeners, getMaxListeners: getMaxListeners2, setMaxListeners: setMaxListeners2, EventEmitter: EventEmitter2, usingDomains: false, captureRejectionSymbol, errorMonitor: kErrorMonitor, addAbortListener, init: EventEmitter2, listenerCount: listenerCount2 });
  events_default = EventEmitter2;
});

// node:stream
var require_stream = __commonJS((exports2, module2) => {
  var __commonJS2 = (cb, mod) => () => (mod || cb((mod = { exports: {} }).exports, mod), mod.exports);
  var require_primordials = __commonJS2((exports22, module22) => {

    class AggregateError extends Error {
      constructor(errors) {
        if (!Array.isArray(errors))
          throw TypeError(`Expected input to be an Array, got ${typeof errors}`);
        let message = "";
        for (let i2 = 0;i2 < errors.length; i2++)
          message += `    ${errors[i2].stack}
`;
        super(message);
        this.name = "AggregateError", this.errors = errors;
      }
    }
    module22.exports = { AggregateError, ArrayIsArray(self2) {
      return Array.isArray(self2);
    }, ArrayPrototypeIncludes(self2, el) {
      return self2.includes(el);
    }, ArrayPrototypeIndexOf(self2, el) {
      return self2.indexOf(el);
    }, ArrayPrototypeJoin(self2, sep) {
      return self2.join(sep);
    }, ArrayPrototypeMap(self2, fn) {
      return self2.map(fn);
    }, ArrayPrototypePop(self2, el) {
      return self2.pop(el);
    }, ArrayPrototypePush(self2, el) {
      return self2.push(el);
    }, ArrayPrototypeSlice(self2, start, end) {
      return self2.slice(start, end);
    }, Error, FunctionPrototypeCall(fn, thisArgs, ...args) {
      return fn.call(thisArgs, ...args);
    }, FunctionPrototypeSymbolHasInstance(self2, instance) {
      return Function.prototype[Symbol.hasInstance].call(self2, instance);
    }, MathFloor: Math.floor, Number, NumberIsInteger: Number.isInteger, NumberIsNaN: Number.isNaN, NumberMAX_SAFE_INTEGER: Number.MAX_SAFE_INTEGER, NumberMIN_SAFE_INTEGER: Number.MIN_SAFE_INTEGER, NumberParseInt: Number.parseInt, ObjectDefineProperties(self2, props) {
      return Object.defineProperties(self2, props);
    }, ObjectDefineProperty(self2, name, prop) {
      return Object.defineProperty(self2, name, prop);
    }, ObjectGetOwnPropertyDescriptor(self2, name) {
      return Object.getOwnPropertyDescriptor(self2, name);
    }, ObjectKeys(obj) {
      return Object.keys(obj);
    }, ObjectSetPrototypeOf(target, proto) {
      return Object.setPrototypeOf(target, proto);
    }, Promise, PromisePrototypeCatch(self2, fn) {
      return self2.catch(fn);
    }, PromisePrototypeThen(self2, thenFn, catchFn) {
      return self2.then(thenFn, catchFn);
    }, PromiseReject(err) {
      return Promise.reject(err);
    }, PromiseResolve(val) {
      return Promise.resolve(val);
    }, ReflectApply: Reflect.apply, RegExpPrototypeTest(self2, value) {
      return self2.test(value);
    }, SafeSet: Set, String, StringPrototypeSlice(self2, start, end) {
      return self2.slice(start, end);
    }, StringPrototypeToLowerCase(self2) {
      return self2.toLowerCase();
    }, StringPrototypeToUpperCase(self2) {
      return self2.toUpperCase();
    }, StringPrototypeTrim(self2) {
      return self2.trim();
    }, Symbol, SymbolFor: Symbol.for, SymbolAsyncIterator: Symbol.asyncIterator, SymbolHasInstance: Symbol.hasInstance, SymbolIterator: Symbol.iterator, SymbolDispose: Symbol.dispose || Symbol("Symbol.dispose"), SymbolAsyncDispose: Symbol.asyncDispose || Symbol("Symbol.asyncDispose"), TypedArrayPrototypeSet(self2, buf, len2) {
      return self2.set(buf, len2);
    }, Boolean, Uint8Array };
  });
  var require_inspect = __commonJS2((exports22, module22) => {
    module22.exports = { format(format2, ...args) {
      return format2.replace(/%([sdifj])/g, function(...[_unused, type]) {
        let replacement = args.shift();
        if (type === "f")
          return replacement.toFixed(6);
        else if (type === "j")
          return JSON.stringify(replacement);
        else if (type === "s" && typeof replacement === "object")
          return `${replacement.constructor !== Object ? replacement.constructor.name : ""} {}`.trim();
        else
          return replacement.toString();
      });
    }, inspect(value) {
      switch (typeof value) {
        case "string":
          if (value.includes("'")) {
            if (!value.includes('"'))
              return `"${value}"`;
            else if (!value.includes("`") && !value.includes("${"))
              return `\`${value}\``;
          }
          return `'${value}'`;
        case "number":
          if (isNaN(value))
            return "NaN";
          else if (Object.is(value, -0))
            return String(value);
          return value;
        case "bigint":
          return `${String(value)}n`;
        case "boolean":
        case "undefined":
          return String(value);
        case "object":
          return "{}";
      }
    } };
  });
  var require_errors = __commonJS2((exports22, module22) => {
    var { format: format2, inspect: inspect2 } = require_inspect(), { AggregateError: CustomAggregateError } = require_primordials(), AggregateError = globalThis.AggregateError || CustomAggregateError, kIsNodeError = Symbol("kIsNodeError"), kTypes = ["string", "function", "number", "object", "Function", "Object", "boolean", "bigint", "symbol"], classRegExp = /^([A-Z][a-z0-9]*)+$/, codes = {};
    function assert(value, message) {
      if (!value)
        throw new codes.ERR_INTERNAL_ASSERTION(message);
    }
    function addNumericalSeparator2(val) {
      let res = "", i2 = val.length, start = val[0] === "-" ? 1 : 0;
      for (;i2 >= start + 4; i2 -= 3)
        res = `_${val.slice(i2 - 3, i2)}${res}`;
      return `${val.slice(0, i2)}${res}`;
    }
    function getMessage(key, msg, args) {
      if (typeof msg === "function")
        return assert(msg.length <= args.length, `Code: ${key}; The provided arguments length (${args.length}) does not match the required ones (${msg.length}).`), msg(...args);
      let expectedLength = (msg.match(/%[dfijoOs]/g) || []).length;
      if (assert(expectedLength === args.length, `Code: ${key}; The provided arguments length (${args.length}) does not match the required ones (${expectedLength}).`), args.length === 0)
        return msg;
      return format2(msg, ...args);
    }
    function E2(code2, message, Base) {
      if (!Base)
        Base = Error;

      class NodeError extends Base {
        constructor(...args) {
          super(getMessage(code2, message, args));
        }
        toString() {
          return `${this.name} [${code2}]: ${this.message}`;
        }
      }
      Object.defineProperties(NodeError.prototype, { name: { value: Base.name, writable: true, enumerable: false, configurable: true }, toString: { value() {
        return `${this.name} [${code2}]: ${this.message}`;
      }, writable: true, enumerable: false, configurable: true } }), NodeError.prototype.code = code2, NodeError.prototype[kIsNodeError] = true, codes[code2] = NodeError;
    }
    function hideStackFrames(fn) {
      let hidden = "__node_internal_" + fn.name;
      return Object.defineProperty(fn, "name", { value: hidden }), fn;
    }
    function aggregateTwoErrors(innerError, outerError) {
      if (innerError && outerError && innerError !== outerError) {
        if (Array.isArray(outerError.errors))
          return outerError.errors.push(innerError), outerError;
        let err = new AggregateError([outerError, innerError], outerError.message);
        return err.code = outerError.code, err;
      }
      return innerError || outerError;
    }

    class AbortError2 extends Error {
      constructor(message = "The operation was aborted", options = undefined) {
        if (options !== undefined && typeof options !== "object")
          throw new codes.ERR_INVALID_ARG_TYPE("options", "Object", options);
        super(message, options);
        this.code = "ABORT_ERR", this.name = "AbortError";
      }
    }
    E2("ERR_ASSERTION", "%s", Error);
    E2("ERR_INVALID_ARG_TYPE", (name, expected, actual) => {
      if (assert(typeof name === "string", "'name' must be a string"), !Array.isArray(expected))
        expected = [expected];
      let msg = "The ";
      if (name.endsWith(" argument"))
        msg += `${name} `;
      else
        msg += `"${name}" ${name.includes(".") ? "property" : "argument"} `;
      msg += "must be ";
      let types2 = [], instances = [], other = [];
      for (let value of expected)
        if (assert(typeof value === "string", "All expected entries have to be of type string"), kTypes.includes(value))
          types2.push(value.toLowerCase());
        else if (classRegExp.test(value))
          instances.push(value);
        else
          assert(value !== "object", 'The value "object" should be written as "Object"'), other.push(value);
      if (instances.length > 0) {
        let pos = types2.indexOf("object");
        if (pos !== -1)
          types2.splice(types2, pos, 1), instances.push("Object");
      }
      if (types2.length > 0) {
        switch (types2.length) {
          case 1:
            msg += `of type ${types2[0]}`;
            break;
          case 2:
            msg += `one of type ${types2[0]} or ${types2[1]}`;
            break;
          default: {
            let last = types2.pop();
            msg += `one of type ${types2.join(", ")}, or ${last}`;
          }
        }
        if (instances.length > 0 || other.length > 0)
          msg += " or ";
      }
      if (instances.length > 0) {
        switch (instances.length) {
          case 1:
            msg += `an instance of ${instances[0]}`;
            break;
          case 2:
            msg += `an instance of ${instances[0]} or ${instances[1]}`;
            break;
          default: {
            let last = instances.pop();
            msg += `an instance of ${instances.join(", ")}, or ${last}`;
          }
        }
        if (other.length > 0)
          msg += " or ";
      }
      switch (other.length) {
        case 0:
          break;
        case 1:
          if (other[0].toLowerCase() !== other[0])
            msg += "an ";
          msg += `${other[0]}`;
          break;
        case 2:
          msg += `one of ${other[0]} or ${other[1]}`;
          break;
        default: {
          let last = other.pop();
          msg += `one of ${other.join(", ")}, or ${last}`;
        }
      }
      if (actual == null)
        msg += `. Received ${actual}`;
      else if (typeof actual === "function" && actual.name)
        msg += `. Received function ${actual.name}`;
      else if (typeof actual === "object") {
        var _actual$constructor;
        if ((_actual$constructor = actual.constructor) !== null && _actual$constructor !== undefined && _actual$constructor.name)
          msg += `. Received an instance of ${actual.constructor.name}`;
        else {
          let inspected = inspect2(actual, { depth: -1 });
          msg += `. Received ${inspected}`;
        }
      } else {
        let inspected = inspect2(actual, { colors: false });
        if (inspected.length > 25)
          inspected = `${inspected.slice(0, 25)}...`;
        msg += `. Received type ${typeof actual} (${inspected})`;
      }
      return msg;
    }, TypeError);
    E2("ERR_INVALID_ARG_VALUE", (name, value, reason = "is invalid") => {
      let inspected = inspect2(value);
      if (inspected.length > 128)
        inspected = inspected.slice(0, 128) + "...";
      return `The ${name.includes(".") ? "property" : "argument"} '${name}' ${reason}. Received ${inspected}`;
    }, TypeError);
    E2("ERR_INVALID_RETURN_VALUE", (input, name, value) => {
      var _value$constructor;
      let type = value !== null && value !== undefined && (_value$constructor = value.constructor) !== null && _value$constructor !== undefined && _value$constructor.name ? `instance of ${value.constructor.name}` : `type ${typeof value}`;
      return `Expected ${input} to be returned from the "${name}" function but got ${type}.`;
    }, TypeError);
    E2("ERR_MISSING_ARGS", (...args) => {
      assert(args.length > 0, "At least one arg needs to be specified");
      let msg, len2 = args.length;
      switch (args = (Array.isArray(args) ? args : [args]).map((a) => `"${a}"`).join(" or "), len2) {
        case 1:
          msg += `The ${args[0]} argument`;
          break;
        case 2:
          msg += `The ${args[0]} and ${args[1]} arguments`;
          break;
        default:
          {
            let last = args.pop();
            msg += `The ${args.join(", ")}, and ${last} arguments`;
          }
          break;
      }
      return `${msg} must be specified`;
    }, TypeError);
    E2("ERR_OUT_OF_RANGE", (str, range, input) => {
      assert(range, 'Missing "range" argument');
      let received;
      if (Number.isInteger(input) && Math.abs(input) > 4294967296)
        received = addNumericalSeparator2(String(input));
      else if (typeof input === "bigint") {
        received = String(input);
        let limit = BigInt(2) ** BigInt(32);
        if (input > limit || input < -limit)
          received = addNumericalSeparator2(received);
        received += "n";
      } else
        received = inspect2(input);
      return `The value of "${str}" is out of range. It must be ${range}. Received ${received}`;
    }, RangeError);
    E2("ERR_MULTIPLE_CALLBACK", "Callback called multiple times", Error);
    E2("ERR_METHOD_NOT_IMPLEMENTED", "The %s method is not implemented", Error);
    E2("ERR_STREAM_ALREADY_FINISHED", "Cannot call %s after a stream was finished", Error);
    E2("ERR_STREAM_CANNOT_PIPE", "Cannot pipe, not readable", Error);
    E2("ERR_STREAM_DESTROYED", "Cannot call %s after a stream was destroyed", Error);
    E2("ERR_STREAM_NULL_VALUES", "May not write null values to stream", TypeError);
    E2("ERR_STREAM_PREMATURE_CLOSE", "Premature close", Error);
    E2("ERR_STREAM_PUSH_AFTER_EOF", "stream.push() after EOF", Error);
    E2("ERR_STREAM_UNSHIFT_AFTER_END_EVENT", "stream.unshift() after end event", Error);
    E2("ERR_STREAM_WRITE_AFTER_END", "write after end", Error);
    E2("ERR_UNKNOWN_ENCODING", "Unknown encoding: %s", TypeError);
    module22.exports = { AbortError: AbortError2, aggregateTwoErrors: hideStackFrames(aggregateTwoErrors), hideStackFrames, codes };
  });
  var require_event_target_shim = __commonJS2((exports22, module22) => {
    Object.defineProperty(exports22, "__esModule", { value: true });
    var privateData = new WeakMap, wrappers = new WeakMap;
    function pd(event) {
      let retv = privateData.get(event);
      return console.assert(retv != null, "'this' is expected an Event object, but got", event), retv;
    }
    function setCancelFlag(data) {
      if (data.passiveListener != null) {
        if (typeof console < "u" && typeof console.error === "function")
          console.error("Unable to preventDefault inside passive event listener invocation.", data.passiveListener);
        return;
      }
      if (!data.event.cancelable)
        return;
      if (data.canceled = true, typeof data.event.preventDefault === "function")
        data.event.preventDefault();
    }
    function Event2(eventTarget, event) {
      privateData.set(this, { eventTarget, event, eventPhase: 2, currentTarget: eventTarget, canceled: false, stopped: false, immediateStopped: false, passiveListener: null, timeStamp: event.timeStamp || Date.now() }), Object.defineProperty(this, "isTrusted", { value: false, enumerable: true });
      let keys = Object.keys(event);
      for (let i2 = 0;i2 < keys.length; ++i2) {
        let key = keys[i2];
        if (!(key in this))
          Object.defineProperty(this, key, defineRedirectDescriptor(key));
      }
    }
    Event2.prototype = { get type() {
      return pd(this).event.type;
    }, get target() {
      return pd(this).eventTarget;
    }, get currentTarget() {
      return pd(this).currentTarget;
    }, composedPath() {
      let currentTarget = pd(this).currentTarget;
      if (currentTarget == null)
        return [];
      return [currentTarget];
    }, get NONE() {
      return 0;
    }, get CAPTURING_PHASE() {
      return 1;
    }, get AT_TARGET() {
      return 2;
    }, get BUBBLING_PHASE() {
      return 3;
    }, get eventPhase() {
      return pd(this).eventPhase;
    }, stopPropagation() {
      let data = pd(this);
      if (data.stopped = true, typeof data.event.stopPropagation === "function")
        data.event.stopPropagation();
    }, stopImmediatePropagation() {
      let data = pd(this);
      if (data.stopped = true, data.immediateStopped = true, typeof data.event.stopImmediatePropagation === "function")
        data.event.stopImmediatePropagation();
    }, get bubbles() {
      return Boolean(pd(this).event.bubbles);
    }, get cancelable() {
      return Boolean(pd(this).event.cancelable);
    }, preventDefault() {
      setCancelFlag(pd(this));
    }, get defaultPrevented() {
      return pd(this).canceled;
    }, get composed() {
      return Boolean(pd(this).event.composed);
    }, get timeStamp() {
      return pd(this).timeStamp;
    }, get srcElement() {
      return pd(this).eventTarget;
    }, get cancelBubble() {
      return pd(this).stopped;
    }, set cancelBubble(value) {
      if (!value)
        return;
      let data = pd(this);
      if (data.stopped = true, typeof data.event.cancelBubble === "boolean")
        data.event.cancelBubble = true;
    }, get returnValue() {
      return !pd(this).canceled;
    }, set returnValue(value) {
      if (!value)
        setCancelFlag(pd(this));
    }, initEvent() {} };
    Object.defineProperty(Event2.prototype, "constructor", { value: Event2, configurable: true, writable: true });
    if (typeof window < "u" && typeof window.Event < "u")
      Object.setPrototypeOf(Event2.prototype, window.Event.prototype), wrappers.set(window.Event.prototype, Event2);
    function defineRedirectDescriptor(key) {
      return { get() {
        return pd(this).event[key];
      }, set(value) {
        pd(this).event[key] = value;
      }, configurable: true, enumerable: true };
    }
    function defineCallDescriptor(key) {
      return { value() {
        let event = pd(this).event;
        return event[key].apply(event, arguments);
      }, configurable: true, enumerable: true };
    }
    function defineWrapper(BaseEvent, proto) {
      let keys = Object.keys(proto);
      if (keys.length === 0)
        return BaseEvent;
      function CustomEvent(eventTarget, event) {
        BaseEvent.call(this, eventTarget, event);
      }
      CustomEvent.prototype = Object.create(BaseEvent.prototype, { constructor: { value: CustomEvent, configurable: true, writable: true } });
      for (let i2 = 0;i2 < keys.length; ++i2) {
        let key = keys[i2];
        if (!(key in BaseEvent.prototype)) {
          let isFunc = typeof Object.getOwnPropertyDescriptor(proto, key).value === "function";
          Object.defineProperty(CustomEvent.prototype, key, isFunc ? defineCallDescriptor(key) : defineRedirectDescriptor(key));
        }
      }
      return CustomEvent;
    }
    function getWrapper(proto) {
      if (proto == null || proto === Object.prototype)
        return Event2;
      let wrapper = wrappers.get(proto);
      if (wrapper == null)
        wrapper = defineWrapper(getWrapper(Object.getPrototypeOf(proto)), proto), wrappers.set(proto, wrapper);
      return wrapper;
    }
    function wrapEvent(eventTarget, event) {
      return new (getWrapper(Object.getPrototypeOf(event)))(eventTarget, event);
    }
    function isStopped(event) {
      return pd(event).immediateStopped;
    }
    function setEventPhase(event, eventPhase) {
      pd(event).eventPhase = eventPhase;
    }
    function setCurrentTarget(event, currentTarget) {
      pd(event).currentTarget = currentTarget;
    }
    function setPassiveListener(event, passiveListener) {
      pd(event).passiveListener = passiveListener;
    }
    var listenersMap = new WeakMap, CAPTURE = 1, BUBBLE = 2, ATTRIBUTE = 3;
    function isObject3(x) {
      return x !== null && typeof x === "object";
    }
    function getListeners(eventTarget) {
      let listeners = listenersMap.get(eventTarget);
      if (listeners == null)
        throw TypeError("'this' is expected an EventTarget object, but got another value.");
      return listeners;
    }
    function defineEventAttributeDescriptor(eventName) {
      return { get() {
        let node = getListeners(this).get(eventName);
        while (node != null) {
          if (node.listenerType === ATTRIBUTE)
            return node.listener;
          node = node.next;
        }
        return null;
      }, set(listener) {
        if (typeof listener !== "function" && !isObject3(listener))
          listener = null;
        let listeners = getListeners(this), prev = null, node = listeners.get(eventName);
        while (node != null) {
          if (node.listenerType === ATTRIBUTE)
            if (prev !== null)
              prev.next = node.next;
            else if (node.next !== null)
              listeners.set(eventName, node.next);
            else
              listeners.delete(eventName);
          else
            prev = node;
          node = node.next;
        }
        if (listener !== null) {
          let newNode = { listener, listenerType: ATTRIBUTE, passive: false, once: false, next: null };
          if (prev === null)
            listeners.set(eventName, newNode);
          else
            prev.next = newNode;
        }
      }, configurable: true, enumerable: true };
    }
    function defineEventAttribute(eventTargetPrototype, eventName) {
      Object.defineProperty(eventTargetPrototype, `on${eventName}`, defineEventAttributeDescriptor(eventName));
    }
    function defineCustomEventTarget(eventNames) {
      function CustomEventTarget() {
        EventTarget.call(this);
      }
      CustomEventTarget.prototype = Object.create(EventTarget.prototype, { constructor: { value: CustomEventTarget, configurable: true, writable: true } });
      for (let i2 = 0;i2 < eventNames.length; ++i2)
        defineEventAttribute(CustomEventTarget.prototype, eventNames[i2]);
      return CustomEventTarget;
    }
    function EventTarget() {
      if (this instanceof EventTarget) {
        listenersMap.set(this, new Map);
        return;
      }
      if (arguments.length === 1 && Array.isArray(arguments[0]))
        return defineCustomEventTarget(arguments[0]);
      if (arguments.length > 0) {
        let types2 = Array(arguments.length);
        for (let i2 = 0;i2 < arguments.length; ++i2)
          types2[i2] = arguments[i2];
        return defineCustomEventTarget(types2);
      }
      throw TypeError("Cannot call a class as a function");
    }
    EventTarget.prototype = { addEventListener(eventName, listener, options) {
      if (listener == null)
        return;
      if (typeof listener !== "function" && !isObject3(listener))
        throw TypeError("'listener' should be a function or an object.");
      let listeners = getListeners(this), optionsIsObj = isObject3(options), listenerType = (optionsIsObj ? Boolean(options.capture) : Boolean(options)) ? CAPTURE : BUBBLE, newNode = { listener, listenerType, passive: optionsIsObj && Boolean(options.passive), once: optionsIsObj && Boolean(options.once), next: null }, node = listeners.get(eventName);
      if (node === undefined) {
        listeners.set(eventName, newNode);
        return;
      }
      let prev = null;
      while (node != null) {
        if (node.listener === listener && node.listenerType === listenerType)
          return;
        prev = node, node = node.next;
      }
      prev.next = newNode;
    }, removeEventListener(eventName, listener, options) {
      if (listener == null)
        return;
      let listeners = getListeners(this), listenerType = (isObject3(options) ? Boolean(options.capture) : Boolean(options)) ? CAPTURE : BUBBLE, prev = null, node = listeners.get(eventName);
      while (node != null) {
        if (node.listener === listener && node.listenerType === listenerType) {
          if (prev !== null)
            prev.next = node.next;
          else if (node.next !== null)
            listeners.set(eventName, node.next);
          else
            listeners.delete(eventName);
          return;
        }
        prev = node, node = node.next;
      }
    }, dispatchEvent(event) {
      if (event == null || typeof event.type !== "string")
        throw TypeError('"event.type" should be a string.');
      let listeners = getListeners(this), eventName = event.type, node = listeners.get(eventName);
      if (node == null)
        return true;
      let wrappedEvent = wrapEvent(this, event), prev = null;
      while (node != null) {
        if (node.once)
          if (prev !== null)
            prev.next = node.next;
          else if (node.next !== null)
            listeners.set(eventName, node.next);
          else
            listeners.delete(eventName);
        else
          prev = node;
        if (setPassiveListener(wrappedEvent, node.passive ? node.listener : null), typeof node.listener === "function")
          try {
            node.listener.call(this, wrappedEvent);
          } catch (err) {
            if (typeof console < "u" && typeof console.error === "function")
              console.error(err);
          }
        else if (node.listenerType !== ATTRIBUTE && typeof node.listener.handleEvent === "function")
          node.listener.handleEvent(wrappedEvent);
        if (isStopped(wrappedEvent))
          break;
        node = node.next;
      }
      return setPassiveListener(wrappedEvent, null), setEventPhase(wrappedEvent, 0), setCurrentTarget(wrappedEvent, null), !wrappedEvent.defaultPrevented;
    } };
    Object.defineProperty(EventTarget.prototype, "constructor", { value: EventTarget, configurable: true, writable: true });
    if (typeof window < "u" && typeof window.EventTarget < "u")
      Object.setPrototypeOf(EventTarget.prototype, window.EventTarget.prototype);
    exports22.defineEventAttribute = defineEventAttribute;
    exports22.EventTarget = EventTarget;
    exports22.default = EventTarget;
    module22.exports = EventTarget;
    module22.exports.EventTarget = module22.exports.default = EventTarget;
    module22.exports.defineEventAttribute = defineEventAttribute;
  });
  var require_abort_controller = __commonJS2((exports22, module22) => {
    Object.defineProperty(exports22, "__esModule", { value: true });
    var eventTargetShim = require_event_target_shim();

    class AbortSignal extends eventTargetShim.EventTarget {
      constructor() {
        super();
        throw TypeError("AbortSignal cannot be constructed directly");
      }
      get aborted() {
        let aborted = abortedFlags.get(this);
        if (typeof aborted !== "boolean")
          throw TypeError(`Expected 'this' to be an 'AbortSignal' object, but got ${this === null ? "null" : typeof this}`);
        return aborted;
      }
    }
    eventTargetShim.defineEventAttribute(AbortSignal.prototype, "abort");
    function createAbortSignal() {
      let signal = Object.create(AbortSignal.prototype);
      return eventTargetShim.EventTarget.call(signal), abortedFlags.set(signal, false), signal;
    }
    function abortSignal(signal) {
      if (abortedFlags.get(signal) !== false)
        return;
      abortedFlags.set(signal, true), signal.dispatchEvent({ type: "abort" });
    }
    var abortedFlags = new WeakMap;
    Object.defineProperties(AbortSignal.prototype, { aborted: { enumerable: true } });
    if (typeof Symbol === "function" && typeof Symbol.toStringTag === "symbol")
      Object.defineProperty(AbortSignal.prototype, Symbol.toStringTag, { configurable: true, value: "AbortSignal" });

    class AbortController2 {
      constructor() {
        signals.set(this, createAbortSignal());
      }
      get signal() {
        return getSignal(this);
      }
      abort() {
        abortSignal(getSignal(this));
      }
    }
    var signals = new WeakMap;
    function getSignal(controller) {
      let signal = signals.get(controller);
      if (signal == null)
        throw TypeError(`Expected 'this' to be an 'AbortController' object, but got ${controller === null ? "null" : typeof controller}`);
      return signal;
    }
    Object.defineProperties(AbortController2.prototype, { signal: { enumerable: true }, abort: { enumerable: true } });
    if (typeof Symbol === "function" && typeof Symbol.toStringTag === "symbol")
      Object.defineProperty(AbortController2.prototype, Symbol.toStringTag, { configurable: true, value: "AbortController" });
    exports22.AbortController = AbortController2;
    exports22.AbortSignal = AbortSignal;
    exports22.default = AbortController2;
    module22.exports = AbortController2;
    module22.exports.AbortController = module22.exports.default = AbortController2;
    module22.exports.AbortSignal = AbortSignal;
  });
  var require_util = __commonJS2((exports22, module22) => {
    var bufferModule = (init_buffer(), __toCommonJS(exports_buffer)), { format: format2, inspect: inspect2 } = require_inspect(), { codes: { ERR_INVALID_ARG_TYPE: ERR_INVALID_ARG_TYPE3 } } = require_errors(), { kResistStopPropagation, AggregateError, SymbolDispose } = require_primordials(), AbortSignal = globalThis.AbortSignal || require_abort_controller().AbortSignal, AbortController2 = globalThis.AbortController || require_abort_controller().AbortController, AsyncFunction = Object.getPrototypeOf(async function() {}).constructor, Blob3 = globalThis.Blob || bufferModule.Blob, isBlob2 = typeof Blob3 < "u" ? function(b) {
      return b instanceof Blob3;
    } : function(b) {
      return false;
    }, validateAbortSignal2 = (signal, name) => {
      if (signal !== undefined && (signal === null || typeof signal !== "object" || !("aborted" in signal)))
        throw new ERR_INVALID_ARG_TYPE3(name, "AbortSignal", signal);
    }, validateFunction = (value, name) => {
      if (typeof value !== "function")
        throw new ERR_INVALID_ARG_TYPE3(name, "Function", value);
    };
    module22.exports = { AggregateError, kEmptyObject: Object.freeze({}), once(callback) {
      let called = false;
      return function(...args) {
        if (called)
          return;
        called = true, callback.apply(this, args);
      };
    }, createDeferredPromise: function() {
      let resolve, reject;
      return { promise: new Promise((res, rej) => {
        resolve = res, reject = rej;
      }), resolve, reject };
    }, promisify(fn) {
      return new Promise((resolve, reject) => {
        fn((err, ...args) => {
          if (err)
            return reject(err);
          return resolve(...args);
        });
      });
    }, debuglog() {
      return function() {};
    }, format: format2, inspect: inspect2, types: { isAsyncFunction(fn) {
      return fn instanceof AsyncFunction;
    }, isArrayBufferView(arr) {
      return ArrayBuffer.isView(arr);
    } }, isBlob: isBlob2, deprecate(fn, message) {
      return fn;
    }, addAbortListener: (init_events(), __toCommonJS(exports_events)).addAbortListener || function(signal, listener) {
      if (signal === undefined)
        throw new ERR_INVALID_ARG_TYPE3("signal", "AbortSignal", signal);
      validateAbortSignal2(signal, "signal"), validateFunction(listener, "listener");
      let removeEventListener;
      if (signal.aborted)
        queueMicrotask(() => listener());
      else
        signal.addEventListener("abort", listener, { __proto__: null, once: true, [kResistStopPropagation]: true }), removeEventListener = () => {
          signal.removeEventListener("abort", listener);
        };
      return { __proto__: null, [SymbolDispose]() {
        var _removeEventListener;
        (_removeEventListener = removeEventListener) === null || _removeEventListener === undefined || _removeEventListener();
      } };
    }, AbortSignalAny: AbortSignal.any || function(signals) {
      if (signals.length === 1)
        return signals[0];
      let ac = new AbortController2, abort = () => ac.abort();
      return signals.forEach((signal) => {
        validateAbortSignal2(signal, "signals"), signal.addEventListener("abort", abort, { once: true });
      }), ac.signal.addEventListener("abort", () => {
        signals.forEach((signal) => signal.removeEventListener("abort", abort));
      }, { once: true }), ac.signal;
    } };
    module22.exports.promisify.custom = Symbol.for("nodejs.util.promisify.custom");
  });
  var require_validators = __commonJS2((exports22, module22) => {
    var { ArrayIsArray, ArrayPrototypeIncludes, ArrayPrototypeJoin, ArrayPrototypeMap, NumberIsInteger, NumberIsNaN, NumberMAX_SAFE_INTEGER, NumberMIN_SAFE_INTEGER, NumberParseInt, ObjectPrototypeHasOwnProperty, RegExpPrototypeExec, String: String2, StringPrototypeToUpperCase, StringPrototypeTrim } = require_primordials(), { hideStackFrames, codes: { ERR_SOCKET_BAD_PORT, ERR_INVALID_ARG_TYPE: ERR_INVALID_ARG_TYPE3, ERR_INVALID_ARG_VALUE, ERR_OUT_OF_RANGE: ERR_OUT_OF_RANGE3, ERR_UNKNOWN_SIGNAL } } = require_errors(), { normalizeEncoding } = require_util(), { isAsyncFunction, isArrayBufferView: isArrayBufferView2 } = require_util().types, signals = {};
    function isInt32(value) {
      return value === (value | 0);
    }
    function isUint32(value) {
      return value === value >>> 0;
    }
    var octalReg = /^[0-7]+$/, modeDesc = "must be a 32-bit unsigned integer or an octal string";
    function parseFileMode(value, name, def) {
      if (typeof value > "u")
        value = def;
      if (typeof value === "string") {
        if (RegExpPrototypeExec(octalReg, value) === null)
          throw new ERR_INVALID_ARG_VALUE(name, value, modeDesc);
        value = NumberParseInt(value, 8);
      }
      return validateUint32(value, name), value;
    }
    var validateInteger = hideStackFrames((value, name, min = NumberMIN_SAFE_INTEGER, max = NumberMAX_SAFE_INTEGER) => {
      if (typeof value !== "number")
        throw new ERR_INVALID_ARG_TYPE3(name, "number", value);
      if (!NumberIsInteger(value))
        throw new ERR_OUT_OF_RANGE3(name, "an integer", value);
      if (value < min || value > max)
        throw new ERR_OUT_OF_RANGE3(name, `>= ${min} && <= ${max}`, value);
    }), validateInt32 = hideStackFrames((value, name, min = -2147483648, max = 2147483647) => {
      if (typeof value !== "number")
        throw new ERR_INVALID_ARG_TYPE3(name, "number", value);
      if (!NumberIsInteger(value))
        throw new ERR_OUT_OF_RANGE3(name, "an integer", value);
      if (value < min || value > max)
        throw new ERR_OUT_OF_RANGE3(name, `>= ${min} && <= ${max}`, value);
    }), validateUint32 = hideStackFrames((value, name, positive = false) => {
      if (typeof value !== "number")
        throw new ERR_INVALID_ARG_TYPE3(name, "number", value);
      if (!NumberIsInteger(value))
        throw new ERR_OUT_OF_RANGE3(name, "an integer", value);
      let min = positive ? 1 : 0, max = 4294967295;
      if (value < min || value > max)
        throw new ERR_OUT_OF_RANGE3(name, `>= ${min} && <= ${max}`, value);
    });
    function validateString(value, name) {
      if (typeof value !== "string")
        throw new ERR_INVALID_ARG_TYPE3(name, "string", value);
    }
    function validateNumber3(value, name, min = undefined, max) {
      if (typeof value !== "number")
        throw new ERR_INVALID_ARG_TYPE3(name, "number", value);
      if (min != null && value < min || max != null && value > max || (min != null || max != null) && NumberIsNaN(value))
        throw new ERR_OUT_OF_RANGE3(name, `${min != null ? `>= ${min}` : ""}${min != null && max != null ? " && " : ""}${max != null ? `<= ${max}` : ""}`, value);
    }
    var validateOneOf = hideStackFrames((value, name, oneOf) => {
      if (!ArrayPrototypeIncludes(oneOf, value)) {
        let reason = "must be one of: " + ArrayPrototypeJoin(ArrayPrototypeMap(oneOf, (v) => typeof v === "string" ? `'${v}'` : String2(v)), ", ");
        throw new ERR_INVALID_ARG_VALUE(name, value, reason);
      }
    });
    function validateBoolean2(value, name) {
      if (typeof value !== "boolean")
        throw new ERR_INVALID_ARG_TYPE3(name, "boolean", value);
    }
    function getOwnPropertyValueOrDefault(options, key, defaultValue) {
      return options == null || !ObjectPrototypeHasOwnProperty(options, key) ? defaultValue : options[key];
    }
    var validateObject = hideStackFrames((value, name, options = null) => {
      let allowArray = getOwnPropertyValueOrDefault(options, "allowArray", false), allowFunction = getOwnPropertyValueOrDefault(options, "allowFunction", false);
      if (!getOwnPropertyValueOrDefault(options, "nullable", false) && value === null || !allowArray && ArrayIsArray(value) || typeof value !== "object" && (!allowFunction || typeof value !== "function"))
        throw new ERR_INVALID_ARG_TYPE3(name, "Object", value);
    }), validateDictionary = hideStackFrames((value, name) => {
      if (value != null && typeof value !== "object" && typeof value !== "function")
        throw new ERR_INVALID_ARG_TYPE3(name, "a dictionary", value);
    }), validateArray = hideStackFrames((value, name, minLength = 0) => {
      if (!ArrayIsArray(value))
        throw new ERR_INVALID_ARG_TYPE3(name, "Array", value);
      if (value.length < minLength) {
        let reason = `must be longer than ${minLength}`;
        throw new ERR_INVALID_ARG_VALUE(name, value, reason);
      }
    });
    function validateStringArray(value, name) {
      validateArray(value, name);
      for (let i2 = 0;i2 < value.length; i2++)
        validateString(value[i2], `${name}[${i2}]`);
    }
    function validateBooleanArray(value, name) {
      validateArray(value, name);
      for (let i2 = 0;i2 < value.length; i2++)
        validateBoolean2(value[i2], `${name}[${i2}]`);
    }
    function validateAbortSignalArray(value, name) {
      validateArray(value, name);
      for (let i2 = 0;i2 < value.length; i2++) {
        let signal = value[i2], indexedName = `${name}[${i2}]`;
        if (signal == null)
          throw new ERR_INVALID_ARG_TYPE3(indexedName, "AbortSignal", signal);
        validateAbortSignal2(signal, indexedName);
      }
    }
    function validateSignalName(signal, name = "signal") {
      if (validateString(signal, name), signals[signal] === undefined) {
        if (signals[StringPrototypeToUpperCase(signal)] !== undefined)
          throw new ERR_UNKNOWN_SIGNAL(signal + " (signals must use all capital letters)");
        throw new ERR_UNKNOWN_SIGNAL(signal);
      }
    }
    var validateBuffer = hideStackFrames((buffer, name = "buffer") => {
      if (!isArrayBufferView2(buffer))
        throw new ERR_INVALID_ARG_TYPE3(name, ["Buffer", "TypedArray", "DataView"], buffer);
    });
    function validateEncoding(data, encoding) {
      let normalizedEncoding = normalizeEncoding(encoding), length = data.length;
      if (normalizedEncoding === "hex" && length % 2 !== 0)
        throw new ERR_INVALID_ARG_VALUE("encoding", encoding, `is invalid for data of length ${length}`);
    }
    function validatePort(port, name = "Port", allowZero = true) {
      if (typeof port !== "number" && typeof port !== "string" || typeof port === "string" && StringPrototypeTrim(port).length === 0 || +port !== +port >>> 0 || port > 65535 || port === 0 && !allowZero)
        throw new ERR_SOCKET_BAD_PORT(name, port, allowZero);
      return port | 0;
    }
    var validateAbortSignal2 = hideStackFrames((signal, name) => {
      if (signal !== undefined && (signal === null || typeof signal !== "object" || !("aborted" in signal)))
        throw new ERR_INVALID_ARG_TYPE3(name, "AbortSignal", signal);
    }), validateFunction = hideStackFrames((value, name) => {
      if (typeof value !== "function")
        throw new ERR_INVALID_ARG_TYPE3(name, "Function", value);
    }), validatePlainFunction = hideStackFrames((value, name) => {
      if (typeof value !== "function" || isAsyncFunction(value))
        throw new ERR_INVALID_ARG_TYPE3(name, "Function", value);
    }), validateUndefined = hideStackFrames((value, name) => {
      if (value !== undefined)
        throw new ERR_INVALID_ARG_TYPE3(name, "undefined", value);
    });
    function validateUnion(value, name, union) {
      if (!ArrayPrototypeIncludes(union, value))
        throw new ERR_INVALID_ARG_TYPE3(name, `('${ArrayPrototypeJoin(union, "|")}')`, value);
    }
    var linkValueRegExp = /^(?:<[^>]*>)(?:\s*;\s*[^;"\s]+(?:=(")?[^;"\s]*\1)?)*$/;
    function validateLinkHeaderFormat(value, name) {
      if (typeof value > "u" || !RegExpPrototypeExec(linkValueRegExp, value))
        throw new ERR_INVALID_ARG_VALUE(name, value, 'must be an array or string of format "</styles.css>; rel=preload; as=style"');
    }
    function validateLinkHeaderValue(hints) {
      if (typeof hints === "string")
        return validateLinkHeaderFormat(hints, "hints"), hints;
      else if (ArrayIsArray(hints)) {
        let hintsLength = hints.length, result = "";
        if (hintsLength === 0)
          return result;
        for (let i2 = 0;i2 < hintsLength; i2++) {
          let link = hints[i2];
          if (validateLinkHeaderFormat(link, "hints"), result += link, i2 !== hintsLength - 1)
            result += ", ";
        }
        return result;
      }
      throw new ERR_INVALID_ARG_VALUE("hints", hints, 'must be an array or string of format "</styles.css>; rel=preload; as=style"');
    }
    module22.exports = { isInt32, isUint32, parseFileMode, validateArray, validateStringArray, validateBooleanArray, validateAbortSignalArray, validateBoolean: validateBoolean2, validateBuffer, validateDictionary, validateEncoding, validateFunction, validateInt32, validateInteger, validateNumber: validateNumber3, validateObject, validateOneOf, validatePlainFunction, validatePort, validateSignalName, validateString, validateUint32, validateUndefined, validateUnion, validateAbortSignal: validateAbortSignal2, validateLinkHeaderValue };
  });
  var require_process = __commonJS2((exports22, module22) => {
    module22.exports = globalThis.process;
  });
  var require_utils = __commonJS2((exports22, module22) => {
    var { SymbolAsyncIterator, SymbolIterator, SymbolFor: SymbolFor2 } = require_primordials(), kIsDestroyed = SymbolFor2("nodejs.stream.destroyed"), kIsErrored = SymbolFor2("nodejs.stream.errored"), kIsReadable = SymbolFor2("nodejs.stream.readable"), kIsWritable = SymbolFor2("nodejs.stream.writable"), kIsDisturbed = SymbolFor2("nodejs.stream.disturbed"), kIsClosedPromise = SymbolFor2("nodejs.webstream.isClosedPromise"), kControllerErrorFunction = SymbolFor2("nodejs.webstream.controllerErrorFunction");
    function isReadableNodeStream(obj, strict = false) {
      var _obj$_readableState;
      return !!(obj && typeof obj.pipe === "function" && typeof obj.on === "function" && (!strict || typeof obj.pause === "function" && typeof obj.resume === "function") && (!obj._writableState || ((_obj$_readableState = obj._readableState) === null || _obj$_readableState === undefined ? undefined : _obj$_readableState.readable) !== false) && (!obj._writableState || obj._readableState));
    }
    function isWritableNodeStream(obj) {
      var _obj$_writableState;
      return !!(obj && typeof obj.write === "function" && typeof obj.on === "function" && (!obj._readableState || ((_obj$_writableState = obj._writableState) === null || _obj$_writableState === undefined ? undefined : _obj$_writableState.writable) !== false));
    }
    function isDuplexNodeStream(obj) {
      return !!(obj && typeof obj.pipe === "function" && obj._readableState && typeof obj.on === "function" && typeof obj.write === "function");
    }
    function isNodeStream(obj) {
      return obj && (obj._readableState || obj._writableState || typeof obj.write === "function" && typeof obj.on === "function" || typeof obj.pipe === "function" && typeof obj.on === "function");
    }
    function isReadableStream2(obj) {
      return !!(obj && !isNodeStream(obj) && typeof obj.pipeThrough === "function" && typeof obj.getReader === "function" && typeof obj.cancel === "function");
    }
    function isWritableStream(obj) {
      return !!(obj && !isNodeStream(obj) && typeof obj.getWriter === "function" && typeof obj.abort === "function");
    }
    function isTransformStream(obj) {
      return !!(obj && !isNodeStream(obj) && typeof obj.readable === "object" && typeof obj.writable === "object");
    }
    function isWebStream(obj) {
      return isReadableStream2(obj) || isWritableStream(obj) || isTransformStream(obj);
    }
    function isIterable2(obj, isAsync) {
      if (obj == null)
        return false;
      if (isAsync === true)
        return typeof obj[SymbolAsyncIterator] === "function";
      if (isAsync === false)
        return typeof obj[SymbolIterator] === "function";
      return typeof obj[SymbolAsyncIterator] === "function" || typeof obj[SymbolIterator] === "function";
    }
    function isDestroyed(stream) {
      if (!isNodeStream(stream))
        return null;
      let { _writableState: wState, _readableState: rState } = stream, state = wState || rState;
      return !!(stream.destroyed || stream[kIsDestroyed] || state !== null && state !== undefined && state.destroyed);
    }
    function isWritableEnded(stream) {
      if (!isWritableNodeStream(stream))
        return null;
      if (stream.writableEnded === true)
        return true;
      let wState = stream._writableState;
      if (wState !== null && wState !== undefined && wState.errored)
        return false;
      if (typeof (wState === null || wState === undefined ? undefined : wState.ended) !== "boolean")
        return null;
      return wState.ended;
    }
    function isWritableFinished(stream, strict) {
      if (!isWritableNodeStream(stream))
        return null;
      if (stream.writableFinished === true)
        return true;
      let wState = stream._writableState;
      if (wState !== null && wState !== undefined && wState.errored)
        return false;
      if (typeof (wState === null || wState === undefined ? undefined : wState.finished) !== "boolean")
        return null;
      return !!(wState.finished || strict === false && wState.ended === true && wState.length === 0);
    }
    function isReadableEnded(stream) {
      if (!isReadableNodeStream(stream))
        return null;
      if (stream.readableEnded === true)
        return true;
      let rState = stream._readableState;
      if (!rState || rState.errored)
        return false;
      if (typeof (rState === null || rState === undefined ? undefined : rState.ended) !== "boolean")
        return null;
      return rState.ended;
    }
    function isReadableFinished(stream, strict) {
      if (!isReadableNodeStream(stream))
        return null;
      let rState = stream._readableState;
      if (rState !== null && rState !== undefined && rState.errored)
        return false;
      if (typeof (rState === null || rState === undefined ? undefined : rState.endEmitted) !== "boolean")
        return null;
      return !!(rState.endEmitted || strict === false && rState.ended === true && rState.length === 0);
    }
    function isReadable(stream) {
      if (stream && stream[kIsReadable] != null)
        return stream[kIsReadable];
      if (typeof (stream === null || stream === undefined ? undefined : stream.readable) !== "boolean")
        return null;
      if (isDestroyed(stream))
        return false;
      return isReadableNodeStream(stream) && stream.readable && !isReadableFinished(stream);
    }
    function isWritable(stream) {
      if (stream && stream[kIsWritable] != null)
        return stream[kIsWritable];
      if (typeof (stream === null || stream === undefined ? undefined : stream.writable) !== "boolean")
        return null;
      if (isDestroyed(stream))
        return false;
      return isWritableNodeStream(stream) && stream.writable && !isWritableEnded(stream);
    }
    function isFinished(stream, opts) {
      if (!isNodeStream(stream))
        return null;
      if (isDestroyed(stream))
        return true;
      if ((opts === null || opts === undefined ? undefined : opts.readable) !== false && isReadable(stream))
        return false;
      if ((opts === null || opts === undefined ? undefined : opts.writable) !== false && isWritable(stream))
        return false;
      return true;
    }
    function isWritableErrored(stream) {
      var _stream$_writableStat, _stream$_writableStat2;
      if (!isNodeStream(stream))
        return null;
      if (stream.writableErrored)
        return stream.writableErrored;
      return (_stream$_writableStat = (_stream$_writableStat2 = stream._writableState) === null || _stream$_writableStat2 === undefined ? undefined : _stream$_writableStat2.errored) !== null && _stream$_writableStat !== undefined ? _stream$_writableStat : null;
    }
    function isReadableErrored(stream) {
      var _stream$_readableStat, _stream$_readableStat2;
      if (!isNodeStream(stream))
        return null;
      if (stream.readableErrored)
        return stream.readableErrored;
      return (_stream$_readableStat = (_stream$_readableStat2 = stream._readableState) === null || _stream$_readableStat2 === undefined ? undefined : _stream$_readableStat2.errored) !== null && _stream$_readableStat !== undefined ? _stream$_readableStat : null;
    }
    function isClosed(stream) {
      if (!isNodeStream(stream))
        return null;
      if (typeof stream.closed === "boolean")
        return stream.closed;
      let { _writableState: wState, _readableState: rState } = stream;
      if (typeof (wState === null || wState === undefined ? undefined : wState.closed) === "boolean" || typeof (rState === null || rState === undefined ? undefined : rState.closed) === "boolean")
        return (wState === null || wState === undefined ? undefined : wState.closed) || (rState === null || rState === undefined ? undefined : rState.closed);
      if (typeof stream._closed === "boolean" && isOutgoingMessage(stream))
        return stream._closed;
      return null;
    }
    function isOutgoingMessage(stream) {
      return typeof stream._closed === "boolean" && typeof stream._defaultKeepAlive === "boolean" && typeof stream._removedConnection === "boolean" && typeof stream._removedContLen === "boolean";
    }
    function isServerResponse(stream) {
      return typeof stream._sent100 === "boolean" && isOutgoingMessage(stream);
    }
    function isServerRequest(stream) {
      var _stream$req;
      return typeof stream._consuming === "boolean" && typeof stream._dumped === "boolean" && ((_stream$req = stream.req) === null || _stream$req === undefined ? undefined : _stream$req.upgradeOrConnect) === undefined;
    }
    function willEmitClose(stream) {
      if (!isNodeStream(stream))
        return null;
      let { _writableState: wState, _readableState: rState } = stream, state = wState || rState;
      return !state && isServerResponse(stream) || !!(state && state.autoDestroy && state.emitClose && state.closed === false);
    }
    function isDisturbed(stream) {
      var _stream$kIsDisturbed;
      return !!(stream && ((_stream$kIsDisturbed = stream[kIsDisturbed]) !== null && _stream$kIsDisturbed !== undefined ? _stream$kIsDisturbed : stream.readableDidRead || stream.readableAborted));
    }
    function isErrored(stream) {
      var _ref, _ref2, _ref3, _ref4, _ref5, _stream$kIsErrored, _stream$_readableStat3, _stream$_writableStat3, _stream$_readableStat4, _stream$_writableStat4;
      return !!(stream && ((_ref = (_ref2 = (_ref3 = (_ref4 = (_ref5 = (_stream$kIsErrored = stream[kIsErrored]) !== null && _stream$kIsErrored !== undefined ? _stream$kIsErrored : stream.readableErrored) !== null && _ref5 !== undefined ? _ref5 : stream.writableErrored) !== null && _ref4 !== undefined ? _ref4 : (_stream$_readableStat3 = stream._readableState) === null || _stream$_readableStat3 === undefined ? undefined : _stream$_readableStat3.errorEmitted) !== null && _ref3 !== undefined ? _ref3 : (_stream$_writableStat3 = stream._writableState) === null || _stream$_writableStat3 === undefined ? undefined : _stream$_writableStat3.errorEmitted) !== null && _ref2 !== undefined ? _ref2 : (_stream$_readableStat4 = stream._readableState) === null || _stream$_readableStat4 === undefined ? undefined : _stream$_readableStat4.errored) !== null && _ref !== undefined ? _ref : (_stream$_writableStat4 = stream._writableState) === null || _stream$_writableStat4 === undefined ? undefined : _stream$_writableStat4.errored));
    }
    module22.exports = { isDestroyed, kIsDestroyed, isDisturbed, kIsDisturbed, isErrored, kIsErrored, isReadable, kIsReadable, kIsClosedPromise, kControllerErrorFunction, kIsWritable, isClosed, isDuplexNodeStream, isFinished, isIterable: isIterable2, isReadableNodeStream, isReadableStream: isReadableStream2, isReadableEnded, isReadableFinished, isReadableErrored, isNodeStream, isWebStream, isWritable, isWritableNodeStream, isWritableStream, isWritableEnded, isWritableFinished, isWritableErrored, isServerRequest, isServerResponse, willEmitClose, isTransformStream };
  });
  var require_end_of_stream = __commonJS2((exports22, module22) => {
    var process2 = require_process(), { AbortError: AbortError2, codes } = require_errors(), { ERR_INVALID_ARG_TYPE: ERR_INVALID_ARG_TYPE3, ERR_STREAM_PREMATURE_CLOSE } = codes, { kEmptyObject, once } = require_util(), { validateAbortSignal: validateAbortSignal2, validateFunction, validateObject, validateBoolean: validateBoolean2 } = require_validators(), { Promise: Promise2, PromisePrototypeThen, SymbolDispose } = require_primordials(), { isClosed, isReadable, isReadableNodeStream, isReadableStream: isReadableStream2, isReadableFinished, isReadableErrored, isWritable, isWritableNodeStream, isWritableStream, isWritableFinished, isWritableErrored, isNodeStream, willEmitClose: _willEmitClose, kIsClosedPromise } = require_utils(), addAbortListener2;
    function isRequest2(stream) {
      return stream.setHeader && typeof stream.abort === "function";
    }
    var nop = () => {};
    function eos(stream, options, callback) {
      var _options$readable, _options$writable;
      if (arguments.length === 2)
        callback = options, options = kEmptyObject;
      else if (options == null)
        options = kEmptyObject;
      else
        validateObject(options, "options");
      if (validateFunction(callback, "callback"), validateAbortSignal2(options.signal, "options.signal"), callback = once(callback), isReadableStream2(stream) || isWritableStream(stream))
        return eosWeb(stream, options, callback);
      if (!isNodeStream(stream))
        throw new ERR_INVALID_ARG_TYPE3("stream", ["ReadableStream", "WritableStream", "Stream"], stream);
      let readable = (_options$readable = options.readable) !== null && _options$readable !== undefined ? _options$readable : isReadableNodeStream(stream), writable = (_options$writable = options.writable) !== null && _options$writable !== undefined ? _options$writable : isWritableNodeStream(stream), wState = stream._writableState, rState = stream._readableState, onlegacyfinish = () => {
        if (!stream.writable)
          onfinish();
      }, willEmitClose = _willEmitClose(stream) && isReadableNodeStream(stream) === readable && isWritableNodeStream(stream) === writable, writableFinished = isWritableFinished(stream, false), onfinish = () => {
        if (writableFinished = true, stream.destroyed)
          willEmitClose = false;
        if (willEmitClose && (!stream.readable || readable))
          return;
        if (!readable || readableFinished)
          callback.call(stream);
      }, readableFinished = isReadableFinished(stream, false), onend = () => {
        if (readableFinished = true, stream.destroyed)
          willEmitClose = false;
        if (willEmitClose && (!stream.writable || writable))
          return;
        if (!writable || writableFinished)
          callback.call(stream);
      }, onerror = (err) => {
        callback.call(stream, err);
      }, closed = isClosed(stream), onclose = () => {
        closed = true;
        let errored = isWritableErrored(stream) || isReadableErrored(stream);
        if (errored && typeof errored !== "boolean")
          return callback.call(stream, errored);
        if (readable && !readableFinished && isReadableNodeStream(stream, true)) {
          if (!isReadableFinished(stream, false))
            return callback.call(stream, new ERR_STREAM_PREMATURE_CLOSE);
        }
        if (writable && !writableFinished) {
          if (!isWritableFinished(stream, false))
            return callback.call(stream, new ERR_STREAM_PREMATURE_CLOSE);
        }
        callback.call(stream);
      }, onclosed = () => {
        closed = true;
        let errored = isWritableErrored(stream) || isReadableErrored(stream);
        if (errored && typeof errored !== "boolean")
          return callback.call(stream, errored);
        callback.call(stream);
      }, onrequest = () => {
        stream.req.on("finish", onfinish);
      };
      if (isRequest2(stream)) {
        if (stream.on("complete", onfinish), !willEmitClose)
          stream.on("abort", onclose);
        if (stream.req)
          onrequest();
        else
          stream.on("request", onrequest);
      } else if (writable && !wState)
        stream.on("end", onlegacyfinish), stream.on("close", onlegacyfinish);
      if (!willEmitClose && typeof stream.aborted === "boolean")
        stream.on("aborted", onclose);
      if (stream.on("end", onend), stream.on("finish", onfinish), options.error !== false)
        stream.on("error", onerror);
      if (stream.on("close", onclose), closed)
        process2.nextTick(onclose);
      else if (wState !== null && wState !== undefined && wState.errorEmitted || rState !== null && rState !== undefined && rState.errorEmitted) {
        if (!willEmitClose)
          process2.nextTick(onclosed);
      } else if (!readable && (!willEmitClose || isReadable(stream)) && (writableFinished || isWritable(stream) === false))
        process2.nextTick(onclosed);
      else if (!writable && (!willEmitClose || isWritable(stream)) && (readableFinished || isReadable(stream) === false))
        process2.nextTick(onclosed);
      else if (rState && stream.req && stream.aborted)
        process2.nextTick(onclosed);
      let cleanup = () => {
        if (callback = nop, stream.removeListener("aborted", onclose), stream.removeListener("complete", onfinish), stream.removeListener("abort", onclose), stream.removeListener("request", onrequest), stream.req)
          stream.req.removeListener("finish", onfinish);
        stream.removeListener("end", onlegacyfinish), stream.removeListener("close", onlegacyfinish), stream.removeListener("finish", onfinish), stream.removeListener("end", onend), stream.removeListener("error", onerror), stream.removeListener("close", onclose);
      };
      if (options.signal && !closed) {
        let abort = () => {
          let endCallback = callback;
          cleanup(), endCallback.call(stream, new AbortError2(undefined, { cause: options.signal.reason }));
        };
        if (options.signal.aborted)
          process2.nextTick(abort);
        else {
          addAbortListener2 = addAbortListener2 || require_util().addAbortListener;
          let disposable = addAbortListener2(options.signal, abort), originalCallback = callback;
          callback = once((...args) => {
            disposable[SymbolDispose](), originalCallback.apply(stream, args);
          });
        }
      }
      return cleanup;
    }
    function eosWeb(stream, options, callback) {
      let isAborted = false, abort = nop;
      if (options.signal)
        if (abort = () => {
          isAborted = true, callback.call(stream, new AbortError2(undefined, { cause: options.signal.reason }));
        }, options.signal.aborted)
          process2.nextTick(abort);
        else {
          addAbortListener2 = addAbortListener2 || require_util().addAbortListener;
          let disposable = addAbortListener2(options.signal, abort), originalCallback = callback;
          callback = once((...args) => {
            disposable[SymbolDispose](), originalCallback.apply(stream, args);
          });
        }
      let resolverFn = (...args) => {
        if (!isAborted)
          process2.nextTick(() => callback.apply(stream, args));
      };
      return PromisePrototypeThen(stream[kIsClosedPromise].promise, resolverFn, resolverFn), nop;
    }
    function finished(stream, opts) {
      var _opts;
      let autoCleanup = false;
      if (opts === null)
        opts = kEmptyObject;
      if ((_opts = opts) !== null && _opts !== undefined && _opts.cleanup)
        validateBoolean2(opts.cleanup, "cleanup"), autoCleanup = opts.cleanup;
      return new Promise2((resolve, reject) => {
        let cleanup = eos(stream, opts, (err) => {
          if (autoCleanup)
            cleanup();
          if (err)
            reject(err);
          else
            resolve();
        });
      });
    }
    module22.exports = eos;
    module22.exports.finished = finished;
  });
  var require_destroy = __commonJS2((exports22, module22) => {
    var process2 = require_process(), { aggregateTwoErrors, codes: { ERR_MULTIPLE_CALLBACK }, AbortError: AbortError2 } = require_errors(), { Symbol: Symbol2 } = require_primordials(), { kIsDestroyed, isDestroyed, isFinished, isServerRequest } = require_utils(), kDestroy = Symbol2("kDestroy"), kConstruct = Symbol2("kConstruct");
    function checkError(err, w, r) {
      if (err) {
        if (err.stack, w && !w.errored)
          w.errored = err;
        if (r && !r.errored)
          r.errored = err;
      }
    }
    function destroy(err, cb) {
      let r = this._readableState, w = this._writableState, s = w || r;
      if (w !== null && w !== undefined && w.destroyed || r !== null && r !== undefined && r.destroyed) {
        if (typeof cb === "function")
          cb();
        return this;
      }
      if (checkError(err, w, r), w)
        w.destroyed = true;
      if (r)
        r.destroyed = true;
      if (!s.constructed)
        this.once(kDestroy, function(er) {
          _destroy(this, aggregateTwoErrors(er, err), cb);
        });
      else
        _destroy(this, err, cb);
      return this;
    }
    function _destroy(self2, err, cb) {
      let called = false;
      function onDestroy(err2) {
        if (called)
          return;
        called = true;
        let { _readableState: r, _writableState: w } = self2;
        if (checkError(err2, w, r), w)
          w.closed = true;
        if (r)
          r.closed = true;
        if (typeof cb === "function")
          cb(err2);
        if (err2)
          process2.nextTick(emitErrorCloseNT, self2, err2);
        else
          process2.nextTick(emitCloseNT, self2);
      }
      try {
        self2._destroy(err || null, onDestroy);
      } catch (err2) {
        onDestroy(err2);
      }
    }
    function emitErrorCloseNT(self2, err) {
      emitErrorNT(self2, err), emitCloseNT(self2);
    }
    function emitCloseNT(self2) {
      let { _readableState: r, _writableState: w } = self2;
      if (w)
        w.closeEmitted = true;
      if (r)
        r.closeEmitted = true;
      if (w !== null && w !== undefined && w.emitClose || r !== null && r !== undefined && r.emitClose)
        self2.emit("close");
    }
    function emitErrorNT(self2, err) {
      let { _readableState: r, _writableState: w } = self2;
      if (w !== null && w !== undefined && w.errorEmitted || r !== null && r !== undefined && r.errorEmitted)
        return;
      if (w)
        w.errorEmitted = true;
      if (r)
        r.errorEmitted = true;
      self2.emit("error", err);
    }
    function undestroy() {
      let r = this._readableState, w = this._writableState;
      if (r)
        r.constructed = true, r.closed = false, r.closeEmitted = false, r.destroyed = false, r.errored = null, r.errorEmitted = false, r.reading = false, r.ended = r.readable === false, r.endEmitted = r.readable === false;
      if (w)
        w.constructed = true, w.destroyed = false, w.closed = false, w.closeEmitted = false, w.errored = null, w.errorEmitted = false, w.finalCalled = false, w.prefinished = false, w.ended = w.writable === false, w.ending = w.writable === false, w.finished = w.writable === false;
    }
    function errorOrDestroy(stream, err, sync) {
      let { _readableState: r, _writableState: w } = stream;
      if (w !== null && w !== undefined && w.destroyed || r !== null && r !== undefined && r.destroyed)
        return this;
      if (r !== null && r !== undefined && r.autoDestroy || w !== null && w !== undefined && w.autoDestroy)
        stream.destroy(err);
      else if (err) {
        if (err.stack, w && !w.errored)
          w.errored = err;
        if (r && !r.errored)
          r.errored = err;
        if (sync)
          process2.nextTick(emitErrorNT, stream, err);
        else
          emitErrorNT(stream, err);
      }
    }
    function construct(stream, cb) {
      if (typeof stream._construct !== "function")
        return;
      let { _readableState: r, _writableState: w } = stream;
      if (r)
        r.constructed = false;
      if (w)
        w.constructed = false;
      if (stream.once(kConstruct, cb), stream.listenerCount(kConstruct) > 1)
        return;
      process2.nextTick(constructNT, stream);
    }
    function constructNT(stream) {
      let called = false;
      function onConstruct(err) {
        if (called) {
          errorOrDestroy(stream, err !== null && err !== undefined ? err : new ERR_MULTIPLE_CALLBACK);
          return;
        }
        called = true;
        let { _readableState: r, _writableState: w } = stream, s = w || r;
        if (r)
          r.constructed = true;
        if (w)
          w.constructed = true;
        if (s.destroyed)
          stream.emit(kDestroy, err);
        else if (err)
          errorOrDestroy(stream, err, true);
        else
          process2.nextTick(emitConstructNT, stream);
      }
      try {
        stream._construct((err) => {
          process2.nextTick(onConstruct, err);
        });
      } catch (err) {
        process2.nextTick(onConstruct, err);
      }
    }
    function emitConstructNT(stream) {
      stream.emit(kConstruct);
    }
    function isRequest2(stream) {
      return (stream === null || stream === undefined ? undefined : stream.setHeader) && typeof stream.abort === "function";
    }
    function emitCloseLegacy(stream) {
      stream.emit("close");
    }
    function emitErrorCloseLegacy(stream, err) {
      stream.emit("error", err), process2.nextTick(emitCloseLegacy, stream);
    }
    function destroyer(stream, err) {
      if (!stream || isDestroyed(stream))
        return;
      if (!err && !isFinished(stream))
        err = new AbortError2;
      if (isServerRequest(stream))
        stream.socket = null, stream.destroy(err);
      else if (isRequest2(stream))
        stream.abort();
      else if (isRequest2(stream.req))
        stream.req.abort();
      else if (typeof stream.destroy === "function")
        stream.destroy(err);
      else if (typeof stream.close === "function")
        stream.close();
      else if (err)
        process2.nextTick(emitErrorCloseLegacy, stream, err);
      else
        process2.nextTick(emitCloseLegacy, stream);
      if (!stream.destroyed)
        stream[kIsDestroyed] = true;
    }
    module22.exports = { construct, destroyer, destroy, undestroy, errorOrDestroy };
  });
  var require_legacy = __commonJS2((exports22, module22) => {
    var { ArrayIsArray, ObjectSetPrototypeOf } = require_primordials(), { EventEmitter: EE } = (init_events(), __toCommonJS(exports_events));
    function Stream(opts) {
      EE.call(this, opts);
    }
    ObjectSetPrototypeOf(Stream.prototype, EE.prototype);
    ObjectSetPrototypeOf(Stream, EE);
    Stream.prototype.pipe = function(dest, options) {
      let source = this;
      function ondata(chunk) {
        if (dest.writable && dest.write(chunk) === false && source.pause)
          source.pause();
      }
      source.on("data", ondata);
      function ondrain() {
        if (source.readable && source.resume)
          source.resume();
      }
      if (dest.on("drain", ondrain), !dest._isStdio && (!options || options.end !== false))
        source.on("end", onend), source.on("close", onclose);
      let didOnEnd = false;
      function onend() {
        if (didOnEnd)
          return;
        didOnEnd = true, dest.end();
      }
      function onclose() {
        if (didOnEnd)
          return;
        if (didOnEnd = true, typeof dest.destroy === "function")
          dest.destroy();
      }
      function onerror(er) {
        if (cleanup(), EE.listenerCount(this, "error") === 0)
          this.emit("error", er);
      }
      prependListener(source, "error", onerror), prependListener(dest, "error", onerror);
      function cleanup() {
        source.removeListener("data", ondata), dest.removeListener("drain", ondrain), source.removeListener("end", onend), source.removeListener("close", onclose), source.removeListener("error", onerror), dest.removeListener("error", onerror), source.removeListener("end", cleanup), source.removeListener("close", cleanup), dest.removeListener("close", cleanup);
      }
      return source.on("end", cleanup), source.on("close", cleanup), dest.on("close", cleanup), dest.emit("pipe", source), dest;
    };
    function prependListener(emitter, event, fn) {
      if (typeof emitter.prependListener === "function")
        return emitter.prependListener(event, fn);
      if (!emitter._events || !emitter._events[event])
        emitter.on(event, fn);
      else if (ArrayIsArray(emitter._events[event]))
        emitter._events[event].unshift(fn);
      else
        emitter._events[event] = [fn, emitter._events[event]];
    }
    module22.exports = { Stream, prependListener };
  });
  var require_add_abort_signal = __commonJS2((exports22, module22) => {
    var { SymbolDispose } = require_primordials(), { AbortError: AbortError2, codes } = require_errors(), { isNodeStream, isWebStream, kControllerErrorFunction } = require_utils(), eos = require_end_of_stream(), { ERR_INVALID_ARG_TYPE: ERR_INVALID_ARG_TYPE3 } = codes, addAbortListener2, validateAbortSignal2 = (signal, name) => {
      if (typeof signal !== "object" || !("aborted" in signal))
        throw new ERR_INVALID_ARG_TYPE3(name, "AbortSignal", signal);
    };
    module22.exports.addAbortSignal = function(signal, stream) {
      if (validateAbortSignal2(signal, "signal"), !isNodeStream(stream) && !isWebStream(stream))
        throw new ERR_INVALID_ARG_TYPE3("stream", ["ReadableStream", "WritableStream", "Stream"], stream);
      return module22.exports.addAbortSignalNoValidate(signal, stream);
    };
    module22.exports.addAbortSignalNoValidate = function(signal, stream) {
      if (typeof signal !== "object" || !("aborted" in signal))
        return stream;
      let onAbort = isNodeStream(stream) ? () => {
        stream.destroy(new AbortError2(undefined, { cause: signal.reason }));
      } : () => {
        stream[kControllerErrorFunction](new AbortError2(undefined, { cause: signal.reason }));
      };
      if (signal.aborted)
        onAbort();
      else {
        addAbortListener2 = addAbortListener2 || require_util().addAbortListener;
        let disposable = addAbortListener2(signal, onAbort);
        eos(stream, disposable[SymbolDispose]);
      }
      return stream;
    };
  });
  var require_buffer_list = __commonJS2((exports22, module22) => {
    var { StringPrototypeSlice, SymbolIterator, TypedArrayPrototypeSet, Uint8Array: Uint8Array2 } = require_primordials(), { Buffer: Buffer3 } = (init_buffer(), __toCommonJS(exports_buffer)), { inspect: inspect2 } = require_util();
    module22.exports = class {
      constructor() {
        this.head = null, this.tail = null, this.length = 0;
      }
      push(v) {
        let entry = { data: v, next: null };
        if (this.length > 0)
          this.tail.next = entry;
        else
          this.head = entry;
        this.tail = entry, ++this.length;
      }
      unshift(v) {
        let entry = { data: v, next: this.head };
        if (this.length === 0)
          this.tail = entry;
        this.head = entry, ++this.length;
      }
      shift() {
        if (this.length === 0)
          return;
        let ret = this.head.data;
        if (this.length === 1)
          this.head = this.tail = null;
        else
          this.head = this.head.next;
        return --this.length, ret;
      }
      clear() {
        this.head = this.tail = null, this.length = 0;
      }
      join(s) {
        if (this.length === 0)
          return "";
        let p = this.head, ret = "" + p.data;
        while ((p = p.next) !== null)
          ret += s + p.data;
        return ret;
      }
      concat(n) {
        if (this.length === 0)
          return Buffer3.alloc(0);
        let ret = Buffer3.allocUnsafe(n >>> 0), p = this.head, i2 = 0;
        while (p)
          TypedArrayPrototypeSet(ret, p.data, i2), i2 += p.data.length, p = p.next;
        return ret;
      }
      consume(n, hasStrings) {
        let data = this.head.data;
        if (n < data.length) {
          let slice = data.slice(0, n);
          return this.head.data = data.slice(n), slice;
        }
        if (n === data.length)
          return this.shift();
        return hasStrings ? this._getString(n) : this._getBuffer(n);
      }
      first() {
        return this.head.data;
      }
      *[SymbolIterator]() {
        for (let p = this.head;p; p = p.next)
          yield p.data;
      }
      _getString(n) {
        let ret = "", p = this.head, c = 0;
        do {
          let str = p.data;
          if (n > str.length)
            ret += str, n -= str.length;
          else {
            if (n === str.length)
              if (ret += str, ++c, p.next)
                this.head = p.next;
              else
                this.head = this.tail = null;
            else
              ret += StringPrototypeSlice(str, 0, n), this.head = p, p.data = StringPrototypeSlice(str, n);
            break;
          }
          ++c;
        } while ((p = p.next) !== null);
        return this.length -= c, ret;
      }
      _getBuffer(n) {
        let ret = Buffer3.allocUnsafe(n), retLen = n, p = this.head, c = 0;
        do {
          let buf = p.data;
          if (n > buf.length)
            TypedArrayPrototypeSet(ret, buf, retLen - n), n -= buf.length;
          else {
            if (n === buf.length)
              if (TypedArrayPrototypeSet(ret, buf, retLen - n), ++c, p.next)
                this.head = p.next;
              else
                this.head = this.tail = null;
            else
              TypedArrayPrototypeSet(ret, new Uint8Array2(buf.buffer, buf.byteOffset, n), retLen - n), this.head = p, p.data = buf.slice(n);
            break;
          }
          ++c;
        } while ((p = p.next) !== null);
        return this.length -= c, ret;
      }
      [Symbol.for("nodejs.util.inspect.custom")](_, options) {
        return inspect2(this, { ...options, depth: 0, customInspect: false });
      }
    };
  });
  var require_state = __commonJS2((exports22, module22) => {
    var { MathFloor, NumberIsInteger } = require_primordials(), { validateInteger } = require_validators(), { ERR_INVALID_ARG_VALUE } = require_errors().codes, defaultHighWaterMarkBytes = 16384, defaultHighWaterMarkObjectMode = 16;
    function highWaterMarkFrom(options, isDuplex, duplexKey) {
      return options.highWaterMark != null ? options.highWaterMark : isDuplex ? options[duplexKey] : null;
    }
    function getDefaultHighWaterMark(objectMode) {
      return objectMode ? defaultHighWaterMarkObjectMode : defaultHighWaterMarkBytes;
    }
    function setDefaultHighWaterMark(objectMode, value) {
      if (validateInteger(value, "value", 0), objectMode)
        defaultHighWaterMarkObjectMode = value;
      else
        defaultHighWaterMarkBytes = value;
    }
    function getHighWaterMark(state, options, duplexKey, isDuplex) {
      let hwm = highWaterMarkFrom(options, isDuplex, duplexKey);
      if (hwm != null) {
        if (!NumberIsInteger(hwm) || hwm < 0) {
          let name = isDuplex ? `options.${duplexKey}` : "options.highWaterMark";
          throw new ERR_INVALID_ARG_VALUE(name, hwm);
        }
        return MathFloor(hwm);
      }
      return getDefaultHighWaterMark(state.objectMode);
    }
    module22.exports = { getHighWaterMark, getDefaultHighWaterMark, setDefaultHighWaterMark };
  });
  var require_safe_buffer = __commonJS2((exports22, module22) => {
    /*! safe-buffer. MIT License. Feross Aboukhadijeh <https://feross.org/opensource> */
    var buffer = (init_buffer(), __toCommonJS(exports_buffer)), Buffer3 = buffer.Buffer;
    function copyProps(src, dst) {
      for (var key in src)
        dst[key] = src[key];
    }
    if (Buffer3.from && Buffer3.alloc && Buffer3.allocUnsafe && Buffer3.allocUnsafeSlow)
      module22.exports = buffer;
    else
      copyProps(buffer, exports22), exports22.Buffer = SafeBuffer;
    function SafeBuffer(arg, encodingOrOffset, length) {
      return Buffer3(arg, encodingOrOffset, length);
    }
    SafeBuffer.prototype = Object.create(Buffer3.prototype);
    copyProps(Buffer3, SafeBuffer);
    SafeBuffer.from = function(arg, encodingOrOffset, length) {
      if (typeof arg === "number")
        throw TypeError("Argument must not be a number");
      return Buffer3(arg, encodingOrOffset, length);
    };
    SafeBuffer.alloc = function(size, fill, encoding) {
      if (typeof size !== "number")
        throw TypeError("Argument must be a number");
      var buf = Buffer3(size);
      if (fill !== undefined)
        if (typeof encoding === "string")
          buf.fill(fill, encoding);
        else
          buf.fill(fill);
      else
        buf.fill(0);
      return buf;
    };
    SafeBuffer.allocUnsafe = function(size) {
      if (typeof size !== "number")
        throw TypeError("Argument must be a number");
      return Buffer3(size);
    };
    SafeBuffer.allocUnsafeSlow = function(size) {
      if (typeof size !== "number")
        throw TypeError("Argument must be a number");
      return buffer.SlowBuffer(size);
    };
  });
  var require_string_decoder = __commonJS2((exports22) => {
    var Buffer3 = require_safe_buffer().Buffer, isEncoding = Buffer3.isEncoding || function(encoding) {
      switch (encoding = "" + encoding, encoding && encoding.toLowerCase()) {
        case "hex":
        case "utf8":
        case "utf-8":
        case "ascii":
        case "binary":
        case "base64":
        case "ucs2":
        case "ucs-2":
        case "utf16le":
        case "utf-16le":
        case "raw":
          return true;
        default:
          return false;
      }
    };
    function _normalizeEncoding(enc) {
      if (!enc)
        return "utf8";
      var retried;
      while (true)
        switch (enc) {
          case "utf8":
          case "utf-8":
            return "utf8";
          case "ucs2":
          case "ucs-2":
          case "utf16le":
          case "utf-16le":
            return "utf16le";
          case "latin1":
          case "binary":
            return "latin1";
          case "base64":
          case "ascii":
          case "hex":
            return enc;
          default:
            if (retried)
              return;
            enc = ("" + enc).toLowerCase(), retried = true;
        }
    }
    function normalizeEncoding(enc) {
      var nenc = _normalizeEncoding(enc);
      if (typeof nenc !== "string" && (Buffer3.isEncoding === isEncoding || !isEncoding(enc)))
        throw Error("Unknown encoding: " + enc);
      return nenc || enc;
    }
    exports22.StringDecoder = StringDecoder;
    function StringDecoder(encoding) {
      this.encoding = normalizeEncoding(encoding);
      var nb;
      switch (this.encoding) {
        case "utf16le":
          this.text = utf16Text, this.end = utf16End, nb = 4;
          break;
        case "utf8":
          this.fillLast = utf8FillLast, nb = 4;
          break;
        case "base64":
          this.text = base64Text, this.end = base64End, nb = 3;
          break;
        default:
          this.write = simpleWrite, this.end = simpleEnd;
          return;
      }
      this.lastNeed = 0, this.lastTotal = 0, this.lastChar = Buffer3.allocUnsafe(nb);
    }
    StringDecoder.prototype.write = function(buf) {
      if (buf.length === 0)
        return "";
      var r, i2;
      if (this.lastNeed) {
        if (r = this.fillLast(buf), r === undefined)
          return "";
        i2 = this.lastNeed, this.lastNeed = 0;
      } else
        i2 = 0;
      if (i2 < buf.length)
        return r ? r + this.text(buf, i2) : this.text(buf, i2);
      return r || "";
    };
    StringDecoder.prototype.end = utf8End;
    StringDecoder.prototype.text = utf8Text;
    StringDecoder.prototype.fillLast = function(buf) {
      if (this.lastNeed <= buf.length)
        return buf.copy(this.lastChar, this.lastTotal - this.lastNeed, 0, this.lastNeed), this.lastChar.toString(this.encoding, 0, this.lastTotal);
      buf.copy(this.lastChar, this.lastTotal - this.lastNeed, 0, buf.length), this.lastNeed -= buf.length;
    };
    function utf8CheckByte(byte) {
      if (byte <= 127)
        return 0;
      else if (byte >> 5 === 6)
        return 2;
      else if (byte >> 4 === 14)
        return 3;
      else if (byte >> 3 === 30)
        return 4;
      return byte >> 6 === 2 ? -1 : -2;
    }
    function utf8CheckIncomplete(self2, buf, i2) {
      var j = buf.length - 1;
      if (j < i2)
        return 0;
      var nb = utf8CheckByte(buf[j]);
      if (nb >= 0) {
        if (nb > 0)
          self2.lastNeed = nb - 1;
        return nb;
      }
      if (--j < i2 || nb === -2)
        return 0;
      if (nb = utf8CheckByte(buf[j]), nb >= 0) {
        if (nb > 0)
          self2.lastNeed = nb - 2;
        return nb;
      }
      if (--j < i2 || nb === -2)
        return 0;
      if (nb = utf8CheckByte(buf[j]), nb >= 0) {
        if (nb > 0)
          if (nb === 2)
            nb = 0;
          else
            self2.lastNeed = nb - 3;
        return nb;
      }
      return 0;
    }
    function utf8CheckExtraBytes(self2, buf, p) {
      if ((buf[0] & 192) !== 128)
        return self2.lastNeed = 0, "�";
      if (self2.lastNeed > 1 && buf.length > 1) {
        if ((buf[1] & 192) !== 128)
          return self2.lastNeed = 1, "�";
        if (self2.lastNeed > 2 && buf.length > 2) {
          if ((buf[2] & 192) !== 128)
            return self2.lastNeed = 2, "�";
        }
      }
    }
    function utf8FillLast(buf) {
      var p = this.lastTotal - this.lastNeed, r = utf8CheckExtraBytes(this, buf, p);
      if (r !== undefined)
        return r;
      if (this.lastNeed <= buf.length)
        return buf.copy(this.lastChar, p, 0, this.lastNeed), this.lastChar.toString(this.encoding, 0, this.lastTotal);
      buf.copy(this.lastChar, p, 0, buf.length), this.lastNeed -= buf.length;
    }
    function utf8Text(buf, i2) {
      var total = utf8CheckIncomplete(this, buf, i2);
      if (!this.lastNeed)
        return buf.toString("utf8", i2);
      this.lastTotal = total;
      var end = buf.length - (total - this.lastNeed);
      return buf.copy(this.lastChar, 0, end), buf.toString("utf8", i2, end);
    }
    function utf8End(buf) {
      var r = buf && buf.length ? this.write(buf) : "";
      if (this.lastNeed)
        return r + "�";
      return r;
    }
    function utf16Text(buf, i2) {
      if ((buf.length - i2) % 2 === 0) {
        var r = buf.toString("utf16le", i2);
        if (r) {
          var c = r.charCodeAt(r.length - 1);
          if (c >= 55296 && c <= 56319)
            return this.lastNeed = 2, this.lastTotal = 4, this.lastChar[0] = buf[buf.length - 2], this.lastChar[1] = buf[buf.length - 1], r.slice(0, -1);
        }
        return r;
      }
      return this.lastNeed = 1, this.lastTotal = 2, this.lastChar[0] = buf[buf.length - 1], buf.toString("utf16le", i2, buf.length - 1);
    }
    function utf16End(buf) {
      var r = buf && buf.length ? this.write(buf) : "";
      if (this.lastNeed) {
        var end = this.lastTotal - this.lastNeed;
        return r + this.lastChar.toString("utf16le", 0, end);
      }
      return r;
    }
    function base64Text(buf, i2) {
      var n = (buf.length - i2) % 3;
      if (n === 0)
        return buf.toString("base64", i2);
      if (this.lastNeed = 3 - n, this.lastTotal = 3, n === 1)
        this.lastChar[0] = buf[buf.length - 1];
      else
        this.lastChar[0] = buf[buf.length - 2], this.lastChar[1] = buf[buf.length - 1];
      return buf.toString("base64", i2, buf.length - n);
    }
    function base64End(buf) {
      var r = buf && buf.length ? this.write(buf) : "";
      if (this.lastNeed)
        return r + this.lastChar.toString("base64", 0, 3 - this.lastNeed);
      return r;
    }
    function simpleWrite(buf) {
      return buf.toString(this.encoding);
    }
    function simpleEnd(buf) {
      return buf && buf.length ? this.write(buf) : "";
    }
  });
  var require_from = __commonJS2((exports22, module22) => {
    var process2 = require_process(), { PromisePrototypeThen, SymbolAsyncIterator, SymbolIterator } = require_primordials(), { Buffer: Buffer3 } = (init_buffer(), __toCommonJS(exports_buffer)), { ERR_INVALID_ARG_TYPE: ERR_INVALID_ARG_TYPE3, ERR_STREAM_NULL_VALUES } = require_errors().codes;
    function from2(Readable, iterable, opts) {
      let iterator2;
      if (typeof iterable === "string" || iterable instanceof Buffer3)
        return new Readable({ objectMode: true, ...opts, read() {
          this.push(iterable), this.push(null);
        } });
      let isAsync;
      if (iterable && iterable[SymbolAsyncIterator])
        isAsync = true, iterator2 = iterable[SymbolAsyncIterator]();
      else if (iterable && iterable[SymbolIterator])
        isAsync = false, iterator2 = iterable[SymbolIterator]();
      else
        throw new ERR_INVALID_ARG_TYPE3("iterable", ["Iterable"], iterable);
      let readable = new Readable({ objectMode: true, highWaterMark: 1, ...opts }), reading = false;
      readable._read = function() {
        if (!reading)
          reading = true, next();
      }, readable._destroy = function(error, cb) {
        PromisePrototypeThen(close(error), () => process2.nextTick(cb, error), (e) => process2.nextTick(cb, e || error));
      };
      async function close(error) {
        let hadError = error !== undefined && error !== null, hasThrow = typeof iterator2.throw === "function";
        if (hadError && hasThrow) {
          let { value, done } = await iterator2.throw(error);
          if (await value, done)
            return;
        }
        if (typeof iterator2.return === "function") {
          let { value } = await iterator2.return();
          await value;
        }
      }
      async function next() {
        for (;; ) {
          try {
            let { value, done } = isAsync ? await iterator2.next() : iterator2.next();
            if (done)
              readable.push(null);
            else {
              let res = value && typeof value.then === "function" ? await value : value;
              if (res === null)
                throw reading = false, new ERR_STREAM_NULL_VALUES;
              else if (readable.push(res))
                continue;
              else
                reading = false;
            }
          } catch (err) {
            readable.destroy(err);
          }
          break;
        }
      }
      return readable;
    }
    module22.exports = from2;
  });
  var require_readable = __commonJS2((exports22, module22) => {
    var process2 = require_process(), { ArrayPrototypeIndexOf, NumberIsInteger, NumberIsNaN, NumberParseInt, ObjectDefineProperties, ObjectKeys, ObjectSetPrototypeOf, Promise: Promise2, SafeSet, SymbolAsyncDispose, SymbolAsyncIterator, Symbol: Symbol2 } = require_primordials();
    module22.exports = Readable;
    Readable.ReadableState = ReadableState;
    var { EventEmitter: EE } = (init_events(), __toCommonJS(exports_events)), { Stream, prependListener } = require_legacy(), { Buffer: Buffer3 } = (init_buffer(), __toCommonJS(exports_buffer)), { addAbortSignal } = require_add_abort_signal(), eos = require_end_of_stream(), debug = require_util().debuglog("stream", (fn) => {
      debug = fn;
    }), BufferList = require_buffer_list(), destroyImpl = require_destroy(), { getHighWaterMark, getDefaultHighWaterMark } = require_state(), { aggregateTwoErrors, codes: { ERR_INVALID_ARG_TYPE: ERR_INVALID_ARG_TYPE3, ERR_METHOD_NOT_IMPLEMENTED, ERR_OUT_OF_RANGE: ERR_OUT_OF_RANGE3, ERR_STREAM_PUSH_AFTER_EOF, ERR_STREAM_UNSHIFT_AFTER_END_EVENT }, AbortError: AbortError2 } = require_errors(), { validateObject } = require_validators(), kPaused = Symbol2("kPaused"), { StringDecoder } = require_string_decoder(), from2 = require_from();
    ObjectSetPrototypeOf(Readable.prototype, Stream.prototype);
    ObjectSetPrototypeOf(Readable, Stream);
    var nop = () => {}, { errorOrDestroy } = destroyImpl, kObjectMode = 1, kEnded = 2, kEndEmitted = 4, kReading = 8, kConstructed = 16, kSync = 32, kNeedReadable = 64, kEmittedReadable = 128, kReadableListening = 256, kResumeScheduled = 512, kErrorEmitted = 1024, kEmitClose = 2048, kAutoDestroy = 4096, kDestroyed = 8192, kClosed = 16384, kCloseEmitted = 32768, kMultiAwaitDrain = 65536, kReadingMore = 131072, kDataEmitted = 262144;
    function makeBitMapDescriptor(bit) {
      return { enumerable: false, get() {
        return (this.state & bit) !== 0;
      }, set(value) {
        if (value)
          this.state |= bit;
        else
          this.state &= ~bit;
      } };
    }
    ObjectDefineProperties(ReadableState.prototype, { objectMode: makeBitMapDescriptor(kObjectMode), ended: makeBitMapDescriptor(kEnded), endEmitted: makeBitMapDescriptor(kEndEmitted), reading: makeBitMapDescriptor(kReading), constructed: makeBitMapDescriptor(kConstructed), sync: makeBitMapDescriptor(kSync), needReadable: makeBitMapDescriptor(kNeedReadable), emittedReadable: makeBitMapDescriptor(kEmittedReadable), readableListening: makeBitMapDescriptor(kReadableListening), resumeScheduled: makeBitMapDescriptor(kResumeScheduled), errorEmitted: makeBitMapDescriptor(kErrorEmitted), emitClose: makeBitMapDescriptor(kEmitClose), autoDestroy: makeBitMapDescriptor(kAutoDestroy), destroyed: makeBitMapDescriptor(kDestroyed), closed: makeBitMapDescriptor(kClosed), closeEmitted: makeBitMapDescriptor(kCloseEmitted), multiAwaitDrain: makeBitMapDescriptor(kMultiAwaitDrain), readingMore: makeBitMapDescriptor(kReadingMore), dataEmitted: makeBitMapDescriptor(kDataEmitted) });
    function ReadableState(options, stream, isDuplex) {
      if (typeof isDuplex !== "boolean")
        isDuplex = stream instanceof require_duplex();
      if (this.state = kEmitClose | kAutoDestroy | kConstructed | kSync, options && options.objectMode)
        this.state |= kObjectMode;
      if (isDuplex && options && options.readableObjectMode)
        this.state |= kObjectMode;
      if (this.highWaterMark = options ? getHighWaterMark(this, options, "readableHighWaterMark", isDuplex) : getDefaultHighWaterMark(false), this.buffer = new BufferList, this.length = 0, this.pipes = [], this.flowing = null, this[kPaused] = null, options && options.emitClose === false)
        this.state &= ~kEmitClose;
      if (options && options.autoDestroy === false)
        this.state &= ~kAutoDestroy;
      if (this.errored = null, this.defaultEncoding = options && options.defaultEncoding || "utf8", this.awaitDrainWriters = null, this.decoder = null, this.encoding = null, options && options.encoding)
        this.decoder = new StringDecoder(options.encoding), this.encoding = options.encoding;
    }
    function Readable(options) {
      if (!(this instanceof Readable))
        return new Readable(options);
      let isDuplex = this instanceof require_duplex();
      if (this._readableState = new ReadableState(options, this, isDuplex), options) {
        if (typeof options.read === "function")
          this._read = options.read;
        if (typeof options.destroy === "function")
          this._destroy = options.destroy;
        if (typeof options.construct === "function")
          this._construct = options.construct;
        if (options.signal && !isDuplex)
          addAbortSignal(options.signal, this);
      }
      Stream.call(this, options), destroyImpl.construct(this, () => {
        if (this._readableState.needReadable)
          maybeReadMore(this, this._readableState);
      });
    }
    Readable.prototype.destroy = destroyImpl.destroy;
    Readable.prototype._undestroy = destroyImpl.undestroy;
    Readable.prototype._destroy = function(err, cb) {
      cb(err);
    };
    Readable.prototype[EE.captureRejectionSymbol] = function(err) {
      this.destroy(err);
    };
    Readable.prototype[SymbolAsyncDispose] = function() {
      let error;
      if (!this.destroyed)
        error = this.readableEnded ? null : new AbortError2, this.destroy(error);
      return new Promise2((resolve, reject) => eos(this, (err) => err && err !== error ? reject(err) : resolve(null)));
    };
    Readable.prototype.push = function(chunk, encoding) {
      return readableAddChunk(this, chunk, encoding, false);
    };
    Readable.prototype.unshift = function(chunk, encoding) {
      return readableAddChunk(this, chunk, encoding, true);
    };
    function readableAddChunk(stream, chunk, encoding, addToFront) {
      debug("readableAddChunk", chunk);
      let state = stream._readableState, err;
      if ((state.state & kObjectMode) === 0) {
        if (typeof chunk === "string") {
          if (encoding = encoding || state.defaultEncoding, state.encoding !== encoding)
            if (addToFront && state.encoding)
              chunk = Buffer3.from(chunk, encoding).toString(state.encoding);
            else
              chunk = Buffer3.from(chunk, encoding), encoding = "";
        } else if (chunk instanceof Buffer3)
          encoding = "";
        else if (Stream._isUint8Array(chunk))
          chunk = Stream._uint8ArrayToBuffer(chunk), encoding = "";
        else if (chunk != null)
          err = new ERR_INVALID_ARG_TYPE3("chunk", ["string", "Buffer", "Uint8Array"], chunk);
      }
      if (err)
        errorOrDestroy(stream, err);
      else if (chunk === null)
        state.state &= ~kReading, onEofChunk(stream, state);
      else if ((state.state & kObjectMode) !== 0 || chunk && chunk.length > 0)
        if (addToFront)
          if ((state.state & kEndEmitted) !== 0)
            errorOrDestroy(stream, new ERR_STREAM_UNSHIFT_AFTER_END_EVENT);
          else if (state.destroyed || state.errored)
            return false;
          else
            addChunk(stream, state, chunk, true);
        else if (state.ended)
          errorOrDestroy(stream, new ERR_STREAM_PUSH_AFTER_EOF);
        else if (state.destroyed || state.errored)
          return false;
        else if (state.state &= ~kReading, state.decoder && !encoding)
          if (chunk = state.decoder.write(chunk), state.objectMode || chunk.length !== 0)
            addChunk(stream, state, chunk, false);
          else
            maybeReadMore(stream, state);
        else
          addChunk(stream, state, chunk, false);
      else if (!addToFront)
        state.state &= ~kReading, maybeReadMore(stream, state);
      return !state.ended && (state.length < state.highWaterMark || state.length === 0);
    }
    function addChunk(stream, state, chunk, addToFront) {
      if (state.flowing && state.length === 0 && !state.sync && stream.listenerCount("data") > 0) {
        if ((state.state & kMultiAwaitDrain) !== 0)
          state.awaitDrainWriters.clear();
        else
          state.awaitDrainWriters = null;
        state.dataEmitted = true, stream.emit("data", chunk);
      } else {
        if (state.length += state.objectMode ? 1 : chunk.length, addToFront)
          state.buffer.unshift(chunk);
        else
          state.buffer.push(chunk);
        if ((state.state & kNeedReadable) !== 0)
          emitReadable(stream);
      }
      maybeReadMore(stream, state);
    }
    Readable.prototype.isPaused = function() {
      let state = this._readableState;
      return state[kPaused] === true || state.flowing === false;
    };
    Readable.prototype.setEncoding = function(enc) {
      let decoder = new StringDecoder(enc);
      this._readableState.decoder = decoder, this._readableState.encoding = this._readableState.decoder.encoding;
      let buffer = this._readableState.buffer, content = "";
      for (let data of buffer)
        content += decoder.write(data);
      if (buffer.clear(), content !== "")
        buffer.push(content);
      return this._readableState.length = content.length, this;
    };
    var MAX_HWM = 1073741824;
    function computeNewHighWaterMark(n) {
      if (n > MAX_HWM)
        throw new ERR_OUT_OF_RANGE3("size", "<= 1GiB", n);
      else
        n--, n |= n >>> 1, n |= n >>> 2, n |= n >>> 4, n |= n >>> 8, n |= n >>> 16, n++;
      return n;
    }
    function howMuchToRead(n, state) {
      if (n <= 0 || state.length === 0 && state.ended)
        return 0;
      if ((state.state & kObjectMode) !== 0)
        return 1;
      if (NumberIsNaN(n)) {
        if (state.flowing && state.length)
          return state.buffer.first().length;
        return state.length;
      }
      if (n <= state.length)
        return n;
      return state.ended ? state.length : 0;
    }
    Readable.prototype.read = function(n) {
      if (debug("read", n), n === undefined)
        n = NaN;
      else if (!NumberIsInteger(n))
        n = NumberParseInt(n, 10);
      let state = this._readableState, nOrig = n;
      if (n > state.highWaterMark)
        state.highWaterMark = computeNewHighWaterMark(n);
      if (n !== 0)
        state.state &= ~kEmittedReadable;
      if (n === 0 && state.needReadable && ((state.highWaterMark !== 0 ? state.length >= state.highWaterMark : state.length > 0) || state.ended)) {
        if (debug("read: emitReadable", state.length, state.ended), state.length === 0 && state.ended)
          endReadable(this);
        else
          emitReadable(this);
        return null;
      }
      if (n = howMuchToRead(n, state), n === 0 && state.ended) {
        if (state.length === 0)
          endReadable(this);
        return null;
      }
      let doRead = (state.state & kNeedReadable) !== 0;
      if (debug("need readable", doRead), state.length === 0 || state.length - n < state.highWaterMark)
        doRead = true, debug("length less than watermark", doRead);
      if (state.ended || state.reading || state.destroyed || state.errored || !state.constructed)
        doRead = false, debug("reading, ended or constructing", doRead);
      else if (doRead) {
        if (debug("do read"), state.state |= kReading | kSync, state.length === 0)
          state.state |= kNeedReadable;
        try {
          this._read(state.highWaterMark);
        } catch (err) {
          errorOrDestroy(this, err);
        }
        if (state.state &= ~kSync, !state.reading)
          n = howMuchToRead(nOrig, state);
      }
      let ret;
      if (n > 0)
        ret = fromList(n, state);
      else
        ret = null;
      if (ret === null)
        state.needReadable = state.length <= state.highWaterMark, n = 0;
      else if (state.length -= n, state.multiAwaitDrain)
        state.awaitDrainWriters.clear();
      else
        state.awaitDrainWriters = null;
      if (state.length === 0) {
        if (!state.ended)
          state.needReadable = true;
        if (nOrig !== n && state.ended)
          endReadable(this);
      }
      if (ret !== null && !state.errorEmitted && !state.closeEmitted)
        state.dataEmitted = true, this.emit("data", ret);
      return ret;
    };
    function onEofChunk(stream, state) {
      if (debug("onEofChunk"), state.ended)
        return;
      if (state.decoder) {
        let chunk = state.decoder.end();
        if (chunk && chunk.length)
          state.buffer.push(chunk), state.length += state.objectMode ? 1 : chunk.length;
      }
      if (state.ended = true, state.sync)
        emitReadable(stream);
      else
        state.needReadable = false, state.emittedReadable = true, emitReadable_(stream);
    }
    function emitReadable(stream) {
      let state = stream._readableState;
      if (debug("emitReadable", state.needReadable, state.emittedReadable), state.needReadable = false, !state.emittedReadable)
        debug("emitReadable", state.flowing), state.emittedReadable = true, process2.nextTick(emitReadable_, stream);
    }
    function emitReadable_(stream) {
      let state = stream._readableState;
      if (debug("emitReadable_", state.destroyed, state.length, state.ended), !state.destroyed && !state.errored && (state.length || state.ended))
        stream.emit("readable"), state.emittedReadable = false;
      state.needReadable = !state.flowing && !state.ended && state.length <= state.highWaterMark, flow(stream);
    }
    function maybeReadMore(stream, state) {
      if (!state.readingMore && state.constructed)
        state.readingMore = true, process2.nextTick(maybeReadMore_, stream, state);
    }
    function maybeReadMore_(stream, state) {
      while (!state.reading && !state.ended && (state.length < state.highWaterMark || state.flowing && state.length === 0)) {
        let len2 = state.length;
        if (debug("maybeReadMore read 0"), stream.read(0), len2 === state.length)
          break;
      }
      state.readingMore = false;
    }
    Readable.prototype._read = function(n) {
      throw new ERR_METHOD_NOT_IMPLEMENTED("_read()");
    };
    Readable.prototype.pipe = function(dest, pipeOpts) {
      let src = this, state = this._readableState;
      if (state.pipes.length === 1) {
        if (!state.multiAwaitDrain)
          state.multiAwaitDrain = true, state.awaitDrainWriters = new SafeSet(state.awaitDrainWriters ? [state.awaitDrainWriters] : []);
      }
      state.pipes.push(dest), debug("pipe count=%d opts=%j", state.pipes.length, pipeOpts);
      let endFn = (!pipeOpts || pipeOpts.end !== false) && dest !== process2.stdout && dest !== process2.stderr ? onend : unpipe;
      if (state.endEmitted)
        process2.nextTick(endFn);
      else
        src.once("end", endFn);
      dest.on("unpipe", onunpipe);
      function onunpipe(readable, unpipeInfo) {
        if (debug("onunpipe"), readable === src) {
          if (unpipeInfo && unpipeInfo.hasUnpiped === false)
            unpipeInfo.hasUnpiped = true, cleanup();
        }
      }
      function onend() {
        debug("onend"), dest.end();
      }
      let ondrain, cleanedUp = false;
      function cleanup() {
        if (debug("cleanup"), dest.removeListener("close", onclose), dest.removeListener("finish", onfinish), ondrain)
          dest.removeListener("drain", ondrain);
        if (dest.removeListener("error", onerror), dest.removeListener("unpipe", onunpipe), src.removeListener("end", onend), src.removeListener("end", unpipe), src.removeListener("data", ondata), cleanedUp = true, ondrain && state.awaitDrainWriters && (!dest._writableState || dest._writableState.needDrain))
          ondrain();
      }
      function pause() {
        if (!cleanedUp) {
          if (state.pipes.length === 1 && state.pipes[0] === dest)
            debug("false write response, pause", 0), state.awaitDrainWriters = dest, state.multiAwaitDrain = false;
          else if (state.pipes.length > 1 && state.pipes.includes(dest))
            debug("false write response, pause", state.awaitDrainWriters.size), state.awaitDrainWriters.add(dest);
          src.pause();
        }
        if (!ondrain)
          ondrain = pipeOnDrain(src, dest), dest.on("drain", ondrain);
      }
      src.on("data", ondata);
      function ondata(chunk) {
        debug("ondata");
        let ret = dest.write(chunk);
        if (debug("dest.write", ret), ret === false)
          pause();
      }
      function onerror(er) {
        if (debug("onerror", er), unpipe(), dest.removeListener("error", onerror), dest.listenerCount("error") === 0) {
          let s = dest._writableState || dest._readableState;
          if (s && !s.errorEmitted)
            errorOrDestroy(dest, er);
          else
            dest.emit("error", er);
        }
      }
      prependListener(dest, "error", onerror);
      function onclose() {
        dest.removeListener("finish", onfinish), unpipe();
      }
      dest.once("close", onclose);
      function onfinish() {
        debug("onfinish"), dest.removeListener("close", onclose), unpipe();
      }
      dest.once("finish", onfinish);
      function unpipe() {
        debug("unpipe"), src.unpipe(dest);
      }
      if (dest.emit("pipe", src), dest.writableNeedDrain === true)
        pause();
      else if (!state.flowing)
        debug("pipe resume"), src.resume();
      return dest;
    };
    function pipeOnDrain(src, dest) {
      return function() {
        let state = src._readableState;
        if (state.awaitDrainWriters === dest)
          debug("pipeOnDrain", 1), state.awaitDrainWriters = null;
        else if (state.multiAwaitDrain)
          debug("pipeOnDrain", state.awaitDrainWriters.size), state.awaitDrainWriters.delete(dest);
        if ((!state.awaitDrainWriters || state.awaitDrainWriters.size === 0) && src.listenerCount("data"))
          src.resume();
      };
    }
    Readable.prototype.unpipe = function(dest) {
      let state = this._readableState, unpipeInfo = { hasUnpiped: false };
      if (state.pipes.length === 0)
        return this;
      if (!dest) {
        let dests = state.pipes;
        state.pipes = [], this.pause();
        for (let i2 = 0;i2 < dests.length; i2++)
          dests[i2].emit("unpipe", this, { hasUnpiped: false });
        return this;
      }
      let index = ArrayPrototypeIndexOf(state.pipes, dest);
      if (index === -1)
        return this;
      if (state.pipes.splice(index, 1), state.pipes.length === 0)
        this.pause();
      return dest.emit("unpipe", this, unpipeInfo), this;
    };
    Readable.prototype.on = function(ev, fn) {
      let res = Stream.prototype.on.call(this, ev, fn), state = this._readableState;
      if (ev === "data") {
        if (state.readableListening = this.listenerCount("readable") > 0, state.flowing !== false)
          this.resume();
      } else if (ev === "readable") {
        if (!state.endEmitted && !state.readableListening) {
          if (state.readableListening = state.needReadable = true, state.flowing = false, state.emittedReadable = false, debug("on readable", state.length, state.reading), state.length)
            emitReadable(this);
          else if (!state.reading)
            process2.nextTick(nReadingNextTick, this);
        }
      }
      return res;
    };
    Readable.prototype.addListener = Readable.prototype.on;
    Readable.prototype.removeListener = function(ev, fn) {
      let res = Stream.prototype.removeListener.call(this, ev, fn);
      if (ev === "readable")
        process2.nextTick(updateReadableListening, this);
      return res;
    };
    Readable.prototype.off = Readable.prototype.removeListener;
    Readable.prototype.removeAllListeners = function(ev) {
      let res = Stream.prototype.removeAllListeners.apply(this, arguments);
      if (ev === "readable" || ev === undefined)
        process2.nextTick(updateReadableListening, this);
      return res;
    };
    function updateReadableListening(self2) {
      let state = self2._readableState;
      if (state.readableListening = self2.listenerCount("readable") > 0, state.resumeScheduled && state[kPaused] === false)
        state.flowing = true;
      else if (self2.listenerCount("data") > 0)
        self2.resume();
      else if (!state.readableListening)
        state.flowing = null;
    }
    function nReadingNextTick(self2) {
      debug("readable nexttick read 0"), self2.read(0);
    }
    Readable.prototype.resume = function() {
      let state = this._readableState;
      if (!state.flowing)
        debug("resume"), state.flowing = !state.readableListening, resume(this, state);
      return state[kPaused] = false, this;
    };
    function resume(stream, state) {
      if (!state.resumeScheduled)
        state.resumeScheduled = true, process2.nextTick(resume_, stream, state);
    }
    function resume_(stream, state) {
      if (debug("resume", state.reading), !state.reading)
        stream.read(0);
      if (state.resumeScheduled = false, stream.emit("resume"), flow(stream), state.flowing && !state.reading)
        stream.read(0);
    }
    Readable.prototype.pause = function() {
      if (debug("call pause flowing=%j", this._readableState.flowing), this._readableState.flowing !== false)
        debug("pause"), this._readableState.flowing = false, this.emit("pause");
      return this._readableState[kPaused] = true, this;
    };
    function flow(stream) {
      let state = stream._readableState;
      debug("flow", state.flowing);
      while (state.flowing && stream.read() !== null)
        ;
    }
    Readable.prototype.wrap = function(stream) {
      let paused = false;
      stream.on("data", (chunk) => {
        if (!this.push(chunk) && stream.pause)
          paused = true, stream.pause();
      }), stream.on("end", () => {
        this.push(null);
      }), stream.on("error", (err) => {
        errorOrDestroy(this, err);
      }), stream.on("close", () => {
        this.destroy();
      }), stream.on("destroy", () => {
        this.destroy();
      }), this._read = () => {
        if (paused && stream.resume)
          paused = false, stream.resume();
      };
      let streamKeys = ObjectKeys(stream);
      for (let j = 1;j < streamKeys.length; j++) {
        let i2 = streamKeys[j];
        if (this[i2] === undefined && typeof stream[i2] === "function")
          this[i2] = stream[i2].bind(stream);
      }
      return this;
    };
    Readable.prototype[SymbolAsyncIterator] = function() {
      return streamToAsyncIterator(this);
    };
    Readable.prototype.iterator = function(options) {
      if (options !== undefined)
        validateObject(options, "options");
      return streamToAsyncIterator(this, options);
    };
    function streamToAsyncIterator(stream, options) {
      if (typeof stream.read !== "function")
        stream = Readable.wrap(stream, { objectMode: true });
      let iter = createAsyncIterator(stream, options);
      return iter.stream = stream, iter;
    }
    async function* createAsyncIterator(stream, options) {
      let callback = nop;
      function next(resolve) {
        if (this === stream)
          callback(), callback = nop;
        else
          callback = resolve;
      }
      stream.on("readable", next);
      let error, cleanup = eos(stream, { writable: false }, (err) => {
        error = err ? aggregateTwoErrors(error, err) : null, callback(), callback = nop;
      });
      try {
        while (true) {
          let chunk = stream.destroyed ? null : stream.read();
          if (chunk !== null)
            yield chunk;
          else if (error)
            throw error;
          else if (error === null)
            return;
          else
            await new Promise2(next);
        }
      } catch (err) {
        throw error = aggregateTwoErrors(error, err), error;
      } finally {
        if ((error || (options === null || options === undefined ? undefined : options.destroyOnReturn) !== false) && (error === undefined || stream._readableState.autoDestroy))
          destroyImpl.destroyer(stream, null);
        else
          stream.off("readable", next), cleanup();
      }
    }
    ObjectDefineProperties(Readable.prototype, { readable: { __proto__: null, get() {
      let r = this._readableState;
      return !!r && r.readable !== false && !r.destroyed && !r.errorEmitted && !r.endEmitted;
    }, set(val) {
      if (this._readableState)
        this._readableState.readable = !!val;
    } }, readableDidRead: { __proto__: null, enumerable: false, get: function() {
      return this._readableState.dataEmitted;
    } }, readableAborted: { __proto__: null, enumerable: false, get: function() {
      return !!(this._readableState.readable !== false && (this._readableState.destroyed || this._readableState.errored) && !this._readableState.endEmitted);
    } }, readableHighWaterMark: { __proto__: null, enumerable: false, get: function() {
      return this._readableState.highWaterMark;
    } }, readableBuffer: { __proto__: null, enumerable: false, get: function() {
      return this._readableState && this._readableState.buffer;
    } }, readableFlowing: { __proto__: null, enumerable: false, get: function() {
      return this._readableState.flowing;
    }, set: function(state) {
      if (this._readableState)
        this._readableState.flowing = state;
    } }, readableLength: { __proto__: null, enumerable: false, get() {
      return this._readableState.length;
    } }, readableObjectMode: { __proto__: null, enumerable: false, get() {
      return this._readableState ? this._readableState.objectMode : false;
    } }, readableEncoding: { __proto__: null, enumerable: false, get() {
      return this._readableState ? this._readableState.encoding : null;
    } }, errored: { __proto__: null, enumerable: false, get() {
      return this._readableState ? this._readableState.errored : null;
    } }, closed: { __proto__: null, get() {
      return this._readableState ? this._readableState.closed : false;
    } }, destroyed: { __proto__: null, enumerable: false, get() {
      return this._readableState ? this._readableState.destroyed : false;
    }, set(value) {
      if (!this._readableState)
        return;
      this._readableState.destroyed = value;
    } }, readableEnded: { __proto__: null, enumerable: false, get() {
      return this._readableState ? this._readableState.endEmitted : false;
    } } });
    ObjectDefineProperties(ReadableState.prototype, { pipesCount: { __proto__: null, get() {
      return this.pipes.length;
    } }, paused: { __proto__: null, get() {
      return this[kPaused] !== false;
    }, set(value) {
      this[kPaused] = !!value;
    } } });
    Readable._fromList = fromList;
    function fromList(n, state) {
      if (state.length === 0)
        return null;
      let ret;
      if (state.objectMode)
        ret = state.buffer.shift();
      else if (!n || n >= state.length) {
        if (state.decoder)
          ret = state.buffer.join("");
        else if (state.buffer.length === 1)
          ret = state.buffer.first();
        else
          ret = state.buffer.concat(state.length);
        state.buffer.clear();
      } else
        ret = state.buffer.consume(n, state.decoder);
      return ret;
    }
    function endReadable(stream) {
      let state = stream._readableState;
      if (debug("endReadable", state.endEmitted), !state.endEmitted)
        state.ended = true, process2.nextTick(endReadableNT, state, stream);
    }
    function endReadableNT(state, stream) {
      if (debug("endReadableNT", state.endEmitted, state.length), !state.errored && !state.closeEmitted && !state.endEmitted && state.length === 0) {
        if (state.endEmitted = true, stream.emit("end"), stream.writable && stream.allowHalfOpen === false)
          process2.nextTick(endWritableNT, stream);
        else if (state.autoDestroy) {
          let wState = stream._writableState;
          if (!wState || wState.autoDestroy && (wState.finished || wState.writable === false))
            stream.destroy();
        }
      }
    }
    function endWritableNT(stream) {
      if (stream.writable && !stream.writableEnded && !stream.destroyed)
        stream.end();
    }
    Readable.from = function(iterable, opts) {
      return from2(Readable, iterable, opts);
    };
    var webStreamsAdapters;
    function lazyWebStreams() {
      if (webStreamsAdapters === undefined)
        webStreamsAdapters = {};
      return webStreamsAdapters;
    }
    Readable.fromWeb = function(readableStream, options) {
      return lazyWebStreams().newStreamReadableFromReadableStream(readableStream, options);
    };
    Readable.toWeb = function(streamReadable, options) {
      return lazyWebStreams().newReadableStreamFromStreamReadable(streamReadable, options);
    };
    Readable.wrap = function(src, options) {
      var _ref, _src$readableObjectMo;
      return new Readable({ objectMode: (_ref = (_src$readableObjectMo = src.readableObjectMode) !== null && _src$readableObjectMo !== undefined ? _src$readableObjectMo : src.objectMode) !== null && _ref !== undefined ? _ref : true, ...options, destroy(err, callback) {
        destroyImpl.destroyer(src, err), callback(err);
      } }).wrap(src);
    };
  });
  var require_writable = __commonJS2((exports22, module22) => {
    var process2 = require_process(), { ArrayPrototypeSlice: ArrayPrototypeSlice2, Error: Error2, FunctionPrototypeSymbolHasInstance, ObjectDefineProperty, ObjectDefineProperties, ObjectSetPrototypeOf, StringPrototypeToLowerCase, Symbol: Symbol2, SymbolHasInstance } = require_primordials();
    module22.exports = Writable;
    Writable.WritableState = WritableState;
    var { EventEmitter: EE } = (init_events(), __toCommonJS(exports_events)), Stream = require_legacy().Stream, { Buffer: Buffer3 } = (init_buffer(), __toCommonJS(exports_buffer)), destroyImpl = require_destroy(), { addAbortSignal } = require_add_abort_signal(), { getHighWaterMark, getDefaultHighWaterMark } = require_state(), { ERR_INVALID_ARG_TYPE: ERR_INVALID_ARG_TYPE3, ERR_METHOD_NOT_IMPLEMENTED, ERR_MULTIPLE_CALLBACK, ERR_STREAM_CANNOT_PIPE, ERR_STREAM_DESTROYED, ERR_STREAM_ALREADY_FINISHED, ERR_STREAM_NULL_VALUES, ERR_STREAM_WRITE_AFTER_END, ERR_UNKNOWN_ENCODING } = require_errors().codes, { errorOrDestroy } = destroyImpl;
    ObjectSetPrototypeOf(Writable.prototype, Stream.prototype);
    ObjectSetPrototypeOf(Writable, Stream);
    function nop() {}
    var kOnFinished = Symbol2("kOnFinished");
    function WritableState(options, stream, isDuplex) {
      if (typeof isDuplex !== "boolean")
        isDuplex = stream instanceof require_duplex();
      if (this.objectMode = !!(options && options.objectMode), isDuplex)
        this.objectMode = this.objectMode || !!(options && options.writableObjectMode);
      this.highWaterMark = options ? getHighWaterMark(this, options, "writableHighWaterMark", isDuplex) : getDefaultHighWaterMark(false), this.finalCalled = false, this.needDrain = false, this.ending = false, this.ended = false, this.finished = false, this.destroyed = false;
      let noDecode = !!(options && options.decodeStrings === false);
      this.decodeStrings = !noDecode, this.defaultEncoding = options && options.defaultEncoding || "utf8", this.length = 0, this.writing = false, this.corked = 0, this.sync = true, this.bufferProcessing = false, this.onwrite = onwrite.bind(undefined, stream), this.writecb = null, this.writelen = 0, this.afterWriteTickInfo = null, resetBuffer(this), this.pendingcb = 0, this.constructed = true, this.prefinished = false, this.errorEmitted = false, this.emitClose = !options || options.emitClose !== false, this.autoDestroy = !options || options.autoDestroy !== false, this.errored = null, this.closed = false, this.closeEmitted = false, this[kOnFinished] = [];
    }
    function resetBuffer(state) {
      state.buffered = [], state.bufferedIndex = 0, state.allBuffers = true, state.allNoop = true;
    }
    WritableState.prototype.getBuffer = function() {
      return ArrayPrototypeSlice2(this.buffered, this.bufferedIndex);
    };
    ObjectDefineProperty(WritableState.prototype, "bufferedRequestCount", { __proto__: null, get() {
      return this.buffered.length - this.bufferedIndex;
    } });
    function Writable(options) {
      let isDuplex = this instanceof require_duplex();
      if (!isDuplex && !FunctionPrototypeSymbolHasInstance(Writable, this))
        return new Writable(options);
      if (this._writableState = new WritableState(options, this, isDuplex), options) {
        if (typeof options.write === "function")
          this._write = options.write;
        if (typeof options.writev === "function")
          this._writev = options.writev;
        if (typeof options.destroy === "function")
          this._destroy = options.destroy;
        if (typeof options.final === "function")
          this._final = options.final;
        if (typeof options.construct === "function")
          this._construct = options.construct;
        if (options.signal)
          addAbortSignal(options.signal, this);
      }
      Stream.call(this, options), destroyImpl.construct(this, () => {
        let state = this._writableState;
        if (!state.writing)
          clearBuffer(this, state);
        finishMaybe(this, state);
      });
    }
    ObjectDefineProperty(Writable, SymbolHasInstance, { __proto__: null, value: function(object) {
      if (FunctionPrototypeSymbolHasInstance(this, object))
        return true;
      if (this !== Writable)
        return false;
      return object && object._writableState instanceof WritableState;
    } });
    Writable.prototype.pipe = function() {
      errorOrDestroy(this, new ERR_STREAM_CANNOT_PIPE);
    };
    function _write(stream, chunk, encoding, cb) {
      let state = stream._writableState;
      if (typeof encoding === "function")
        cb = encoding, encoding = state.defaultEncoding;
      else {
        if (!encoding)
          encoding = state.defaultEncoding;
        else if (encoding !== "buffer" && !Buffer3.isEncoding(encoding))
          throw new ERR_UNKNOWN_ENCODING(encoding);
        if (typeof cb !== "function")
          cb = nop;
      }
      if (chunk === null)
        throw new ERR_STREAM_NULL_VALUES;
      else if (!state.objectMode)
        if (typeof chunk === "string") {
          if (state.decodeStrings !== false)
            chunk = Buffer3.from(chunk, encoding), encoding = "buffer";
        } else if (chunk instanceof Buffer3)
          encoding = "buffer";
        else if (Stream._isUint8Array(chunk))
          chunk = Stream._uint8ArrayToBuffer(chunk), encoding = "buffer";
        else
          throw new ERR_INVALID_ARG_TYPE3("chunk", ["string", "Buffer", "Uint8Array"], chunk);
      let err;
      if (state.ending)
        err = new ERR_STREAM_WRITE_AFTER_END;
      else if (state.destroyed)
        err = new ERR_STREAM_DESTROYED("write");
      if (err)
        return process2.nextTick(cb, err), errorOrDestroy(stream, err, true), err;
      return state.pendingcb++, writeOrBuffer(stream, state, chunk, encoding, cb);
    }
    Writable.prototype.write = function(chunk, encoding, cb) {
      return _write(this, chunk, encoding, cb) === true;
    };
    Writable.prototype.cork = function() {
      this._writableState.corked++;
    };
    Writable.prototype.uncork = function() {
      let state = this._writableState;
      if (state.corked) {
        if (state.corked--, !state.writing)
          clearBuffer(this, state);
      }
    };
    Writable.prototype.setDefaultEncoding = function(encoding) {
      if (typeof encoding === "string")
        encoding = StringPrototypeToLowerCase(encoding);
      if (!Buffer3.isEncoding(encoding))
        throw new ERR_UNKNOWN_ENCODING(encoding);
      return this._writableState.defaultEncoding = encoding, this;
    };
    function writeOrBuffer(stream, state, chunk, encoding, callback) {
      let len2 = state.objectMode ? 1 : chunk.length;
      state.length += len2;
      let ret = state.length < state.highWaterMark;
      if (!ret)
        state.needDrain = true;
      if (state.writing || state.corked || state.errored || !state.constructed) {
        if (state.buffered.push({ chunk, encoding, callback }), state.allBuffers && encoding !== "buffer")
          state.allBuffers = false;
        if (state.allNoop && callback !== nop)
          state.allNoop = false;
      } else
        state.writelen = len2, state.writecb = callback, state.writing = true, state.sync = true, stream._write(chunk, encoding, state.onwrite), state.sync = false;
      return ret && !state.errored && !state.destroyed;
    }
    function doWrite(stream, state, writev, len2, chunk, encoding, cb) {
      if (state.writelen = len2, state.writecb = cb, state.writing = true, state.sync = true, state.destroyed)
        state.onwrite(new ERR_STREAM_DESTROYED("write"));
      else if (writev)
        stream._writev(chunk, state.onwrite);
      else
        stream._write(chunk, encoding, state.onwrite);
      state.sync = false;
    }
    function onwriteError(stream, state, er, cb) {
      --state.pendingcb, cb(er), errorBuffer(state), errorOrDestroy(stream, er);
    }
    function onwrite(stream, er) {
      let state = stream._writableState, sync = state.sync, cb = state.writecb;
      if (typeof cb !== "function") {
        errorOrDestroy(stream, new ERR_MULTIPLE_CALLBACK);
        return;
      }
      if (state.writing = false, state.writecb = null, state.length -= state.writelen, state.writelen = 0, er) {
        if (er.stack, !state.errored)
          state.errored = er;
        if (stream._readableState && !stream._readableState.errored)
          stream._readableState.errored = er;
        if (sync)
          process2.nextTick(onwriteError, stream, state, er, cb);
        else
          onwriteError(stream, state, er, cb);
      } else {
        if (state.buffered.length > state.bufferedIndex)
          clearBuffer(stream, state);
        if (sync)
          if (state.afterWriteTickInfo !== null && state.afterWriteTickInfo.cb === cb)
            state.afterWriteTickInfo.count++;
          else
            state.afterWriteTickInfo = { count: 1, cb, stream, state }, process2.nextTick(afterWriteTick, state.afterWriteTickInfo);
        else
          afterWrite(stream, state, 1, cb);
      }
    }
    function afterWriteTick({ stream, state, count, cb }) {
      return state.afterWriteTickInfo = null, afterWrite(stream, state, count, cb);
    }
    function afterWrite(stream, state, count, cb) {
      if (!state.ending && !stream.destroyed && state.length === 0 && state.needDrain)
        state.needDrain = false, stream.emit("drain");
      while (count-- > 0)
        state.pendingcb--, cb();
      if (state.destroyed)
        errorBuffer(state);
      finishMaybe(stream, state);
    }
    function errorBuffer(state) {
      if (state.writing)
        return;
      for (let n = state.bufferedIndex;n < state.buffered.length; ++n) {
        var _state$errored;
        let { chunk, callback } = state.buffered[n], len2 = state.objectMode ? 1 : chunk.length;
        state.length -= len2, callback((_state$errored = state.errored) !== null && _state$errored !== undefined ? _state$errored : new ERR_STREAM_DESTROYED("write"));
      }
      let onfinishCallbacks = state[kOnFinished].splice(0);
      for (let i2 = 0;i2 < onfinishCallbacks.length; i2++) {
        var _state$errored2;
        onfinishCallbacks[i2]((_state$errored2 = state.errored) !== null && _state$errored2 !== undefined ? _state$errored2 : new ERR_STREAM_DESTROYED("end"));
      }
      resetBuffer(state);
    }
    function clearBuffer(stream, state) {
      if (state.corked || state.bufferProcessing || state.destroyed || !state.constructed)
        return;
      let { buffered, bufferedIndex, objectMode } = state, bufferedLength = buffered.length - bufferedIndex;
      if (!bufferedLength)
        return;
      let i2 = bufferedIndex;
      if (state.bufferProcessing = true, bufferedLength > 1 && stream._writev) {
        state.pendingcb -= bufferedLength - 1;
        let callback = state.allNoop ? nop : (err) => {
          for (let n = i2;n < buffered.length; ++n)
            buffered[n].callback(err);
        }, chunks = state.allNoop && i2 === 0 ? buffered : ArrayPrototypeSlice2(buffered, i2);
        chunks.allBuffers = state.allBuffers, doWrite(stream, state, true, state.length, chunks, "", callback), resetBuffer(state);
      } else {
        do {
          let { chunk, encoding, callback } = buffered[i2];
          buffered[i2++] = null;
          let len2 = objectMode ? 1 : chunk.length;
          doWrite(stream, state, false, len2, chunk, encoding, callback);
        } while (i2 < buffered.length && !state.writing);
        if (i2 === buffered.length)
          resetBuffer(state);
        else if (i2 > 256)
          buffered.splice(0, i2), state.bufferedIndex = 0;
        else
          state.bufferedIndex = i2;
      }
      state.bufferProcessing = false;
    }
    Writable.prototype._write = function(chunk, encoding, cb) {
      if (this._writev)
        this._writev([{ chunk, encoding }], cb);
      else
        throw new ERR_METHOD_NOT_IMPLEMENTED("_write()");
    };
    Writable.prototype._writev = null;
    Writable.prototype.end = function(chunk, encoding, cb) {
      let state = this._writableState;
      if (typeof chunk === "function")
        cb = chunk, chunk = null, encoding = null;
      else if (typeof encoding === "function")
        cb = encoding, encoding = null;
      let err;
      if (chunk !== null && chunk !== undefined) {
        let ret = _write(this, chunk, encoding);
        if (ret instanceof Error2)
          err = ret;
      }
      if (state.corked)
        state.corked = 1, this.uncork();
      if (err)
        ;
      else if (!state.errored && !state.ending)
        state.ending = true, finishMaybe(this, state, true), state.ended = true;
      else if (state.finished)
        err = new ERR_STREAM_ALREADY_FINISHED("end");
      else if (state.destroyed)
        err = new ERR_STREAM_DESTROYED("end");
      if (typeof cb === "function")
        if (err || state.finished)
          process2.nextTick(cb, err);
        else
          state[kOnFinished].push(cb);
      return this;
    };
    function needFinish(state) {
      return state.ending && !state.destroyed && state.constructed && state.length === 0 && !state.errored && state.buffered.length === 0 && !state.finished && !state.writing && !state.errorEmitted && !state.closeEmitted;
    }
    function callFinal(stream, state) {
      let called = false;
      function onFinish(err) {
        if (called) {
          errorOrDestroy(stream, err !== null && err !== undefined ? err : ERR_MULTIPLE_CALLBACK());
          return;
        }
        if (called = true, state.pendingcb--, err) {
          let onfinishCallbacks = state[kOnFinished].splice(0);
          for (let i2 = 0;i2 < onfinishCallbacks.length; i2++)
            onfinishCallbacks[i2](err);
          errorOrDestroy(stream, err, state.sync);
        } else if (needFinish(state))
          state.prefinished = true, stream.emit("prefinish"), state.pendingcb++, process2.nextTick(finish, stream, state);
      }
      state.sync = true, state.pendingcb++;
      try {
        stream._final(onFinish);
      } catch (err) {
        onFinish(err);
      }
      state.sync = false;
    }
    function prefinish(stream, state) {
      if (!state.prefinished && !state.finalCalled)
        if (typeof stream._final === "function" && !state.destroyed)
          state.finalCalled = true, callFinal(stream, state);
        else
          state.prefinished = true, stream.emit("prefinish");
    }
    function finishMaybe(stream, state, sync) {
      if (needFinish(state)) {
        if (prefinish(stream, state), state.pendingcb === 0) {
          if (sync)
            state.pendingcb++, process2.nextTick((stream2, state2) => {
              if (needFinish(state2))
                finish(stream2, state2);
              else
                state2.pendingcb--;
            }, stream, state);
          else if (needFinish(state))
            state.pendingcb++, finish(stream, state);
        }
      }
    }
    function finish(stream, state) {
      state.pendingcb--, state.finished = true;
      let onfinishCallbacks = state[kOnFinished].splice(0);
      for (let i2 = 0;i2 < onfinishCallbacks.length; i2++)
        onfinishCallbacks[i2]();
      if (stream.emit("finish"), state.autoDestroy) {
        let rState = stream._readableState;
        if (!rState || rState.autoDestroy && (rState.endEmitted || rState.readable === false))
          stream.destroy();
      }
    }
    ObjectDefineProperties(Writable.prototype, { closed: { __proto__: null, get() {
      return this._writableState ? this._writableState.closed : false;
    } }, destroyed: { __proto__: null, get() {
      return this._writableState ? this._writableState.destroyed : false;
    }, set(value) {
      if (this._writableState)
        this._writableState.destroyed = value;
    } }, writable: { __proto__: null, get() {
      let w = this._writableState;
      return !!w && w.writable !== false && !w.destroyed && !w.errored && !w.ending && !w.ended;
    }, set(val) {
      if (this._writableState)
        this._writableState.writable = !!val;
    } }, writableFinished: { __proto__: null, get() {
      return this._writableState ? this._writableState.finished : false;
    } }, writableObjectMode: { __proto__: null, get() {
      return this._writableState ? this._writableState.objectMode : false;
    } }, writableBuffer: { __proto__: null, get() {
      return this._writableState && this._writableState.getBuffer();
    } }, writableEnded: { __proto__: null, get() {
      return this._writableState ? this._writableState.ending : false;
    } }, writableNeedDrain: { __proto__: null, get() {
      let wState = this._writableState;
      if (!wState)
        return false;
      return !wState.destroyed && !wState.ending && wState.needDrain;
    } }, writableHighWaterMark: { __proto__: null, get() {
      return this._writableState && this._writableState.highWaterMark;
    } }, writableCorked: { __proto__: null, get() {
      return this._writableState ? this._writableState.corked : 0;
    } }, writableLength: { __proto__: null, get() {
      return this._writableState && this._writableState.length;
    } }, errored: { __proto__: null, enumerable: false, get() {
      return this._writableState ? this._writableState.errored : null;
    } }, writableAborted: { __proto__: null, enumerable: false, get: function() {
      return !!(this._writableState.writable !== false && (this._writableState.destroyed || this._writableState.errored) && !this._writableState.finished);
    } } });
    var destroy = destroyImpl.destroy;
    Writable.prototype.destroy = function(err, cb) {
      let state = this._writableState;
      if (!state.destroyed && (state.bufferedIndex < state.buffered.length || state[kOnFinished].length))
        process2.nextTick(errorBuffer, state);
      return destroy.call(this, err, cb), this;
    };
    Writable.prototype._undestroy = destroyImpl.undestroy;
    Writable.prototype._destroy = function(err, cb) {
      cb(err);
    };
    Writable.prototype[EE.captureRejectionSymbol] = function(err) {
      this.destroy(err);
    };
    var webStreamsAdapters;
    function lazyWebStreams() {
      if (webStreamsAdapters === undefined)
        webStreamsAdapters = {};
      return webStreamsAdapters;
    }
    Writable.fromWeb = function(writableStream, options) {
      return lazyWebStreams().newStreamWritableFromWritableStream(writableStream, options);
    };
    Writable.toWeb = function(streamWritable) {
      return lazyWebStreams().newWritableStreamFromStreamWritable(streamWritable);
    };
  });
  var require_duplexify = __commonJS2((exports22, module22) => {
    var process2 = require_process(), bufferModule = (init_buffer(), __toCommonJS(exports_buffer)), { isReadable, isWritable, isIterable: isIterable2, isNodeStream, isReadableNodeStream, isWritableNodeStream, isDuplexNodeStream, isReadableStream: isReadableStream2, isWritableStream } = require_utils(), eos = require_end_of_stream(), { AbortError: AbortError2, codes: { ERR_INVALID_ARG_TYPE: ERR_INVALID_ARG_TYPE3, ERR_INVALID_RETURN_VALUE } } = require_errors(), { destroyer } = require_destroy(), Duplex = require_duplex(), Readable = require_readable(), Writable = require_writable(), { createDeferredPromise } = require_util(), from2 = require_from(), Blob3 = globalThis.Blob || bufferModule.Blob, isBlob2 = typeof Blob3 < "u" ? function(b) {
      return b instanceof Blob3;
    } : function(b) {
      return false;
    }, AbortController2 = globalThis.AbortController || require_abort_controller().AbortController, { FunctionPrototypeCall } = require_primordials();

    class Duplexify extends Duplex {
      constructor(options) {
        super(options);
        if ((options === null || options === undefined ? undefined : options.readable) === false)
          this._readableState.readable = false, this._readableState.ended = true, this._readableState.endEmitted = true;
        if ((options === null || options === undefined ? undefined : options.writable) === false)
          this._writableState.writable = false, this._writableState.ending = true, this._writableState.ended = true, this._writableState.finished = true;
      }
    }
    module22.exports = function duplexify(body, name) {
      if (isDuplexNodeStream(body))
        return body;
      if (isReadableNodeStream(body))
        return _duplexify({ readable: body });
      if (isWritableNodeStream(body))
        return _duplexify({ writable: body });
      if (isNodeStream(body))
        return _duplexify({ writable: false, readable: false });
      if (isReadableStream2(body))
        return _duplexify({ readable: Readable.fromWeb(body) });
      if (isWritableStream(body))
        return _duplexify({ writable: Writable.fromWeb(body) });
      if (typeof body === "function") {
        let { value, write: write2, final, destroy } = fromAsyncGen(body);
        if (isIterable2(value))
          return from2(Duplexify, value, { objectMode: true, write: write2, final, destroy });
        let then2 = value === null || value === undefined ? undefined : value.then;
        if (typeof then2 === "function") {
          let d, promise = FunctionPrototypeCall(then2, value, (val) => {
            if (val != null)
              throw new ERR_INVALID_RETURN_VALUE("nully", "body", val);
          }, (err) => {
            destroyer(d, err);
          });
          return d = new Duplexify({ objectMode: true, readable: false, write: write2, final(cb) {
            final(async () => {
              try {
                await promise, process2.nextTick(cb, null);
              } catch (err) {
                process2.nextTick(cb, err);
              }
            });
          }, destroy });
        }
        throw new ERR_INVALID_RETURN_VALUE("Iterable, AsyncIterable or AsyncFunction", name, value);
      }
      if (isBlob2(body))
        return duplexify(body.arrayBuffer());
      if (isIterable2(body))
        return from2(Duplexify, body, { objectMode: true, writable: false });
      if (isReadableStream2(body === null || body === undefined ? undefined : body.readable) && isWritableStream(body === null || body === undefined ? undefined : body.writable))
        return Duplexify.fromWeb(body);
      if (typeof (body === null || body === undefined ? undefined : body.writable) === "object" || typeof (body === null || body === undefined ? undefined : body.readable) === "object") {
        let readable = body !== null && body !== undefined && body.readable ? isReadableNodeStream(body === null || body === undefined ? undefined : body.readable) ? body === null || body === undefined ? undefined : body.readable : duplexify(body.readable) : undefined, writable = body !== null && body !== undefined && body.writable ? isWritableNodeStream(body === null || body === undefined ? undefined : body.writable) ? body === null || body === undefined ? undefined : body.writable : duplexify(body.writable) : undefined;
        return _duplexify({ readable, writable });
      }
      let then = body === null || body === undefined ? undefined : body.then;
      if (typeof then === "function") {
        let d;
        return FunctionPrototypeCall(then, body, (val) => {
          if (val != null)
            d.push(val);
          d.push(null);
        }, (err) => {
          destroyer(d, err);
        }), d = new Duplexify({ objectMode: true, writable: false, read() {} });
      }
      throw new ERR_INVALID_ARG_TYPE3(name, ["Blob", "ReadableStream", "WritableStream", "Stream", "Iterable", "AsyncIterable", "Function", "{ readable, writable } pair", "Promise"], body);
    };
    function fromAsyncGen(fn) {
      let { promise, resolve } = createDeferredPromise(), ac = new AbortController2, signal = ac.signal;
      return { value: fn(async function* () {
        while (true) {
          let _promise = promise;
          promise = null;
          let { chunk, done, cb } = await _promise;
          if (process2.nextTick(cb), done)
            return;
          if (signal.aborted)
            throw new AbortError2(undefined, { cause: signal.reason });
          ({ promise, resolve } = createDeferredPromise()), yield chunk;
        }
      }(), { signal }), write(chunk, encoding, cb) {
        let _resolve = resolve;
        resolve = null, _resolve({ chunk, done: false, cb });
      }, final(cb) {
        let _resolve = resolve;
        resolve = null, _resolve({ done: true, cb });
      }, destroy(err, cb) {
        ac.abort(), cb(err);
      } };
    }
    function _duplexify(pair) {
      let r = pair.readable && typeof pair.readable.read !== "function" ? Readable.wrap(pair.readable) : pair.readable, w = pair.writable, readable = !!isReadable(r), writable = !!isWritable(w), ondrain, onfinish, onreadable, onclose, d;
      function onfinished(err) {
        let cb = onclose;
        if (onclose = null, cb)
          cb(err);
        else if (err)
          d.destroy(err);
      }
      if (d = new Duplexify({ readableObjectMode: !!(r !== null && r !== undefined && r.readableObjectMode), writableObjectMode: !!(w !== null && w !== undefined && w.writableObjectMode), readable, writable }), writable)
        eos(w, (err) => {
          if (writable = false, err)
            destroyer(r, err);
          onfinished(err);
        }), d._write = function(chunk, encoding, callback) {
          if (w.write(chunk, encoding))
            callback();
          else
            ondrain = callback;
        }, d._final = function(callback) {
          w.end(), onfinish = callback;
        }, w.on("drain", function() {
          if (ondrain) {
            let cb = ondrain;
            ondrain = null, cb();
          }
        }), w.on("finish", function() {
          if (onfinish) {
            let cb = onfinish;
            onfinish = null, cb();
          }
        });
      if (readable)
        eos(r, (err) => {
          if (readable = false, err)
            destroyer(r, err);
          onfinished(err);
        }), r.on("readable", function() {
          if (onreadable) {
            let cb = onreadable;
            onreadable = null, cb();
          }
        }), r.on("end", function() {
          d.push(null);
        }), d._read = function() {
          while (true) {
            let buf = r.read();
            if (buf === null) {
              onreadable = d._read;
              return;
            }
            if (!d.push(buf))
              return;
          }
        };
      return d._destroy = function(err, callback) {
        if (!err && onclose !== null)
          err = new AbortError2;
        if (onreadable = null, ondrain = null, onfinish = null, onclose === null)
          callback(err);
        else
          onclose = callback, destroyer(w, err), destroyer(r, err);
      }, d;
    }
  });
  var require_duplex = __commonJS2((exports22, module22) => {
    var { ObjectDefineProperties, ObjectGetOwnPropertyDescriptor, ObjectKeys, ObjectSetPrototypeOf } = require_primordials();
    module22.exports = Duplex;
    var Readable = require_readable(), Writable = require_writable();
    ObjectSetPrototypeOf(Duplex.prototype, Readable.prototype);
    ObjectSetPrototypeOf(Duplex, Readable);
    {
      let keys = ObjectKeys(Writable.prototype);
      for (let i2 = 0;i2 < keys.length; i2++) {
        let method = keys[i2];
        if (!Duplex.prototype[method])
          Duplex.prototype[method] = Writable.prototype[method];
      }
    }
    function Duplex(options) {
      if (!(this instanceof Duplex))
        return new Duplex(options);
      if (Readable.call(this, options), Writable.call(this, options), options) {
        if (this.allowHalfOpen = options.allowHalfOpen !== false, options.readable === false)
          this._readableState.readable = false, this._readableState.ended = true, this._readableState.endEmitted = true;
        if (options.writable === false)
          this._writableState.writable = false, this._writableState.ending = true, this._writableState.ended = true, this._writableState.finished = true;
      } else
        this.allowHalfOpen = true;
    }
    ObjectDefineProperties(Duplex.prototype, { writable: { __proto__: null, ...ObjectGetOwnPropertyDescriptor(Writable.prototype, "writable") }, writableHighWaterMark: { __proto__: null, ...ObjectGetOwnPropertyDescriptor(Writable.prototype, "writableHighWaterMark") }, writableObjectMode: { __proto__: null, ...ObjectGetOwnPropertyDescriptor(Writable.prototype, "writableObjectMode") }, writableBuffer: { __proto__: null, ...ObjectGetOwnPropertyDescriptor(Writable.prototype, "writableBuffer") }, writableLength: { __proto__: null, ...ObjectGetOwnPropertyDescriptor(Writable.prototype, "writableLength") }, writableFinished: { __proto__: null, ...ObjectGetOwnPropertyDescriptor(Writable.prototype, "writableFinished") }, writableCorked: { __proto__: null, ...ObjectGetOwnPropertyDescriptor(Writable.prototype, "writableCorked") }, writableEnded: { __proto__: null, ...ObjectGetOwnPropertyDescriptor(Writable.prototype, "writableEnded") }, writableNeedDrain: { __proto__: null, ...ObjectGetOwnPropertyDescriptor(Writable.prototype, "writableNeedDrain") }, destroyed: { __proto__: null, get() {
      if (this._readableState === undefined || this._writableState === undefined)
        return false;
      return this._readableState.destroyed && this._writableState.destroyed;
    }, set(value) {
      if (this._readableState && this._writableState)
        this._readableState.destroyed = value, this._writableState.destroyed = value;
    } } });
    var webStreamsAdapters;
    function lazyWebStreams() {
      if (webStreamsAdapters === undefined)
        webStreamsAdapters = {};
      return webStreamsAdapters;
    }
    Duplex.fromWeb = function(pair, options) {
      return lazyWebStreams().newStreamDuplexFromReadableWritablePair(pair, options);
    };
    Duplex.toWeb = function(duplex) {
      return lazyWebStreams().newReadableWritablePairFromDuplex(duplex);
    };
    var duplexify;
    Duplex.from = function(body) {
      if (!duplexify)
        duplexify = require_duplexify();
      return duplexify(body, "body");
    };
  });
  var require_transform = __commonJS2((exports22, module22) => {
    var { ObjectSetPrototypeOf, Symbol: Symbol2 } = require_primordials();
    module22.exports = Transform;
    var { ERR_METHOD_NOT_IMPLEMENTED } = require_errors().codes, Duplex = require_duplex(), { getHighWaterMark } = require_state();
    ObjectSetPrototypeOf(Transform.prototype, Duplex.prototype);
    ObjectSetPrototypeOf(Transform, Duplex);
    var kCallback = Symbol2("kCallback");
    function Transform(options) {
      if (!(this instanceof Transform))
        return new Transform(options);
      let readableHighWaterMark = options ? getHighWaterMark(this, options, "readableHighWaterMark", true) : null;
      if (readableHighWaterMark === 0)
        options = { ...options, highWaterMark: null, readableHighWaterMark, writableHighWaterMark: options.writableHighWaterMark || 0 };
      if (Duplex.call(this, options), this._readableState.sync = false, this[kCallback] = null, options) {
        if (typeof options.transform === "function")
          this._transform = options.transform;
        if (typeof options.flush === "function")
          this._flush = options.flush;
      }
      this.on("prefinish", prefinish);
    }
    function final(cb) {
      if (typeof this._flush === "function" && !this.destroyed)
        this._flush((er, data) => {
          if (er) {
            if (cb)
              cb(er);
            else
              this.destroy(er);
            return;
          }
          if (data != null)
            this.push(data);
          if (this.push(null), cb)
            cb();
        });
      else if (this.push(null), cb)
        cb();
    }
    function prefinish() {
      if (this._final !== final)
        final.call(this);
    }
    Transform.prototype._final = final;
    Transform.prototype._transform = function(chunk, encoding, callback) {
      throw new ERR_METHOD_NOT_IMPLEMENTED("_transform()");
    };
    Transform.prototype._write = function(chunk, encoding, callback) {
      let rState = this._readableState, wState = this._writableState, length = rState.length;
      this._transform(chunk, encoding, (err, val) => {
        if (err) {
          callback(err);
          return;
        }
        if (val != null)
          this.push(val);
        if (wState.ended || length === rState.length || rState.length < rState.highWaterMark)
          callback();
        else
          this[kCallback] = callback;
      });
    };
    Transform.prototype._read = function() {
      if (this[kCallback]) {
        let callback = this[kCallback];
        this[kCallback] = null, callback();
      }
    };
  });
  var require_passthrough = __commonJS2((exports22, module22) => {
    var { ObjectSetPrototypeOf } = require_primordials();
    module22.exports = PassThrough;
    var Transform = require_transform();
    ObjectSetPrototypeOf(PassThrough.prototype, Transform.prototype);
    ObjectSetPrototypeOf(PassThrough, Transform);
    function PassThrough(options) {
      if (!(this instanceof PassThrough))
        return new PassThrough(options);
      Transform.call(this, options);
    }
    PassThrough.prototype._transform = function(chunk, encoding, cb) {
      cb(null, chunk);
    };
  });
  var require_pipeline = __commonJS2((exports22, module22) => {
    var process2 = require_process(), { ArrayIsArray, Promise: Promise2, SymbolAsyncIterator, SymbolDispose } = require_primordials(), eos = require_end_of_stream(), { once } = require_util(), destroyImpl = require_destroy(), Duplex = require_duplex(), { aggregateTwoErrors, codes: { ERR_INVALID_ARG_TYPE: ERR_INVALID_ARG_TYPE3, ERR_INVALID_RETURN_VALUE, ERR_MISSING_ARGS, ERR_STREAM_DESTROYED, ERR_STREAM_PREMATURE_CLOSE }, AbortError: AbortError2 } = require_errors(), { validateFunction, validateAbortSignal: validateAbortSignal2 } = require_validators(), { isIterable: isIterable2, isReadable, isReadableNodeStream, isNodeStream, isTransformStream, isWebStream, isReadableStream: isReadableStream2, isReadableFinished } = require_utils(), AbortController2 = globalThis.AbortController || require_abort_controller().AbortController, PassThrough, Readable, addAbortListener2;
    function destroyer(stream, reading, writing) {
      let finished = false;
      stream.on("close", () => {
        finished = true;
      });
      let cleanup = eos(stream, { readable: reading, writable: writing }, (err) => {
        finished = !err;
      });
      return { destroy: (err) => {
        if (finished)
          return;
        finished = true, destroyImpl.destroyer(stream, err || new ERR_STREAM_DESTROYED("pipe"));
      }, cleanup };
    }
    function popCallback(streams) {
      return validateFunction(streams[streams.length - 1], "streams[stream.length - 1]"), streams.pop();
    }
    function makeAsyncIterable(val) {
      if (isIterable2(val))
        return val;
      else if (isReadableNodeStream(val))
        return fromReadable(val);
      throw new ERR_INVALID_ARG_TYPE3("val", ["Readable", "Iterable", "AsyncIterable"], val);
    }
    async function* fromReadable(val) {
      if (!Readable)
        Readable = require_readable();
      yield* Readable.prototype[SymbolAsyncIterator].call(val);
    }
    async function pumpToNode(iterable, writable, finish, { end }) {
      let error, onresolve = null, resume = (err) => {
        if (err)
          error = err;
        if (onresolve) {
          let callback = onresolve;
          onresolve = null, callback();
        }
      }, wait = () => new Promise2((resolve, reject) => {
        if (error)
          reject(error);
        else
          onresolve = () => {
            if (error)
              reject(error);
            else
              resolve();
          };
      });
      writable.on("drain", resume);
      let cleanup = eos(writable, { readable: false }, resume);
      try {
        if (writable.writableNeedDrain)
          await wait();
        for await (let chunk of iterable)
          if (!writable.write(chunk))
            await wait();
        if (end)
          writable.end(), await wait();
        finish();
      } catch (err) {
        finish(error !== err ? aggregateTwoErrors(error, err) : err);
      } finally {
        cleanup(), writable.off("drain", resume);
      }
    }
    async function pumpToWeb(readable, writable, finish, { end }) {
      if (isTransformStream(writable))
        writable = writable.writable;
      let writer = writable.getWriter();
      try {
        for await (let chunk of readable)
          await writer.ready, writer.write(chunk).catch(() => {});
        if (await writer.ready, end)
          await writer.close();
        finish();
      } catch (err) {
        try {
          await writer.abort(err), finish(err);
        } catch (err2) {
          finish(err2);
        }
      }
    }
    function pipeline(...streams) {
      return pipelineImpl(streams, once(popCallback(streams)));
    }
    function pipelineImpl(streams, callback, opts) {
      if (streams.length === 1 && ArrayIsArray(streams[0]))
        streams = streams[0];
      if (streams.length < 2)
        throw new ERR_MISSING_ARGS("streams");
      let ac = new AbortController2, signal = ac.signal, outerSignal = opts === null || opts === undefined ? undefined : opts.signal, lastStreamCleanup = [];
      validateAbortSignal2(outerSignal, "options.signal");
      function abort() {
        finishImpl(new AbortError2);
      }
      addAbortListener2 = addAbortListener2 || require_util().addAbortListener;
      let disposable;
      if (outerSignal)
        disposable = addAbortListener2(outerSignal, abort);
      let error, value, destroys = [], finishCount = 0;
      function finish(err) {
        finishImpl(err, --finishCount === 0);
      }
      function finishImpl(err, final) {
        var _disposable;
        if (err && (!error || error.code === "ERR_STREAM_PREMATURE_CLOSE"))
          error = err;
        if (!error && !final)
          return;
        while (destroys.length)
          destroys.shift()(error);
        if ((_disposable = disposable) === null || _disposable === undefined || _disposable[SymbolDispose](), ac.abort(), final) {
          if (!error)
            lastStreamCleanup.forEach((fn) => fn());
          process2.nextTick(callback, error, value);
        }
      }
      let ret;
      for (let i2 = 0;i2 < streams.length; i2++) {
        let stream = streams[i2], reading = i2 < streams.length - 1, writing = i2 > 0, end = reading || (opts === null || opts === undefined ? undefined : opts.end) !== false, isLastStream = i2 === streams.length - 1;
        if (isNodeStream(stream)) {
          let onError2 = function(err) {
            if (err && err.name !== "AbortError" && err.code !== "ERR_STREAM_PREMATURE_CLOSE")
              finish(err);
          };
          var onError = onError2;
          if (end) {
            let { destroy, cleanup } = destroyer(stream, reading, writing);
            if (destroys.push(destroy), isReadable(stream) && isLastStream)
              lastStreamCleanup.push(cleanup);
          }
          if (stream.on("error", onError2), isReadable(stream) && isLastStream)
            lastStreamCleanup.push(() => {
              stream.removeListener("error", onError2);
            });
        }
        if (i2 === 0)
          if (typeof stream === "function") {
            if (ret = stream({ signal }), !isIterable2(ret))
              throw new ERR_INVALID_RETURN_VALUE("Iterable, AsyncIterable or Stream", "source", ret);
          } else if (isIterable2(stream) || isReadableNodeStream(stream) || isTransformStream(stream))
            ret = stream;
          else
            ret = Duplex.from(stream);
        else if (typeof stream === "function") {
          if (isTransformStream(ret)) {
            var _ret;
            ret = makeAsyncIterable((_ret = ret) === null || _ret === undefined ? undefined : _ret.readable);
          } else
            ret = makeAsyncIterable(ret);
          if (ret = stream(ret, { signal }), reading) {
            if (!isIterable2(ret, true))
              throw new ERR_INVALID_RETURN_VALUE("AsyncIterable", `transform[${i2 - 1}]`, ret);
          } else {
            var _ret2;
            if (!PassThrough)
              PassThrough = require_passthrough();
            let pt = new PassThrough({ objectMode: true }), then = (_ret2 = ret) === null || _ret2 === undefined ? undefined : _ret2.then;
            if (typeof then === "function")
              finishCount++, then.call(ret, (val) => {
                if (value = val, val != null)
                  pt.write(val);
                if (end)
                  pt.end();
                process2.nextTick(finish);
              }, (err) => {
                pt.destroy(err), process2.nextTick(finish, err);
              });
            else if (isIterable2(ret, true))
              finishCount++, pumpToNode(ret, pt, finish, { end });
            else if (isReadableStream2(ret) || isTransformStream(ret)) {
              let toRead = ret.readable || ret;
              finishCount++, pumpToNode(toRead, pt, finish, { end });
            } else
              throw new ERR_INVALID_RETURN_VALUE("AsyncIterable or Promise", "destination", ret);
            ret = pt;
            let { destroy, cleanup } = destroyer(ret, false, true);
            if (destroys.push(destroy), isLastStream)
              lastStreamCleanup.push(cleanup);
          }
        } else if (isNodeStream(stream)) {
          if (isReadableNodeStream(ret)) {
            finishCount += 2;
            let cleanup = pipe(ret, stream, finish, { end });
            if (isReadable(stream) && isLastStream)
              lastStreamCleanup.push(cleanup);
          } else if (isTransformStream(ret) || isReadableStream2(ret)) {
            let toRead = ret.readable || ret;
            finishCount++, pumpToNode(toRead, stream, finish, { end });
          } else if (isIterable2(ret))
            finishCount++, pumpToNode(ret, stream, finish, { end });
          else
            throw new ERR_INVALID_ARG_TYPE3("val", ["Readable", "Iterable", "AsyncIterable", "ReadableStream", "TransformStream"], ret);
          ret = stream;
        } else if (isWebStream(stream)) {
          if (isReadableNodeStream(ret))
            finishCount++, pumpToWeb(makeAsyncIterable(ret), stream, finish, { end });
          else if (isReadableStream2(ret) || isIterable2(ret))
            finishCount++, pumpToWeb(ret, stream, finish, { end });
          else if (isTransformStream(ret))
            finishCount++, pumpToWeb(ret.readable, stream, finish, { end });
          else
            throw new ERR_INVALID_ARG_TYPE3("val", ["Readable", "Iterable", "AsyncIterable", "ReadableStream", "TransformStream"], ret);
          ret = stream;
        } else
          ret = Duplex.from(stream);
      }
      if (signal !== null && signal !== undefined && signal.aborted || outerSignal !== null && outerSignal !== undefined && outerSignal.aborted)
        process2.nextTick(abort);
      return ret;
    }
    function pipe(src, dst, finish, { end }) {
      let ended = false;
      if (dst.on("close", () => {
        if (!ended)
          finish(new ERR_STREAM_PREMATURE_CLOSE);
      }), src.pipe(dst, { end: false }), end) {
        let endFn2 = function() {
          ended = true, dst.end();
        };
        var endFn = endFn2;
        if (isReadableFinished(src))
          process2.nextTick(endFn2);
        else
          src.once("end", endFn2);
      } else
        finish();
      return eos(src, { readable: true, writable: false }, (err) => {
        let rState = src._readableState;
        if (err && err.code === "ERR_STREAM_PREMATURE_CLOSE" && rState && rState.ended && !rState.errored && !rState.errorEmitted)
          src.once("end", finish).once("error", finish);
        else
          finish(err);
      }), eos(dst, { readable: false, writable: true }, finish);
    }
    module22.exports = { pipelineImpl, pipeline };
  });
  var require_compose = __commonJS2((exports22, module22) => {
    var { pipeline } = require_pipeline(), Duplex = require_duplex(), { destroyer } = require_destroy(), { isNodeStream, isReadable, isWritable, isWebStream, isTransformStream, isWritableStream, isReadableStream: isReadableStream2 } = require_utils(), { AbortError: AbortError2, codes: { ERR_INVALID_ARG_VALUE, ERR_MISSING_ARGS } } = require_errors(), eos = require_end_of_stream();
    module22.exports = function(...streams) {
      if (streams.length === 0)
        throw new ERR_MISSING_ARGS("streams");
      if (streams.length === 1)
        return Duplex.from(streams[0]);
      let orgStreams = [...streams];
      if (typeof streams[0] === "function")
        streams[0] = Duplex.from(streams[0]);
      if (typeof streams[streams.length - 1] === "function") {
        let idx = streams.length - 1;
        streams[idx] = Duplex.from(streams[idx]);
      }
      for (let n = 0;n < streams.length; ++n) {
        if (!isNodeStream(streams[n]) && !isWebStream(streams[n]))
          continue;
        if (n < streams.length - 1 && !(isReadable(streams[n]) || isReadableStream2(streams[n]) || isTransformStream(streams[n])))
          throw new ERR_INVALID_ARG_VALUE(`streams[${n}]`, orgStreams[n], "must be readable");
        if (n > 0 && !(isWritable(streams[n]) || isWritableStream(streams[n]) || isTransformStream(streams[n])))
          throw new ERR_INVALID_ARG_VALUE(`streams[${n}]`, orgStreams[n], "must be writable");
      }
      let ondrain, onfinish, onreadable, onclose, d;
      function onfinished(err) {
        let cb = onclose;
        if (onclose = null, cb)
          cb(err);
        else if (err)
          d.destroy(err);
        else if (!readable && !writable)
          d.destroy();
      }
      let head = streams[0], tail = pipeline(streams, onfinished), writable = !!(isWritable(head) || isWritableStream(head) || isTransformStream(head)), readable = !!(isReadable(tail) || isReadableStream2(tail) || isTransformStream(tail));
      if (d = new Duplex({ writableObjectMode: !!(head !== null && head !== undefined && head.writableObjectMode), readableObjectMode: !!(tail !== null && tail !== undefined && tail.readableObjectMode), writable, readable }), writable) {
        if (isNodeStream(head))
          d._write = function(chunk, encoding, callback) {
            if (head.write(chunk, encoding))
              callback();
            else
              ondrain = callback;
          }, d._final = function(callback) {
            head.end(), onfinish = callback;
          }, head.on("drain", function() {
            if (ondrain) {
              let cb = ondrain;
              ondrain = null, cb();
            }
          });
        else if (isWebStream(head)) {
          let writer = (isTransformStream(head) ? head.writable : head).getWriter();
          d._write = async function(chunk, encoding, callback) {
            try {
              await writer.ready, writer.write(chunk).catch(() => {}), callback();
            } catch (err) {
              callback(err);
            }
          }, d._final = async function(callback) {
            try {
              await writer.ready, writer.close().catch(() => {}), onfinish = callback;
            } catch (err) {
              callback(err);
            }
          };
        }
        let toRead = isTransformStream(tail) ? tail.readable : tail;
        eos(toRead, () => {
          if (onfinish) {
            let cb = onfinish;
            onfinish = null, cb();
          }
        });
      }
      if (readable) {
        if (isNodeStream(tail))
          tail.on("readable", function() {
            if (onreadable) {
              let cb = onreadable;
              onreadable = null, cb();
            }
          }), tail.on("end", function() {
            d.push(null);
          }), d._read = function() {
            while (true) {
              let buf = tail.read();
              if (buf === null) {
                onreadable = d._read;
                return;
              }
              if (!d.push(buf))
                return;
            }
          };
        else if (isWebStream(tail)) {
          let reader = (isTransformStream(tail) ? tail.readable : tail).getReader();
          d._read = async function() {
            while (true)
              try {
                let { value, done } = await reader.read();
                if (!d.push(value))
                  return;
                if (done) {
                  d.push(null);
                  return;
                }
              } catch {
                return;
              }
          };
        }
      }
      return d._destroy = function(err, callback) {
        if (!err && onclose !== null)
          err = new AbortError2;
        if (onreadable = null, ondrain = null, onfinish = null, onclose === null)
          callback(err);
        else if (onclose = callback, isNodeStream(tail))
          destroyer(tail, err);
      }, d;
    };
  });
  var require_operators = __commonJS2((exports22, module22) => {
    var AbortController2 = globalThis.AbortController || require_abort_controller().AbortController, { codes: { ERR_INVALID_ARG_VALUE, ERR_INVALID_ARG_TYPE: ERR_INVALID_ARG_TYPE3, ERR_MISSING_ARGS, ERR_OUT_OF_RANGE: ERR_OUT_OF_RANGE3 }, AbortError: AbortError2 } = require_errors(), { validateAbortSignal: validateAbortSignal2, validateInteger, validateObject } = require_validators(), kWeakHandler = require_primordials().Symbol("kWeak"), kResistStopPropagation = require_primordials().Symbol("kResistStopPropagation"), { finished } = require_end_of_stream(), staticCompose = require_compose(), { addAbortSignalNoValidate } = require_add_abort_signal(), { isWritable, isNodeStream } = require_utils(), { deprecate: deprecate2 } = require_util(), { ArrayPrototypePush, Boolean: Boolean2, MathFloor, Number: Number2, NumberIsNaN, Promise: Promise2, PromiseReject, PromiseResolve, PromisePrototypeThen, Symbol: Symbol2 } = require_primordials(), kEmpty = Symbol2("kEmpty"), kEof = Symbol2("kEof");
    function compose(stream, options) {
      if (options != null)
        validateObject(options, "options");
      if ((options === null || options === undefined ? undefined : options.signal) != null)
        validateAbortSignal2(options.signal, "options.signal");
      if (isNodeStream(stream) && !isWritable(stream))
        throw new ERR_INVALID_ARG_VALUE("stream", stream, "must be writable");
      let composedStream = staticCompose(this, stream);
      if (options !== null && options !== undefined && options.signal)
        addAbortSignalNoValidate(options.signal, composedStream);
      return composedStream;
    }
    function map(fn, options) {
      if (typeof fn !== "function")
        throw new ERR_INVALID_ARG_TYPE3("fn", ["Function", "AsyncFunction"], fn);
      if (options != null)
        validateObject(options, "options");
      if ((options === null || options === undefined ? undefined : options.signal) != null)
        validateAbortSignal2(options.signal, "options.signal");
      let concurrency = 1;
      if ((options === null || options === undefined ? undefined : options.concurrency) != null)
        concurrency = MathFloor(options.concurrency);
      let highWaterMark = concurrency - 1;
      if ((options === null || options === undefined ? undefined : options.highWaterMark) != null)
        highWaterMark = MathFloor(options.highWaterMark);
      return validateInteger(concurrency, "options.concurrency", 1), validateInteger(highWaterMark, "options.highWaterMark", 0), highWaterMark += concurrency, async function* () {
        let signal = require_util().AbortSignalAny([options === null || options === undefined ? undefined : options.signal].filter(Boolean2)), stream = this, queue = [], signalOpt = { signal }, next, resume, done = false, cnt = 0;
        function onCatch() {
          done = true, afterItemProcessed();
        }
        function afterItemProcessed() {
          cnt -= 1, maybeResume();
        }
        function maybeResume() {
          if (resume && !done && cnt < concurrency && queue.length < highWaterMark)
            resume(), resume = null;
        }
        async function pump() {
          try {
            for await (let val of stream) {
              if (done)
                return;
              if (signal.aborted)
                throw new AbortError2;
              try {
                if (val = fn(val, signalOpt), val === kEmpty)
                  continue;
                val = PromiseResolve(val);
              } catch (err) {
                val = PromiseReject(err);
              }
              if (cnt += 1, PromisePrototypeThen(val, afterItemProcessed, onCatch), queue.push(val), next)
                next(), next = null;
              if (!done && (queue.length >= highWaterMark || cnt >= concurrency))
                await new Promise2((resolve) => {
                  resume = resolve;
                });
            }
            queue.push(kEof);
          } catch (err) {
            let val = PromiseReject(err);
            PromisePrototypeThen(val, afterItemProcessed, onCatch), queue.push(val);
          } finally {
            if (done = true, next)
              next(), next = null;
          }
        }
        pump();
        try {
          while (true) {
            while (queue.length > 0) {
              let val = await queue[0];
              if (val === kEof)
                return;
              if (signal.aborted)
                throw new AbortError2;
              if (val !== kEmpty)
                yield val;
              queue.shift(), maybeResume();
            }
            await new Promise2((resolve) => {
              next = resolve;
            });
          }
        } finally {
          if (done = true, resume)
            resume(), resume = null;
        }
      }.call(this);
    }
    function asIndexedPairs(options = undefined) {
      if (options != null)
        validateObject(options, "options");
      if ((options === null || options === undefined ? undefined : options.signal) != null)
        validateAbortSignal2(options.signal, "options.signal");
      return async function* () {
        let index = 0;
        for await (let val of this) {
          var _options$signal;
          if (options !== null && options !== undefined && (_options$signal = options.signal) !== null && _options$signal !== undefined && _options$signal.aborted)
            throw new AbortError2({ cause: options.signal.reason });
          yield [index++, val];
        }
      }.call(this);
    }
    async function some(fn, options = undefined) {
      for await (let unused of filter2.call(this, fn, options))
        return true;
      return false;
    }
    async function every(fn, options = undefined) {
      if (typeof fn !== "function")
        throw new ERR_INVALID_ARG_TYPE3("fn", ["Function", "AsyncFunction"], fn);
      return !await some.call(this, async (...args) => {
        return !await fn(...args);
      }, options);
    }
    async function find(fn, options) {
      for await (let result of filter2.call(this, fn, options))
        return result;
      return;
    }
    async function forEach2(fn, options) {
      if (typeof fn !== "function")
        throw new ERR_INVALID_ARG_TYPE3("fn", ["Function", "AsyncFunction"], fn);
      async function forEachFn(value, options2) {
        return await fn(value, options2), kEmpty;
      }
      for await (let unused of map.call(this, forEachFn, options))
        ;
    }
    function filter2(fn, options) {
      if (typeof fn !== "function")
        throw new ERR_INVALID_ARG_TYPE3("fn", ["Function", "AsyncFunction"], fn);
      async function filterFn(value, options2) {
        if (await fn(value, options2))
          return value;
        return kEmpty;
      }
      return map.call(this, filterFn, options);
    }

    class ReduceAwareErrMissingArgs extends ERR_MISSING_ARGS {
      constructor() {
        super("reduce");
        this.message = "Reduce of an empty stream requires an initial value";
      }
    }
    async function reduce(reducer, initialValue, options) {
      var _options$signal2;
      if (typeof reducer !== "function")
        throw new ERR_INVALID_ARG_TYPE3("reducer", ["Function", "AsyncFunction"], reducer);
      if (options != null)
        validateObject(options, "options");
      if ((options === null || options === undefined ? undefined : options.signal) != null)
        validateAbortSignal2(options.signal, "options.signal");
      let hasInitialValue = arguments.length > 1;
      if (options !== null && options !== undefined && (_options$signal2 = options.signal) !== null && _options$signal2 !== undefined && _options$signal2.aborted) {
        let err = new AbortError2(undefined, { cause: options.signal.reason });
        throw this.once("error", () => {}), await finished(this.destroy(err)), err;
      }
      let ac = new AbortController2, signal = ac.signal;
      if (options !== null && options !== undefined && options.signal) {
        let opts = { once: true, [kWeakHandler]: this, [kResistStopPropagation]: true };
        options.signal.addEventListener("abort", () => ac.abort(), opts);
      }
      let gotAnyItemFromStream = false;
      try {
        for await (let value of this) {
          var _options$signal3;
          if (gotAnyItemFromStream = true, options !== null && options !== undefined && (_options$signal3 = options.signal) !== null && _options$signal3 !== undefined && _options$signal3.aborted)
            throw new AbortError2;
          if (!hasInitialValue)
            initialValue = value, hasInitialValue = true;
          else
            initialValue = await reducer(initialValue, value, { signal });
        }
        if (!gotAnyItemFromStream && !hasInitialValue)
          throw new ReduceAwareErrMissingArgs;
      } finally {
        ac.abort();
      }
      return initialValue;
    }
    async function toArray2(options) {
      if (options != null)
        validateObject(options, "options");
      if ((options === null || options === undefined ? undefined : options.signal) != null)
        validateAbortSignal2(options.signal, "options.signal");
      let result = [];
      for await (let val of this) {
        var _options$signal4;
        if (options !== null && options !== undefined && (_options$signal4 = options.signal) !== null && _options$signal4 !== undefined && _options$signal4.aborted)
          throw new AbortError2(undefined, { cause: options.signal.reason });
        ArrayPrototypePush(result, val);
      }
      return result;
    }
    function flatMap(fn, options) {
      let values = map.call(this, fn, options);
      return async function* () {
        for await (let val of values)
          yield* val;
      }.call(this);
    }
    function toIntegerOrInfinity(number) {
      if (number = Number2(number), NumberIsNaN(number))
        return 0;
      if (number < 0)
        throw new ERR_OUT_OF_RANGE3("number", ">= 0", number);
      return number;
    }
    function drop(number, options = undefined) {
      if (options != null)
        validateObject(options, "options");
      if ((options === null || options === undefined ? undefined : options.signal) != null)
        validateAbortSignal2(options.signal, "options.signal");
      return number = toIntegerOrInfinity(number), async function* () {
        var _options$signal5;
        if (options !== null && options !== undefined && (_options$signal5 = options.signal) !== null && _options$signal5 !== undefined && _options$signal5.aborted)
          throw new AbortError2;
        for await (let val of this) {
          var _options$signal6;
          if (options !== null && options !== undefined && (_options$signal6 = options.signal) !== null && _options$signal6 !== undefined && _options$signal6.aborted)
            throw new AbortError2;
          if (number-- <= 0)
            yield val;
        }
      }.call(this);
    }
    function take(number, options = undefined) {
      if (options != null)
        validateObject(options, "options");
      if ((options === null || options === undefined ? undefined : options.signal) != null)
        validateAbortSignal2(options.signal, "options.signal");
      return number = toIntegerOrInfinity(number), async function* () {
        var _options$signal7;
        if (options !== null && options !== undefined && (_options$signal7 = options.signal) !== null && _options$signal7 !== undefined && _options$signal7.aborted)
          throw new AbortError2;
        for await (let val of this) {
          var _options$signal8;
          if (options !== null && options !== undefined && (_options$signal8 = options.signal) !== null && _options$signal8 !== undefined && _options$signal8.aborted)
            throw new AbortError2;
          if (number-- > 0)
            yield val;
          if (number <= 0)
            return;
        }
      }.call(this);
    }
    module22.exports.streamReturningOperators = { asIndexedPairs: deprecate2(asIndexedPairs, "readable.asIndexedPairs will be removed in a future version."), drop, filter: filter2, flatMap, map, take, compose };
    module22.exports.promiseReturningOperators = { every, forEach: forEach2, reduce, toArray: toArray2, some, find };
  });
  var require_promises = __commonJS2((exports22, module22) => {
    var { ArrayPrototypePop, Promise: Promise2 } = require_primordials(), { isIterable: isIterable2, isNodeStream, isWebStream } = require_utils(), { pipelineImpl: pl } = require_pipeline(), { finished } = require_end_of_stream();
    require_stream2();
    function pipeline(...streams) {
      return new Promise2((resolve, reject) => {
        let signal, end, lastArg = streams[streams.length - 1];
        if (lastArg && typeof lastArg === "object" && !isNodeStream(lastArg) && !isIterable2(lastArg) && !isWebStream(lastArg)) {
          let options = ArrayPrototypePop(streams);
          signal = options.signal, end = options.end;
        }
        pl(streams, (err, value) => {
          if (err)
            reject(err);
          else
            resolve(value);
        }, { signal, end });
      });
    }
    module22.exports = { finished, pipeline };
  });
  var require_stream2 = __commonJS2((exports22, module22) => {
    var { Buffer: Buffer3 } = (init_buffer(), __toCommonJS(exports_buffer)), { ObjectDefineProperty, ObjectKeys, ReflectApply } = require_primordials(), { promisify: { custom: customPromisify } } = require_util(), { streamReturningOperators, promiseReturningOperators } = require_operators(), { codes: { ERR_ILLEGAL_CONSTRUCTOR } } = require_errors(), compose = require_compose(), { setDefaultHighWaterMark, getDefaultHighWaterMark } = require_state(), { pipeline } = require_pipeline(), { destroyer } = require_destroy(), eos = require_end_of_stream(), promises = require_promises(), utils = require_utils(), Stream = module22.exports = require_legacy().Stream;
    Stream.isDestroyed = utils.isDestroyed;
    Stream.isDisturbed = utils.isDisturbed;
    Stream.isErrored = utils.isErrored;
    Stream.isReadable = utils.isReadable;
    Stream.isWritable = utils.isWritable;
    Stream.Readable = require_readable();
    for (let key of ObjectKeys(streamReturningOperators)) {
      let fn = function(...args) {
        if (new.target)
          throw ERR_ILLEGAL_CONSTRUCTOR();
        return Stream.Readable.from(ReflectApply(op, this, args));
      }, op = streamReturningOperators[key];
      ObjectDefineProperty(fn, "name", { __proto__: null, value: op.name }), ObjectDefineProperty(fn, "length", { __proto__: null, value: op.length }), ObjectDefineProperty(Stream.Readable.prototype, key, { __proto__: null, value: fn, enumerable: false, configurable: true, writable: true });
    }
    for (let key of ObjectKeys(promiseReturningOperators)) {
      let fn = function(...args) {
        if (new.target)
          throw ERR_ILLEGAL_CONSTRUCTOR();
        return ReflectApply(op, this, args);
      }, op = promiseReturningOperators[key];
      ObjectDefineProperty(fn, "name", { __proto__: null, value: op.name }), ObjectDefineProperty(fn, "length", { __proto__: null, value: op.length }), ObjectDefineProperty(Stream.Readable.prototype, key, { __proto__: null, value: fn, enumerable: false, configurable: true, writable: true });
    }
    Stream.Writable = require_writable();
    Stream.Duplex = require_duplex();
    Stream.Transform = require_transform();
    Stream.PassThrough = require_passthrough();
    Stream.pipeline = pipeline;
    var { addAbortSignal } = require_add_abort_signal();
    Stream.addAbortSignal = addAbortSignal;
    Stream.finished = eos;
    Stream.destroy = destroyer;
    Stream.compose = compose;
    Stream.setDefaultHighWaterMark = setDefaultHighWaterMark;
    Stream.getDefaultHighWaterMark = getDefaultHighWaterMark;
    ObjectDefineProperty(Stream, "promises", { __proto__: null, configurable: true, enumerable: true, get() {
      return promises;
    } });
    ObjectDefineProperty(pipeline, customPromisify, { __proto__: null, enumerable: true, get() {
      return promises.pipeline;
    } });
    ObjectDefineProperty(eos, customPromisify, { __proto__: null, enumerable: true, get() {
      return promises.finished;
    } });
    Stream.Stream = Stream;
    Stream._isUint8Array = function(value) {
      return value instanceof Uint8Array;
    };
    Stream._uint8ArrayToBuffer = function(chunk) {
      return Buffer3.from(chunk.buffer, chunk.byteOffset, chunk.byteLength);
    };
  });
  var require_ours = __commonJS2((exports22, module22) => {
    var Stream = require_stream();
    {
      let CustomStream = require_stream2(), promises = require_promises(), originalDestroy = CustomStream.Readable.destroy;
      module22.exports = CustomStream.Readable, module22.exports._uint8ArrayToBuffer = CustomStream._uint8ArrayToBuffer, module22.exports._isUint8Array = CustomStream._isUint8Array, module22.exports.isDisturbed = CustomStream.isDisturbed, module22.exports.isErrored = CustomStream.isErrored, module22.exports.isReadable = CustomStream.isReadable, module22.exports.Readable = CustomStream.Readable, module22.exports.Writable = CustomStream.Writable, module22.exports.Duplex = CustomStream.Duplex, module22.exports.Transform = CustomStream.Transform, module22.exports.PassThrough = CustomStream.PassThrough, module22.exports.addAbortSignal = CustomStream.addAbortSignal, module22.exports.finished = CustomStream.finished, module22.exports.destroy = CustomStream.destroy, module22.exports.destroy = originalDestroy, module22.exports.pipeline = CustomStream.pipeline, module22.exports.compose = CustomStream.compose, Object.defineProperty(CustomStream, "promises", { configurable: true, enumerable: true, get() {
        return promises;
      } }), module22.exports.Stream = CustomStream.Stream;
    }
    module22.exports.default = module22.exports;
  });
  module2.exports = require_ours();
});

// node:url
var exports_url = {};
__export(exports_url, {
  resolveObject: () => urlResolveObject,
  resolve: () => urlResolve,
  parse: () => urlParse,
  format: () => urlFormat,
  default: () => url_default,
  Url: () => Url,
  URLSearchParams: () => URLSearchParams2,
  URL: () => URL2
});
function util_isString(arg) {
  return typeof arg === "string";
}
function util_isObject(arg) {
  return typeof arg === "object" && arg !== null;
}
function util_isNull(arg) {
  return arg === null;
}
function util_isNullOrUndefined(arg) {
  return arg == null;
}
function Url() {
  this.protocol = null, this.slashes = null, this.auth = null, this.host = null, this.port = null, this.hostname = null, this.hash = null, this.search = null, this.query = null, this.pathname = null, this.path = null, this.href = null;
}
function urlParse(url, parseQueryString, slashesDenoteHost) {
  if (url && util_isObject(url) && url instanceof Url)
    return url;
  var u = new Url;
  return u.parse(url, parseQueryString, slashesDenoteHost), u;
}
function urlFormat(obj) {
  if (util_isString(obj))
    obj = urlParse(obj);
  if (!(obj instanceof Url))
    return Url.prototype.format.call(obj);
  return obj.format();
}
function urlResolve(source, relative) {
  return urlParse(source, false, true).resolve(relative);
}
function urlResolveObject(source, relative) {
  if (!source)
    return relative;
  return urlParse(source, false, true).resolveObject(relative);
}
var URL2, URLSearchParams2, protocolPattern, portPattern, simplePathPattern, delims, unwise, autoEscape, nonHostChars, hostEndingChars, hostnameMaxLen = 255, hostnamePartPattern, hostnamePartStart, unsafeProtocol, hostlessProtocol, slashedProtocol, querystring, url_default;
var init_url = __esm(() => {
  ({ URL: URL2, URLSearchParams: URLSearchParams2 } = globalThis);
  protocolPattern = /^([a-z0-9.+-]+:)/i;
  portPattern = /:[0-9]*$/;
  simplePathPattern = /^(\/\/?(?!\/)[^\?\s]*)(\?[^\s]*)?$/;
  delims = ["<", ">", '"', "`", " ", "\r", `
`, "\t"];
  unwise = ["{", "}", "|", "\\", "^", "`"].concat(delims);
  autoEscape = ["'"].concat(unwise);
  nonHostChars = ["%", "/", "?", ";", "#"].concat(autoEscape);
  hostEndingChars = ["/", "?", "#"];
  hostnamePartPattern = /^[+a-z0-9A-Z_-]{0,63}$/;
  hostnamePartStart = /^([+a-z0-9A-Z_-]{0,63})(.*)$/;
  unsafeProtocol = { javascript: true, "javascript:": true };
  hostlessProtocol = { javascript: true, "javascript:": true };
  slashedProtocol = { http: true, https: true, ftp: true, gopher: true, file: true, "http:": true, "https:": true, "ftp:": true, "gopher:": true, "file:": true };
  querystring = { parse(str) {
    var decode = decodeURIComponent;
    return (str + "").replace(/\+/g, " ").split("&").filter(Boolean).reduce(function(obj, item, index) {
      var ref = item.split("="), key = decode(ref[0] || ""), val = decode(ref[1] || ""), prev = obj[key];
      return obj[key] = prev === undefined ? val : [].concat(prev, val), obj;
    }, {});
  }, stringify(obj) {
    var encode3 = encodeURIComponent;
    return Object.keys(obj || {}).reduce(function(arr, key) {
      return [].concat(obj[key]).forEach(function(v) {
        arr.push(encode3(key) + "=" + encode3(v));
      }), arr;
    }, []).join("&").replace(/\s/g, "+");
  } };
  Url.prototype.parse = function(url, parseQueryString, slashesDenoteHost) {
    if (!util_isString(url))
      throw TypeError("Parameter 'url' must be a string, not " + typeof url);
    var queryIndex = url.indexOf("?"), splitter = queryIndex !== -1 && queryIndex < url.indexOf("#") ? "?" : "#", uSplit = url.split(splitter), slashRegex = /\\/g;
    uSplit[0] = uSplit[0].replace(slashRegex, "/"), url = uSplit.join(splitter);
    var rest = url;
    if (rest = rest.trim(), !slashesDenoteHost && url.split("#").length === 1) {
      var simplePath = simplePathPattern.exec(rest);
      if (simplePath) {
        if (this.path = rest, this.href = rest, this.pathname = simplePath[1], simplePath[2])
          if (this.search = simplePath[2], parseQueryString)
            this.query = querystring.parse(this.search.substr(1));
          else
            this.query = this.search.substr(1);
        else if (parseQueryString)
          this.search = "", this.query = {};
        return this;
      }
    }
    var proto = protocolPattern.exec(rest);
    if (proto) {
      proto = proto[0];
      var lowerProto = proto.toLowerCase();
      this.protocol = lowerProto, rest = rest.substr(proto.length);
    }
    if (slashesDenoteHost || proto || rest.match(/^\/\/[^@\/]+@[^@\/]+/)) {
      var slashes = rest.substr(0, 2) === "//";
      if (slashes && !(proto && hostlessProtocol[proto]))
        rest = rest.substr(2), this.slashes = true;
    }
    if (!hostlessProtocol[proto] && (slashes || proto && !slashedProtocol[proto])) {
      var hostEnd = -1;
      for (var i2 = 0;i2 < hostEndingChars.length; i2++) {
        var hec = rest.indexOf(hostEndingChars[i2]);
        if (hec !== -1 && (hostEnd === -1 || hec < hostEnd))
          hostEnd = hec;
      }
      var auth, atSign;
      if (hostEnd === -1)
        atSign = rest.lastIndexOf("@");
      else
        atSign = rest.lastIndexOf("@", hostEnd);
      if (atSign !== -1)
        auth = rest.slice(0, atSign), rest = rest.slice(atSign + 1), this.auth = decodeURIComponent(auth);
      hostEnd = -1;
      for (var i2 = 0;i2 < nonHostChars.length; i2++) {
        var hec = rest.indexOf(nonHostChars[i2]);
        if (hec !== -1 && (hostEnd === -1 || hec < hostEnd))
          hostEnd = hec;
      }
      if (hostEnd === -1)
        hostEnd = rest.length;
      this.host = rest.slice(0, hostEnd), rest = rest.slice(hostEnd), this.parseHost(), this.hostname = this.hostname || "";
      var ipv6Hostname = this.hostname[0] === "[" && this.hostname[this.hostname.length - 1] === "]";
      if (!ipv6Hostname) {
        var hostparts = this.hostname.split(/\./);
        for (var i2 = 0, l = hostparts.length;i2 < l; i2++) {
          var part = hostparts[i2];
          if (!part)
            continue;
          if (!part.match(hostnamePartPattern)) {
            var newpart = "";
            for (var j = 0, k = part.length;j < k; j++)
              if (part.charCodeAt(j) > 127)
                newpart += "x";
              else
                newpart += part[j];
            if (!newpart.match(hostnamePartPattern)) {
              var validParts = hostparts.slice(0, i2), notHost = hostparts.slice(i2 + 1), bit = part.match(hostnamePartStart);
              if (bit)
                validParts.push(bit[1]), notHost.unshift(bit[2]);
              if (notHost.length)
                rest = "/" + notHost.join(".") + rest;
              this.hostname = validParts.join(".");
              break;
            }
          }
        }
      }
      if (this.hostname.length > hostnameMaxLen)
        this.hostname = "";
      else
        this.hostname = this.hostname.toLowerCase();
      if (!ipv6Hostname)
        this.hostname = new URL2(`https://${this.hostname}`).hostname;
      var p = this.port ? ":" + this.port : "", h = this.hostname || "";
      if (this.host = h + p, this.href += this.host, ipv6Hostname) {
        if (this.hostname = this.hostname.substr(1, this.hostname.length - 2), rest[0] !== "/")
          rest = "/" + rest;
      }
    }
    if (!unsafeProtocol[lowerProto])
      for (var i2 = 0, l = autoEscape.length;i2 < l; i2++) {
        var ae = autoEscape[i2];
        if (rest.indexOf(ae) === -1)
          continue;
        var esc = encodeURIComponent(ae);
        if (esc === ae)
          esc = escape(ae);
        rest = rest.split(ae).join(esc);
      }
    var hash = rest.indexOf("#");
    if (hash !== -1)
      this.hash = rest.substr(hash), rest = rest.slice(0, hash);
    var qm = rest.indexOf("?");
    if (qm !== -1) {
      if (this.search = rest.substr(qm), this.query = rest.substr(qm + 1), parseQueryString)
        this.query = querystring.parse(this.query);
      rest = rest.slice(0, qm);
    } else if (parseQueryString)
      this.search = "", this.query = {};
    if (rest)
      this.pathname = rest;
    if (slashedProtocol[lowerProto] && this.hostname && !this.pathname)
      this.pathname = "/";
    if (this.pathname || this.search) {
      var p = this.pathname || "", s = this.search || "";
      this.path = p + s;
    }
    return this.href = this.format(), this;
  };
  Url.prototype.format = function() {
    var auth = this.auth || "";
    if (auth)
      auth = encodeURIComponent(auth), auth = auth.replace(/%3A/i, ":"), auth += "@";
    var protocol = this.protocol || "", pathname = this.pathname || "", hash = this.hash || "", host = false, query = "";
    if (this.host)
      host = auth + this.host;
    else if (this.hostname) {
      if (host = auth + (this.hostname.indexOf(":") === -1 ? this.hostname : "[" + this.hostname + "]"), this.port)
        host += ":" + this.port;
    }
    if (this.query && util_isObject(this.query) && Object.keys(this.query).length)
      query = querystring.stringify(this.query);
    var search = this.search || query && "?" + query || "";
    if (protocol && protocol.substr(-1) !== ":")
      protocol += ":";
    if (this.slashes || (!protocol || slashedProtocol[protocol]) && host !== false) {
      if (host = "//" + (host || ""), pathname && pathname.charAt(0) !== "/")
        pathname = "/" + pathname;
    } else if (!host)
      host = "";
    if (hash && hash.charAt(0) !== "#")
      hash = "#" + hash;
    if (search && search.charAt(0) !== "?")
      search = "?" + search;
    return pathname = pathname.replace(/[?#]/g, function(match) {
      return encodeURIComponent(match);
    }), search = search.replace("#", "%23"), protocol + host + pathname + search + hash;
  };
  Url.prototype.resolve = function(relative) {
    return this.resolveObject(urlParse(relative, false, true)).format();
  };
  Url.prototype.resolveObject = function(relative) {
    if (util_isString(relative)) {
      var rel = new Url;
      rel.parse(relative, false, true), relative = rel;
    }
    var result = new Url, tkeys = Object.keys(this);
    for (var tk = 0;tk < tkeys.length; tk++) {
      var tkey = tkeys[tk];
      result[tkey] = this[tkey];
    }
    if (result.hash = relative.hash, relative.href === "")
      return result.href = result.format(), result;
    if (relative.slashes && !relative.protocol) {
      var rkeys = Object.keys(relative);
      for (var rk = 0;rk < rkeys.length; rk++) {
        var rkey = rkeys[rk];
        if (rkey !== "protocol")
          result[rkey] = relative[rkey];
      }
      if (slashedProtocol[result.protocol] && result.hostname && !result.pathname)
        result.path = result.pathname = "/";
      return result.href = result.format(), result;
    }
    if (relative.protocol && relative.protocol !== result.protocol) {
      if (!slashedProtocol[relative.protocol]) {
        var keys = Object.keys(relative);
        for (var v = 0;v < keys.length; v++) {
          var k = keys[v];
          result[k] = relative[k];
        }
        return result.href = result.format(), result;
      }
      if (result.protocol = relative.protocol, !relative.host && !hostlessProtocol[relative.protocol]) {
        var relPath = (relative.pathname || "").split("/");
        while (relPath.length && !(relative.host = relPath.shift()))
          ;
        if (!relative.host)
          relative.host = "";
        if (!relative.hostname)
          relative.hostname = "";
        if (relPath[0] !== "")
          relPath.unshift("");
        if (relPath.length < 2)
          relPath.unshift("");
        result.pathname = relPath.join("/");
      } else
        result.pathname = relative.pathname;
      if (result.search = relative.search, result.query = relative.query, result.host = relative.host || "", result.auth = relative.auth, result.hostname = relative.hostname || relative.host, result.port = relative.port, result.pathname || result.search) {
        var p = result.pathname || "", s = result.search || "";
        result.path = p + s;
      }
      return result.slashes = result.slashes || relative.slashes, result.href = result.format(), result;
    }
    var isSourceAbs = result.pathname && result.pathname.charAt(0) === "/", isRelAbs = relative.host || relative.pathname && relative.pathname.charAt(0) === "/", mustEndAbs = isRelAbs || isSourceAbs || result.host && relative.pathname, removeAllDots = mustEndAbs, srcPath = result.pathname && result.pathname.split("/") || [], relPath = relative.pathname && relative.pathname.split("/") || [], psychotic = result.protocol && !slashedProtocol[result.protocol];
    if (psychotic) {
      if (result.hostname = "", result.port = null, result.host)
        if (srcPath[0] === "")
          srcPath[0] = result.host;
        else
          srcPath.unshift(result.host);
      if (result.host = "", relative.protocol) {
        if (relative.hostname = null, relative.port = null, relative.host)
          if (relPath[0] === "")
            relPath[0] = relative.host;
          else
            relPath.unshift(relative.host);
        relative.host = null;
      }
      mustEndAbs = mustEndAbs && (relPath[0] === "" || srcPath[0] === "");
    }
    if (isRelAbs)
      result.host = relative.host || relative.host === "" ? relative.host : result.host, result.hostname = relative.hostname || relative.hostname === "" ? relative.hostname : result.hostname, result.search = relative.search, result.query = relative.query, srcPath = relPath;
    else if (relPath.length) {
      if (!srcPath)
        srcPath = [];
      srcPath.pop(), srcPath = srcPath.concat(relPath), result.search = relative.search, result.query = relative.query;
    } else if (!util_isNullOrUndefined(relative.search)) {
      if (psychotic) {
        result.hostname = result.host = srcPath.shift();
        var authInHost = result.host && result.host.indexOf("@") > 0 ? result.host.split("@") : false;
        if (authInHost)
          result.auth = authInHost.shift(), result.host = result.hostname = authInHost.shift();
      }
      if (result.search = relative.search, result.query = relative.query, !util_isNull(result.pathname) || !util_isNull(result.search))
        result.path = (result.pathname ? result.pathname : "") + (result.search ? result.search : "");
      return result.href = result.format(), result;
    }
    if (!srcPath.length) {
      if (result.pathname = null, result.search)
        result.path = "/" + result.search;
      else
        result.path = null;
      return result.href = result.format(), result;
    }
    var last = srcPath.slice(-1)[0], hasTrailingSlash = (result.host || relative.host || srcPath.length > 1) && (last === "." || last === "..") || last === "", up = 0;
    for (var i2 = srcPath.length;i2 >= 0; i2--)
      if (last = srcPath[i2], last === ".")
        srcPath.splice(i2, 1);
      else if (last === "..")
        srcPath.splice(i2, 1), up++;
      else if (up)
        srcPath.splice(i2, 1), up--;
    if (!mustEndAbs && !removeAllDots)
      for (;up--; up)
        srcPath.unshift("..");
    if (mustEndAbs && srcPath[0] !== "" && (!srcPath[0] || srcPath[0].charAt(0) !== "/"))
      srcPath.unshift("");
    if (hasTrailingSlash && srcPath.join("/").substr(-1) !== "/")
      srcPath.push("");
    var isAbsolute = srcPath[0] === "" || srcPath[0] && srcPath[0].charAt(0) === "/";
    if (psychotic) {
      result.hostname = result.host = isAbsolute ? "" : srcPath.length ? srcPath.shift() : "";
      var authInHost = result.host && result.host.indexOf("@") > 0 ? result.host.split("@") : false;
      if (authInHost)
        result.auth = authInHost.shift(), result.host = result.hostname = authInHost.shift();
    }
    if (mustEndAbs = mustEndAbs || result.host && srcPath.length, mustEndAbs && !isAbsolute)
      srcPath.unshift("");
    if (!srcPath.length)
      result.pathname = null, result.path = null;
    else
      result.pathname = srcPath.join("/");
    if (!util_isNull(result.pathname) || !util_isNull(result.search))
      result.path = (result.pathname ? result.pathname : "") + (result.search ? result.search : "");
    return result.auth = relative.auth || result.auth, result.slashes = result.slashes || relative.slashes, result.href = result.format(), result;
  };
  Url.prototype.parseHost = function() {
    var host = this.host, port = portPattern.exec(host);
    if (port) {
      if (port = port[0], port !== ":")
        this.port = port.substr(1);
      host = host.substr(0, host.length - port.length);
    }
    if (host)
      this.hostname = host;
  };
  url_default = { parse: urlParse, resolve: urlResolve, resolveObject: urlResolveObject, format: urlFormat, Url, URL: URL2, URLSearchParams: URLSearchParams2 };
});

// node:http
var exports_http = {};
__export(exports_http, {
  request: () => request,
  globalAgent: () => globalAgent,
  get: () => get,
  default: () => http_default,
  STATUS_CODES: () => STATUS_CODES,
  METHODS: () => METHODS,
  IncomingMessage: () => IncomingMessage,
  ClientRequest: () => ClientRequest,
  Agent: () => Agent
});
var __create, __getProtoOf, __defProp2, __getOwnPropNames2, __hasOwnProp2, __toESM = (mod, isNodeMode, target) => {
  target = mod != null ? __create(__getProtoOf(mod)) : {};
  let to = isNodeMode || !mod || !mod.__esModule ? __defProp2(target, "default", { value: mod, enumerable: true }) : target;
  for (let key of __getOwnPropNames2(mod))
    if (!__hasOwnProp2.call(to, key))
      __defProp2(to, key, { get: () => mod[key], enumerable: true });
  return to;
}, __commonJS2 = (cb, mod) => () => (mod || cb((mod = { exports: {} }).exports, mod), mod.exports), require_capability, require_inherits_browser, require_inherits, require_buffer_list, require_destroy, require_errors, require_state, require_node, require__stream_writable, require__stream_duplex, require_safe_buffer, require_string_decoder, require_end_of_stream, require_async_iterator, require_from, require__stream_readable, require__stream_transform, require__stream_passthrough, require_pipeline, require_readable, require_response, require_request, require_immutable, require_builtin_status_codes, require_stream_http, import_stream_http, request, get, ClientRequest, IncomingMessage, Agent, globalAgent, STATUS_CODES, METHODS, http_default;
var init_http = __esm(() => {
  __create = Object.create;
  ({ getPrototypeOf: __getProtoOf, defineProperty: __defProp2, getOwnPropertyNames: __getOwnPropNames2 } = Object);
  __hasOwnProp2 = Object.prototype.hasOwnProperty;
  require_capability = __commonJS2((exports2) => {
    exports2.fetch = isFunction4(globalThis.fetch) && isFunction4(globalThis.ReadableStream);
    exports2.writableStream = isFunction4(globalThis.WritableStream);
    exports2.abortController = isFunction4(globalThis.AbortController);
    var xhr;
    function getXHR() {
      if (xhr !== undefined)
        return xhr;
      if (globalThis.XMLHttpRequest) {
        xhr = new globalThis.XMLHttpRequest;
        try {
          xhr.open("GET", globalThis.XDomainRequest ? "/" : "https://example.com");
        } catch (e) {
          xhr = null;
        }
      } else
        xhr = null;
      return xhr;
    }
    function checkTypeSupport(type) {
      var xhr2 = getXHR();
      if (!xhr2)
        return false;
      try {
        return xhr2.responseType = type, xhr2.responseType === type;
      } catch (e) {}
      return false;
    }
    exports2.arraybuffer = exports2.fetch || checkTypeSupport("arraybuffer");
    exports2.msstream = !exports2.fetch && checkTypeSupport("ms-stream");
    exports2.mozchunkedarraybuffer = !exports2.fetch && checkTypeSupport("moz-chunked-arraybuffer");
    exports2.overrideMimeType = exports2.fetch || (getXHR() ? isFunction4(getXHR().overrideMimeType) : false);
    function isFunction4(value) {
      return typeof value === "function";
    }
    xhr = null;
  });
  require_inherits_browser = __commonJS2((exports2, module2) => {
    if (typeof Object.create === "function")
      module2.exports = function(ctor, superCtor) {
        if (superCtor)
          ctor.super_ = superCtor, ctor.prototype = Object.create(superCtor.prototype, { constructor: { value: ctor, enumerable: false, writable: true, configurable: true } });
      };
    else
      module2.exports = function(ctor, superCtor) {
        if (superCtor) {
          ctor.super_ = superCtor;
          var TempCtor = function() {};
          TempCtor.prototype = superCtor.prototype, ctor.prototype = new TempCtor, ctor.prototype.constructor = ctor;
        }
      };
  });
  require_inherits = __commonJS2((exports2, module2) => {
    try {
      if (util = (init_util(), __toCommonJS(exports_util)), typeof util.inherits !== "function")
        throw "";
      module2.exports = util.inherits;
    } catch (e) {
      module2.exports = require_inherits_browser();
    }
    var util;
  });
  require_buffer_list = __commonJS2((exports2, module2) => {
    function ownKeys(object, enumerableOnly) {
      var keys = Object.keys(object);
      if (Object.getOwnPropertySymbols) {
        var symbols = Object.getOwnPropertySymbols(object);
        enumerableOnly && (symbols = symbols.filter(function(sym) {
          return Object.getOwnPropertyDescriptor(object, sym).enumerable;
        })), keys.push.apply(keys, symbols);
      }
      return keys;
    }
    function _objectSpread(target) {
      for (var i2 = 1;i2 < arguments.length; i2++) {
        var source = arguments[i2] != null ? arguments[i2] : {};
        i2 % 2 ? ownKeys(Object(source), true).forEach(function(key) {
          _defineProperty(target, key, source[key]);
        }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)) : ownKeys(Object(source)).forEach(function(key) {
          Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key));
        });
      }
      return target;
    }
    function _defineProperty(obj, key, value) {
      if (key = _toPropertyKey(key), key in obj)
        Object.defineProperty(obj, key, { value, enumerable: true, configurable: true, writable: true });
      else
        obj[key] = value;
      return obj;
    }
    function _classCallCheck(instance, Constructor) {
      if (!(instance instanceof Constructor))
        throw TypeError("Cannot call a class as a function");
    }
    function _defineProperties(target, props) {
      for (var i2 = 0;i2 < props.length; i2++) {
        var descriptor = props[i2];
        if (descriptor.enumerable = descriptor.enumerable || false, descriptor.configurable = true, "value" in descriptor)
          descriptor.writable = true;
        Object.defineProperty(target, _toPropertyKey(descriptor.key), descriptor);
      }
    }
    function _createClass(Constructor, protoProps, staticProps) {
      if (protoProps)
        _defineProperties(Constructor.prototype, protoProps);
      if (staticProps)
        _defineProperties(Constructor, staticProps);
      return Object.defineProperty(Constructor, "prototype", { writable: false }), Constructor;
    }
    function _toPropertyKey(arg) {
      var key = _toPrimitive(arg, "string");
      return typeof key === "symbol" ? key : String(key);
    }
    function _toPrimitive(input, hint) {
      if (typeof input !== "object" || input === null)
        return input;
      var prim = input[Symbol.toPrimitive];
      if (prim !== undefined) {
        var res = prim.call(input, hint || "default");
        if (typeof res !== "object")
          return res;
        throw TypeError("@@toPrimitive must return a primitive value.");
      }
      return (hint === "string" ? String : Number)(input);
    }
    var _require = (init_buffer(), __toCommonJS(exports_buffer)), Buffer22 = _require.Buffer, _require2 = (init_util(), __toCommonJS(exports_util)), inspect2 = _require2.inspect, custom = inspect2 && inspect2.custom || "inspect";
    function copyBuffer(src, target, offset) {
      Buffer22.prototype.copy.call(src, target, offset);
    }
    module2.exports = function() {
      function BufferList() {
        _classCallCheck(this, BufferList), this.head = null, this.tail = null, this.length = 0;
      }
      return _createClass(BufferList, [{ key: "push", value: function(v) {
        var entry = { data: v, next: null };
        if (this.length > 0)
          this.tail.next = entry;
        else
          this.head = entry;
        this.tail = entry, ++this.length;
      } }, { key: "unshift", value: function(v) {
        var entry = { data: v, next: this.head };
        if (this.length === 0)
          this.tail = entry;
        this.head = entry, ++this.length;
      } }, { key: "shift", value: function() {
        if (this.length === 0)
          return;
        var ret = this.head.data;
        if (this.length === 1)
          this.head = this.tail = null;
        else
          this.head = this.head.next;
        return --this.length, ret;
      } }, { key: "clear", value: function() {
        this.head = this.tail = null, this.length = 0;
      } }, { key: "join", value: function(s) {
        if (this.length === 0)
          return "";
        var p = this.head, ret = "" + p.data;
        while (p = p.next)
          ret += s + p.data;
        return ret;
      } }, { key: "concat", value: function(n) {
        if (this.length === 0)
          return Buffer22.alloc(0);
        var ret = Buffer22.allocUnsafe(n >>> 0), p = this.head, i2 = 0;
        while (p)
          copyBuffer(p.data, ret, i2), i2 += p.data.length, p = p.next;
        return ret;
      } }, { key: "consume", value: function(n, hasStrings) {
        var ret;
        if (n < this.head.data.length)
          ret = this.head.data.slice(0, n), this.head.data = this.head.data.slice(n);
        else if (n === this.head.data.length)
          ret = this.shift();
        else
          ret = hasStrings ? this._getString(n) : this._getBuffer(n);
        return ret;
      } }, { key: "first", value: function() {
        return this.head.data;
      } }, { key: "_getString", value: function(n) {
        var p = this.head, c = 1, ret = p.data;
        n -= ret.length;
        while (p = p.next) {
          var str = p.data, nb = n > str.length ? str.length : n;
          if (nb === str.length)
            ret += str;
          else
            ret += str.slice(0, n);
          if (n -= nb, n === 0) {
            if (nb === str.length)
              if (++c, p.next)
                this.head = p.next;
              else
                this.head = this.tail = null;
            else
              this.head = p, p.data = str.slice(nb);
            break;
          }
          ++c;
        }
        return this.length -= c, ret;
      } }, { key: "_getBuffer", value: function(n) {
        var ret = Buffer22.allocUnsafe(n), p = this.head, c = 1;
        p.data.copy(ret), n -= p.data.length;
        while (p = p.next) {
          var buf = p.data, nb = n > buf.length ? buf.length : n;
          if (buf.copy(ret, ret.length - n, 0, nb), n -= nb, n === 0) {
            if (nb === buf.length)
              if (++c, p.next)
                this.head = p.next;
              else
                this.head = this.tail = null;
            else
              this.head = p, p.data = buf.slice(nb);
            break;
          }
          ++c;
        }
        return this.length -= c, ret;
      } }, { key: custom, value: function(_, options) {
        return inspect2(this, _objectSpread(_objectSpread({}, options), {}, { depth: 0, customInspect: false }));
      } }]), BufferList;
    }();
  });
  require_destroy = __commonJS2((exports2, module2) => {
    function destroy(err, cb) {
      var _this = this, readableDestroyed = this._readableState && this._readableState.destroyed, writableDestroyed = this._writableState && this._writableState.destroyed;
      if (readableDestroyed || writableDestroyed) {
        if (cb)
          cb(err);
        else if (err) {
          if (!this._writableState)
            process.nextTick(emitErrorNT, this, err);
          else if (!this._writableState.errorEmitted)
            this._writableState.errorEmitted = true, process.nextTick(emitErrorNT, this, err);
        }
        return this;
      }
      if (this._readableState)
        this._readableState.destroyed = true;
      if (this._writableState)
        this._writableState.destroyed = true;
      return this._destroy(err || null, function(err2) {
        if (!cb && err2)
          if (!_this._writableState)
            process.nextTick(emitErrorAndCloseNT, _this, err2);
          else if (!_this._writableState.errorEmitted)
            _this._writableState.errorEmitted = true, process.nextTick(emitErrorAndCloseNT, _this, err2);
          else
            process.nextTick(emitCloseNT, _this);
        else if (cb)
          process.nextTick(emitCloseNT, _this), cb(err2);
        else
          process.nextTick(emitCloseNT, _this);
      }), this;
    }
    function emitErrorAndCloseNT(self2, err) {
      emitErrorNT(self2, err), emitCloseNT(self2);
    }
    function emitCloseNT(self2) {
      if (self2._writableState && !self2._writableState.emitClose)
        return;
      if (self2._readableState && !self2._readableState.emitClose)
        return;
      self2.emit("close");
    }
    function undestroy() {
      if (this._readableState)
        this._readableState.destroyed = false, this._readableState.reading = false, this._readableState.ended = false, this._readableState.endEmitted = false;
      if (this._writableState)
        this._writableState.destroyed = false, this._writableState.ended = false, this._writableState.ending = false, this._writableState.finalCalled = false, this._writableState.prefinished = false, this._writableState.finished = false, this._writableState.errorEmitted = false;
    }
    function emitErrorNT(self2, err) {
      self2.emit("error", err);
    }
    function errorOrDestroy(stream, err) {
      var { _readableState: rState, _writableState: wState } = stream;
      if (rState && rState.autoDestroy || wState && wState.autoDestroy)
        stream.destroy(err);
      else
        stream.emit("error", err);
    }
    module2.exports = { destroy, undestroy, errorOrDestroy };
  });
  require_errors = __commonJS2((exports2, module2) => {
    var codes = {};
    function createErrorType(code2, message, Base) {
      if (!Base)
        Base = Error;
      function getMessage(arg1, arg2, arg3) {
        if (typeof message === "string")
          return message;
        else
          return message(arg1, arg2, arg3);
      }

      class NodeError extends Base {
        constructor(arg1, arg2, arg3) {
          super(getMessage(arg1, arg2, arg3));
        }
      }
      NodeError.prototype.name = Base.name, NodeError.prototype.code = code2, codes[code2] = NodeError;
    }
    function oneOf(expected, thing) {
      if (Array.isArray(expected)) {
        let len2 = expected.length;
        if (expected = expected.map((i2) => String(i2)), len2 > 2)
          return `one of ${thing} ${expected.slice(0, len2 - 1).join(", ")}, or ` + expected[len2 - 1];
        else if (len2 === 2)
          return `one of ${thing} ${expected[0]} or ${expected[1]}`;
        else
          return `of ${thing} ${expected[0]}`;
      } else
        return `of ${thing} ${String(expected)}`;
    }
    function startsWith(str, search, pos) {
      return str.substr(!pos || pos < 0 ? 0 : +pos, search.length) === search;
    }
    function endsWith2(str, search, this_len) {
      if (this_len === undefined || this_len > str.length)
        this_len = str.length;
      return str.substring(this_len - search.length, this_len) === search;
    }
    function includes(str, search, start) {
      if (typeof start !== "number")
        start = 0;
      if (start + search.length > str.length)
        return false;
      else
        return str.indexOf(search, start) !== -1;
    }
    createErrorType("ERR_INVALID_OPT_VALUE", function(name, value) {
      return 'The value "' + value + '" is invalid for option "' + name + '"';
    }, TypeError);
    createErrorType("ERR_INVALID_ARG_TYPE", function(name, expected, actual) {
      let determiner;
      if (typeof expected === "string" && startsWith(expected, "not "))
        determiner = "must not be", expected = expected.replace(/^not /, "");
      else
        determiner = "must be";
      let msg;
      if (endsWith2(name, " argument"))
        msg = `The ${name} ${determiner} ${oneOf(expected, "type")}`;
      else {
        let type = includes(name, ".") ? "property" : "argument";
        msg = `The "${name}" ${type} ${determiner} ${oneOf(expected, "type")}`;
      }
      return msg += `. Received type ${typeof actual}`, msg;
    }, TypeError);
    createErrorType("ERR_STREAM_PUSH_AFTER_EOF", "stream.push() after EOF");
    createErrorType("ERR_METHOD_NOT_IMPLEMENTED", function(name) {
      return "The " + name + " method is not implemented";
    });
    createErrorType("ERR_STREAM_PREMATURE_CLOSE", "Premature close");
    createErrorType("ERR_STREAM_DESTROYED", function(name) {
      return "Cannot call " + name + " after a stream was destroyed";
    });
    createErrorType("ERR_MULTIPLE_CALLBACK", "Callback called multiple times");
    createErrorType("ERR_STREAM_CANNOT_PIPE", "Cannot pipe, not readable");
    createErrorType("ERR_STREAM_WRITE_AFTER_END", "write after end");
    createErrorType("ERR_STREAM_NULL_VALUES", "May not write null values to stream", TypeError);
    createErrorType("ERR_UNKNOWN_ENCODING", function(arg) {
      return "Unknown encoding: " + arg;
    }, TypeError);
    createErrorType("ERR_STREAM_UNSHIFT_AFTER_END_EVENT", "stream.unshift() after end event");
    exports2.codes = codes;
  });
  require_state = __commonJS2((exports2, module2) => {
    var ERR_INVALID_OPT_VALUE = require_errors().codes.ERR_INVALID_OPT_VALUE;
    function highWaterMarkFrom(options, isDuplex, duplexKey) {
      return options.highWaterMark != null ? options.highWaterMark : isDuplex ? options[duplexKey] : null;
    }
    function getHighWaterMark(state, options, duplexKey, isDuplex) {
      var hwm = highWaterMarkFrom(options, isDuplex, duplexKey);
      if (hwm != null) {
        if (!(isFinite(hwm) && Math.floor(hwm) === hwm) || hwm < 0) {
          var name = isDuplex ? duplexKey : "highWaterMark";
          throw new ERR_INVALID_OPT_VALUE(name, hwm);
        }
        return Math.floor(hwm);
      }
      return state.objectMode ? 16 : 16384;
    }
    module2.exports = { getHighWaterMark };
  });
  require_node = __commonJS2((exports2, module2) => {
    module2.exports = (init_util(), __toCommonJS(exports_util)).deprecate;
  });
  require__stream_writable = __commonJS2((exports2, module2) => {
    module2.exports = Writable;
    function CorkedRequest(state) {
      var _this = this;
      this.next = null, this.entry = null, this.finish = function() {
        onCorkedFinish(_this, state);
      };
    }
    var Duplex;
    Writable.WritableState = WritableState;
    var internalUtil = { deprecate: require_node() }, Stream = require_stream(), Buffer22 = (init_buffer(), __toCommonJS(exports_buffer)).Buffer, OurUint8Array = (typeof globalThis < "u" ? globalThis : typeof window < "u" ? window : typeof self < "u" ? self : {}).Uint8Array || function() {};
    function _uint8ArrayToBuffer(chunk) {
      return Buffer22.from(chunk);
    }
    function _isUint8Array(obj) {
      return Buffer22.isBuffer(obj) || obj instanceof OurUint8Array;
    }
    var destroyImpl = require_destroy(), _require = require_state(), getHighWaterMark = _require.getHighWaterMark, _require$codes = require_errors().codes, ERR_INVALID_ARG_TYPE3 = _require$codes.ERR_INVALID_ARG_TYPE, ERR_METHOD_NOT_IMPLEMENTED = _require$codes.ERR_METHOD_NOT_IMPLEMENTED, ERR_MULTIPLE_CALLBACK = _require$codes.ERR_MULTIPLE_CALLBACK, ERR_STREAM_CANNOT_PIPE = _require$codes.ERR_STREAM_CANNOT_PIPE, ERR_STREAM_DESTROYED = _require$codes.ERR_STREAM_DESTROYED, ERR_STREAM_NULL_VALUES = _require$codes.ERR_STREAM_NULL_VALUES, ERR_STREAM_WRITE_AFTER_END = _require$codes.ERR_STREAM_WRITE_AFTER_END, ERR_UNKNOWN_ENCODING = _require$codes.ERR_UNKNOWN_ENCODING, errorOrDestroy = destroyImpl.errorOrDestroy;
    require_inherits()(Writable, Stream);
    function nop() {}
    function WritableState(options, stream, isDuplex) {
      if (Duplex = Duplex || require__stream_duplex(), options = options || {}, typeof isDuplex !== "boolean")
        isDuplex = stream instanceof Duplex;
      if (this.objectMode = !!options.objectMode, isDuplex)
        this.objectMode = this.objectMode || !!options.writableObjectMode;
      this.highWaterMark = getHighWaterMark(this, options, "writableHighWaterMark", isDuplex), this.finalCalled = false, this.needDrain = false, this.ending = false, this.ended = false, this.finished = false, this.destroyed = false;
      var noDecode = options.decodeStrings === false;
      this.decodeStrings = !noDecode, this.defaultEncoding = options.defaultEncoding || "utf8", this.length = 0, this.writing = false, this.corked = 0, this.sync = true, this.bufferProcessing = false, this.onwrite = function(er) {
        onwrite(stream, er);
      }, this.writecb = null, this.writelen = 0, this.bufferedRequest = null, this.lastBufferedRequest = null, this.pendingcb = 0, this.prefinished = false, this.errorEmitted = false, this.emitClose = options.emitClose !== false, this.autoDestroy = !!options.autoDestroy, this.bufferedRequestCount = 0, this.corkedRequestsFree = new CorkedRequest(this);
    }
    WritableState.prototype.getBuffer = function() {
      var current = this.bufferedRequest, out = [];
      while (current)
        out.push(current), current = current.next;
      return out;
    };
    (function() {
      try {
        Object.defineProperty(WritableState.prototype, "buffer", { get: internalUtil.deprecate(function() {
          return this.getBuffer();
        }, "_writableState.buffer is deprecated. Use _writableState.getBuffer instead.", "DEP0003") });
      } catch (_) {}
    })();
    var realHasInstance;
    if (typeof Symbol === "function" && Symbol.hasInstance && typeof Function.prototype[Symbol.hasInstance] === "function")
      realHasInstance = Function.prototype[Symbol.hasInstance], Object.defineProperty(Writable, Symbol.hasInstance, { value: function(object) {
        if (realHasInstance.call(this, object))
          return true;
        if (this !== Writable)
          return false;
        return object && object._writableState instanceof WritableState;
      } });
    else
      realHasInstance = function(object) {
        return object instanceof this;
      };
    function Writable(options) {
      Duplex = Duplex || require__stream_duplex();
      var isDuplex = this instanceof Duplex;
      if (!isDuplex && !realHasInstance.call(Writable, this))
        return new Writable(options);
      if (this._writableState = new WritableState(options, this, isDuplex), this.writable = true, options) {
        if (typeof options.write === "function")
          this._write = options.write;
        if (typeof options.writev === "function")
          this._writev = options.writev;
        if (typeof options.destroy === "function")
          this._destroy = options.destroy;
        if (typeof options.final === "function")
          this._final = options.final;
      }
      Stream.call(this);
    }
    Writable.prototype.pipe = function() {
      errorOrDestroy(this, new ERR_STREAM_CANNOT_PIPE);
    };
    function writeAfterEnd(stream, cb) {
      var er = new ERR_STREAM_WRITE_AFTER_END;
      errorOrDestroy(stream, er), process.nextTick(cb, er);
    }
    function validChunk(stream, state, chunk, cb) {
      var er;
      if (chunk === null)
        er = new ERR_STREAM_NULL_VALUES;
      else if (typeof chunk !== "string" && !state.objectMode)
        er = new ERR_INVALID_ARG_TYPE3("chunk", ["string", "Buffer"], chunk);
      if (er)
        return errorOrDestroy(stream, er), process.nextTick(cb, er), false;
      return true;
    }
    Writable.prototype.write = function(chunk, encoding, cb) {
      var state = this._writableState, ret = false, isBuf = !state.objectMode && _isUint8Array(chunk);
      if (isBuf && !Buffer22.isBuffer(chunk))
        chunk = _uint8ArrayToBuffer(chunk);
      if (typeof encoding === "function")
        cb = encoding, encoding = null;
      if (isBuf)
        encoding = "buffer";
      else if (!encoding)
        encoding = state.defaultEncoding;
      if (typeof cb !== "function")
        cb = nop;
      if (state.ending)
        writeAfterEnd(this, cb);
      else if (isBuf || validChunk(this, state, chunk, cb))
        state.pendingcb++, ret = writeOrBuffer(this, state, isBuf, chunk, encoding, cb);
      return ret;
    };
    Writable.prototype.cork = function() {
      this._writableState.corked++;
    };
    Writable.prototype.uncork = function() {
      var state = this._writableState;
      if (state.corked) {
        if (state.corked--, !state.writing && !state.corked && !state.bufferProcessing && state.bufferedRequest)
          clearBuffer(this, state);
      }
    };
    Writable.prototype.setDefaultEncoding = function(encoding) {
      if (typeof encoding === "string")
        encoding = encoding.toLowerCase();
      if (!(["hex", "utf8", "utf-8", "ascii", "binary", "base64", "ucs2", "ucs-2", "utf16le", "utf-16le", "raw"].indexOf((encoding + "").toLowerCase()) > -1))
        throw new ERR_UNKNOWN_ENCODING(encoding);
      return this._writableState.defaultEncoding = encoding, this;
    };
    Object.defineProperty(Writable.prototype, "writableBuffer", { enumerable: false, get: function() {
      return this._writableState && this._writableState.getBuffer();
    } });
    function decodeChunk(state, chunk, encoding) {
      if (!state.objectMode && state.decodeStrings !== false && typeof chunk === "string")
        chunk = Buffer22.from(chunk, encoding);
      return chunk;
    }
    Object.defineProperty(Writable.prototype, "writableHighWaterMark", { enumerable: false, get: function() {
      return this._writableState.highWaterMark;
    } });
    function writeOrBuffer(stream, state, isBuf, chunk, encoding, cb) {
      if (!isBuf) {
        var newChunk = decodeChunk(state, chunk, encoding);
        if (chunk !== newChunk)
          isBuf = true, encoding = "buffer", chunk = newChunk;
      }
      var len2 = state.objectMode ? 1 : chunk.length;
      state.length += len2;
      var ret = state.length < state.highWaterMark;
      if (!ret)
        state.needDrain = true;
      if (state.writing || state.corked) {
        var last = state.lastBufferedRequest;
        if (state.lastBufferedRequest = { chunk, encoding, isBuf, callback: cb, next: null }, last)
          last.next = state.lastBufferedRequest;
        else
          state.bufferedRequest = state.lastBufferedRequest;
        state.bufferedRequestCount += 1;
      } else
        doWrite(stream, state, false, len2, chunk, encoding, cb);
      return ret;
    }
    function doWrite(stream, state, writev, len2, chunk, encoding, cb) {
      if (state.writelen = len2, state.writecb = cb, state.writing = true, state.sync = true, state.destroyed)
        state.onwrite(new ERR_STREAM_DESTROYED("write"));
      else if (writev)
        stream._writev(chunk, state.onwrite);
      else
        stream._write(chunk, encoding, state.onwrite);
      state.sync = false;
    }
    function onwriteError(stream, state, sync, er, cb) {
      if (--state.pendingcb, sync)
        process.nextTick(cb, er), process.nextTick(finishMaybe, stream, state), stream._writableState.errorEmitted = true, errorOrDestroy(stream, er);
      else
        cb(er), stream._writableState.errorEmitted = true, errorOrDestroy(stream, er), finishMaybe(stream, state);
    }
    function onwriteStateUpdate(state) {
      state.writing = false, state.writecb = null, state.length -= state.writelen, state.writelen = 0;
    }
    function onwrite(stream, er) {
      var state = stream._writableState, sync = state.sync, cb = state.writecb;
      if (typeof cb !== "function")
        throw new ERR_MULTIPLE_CALLBACK;
      if (onwriteStateUpdate(state), er)
        onwriteError(stream, state, sync, er, cb);
      else {
        var finished = needFinish(state) || stream.destroyed;
        if (!finished && !state.corked && !state.bufferProcessing && state.bufferedRequest)
          clearBuffer(stream, state);
        if (sync)
          process.nextTick(afterWrite, stream, state, finished, cb);
        else
          afterWrite(stream, state, finished, cb);
      }
    }
    function afterWrite(stream, state, finished, cb) {
      if (!finished)
        onwriteDrain(stream, state);
      state.pendingcb--, cb(), finishMaybe(stream, state);
    }
    function onwriteDrain(stream, state) {
      if (state.length === 0 && state.needDrain)
        state.needDrain = false, stream.emit("drain");
    }
    function clearBuffer(stream, state) {
      state.bufferProcessing = true;
      var entry = state.bufferedRequest;
      if (stream._writev && entry && entry.next) {
        var l = state.bufferedRequestCount, buffer = Array(l), holder = state.corkedRequestsFree;
        holder.entry = entry;
        var count = 0, allBuffers = true;
        while (entry) {
          if (buffer[count] = entry, !entry.isBuf)
            allBuffers = false;
          entry = entry.next, count += 1;
        }
        if (buffer.allBuffers = allBuffers, doWrite(stream, state, true, state.length, buffer, "", holder.finish), state.pendingcb++, state.lastBufferedRequest = null, holder.next)
          state.corkedRequestsFree = holder.next, holder.next = null;
        else
          state.corkedRequestsFree = new CorkedRequest(state);
        state.bufferedRequestCount = 0;
      } else {
        while (entry) {
          var { chunk, encoding, callback: cb } = entry, len2 = state.objectMode ? 1 : chunk.length;
          if (doWrite(stream, state, false, len2, chunk, encoding, cb), entry = entry.next, state.bufferedRequestCount--, state.writing)
            break;
        }
        if (entry === null)
          state.lastBufferedRequest = null;
      }
      state.bufferedRequest = entry, state.bufferProcessing = false;
    }
    Writable.prototype._write = function(chunk, encoding, cb) {
      cb(new ERR_METHOD_NOT_IMPLEMENTED("_write()"));
    };
    Writable.prototype._writev = null;
    Writable.prototype.end = function(chunk, encoding, cb) {
      var state = this._writableState;
      if (typeof chunk === "function")
        cb = chunk, chunk = null, encoding = null;
      else if (typeof encoding === "function")
        cb = encoding, encoding = null;
      if (chunk !== null && chunk !== undefined)
        this.write(chunk, encoding);
      if (state.corked)
        state.corked = 1, this.uncork();
      if (!state.ending)
        endWritable(this, state, cb);
      return this;
    };
    Object.defineProperty(Writable.prototype, "writableLength", { enumerable: false, get: function() {
      return this._writableState.length;
    } });
    function needFinish(state) {
      return state.ending && state.length === 0 && state.bufferedRequest === null && !state.finished && !state.writing;
    }
    function callFinal(stream, state) {
      stream._final(function(err) {
        if (state.pendingcb--, err)
          errorOrDestroy(stream, err);
        state.prefinished = true, stream.emit("prefinish"), finishMaybe(stream, state);
      });
    }
    function prefinish(stream, state) {
      if (!state.prefinished && !state.finalCalled)
        if (typeof stream._final === "function" && !state.destroyed)
          state.pendingcb++, state.finalCalled = true, process.nextTick(callFinal, stream, state);
        else
          state.prefinished = true, stream.emit("prefinish");
    }
    function finishMaybe(stream, state) {
      var need = needFinish(state);
      if (need) {
        if (prefinish(stream, state), state.pendingcb === 0) {
          if (state.finished = true, stream.emit("finish"), state.autoDestroy) {
            var rState = stream._readableState;
            if (!rState || rState.autoDestroy && rState.endEmitted)
              stream.destroy();
          }
        }
      }
      return need;
    }
    function endWritable(stream, state, cb) {
      if (state.ending = true, finishMaybe(stream, state), cb)
        if (state.finished)
          process.nextTick(cb);
        else
          stream.once("finish", cb);
      state.ended = true, stream.writable = false;
    }
    function onCorkedFinish(corkReq, state, err) {
      var entry = corkReq.entry;
      corkReq.entry = null;
      while (entry) {
        var cb = entry.callback;
        state.pendingcb--, cb(err), entry = entry.next;
      }
      state.corkedRequestsFree.next = corkReq;
    }
    Object.defineProperty(Writable.prototype, "destroyed", { enumerable: false, get: function() {
      if (this._writableState === undefined)
        return false;
      return this._writableState.destroyed;
    }, set: function(value) {
      if (!this._writableState)
        return;
      this._writableState.destroyed = value;
    } });
    Writable.prototype.destroy = destroyImpl.destroy;
    Writable.prototype._undestroy = destroyImpl.undestroy;
    Writable.prototype._destroy = function(err, cb) {
      cb(err);
    };
  });
  require__stream_duplex = __commonJS2((exports2, module2) => {
    var objectKeys = Object.keys || function(obj) {
      var keys2 = [];
      for (var key in obj)
        keys2.push(key);
      return keys2;
    };
    module2.exports = Duplex;
    var Readable = require__stream_readable(), Writable = require__stream_writable();
    require_inherits()(Duplex, Readable);
    {
      keys = objectKeys(Writable.prototype);
      for (v = 0;v < keys.length; v++)
        if (method = keys[v], !Duplex.prototype[method])
          Duplex.prototype[method] = Writable.prototype[method];
    }
    var keys, method, v;
    function Duplex(options) {
      if (!(this instanceof Duplex))
        return new Duplex(options);
      if (Readable.call(this, options), Writable.call(this, options), this.allowHalfOpen = true, options) {
        if (options.readable === false)
          this.readable = false;
        if (options.writable === false)
          this.writable = false;
        if (options.allowHalfOpen === false)
          this.allowHalfOpen = false, this.once("end", onend);
      }
    }
    Object.defineProperty(Duplex.prototype, "writableHighWaterMark", { enumerable: false, get: function() {
      return this._writableState.highWaterMark;
    } });
    Object.defineProperty(Duplex.prototype, "writableBuffer", { enumerable: false, get: function() {
      return this._writableState && this._writableState.getBuffer();
    } });
    Object.defineProperty(Duplex.prototype, "writableLength", { enumerable: false, get: function() {
      return this._writableState.length;
    } });
    function onend() {
      if (this._writableState.ended)
        return;
      process.nextTick(onEndNT, this);
    }
    function onEndNT(self2) {
      self2.end();
    }
    Object.defineProperty(Duplex.prototype, "destroyed", { enumerable: false, get: function() {
      if (this._readableState === undefined || this._writableState === undefined)
        return false;
      return this._readableState.destroyed && this._writableState.destroyed;
    }, set: function(value) {
      if (this._readableState === undefined || this._writableState === undefined)
        return;
      this._readableState.destroyed = value, this._writableState.destroyed = value;
    } });
  });
  require_safe_buffer = __commonJS2((exports2, module2) => {
    /*! safe-buffer. MIT License. Feross Aboukhadijeh <https://feross.org/opensource> */
    var buffer = (init_buffer(), __toCommonJS(exports_buffer)), Buffer22 = buffer.Buffer;
    function copyProps(src, dst) {
      for (var key in src)
        dst[key] = src[key];
    }
    if (Buffer22.from && Buffer22.alloc && Buffer22.allocUnsafe && Buffer22.allocUnsafeSlow)
      module2.exports = buffer;
    else
      copyProps(buffer, exports2), exports2.Buffer = SafeBuffer;
    function SafeBuffer(arg, encodingOrOffset, length) {
      return Buffer22(arg, encodingOrOffset, length);
    }
    SafeBuffer.prototype = Object.create(Buffer22.prototype);
    copyProps(Buffer22, SafeBuffer);
    SafeBuffer.from = function(arg, encodingOrOffset, length) {
      if (typeof arg === "number")
        throw TypeError("Argument must not be a number");
      return Buffer22(arg, encodingOrOffset, length);
    };
    SafeBuffer.alloc = function(size, fill, encoding) {
      if (typeof size !== "number")
        throw TypeError("Argument must be a number");
      var buf = Buffer22(size);
      if (fill !== undefined)
        if (typeof encoding === "string")
          buf.fill(fill, encoding);
        else
          buf.fill(fill);
      else
        buf.fill(0);
      return buf;
    };
    SafeBuffer.allocUnsafe = function(size) {
      if (typeof size !== "number")
        throw TypeError("Argument must be a number");
      return Buffer22(size);
    };
    SafeBuffer.allocUnsafeSlow = function(size) {
      if (typeof size !== "number")
        throw TypeError("Argument must be a number");
      return buffer.SlowBuffer(size);
    };
  });
  require_string_decoder = __commonJS2((exports2) => {
    var Buffer22 = require_safe_buffer().Buffer, isEncoding = Buffer22.isEncoding || function(encoding) {
      switch (encoding = "" + encoding, encoding && encoding.toLowerCase()) {
        case "hex":
        case "utf8":
        case "utf-8":
        case "ascii":
        case "binary":
        case "base64":
        case "ucs2":
        case "ucs-2":
        case "utf16le":
        case "utf-16le":
        case "raw":
          return true;
        default:
          return false;
      }
    };
    function _normalizeEncoding(enc) {
      if (!enc)
        return "utf8";
      var retried;
      while (true)
        switch (enc) {
          case "utf8":
          case "utf-8":
            return "utf8";
          case "ucs2":
          case "ucs-2":
          case "utf16le":
          case "utf-16le":
            return "utf16le";
          case "latin1":
          case "binary":
            return "latin1";
          case "base64":
          case "ascii":
          case "hex":
            return enc;
          default:
            if (retried)
              return;
            enc = ("" + enc).toLowerCase(), retried = true;
        }
    }
    function normalizeEncoding(enc) {
      var nenc = _normalizeEncoding(enc);
      if (typeof nenc !== "string" && (Buffer22.isEncoding === isEncoding || !isEncoding(enc)))
        throw Error("Unknown encoding: " + enc);
      return nenc || enc;
    }
    exports2.StringDecoder = StringDecoder;
    function StringDecoder(encoding) {
      this.encoding = normalizeEncoding(encoding);
      var nb;
      switch (this.encoding) {
        case "utf16le":
          this.text = utf16Text, this.end = utf16End, nb = 4;
          break;
        case "utf8":
          this.fillLast = utf8FillLast, nb = 4;
          break;
        case "base64":
          this.text = base64Text, this.end = base64End, nb = 3;
          break;
        default:
          this.write = simpleWrite, this.end = simpleEnd;
          return;
      }
      this.lastNeed = 0, this.lastTotal = 0, this.lastChar = Buffer22.allocUnsafe(nb);
    }
    StringDecoder.prototype.write = function(buf) {
      if (buf.length === 0)
        return "";
      var r, i2;
      if (this.lastNeed) {
        if (r = this.fillLast(buf), r === undefined)
          return "";
        i2 = this.lastNeed, this.lastNeed = 0;
      } else
        i2 = 0;
      if (i2 < buf.length)
        return r ? r + this.text(buf, i2) : this.text(buf, i2);
      return r || "";
    };
    StringDecoder.prototype.end = utf8End;
    StringDecoder.prototype.text = utf8Text;
    StringDecoder.prototype.fillLast = function(buf) {
      if (this.lastNeed <= buf.length)
        return buf.copy(this.lastChar, this.lastTotal - this.lastNeed, 0, this.lastNeed), this.lastChar.toString(this.encoding, 0, this.lastTotal);
      buf.copy(this.lastChar, this.lastTotal - this.lastNeed, 0, buf.length), this.lastNeed -= buf.length;
    };
    function utf8CheckByte(byte) {
      if (byte <= 127)
        return 0;
      else if (byte >> 5 === 6)
        return 2;
      else if (byte >> 4 === 14)
        return 3;
      else if (byte >> 3 === 30)
        return 4;
      return byte >> 6 === 2 ? -1 : -2;
    }
    function utf8CheckIncomplete(self2, buf, i2) {
      var j = buf.length - 1;
      if (j < i2)
        return 0;
      var nb = utf8CheckByte(buf[j]);
      if (nb >= 0) {
        if (nb > 0)
          self2.lastNeed = nb - 1;
        return nb;
      }
      if (--j < i2 || nb === -2)
        return 0;
      if (nb = utf8CheckByte(buf[j]), nb >= 0) {
        if (nb > 0)
          self2.lastNeed = nb - 2;
        return nb;
      }
      if (--j < i2 || nb === -2)
        return 0;
      if (nb = utf8CheckByte(buf[j]), nb >= 0) {
        if (nb > 0)
          if (nb === 2)
            nb = 0;
          else
            self2.lastNeed = nb - 3;
        return nb;
      }
      return 0;
    }
    function utf8CheckExtraBytes(self2, buf, p) {
      if ((buf[0] & 192) !== 128)
        return self2.lastNeed = 0, "�";
      if (self2.lastNeed > 1 && buf.length > 1) {
        if ((buf[1] & 192) !== 128)
          return self2.lastNeed = 1, "�";
        if (self2.lastNeed > 2 && buf.length > 2) {
          if ((buf[2] & 192) !== 128)
            return self2.lastNeed = 2, "�";
        }
      }
    }
    function utf8FillLast(buf) {
      var p = this.lastTotal - this.lastNeed, r = utf8CheckExtraBytes(this, buf, p);
      if (r !== undefined)
        return r;
      if (this.lastNeed <= buf.length)
        return buf.copy(this.lastChar, p, 0, this.lastNeed), this.lastChar.toString(this.encoding, 0, this.lastTotal);
      buf.copy(this.lastChar, p, 0, buf.length), this.lastNeed -= buf.length;
    }
    function utf8Text(buf, i2) {
      var total = utf8CheckIncomplete(this, buf, i2);
      if (!this.lastNeed)
        return buf.toString("utf8", i2);
      this.lastTotal = total;
      var end = buf.length - (total - this.lastNeed);
      return buf.copy(this.lastChar, 0, end), buf.toString("utf8", i2, end);
    }
    function utf8End(buf) {
      var r = buf && buf.length ? this.write(buf) : "";
      if (this.lastNeed)
        return r + "�";
      return r;
    }
    function utf16Text(buf, i2) {
      if ((buf.length - i2) % 2 === 0) {
        var r = buf.toString("utf16le", i2);
        if (r) {
          var c = r.charCodeAt(r.length - 1);
          if (c >= 55296 && c <= 56319)
            return this.lastNeed = 2, this.lastTotal = 4, this.lastChar[0] = buf[buf.length - 2], this.lastChar[1] = buf[buf.length - 1], r.slice(0, -1);
        }
        return r;
      }
      return this.lastNeed = 1, this.lastTotal = 2, this.lastChar[0] = buf[buf.length - 1], buf.toString("utf16le", i2, buf.length - 1);
    }
    function utf16End(buf) {
      var r = buf && buf.length ? this.write(buf) : "";
      if (this.lastNeed) {
        var end = this.lastTotal - this.lastNeed;
        return r + this.lastChar.toString("utf16le", 0, end);
      }
      return r;
    }
    function base64Text(buf, i2) {
      var n = (buf.length - i2) % 3;
      if (n === 0)
        return buf.toString("base64", i2);
      if (this.lastNeed = 3 - n, this.lastTotal = 3, n === 1)
        this.lastChar[0] = buf[buf.length - 1];
      else
        this.lastChar[0] = buf[buf.length - 2], this.lastChar[1] = buf[buf.length - 1];
      return buf.toString("base64", i2, buf.length - n);
    }
    function base64End(buf) {
      var r = buf && buf.length ? this.write(buf) : "";
      if (this.lastNeed)
        return r + this.lastChar.toString("base64", 0, 3 - this.lastNeed);
      return r;
    }
    function simpleWrite(buf) {
      return buf.toString(this.encoding);
    }
    function simpleEnd(buf) {
      return buf && buf.length ? this.write(buf) : "";
    }
  });
  require_end_of_stream = __commonJS2((exports2, module2) => {
    var ERR_STREAM_PREMATURE_CLOSE = require_errors().codes.ERR_STREAM_PREMATURE_CLOSE;
    function once(callback) {
      var called = false;
      return function() {
        if (called)
          return;
        called = true;
        for (var _len = arguments.length, args = Array(_len), _key = 0;_key < _len; _key++)
          args[_key] = arguments[_key];
        callback.apply(this, args);
      };
    }
    function noop2() {}
    function isRequest2(stream) {
      return stream.setHeader && typeof stream.abort === "function";
    }
    function eos(stream, opts, callback) {
      if (typeof opts === "function")
        return eos(stream, null, opts);
      if (!opts)
        opts = {};
      callback = once(callback || noop2);
      var readable = opts.readable || opts.readable !== false && stream.readable, writable = opts.writable || opts.writable !== false && stream.writable, onlegacyfinish = function() {
        if (!stream.writable)
          onfinish();
      }, writableEnded = stream._writableState && stream._writableState.finished, onfinish = function() {
        if (writable = false, writableEnded = true, !readable)
          callback.call(stream);
      }, readableEnded = stream._readableState && stream._readableState.endEmitted, onend = function() {
        if (readable = false, readableEnded = true, !writable)
          callback.call(stream);
      }, onerror = function(err) {
        callback.call(stream, err);
      }, onclose = function() {
        var err;
        if (readable && !readableEnded) {
          if (!stream._readableState || !stream._readableState.ended)
            err = new ERR_STREAM_PREMATURE_CLOSE;
          return callback.call(stream, err);
        }
        if (writable && !writableEnded) {
          if (!stream._writableState || !stream._writableState.ended)
            err = new ERR_STREAM_PREMATURE_CLOSE;
          return callback.call(stream, err);
        }
      }, onrequest = function() {
        stream.req.on("finish", onfinish);
      };
      if (isRequest2(stream))
        if (stream.on("complete", onfinish), stream.on("abort", onclose), stream.req)
          onrequest();
        else
          stream.on("request", onrequest);
      else if (writable && !stream._writableState)
        stream.on("end", onlegacyfinish), stream.on("close", onlegacyfinish);
      if (stream.on("end", onend), stream.on("finish", onfinish), opts.error !== false)
        stream.on("error", onerror);
      return stream.on("close", onclose), function() {
        if (stream.removeListener("complete", onfinish), stream.removeListener("abort", onclose), stream.removeListener("request", onrequest), stream.req)
          stream.req.removeListener("finish", onfinish);
        stream.removeListener("end", onlegacyfinish), stream.removeListener("close", onlegacyfinish), stream.removeListener("finish", onfinish), stream.removeListener("end", onend), stream.removeListener("error", onerror), stream.removeListener("close", onclose);
      };
    }
    module2.exports = eos;
  });
  require_async_iterator = __commonJS2((exports2, module2) => {
    var _Object$setPrototypeO;
    function _defineProperty(obj, key, value) {
      if (key = _toPropertyKey(key), key in obj)
        Object.defineProperty(obj, key, { value, enumerable: true, configurable: true, writable: true });
      else
        obj[key] = value;
      return obj;
    }
    function _toPropertyKey(arg) {
      var key = _toPrimitive(arg, "string");
      return typeof key === "symbol" ? key : String(key);
    }
    function _toPrimitive(input, hint) {
      if (typeof input !== "object" || input === null)
        return input;
      var prim = input[Symbol.toPrimitive];
      if (prim !== undefined) {
        var res = prim.call(input, hint || "default");
        if (typeof res !== "object")
          return res;
        throw TypeError("@@toPrimitive must return a primitive value.");
      }
      return (hint === "string" ? String : Number)(input);
    }
    var finished = require_end_of_stream(), kLastResolve = Symbol("lastResolve"), kLastReject = Symbol("lastReject"), kError = Symbol("error"), kEnded = Symbol("ended"), kLastPromise = Symbol("lastPromise"), kHandlePromise = Symbol("handlePromise"), kStream = Symbol("stream");
    function createIterResult(value, done) {
      return { value, done };
    }
    function readAndResolve(iter) {
      var resolve = iter[kLastResolve];
      if (resolve !== null) {
        var data = iter[kStream].read();
        if (data !== null)
          iter[kLastPromise] = null, iter[kLastResolve] = null, iter[kLastReject] = null, resolve(createIterResult(data, false));
      }
    }
    function onReadable(iter) {
      process.nextTick(readAndResolve, iter);
    }
    function wrapForNext(lastPromise, iter) {
      return function(resolve, reject) {
        lastPromise.then(function() {
          if (iter[kEnded]) {
            resolve(createIterResult(undefined, true));
            return;
          }
          iter[kHandlePromise](resolve, reject);
        }, reject);
      };
    }
    var AsyncIteratorPrototype = Object.getPrototypeOf(function() {}), ReadableStreamAsyncIteratorPrototype = Object.setPrototypeOf((_Object$setPrototypeO = { get stream() {
      return this[kStream];
    }, next: function() {
      var _this = this, error = this[kError];
      if (error !== null)
        return Promise.reject(error);
      if (this[kEnded])
        return Promise.resolve(createIterResult(undefined, true));
      if (this[kStream].destroyed)
        return new Promise(function(resolve, reject) {
          process.nextTick(function() {
            if (_this[kError])
              reject(_this[kError]);
            else
              resolve(createIterResult(undefined, true));
          });
        });
      var lastPromise = this[kLastPromise], promise;
      if (lastPromise)
        promise = new Promise(wrapForNext(lastPromise, this));
      else {
        var data = this[kStream].read();
        if (data !== null)
          return Promise.resolve(createIterResult(data, false));
        promise = new Promise(this[kHandlePromise]);
      }
      return this[kLastPromise] = promise, promise;
    } }, _defineProperty(_Object$setPrototypeO, Symbol.asyncIterator, function() {
      return this;
    }), _defineProperty(_Object$setPrototypeO, "return", function() {
      var _this2 = this;
      return new Promise(function(resolve, reject) {
        _this2[kStream].destroy(null, function(err) {
          if (err) {
            reject(err);
            return;
          }
          resolve(createIterResult(undefined, true));
        });
      });
    }), _Object$setPrototypeO), AsyncIteratorPrototype), createReadableStreamAsyncIterator = function(stream) {
      var _Object$create, iterator2 = Object.create(ReadableStreamAsyncIteratorPrototype, (_Object$create = {}, _defineProperty(_Object$create, kStream, { value: stream, writable: true }), _defineProperty(_Object$create, kLastResolve, { value: null, writable: true }), _defineProperty(_Object$create, kLastReject, { value: null, writable: true }), _defineProperty(_Object$create, kError, { value: null, writable: true }), _defineProperty(_Object$create, kEnded, { value: stream._readableState.endEmitted, writable: true }), _defineProperty(_Object$create, kHandlePromise, { value: function(resolve, reject) {
        var data = iterator2[kStream].read();
        if (data)
          iterator2[kLastPromise] = null, iterator2[kLastResolve] = null, iterator2[kLastReject] = null, resolve(createIterResult(data, false));
        else
          iterator2[kLastResolve] = resolve, iterator2[kLastReject] = reject;
      }, writable: true }), _Object$create));
      return iterator2[kLastPromise] = null, finished(stream, function(err) {
        if (err && err.code !== "ERR_STREAM_PREMATURE_CLOSE") {
          var reject = iterator2[kLastReject];
          if (reject !== null)
            iterator2[kLastPromise] = null, iterator2[kLastResolve] = null, iterator2[kLastReject] = null, reject(err);
          iterator2[kError] = err;
          return;
        }
        var resolve = iterator2[kLastResolve];
        if (resolve !== null)
          iterator2[kLastPromise] = null, iterator2[kLastResolve] = null, iterator2[kLastReject] = null, resolve(createIterResult(undefined, true));
        iterator2[kEnded] = true;
      }), stream.on("readable", onReadable.bind(null, iterator2)), iterator2;
    };
    module2.exports = createReadableStreamAsyncIterator;
  });
  require_from = __commonJS2((exports2, module2) => {
    function asyncGeneratorStep(gen, resolve, reject, _next, _throw, key, arg) {
      try {
        var info = gen[key](arg), value = info.value;
      } catch (error) {
        reject(error);
        return;
      }
      if (info.done)
        resolve(value);
      else
        Promise.resolve(value).then(_next, _throw);
    }
    function _asyncToGenerator(fn) {
      return function() {
        var self2 = this, args = arguments;
        return new Promise(function(resolve, reject) {
          var gen = fn.apply(self2, args);
          function _next(value) {
            asyncGeneratorStep(gen, resolve, reject, _next, _throw, "next", value);
          }
          function _throw(err) {
            asyncGeneratorStep(gen, resolve, reject, _next, _throw, "throw", err);
          }
          _next(undefined);
        });
      };
    }
    function ownKeys(object, enumerableOnly) {
      var keys = Object.keys(object);
      if (Object.getOwnPropertySymbols) {
        var symbols = Object.getOwnPropertySymbols(object);
        enumerableOnly && (symbols = symbols.filter(function(sym) {
          return Object.getOwnPropertyDescriptor(object, sym).enumerable;
        })), keys.push.apply(keys, symbols);
      }
      return keys;
    }
    function _objectSpread(target) {
      for (var i2 = 1;i2 < arguments.length; i2++) {
        var source = arguments[i2] != null ? arguments[i2] : {};
        i2 % 2 ? ownKeys(Object(source), true).forEach(function(key) {
          _defineProperty(target, key, source[key]);
        }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)) : ownKeys(Object(source)).forEach(function(key) {
          Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key));
        });
      }
      return target;
    }
    function _defineProperty(obj, key, value) {
      if (key = _toPropertyKey(key), key in obj)
        Object.defineProperty(obj, key, { value, enumerable: true, configurable: true, writable: true });
      else
        obj[key] = value;
      return obj;
    }
    function _toPropertyKey(arg) {
      var key = _toPrimitive(arg, "string");
      return typeof key === "symbol" ? key : String(key);
    }
    function _toPrimitive(input, hint) {
      if (typeof input !== "object" || input === null)
        return input;
      var prim = input[Symbol.toPrimitive];
      if (prim !== undefined) {
        var res = prim.call(input, hint || "default");
        if (typeof res !== "object")
          return res;
        throw TypeError("@@toPrimitive must return a primitive value.");
      }
      return (hint === "string" ? String : Number)(input);
    }
    var ERR_INVALID_ARG_TYPE3 = require_errors().codes.ERR_INVALID_ARG_TYPE;
    function from2(Readable, iterable, opts) {
      var iterator2;
      if (iterable && typeof iterable.next === "function")
        iterator2 = iterable;
      else if (iterable && iterable[Symbol.asyncIterator])
        iterator2 = iterable[Symbol.asyncIterator]();
      else if (iterable && iterable[Symbol.iterator])
        iterator2 = iterable[Symbol.iterator]();
      else
        throw new ERR_INVALID_ARG_TYPE3("iterable", ["Iterable"], iterable);
      var readable = new Readable(_objectSpread({ objectMode: true }, opts)), reading = false;
      readable._read = function() {
        if (!reading)
          reading = true, next();
      };
      function next() {
        return _next2.apply(this, arguments);
      }
      function _next2() {
        return _next2 = _asyncToGenerator(function* () {
          try {
            var _yield$iterator$next = yield iterator2.next(), value = _yield$iterator$next.value, done = _yield$iterator$next.done;
            if (done)
              readable.push(null);
            else if (readable.push(yield value))
              next();
            else
              reading = false;
          } catch (err) {
            readable.destroy(err);
          }
        }), _next2.apply(this, arguments);
      }
      return readable;
    }
    module2.exports = from2;
  });
  require__stream_readable = __commonJS2((exports2, module2) => {
    module2.exports = Readable;
    var Duplex;
    Readable.ReadableState = ReadableState;
    var EE = (init_events(), __toCommonJS(exports_events)).EventEmitter, EElistenerCount = function(emitter, type) {
      return emitter.listeners(type).length;
    }, Stream = require_stream(), Buffer22 = (init_buffer(), __toCommonJS(exports_buffer)).Buffer, OurUint8Array = (typeof globalThis < "u" ? globalThis : typeof window < "u" ? window : typeof self < "u" ? self : {}).Uint8Array || function() {};
    function _uint8ArrayToBuffer(chunk) {
      return Buffer22.from(chunk);
    }
    function _isUint8Array(obj) {
      return Buffer22.isBuffer(obj) || obj instanceof OurUint8Array;
    }
    var debugUtil = (init_util(), __toCommonJS(exports_util)), debug;
    if (debugUtil && debugUtil.debuglog)
      debug = debugUtil.debuglog("stream");
    else
      debug = function() {};
    var BufferList = require_buffer_list(), destroyImpl = require_destroy(), _require = require_state(), getHighWaterMark = _require.getHighWaterMark, _require$codes = require_errors().codes, ERR_INVALID_ARG_TYPE3 = _require$codes.ERR_INVALID_ARG_TYPE, ERR_STREAM_PUSH_AFTER_EOF = _require$codes.ERR_STREAM_PUSH_AFTER_EOF, ERR_METHOD_NOT_IMPLEMENTED = _require$codes.ERR_METHOD_NOT_IMPLEMENTED, ERR_STREAM_UNSHIFT_AFTER_END_EVENT = _require$codes.ERR_STREAM_UNSHIFT_AFTER_END_EVENT, StringDecoder, createReadableStreamAsyncIterator, from2;
    require_inherits()(Readable, Stream);
    var errorOrDestroy = destroyImpl.errorOrDestroy, kProxyEvents = ["error", "close", "destroy", "pause", "resume"];
    function prependListener(emitter, event, fn) {
      if (typeof emitter.prependListener === "function")
        return emitter.prependListener(event, fn);
      if (!emitter._events || !emitter._events[event])
        emitter.on(event, fn);
      else if (Array.isArray(emitter._events[event]))
        emitter._events[event].unshift(fn);
      else
        emitter._events[event] = [fn, emitter._events[event]];
    }
    function ReadableState(options, stream, isDuplex) {
      if (Duplex = Duplex || require__stream_duplex(), options = options || {}, typeof isDuplex !== "boolean")
        isDuplex = stream instanceof Duplex;
      if (this.objectMode = !!options.objectMode, isDuplex)
        this.objectMode = this.objectMode || !!options.readableObjectMode;
      if (this.highWaterMark = getHighWaterMark(this, options, "readableHighWaterMark", isDuplex), this.buffer = new BufferList, this.length = 0, this.pipes = null, this.pipesCount = 0, this.flowing = null, this.ended = false, this.endEmitted = false, this.reading = false, this.sync = true, this.needReadable = false, this.emittedReadable = false, this.readableListening = false, this.resumeScheduled = false, this.paused = true, this.emitClose = options.emitClose !== false, this.autoDestroy = !!options.autoDestroy, this.destroyed = false, this.defaultEncoding = options.defaultEncoding || "utf8", this.awaitDrain = 0, this.readingMore = false, this.decoder = null, this.encoding = null, options.encoding) {
        if (!StringDecoder)
          StringDecoder = require_string_decoder().StringDecoder;
        this.decoder = new StringDecoder(options.encoding), this.encoding = options.encoding;
      }
    }
    function Readable(options) {
      if (Duplex = Duplex || require__stream_duplex(), !(this instanceof Readable))
        return new Readable(options);
      var isDuplex = this instanceof Duplex;
      if (this._readableState = new ReadableState(options, this, isDuplex), this.readable = true, options) {
        if (typeof options.read === "function")
          this._read = options.read;
        if (typeof options.destroy === "function")
          this._destroy = options.destroy;
      }
      Stream.call(this);
    }
    Object.defineProperty(Readable.prototype, "destroyed", { enumerable: false, get: function() {
      if (this._readableState === undefined)
        return false;
      return this._readableState.destroyed;
    }, set: function(value) {
      if (!this._readableState)
        return;
      this._readableState.destroyed = value;
    } });
    Readable.prototype.destroy = destroyImpl.destroy;
    Readable.prototype._undestroy = destroyImpl.undestroy;
    Readable.prototype._destroy = function(err, cb) {
      cb(err);
    };
    Readable.prototype.push = function(chunk, encoding) {
      var state = this._readableState, skipChunkCheck;
      if (!state.objectMode) {
        if (typeof chunk === "string") {
          if (encoding = encoding || state.defaultEncoding, encoding !== state.encoding)
            chunk = Buffer22.from(chunk, encoding), encoding = "";
          skipChunkCheck = true;
        }
      } else
        skipChunkCheck = true;
      return readableAddChunk(this, chunk, encoding, false, skipChunkCheck);
    };
    Readable.prototype.unshift = function(chunk) {
      return readableAddChunk(this, chunk, null, true, false);
    };
    function readableAddChunk(stream, chunk, encoding, addToFront, skipChunkCheck) {
      debug("readableAddChunk", chunk);
      var state = stream._readableState;
      if (chunk === null)
        state.reading = false, onEofChunk(stream, state);
      else {
        var er;
        if (!skipChunkCheck)
          er = chunkInvalid(state, chunk);
        if (er)
          errorOrDestroy(stream, er);
        else if (state.objectMode || chunk && chunk.length > 0) {
          if (typeof chunk !== "string" && !state.objectMode && Object.getPrototypeOf(chunk) !== Buffer22.prototype)
            chunk = _uint8ArrayToBuffer(chunk);
          if (addToFront)
            if (state.endEmitted)
              errorOrDestroy(stream, new ERR_STREAM_UNSHIFT_AFTER_END_EVENT);
            else
              addChunk(stream, state, chunk, true);
          else if (state.ended)
            errorOrDestroy(stream, new ERR_STREAM_PUSH_AFTER_EOF);
          else if (state.destroyed)
            return false;
          else if (state.reading = false, state.decoder && !encoding)
            if (chunk = state.decoder.write(chunk), state.objectMode || chunk.length !== 0)
              addChunk(stream, state, chunk, false);
            else
              maybeReadMore(stream, state);
          else
            addChunk(stream, state, chunk, false);
        } else if (!addToFront)
          state.reading = false, maybeReadMore(stream, state);
      }
      return !state.ended && (state.length < state.highWaterMark || state.length === 0);
    }
    function addChunk(stream, state, chunk, addToFront) {
      if (state.flowing && state.length === 0 && !state.sync)
        state.awaitDrain = 0, stream.emit("data", chunk);
      else {
        if (state.length += state.objectMode ? 1 : chunk.length, addToFront)
          state.buffer.unshift(chunk);
        else
          state.buffer.push(chunk);
        if (state.needReadable)
          emitReadable(stream);
      }
      maybeReadMore(stream, state);
    }
    function chunkInvalid(state, chunk) {
      var er;
      if (!_isUint8Array(chunk) && typeof chunk !== "string" && chunk !== undefined && !state.objectMode)
        er = new ERR_INVALID_ARG_TYPE3("chunk", ["string", "Buffer", "Uint8Array"], chunk);
      return er;
    }
    Readable.prototype.isPaused = function() {
      return this._readableState.flowing === false;
    };
    Readable.prototype.setEncoding = function(enc) {
      if (!StringDecoder)
        StringDecoder = require_string_decoder().StringDecoder;
      var decoder = new StringDecoder(enc);
      this._readableState.decoder = decoder, this._readableState.encoding = this._readableState.decoder.encoding;
      var p = this._readableState.buffer.head, content = "";
      while (p !== null)
        content += decoder.write(p.data), p = p.next;
      if (this._readableState.buffer.clear(), content !== "")
        this._readableState.buffer.push(content);
      return this._readableState.length = content.length, this;
    };
    var MAX_HWM = 1073741824;
    function computeNewHighWaterMark(n) {
      if (n >= MAX_HWM)
        n = MAX_HWM;
      else
        n--, n |= n >>> 1, n |= n >>> 2, n |= n >>> 4, n |= n >>> 8, n |= n >>> 16, n++;
      return n;
    }
    function howMuchToRead(n, state) {
      if (n <= 0 || state.length === 0 && state.ended)
        return 0;
      if (state.objectMode)
        return 1;
      if (n !== n)
        if (state.flowing && state.length)
          return state.buffer.head.data.length;
        else
          return state.length;
      if (n > state.highWaterMark)
        state.highWaterMark = computeNewHighWaterMark(n);
      if (n <= state.length)
        return n;
      if (!state.ended)
        return state.needReadable = true, 0;
      return state.length;
    }
    Readable.prototype.read = function(n) {
      debug("read", n), n = parseInt(n, 10);
      var state = this._readableState, nOrig = n;
      if (n !== 0)
        state.emittedReadable = false;
      if (n === 0 && state.needReadable && ((state.highWaterMark !== 0 ? state.length >= state.highWaterMark : state.length > 0) || state.ended)) {
        if (debug("read: emitReadable", state.length, state.ended), state.length === 0 && state.ended)
          endReadable(this);
        else
          emitReadable(this);
        return null;
      }
      if (n = howMuchToRead(n, state), n === 0 && state.ended) {
        if (state.length === 0)
          endReadable(this);
        return null;
      }
      var doRead = state.needReadable;
      if (debug("need readable", doRead), state.length === 0 || state.length - n < state.highWaterMark)
        doRead = true, debug("length less than watermark", doRead);
      if (state.ended || state.reading)
        doRead = false, debug("reading or ended", doRead);
      else if (doRead) {
        if (debug("do read"), state.reading = true, state.sync = true, state.length === 0)
          state.needReadable = true;
        if (this._read(state.highWaterMark), state.sync = false, !state.reading)
          n = howMuchToRead(nOrig, state);
      }
      var ret;
      if (n > 0)
        ret = fromList(n, state);
      else
        ret = null;
      if (ret === null)
        state.needReadable = state.length <= state.highWaterMark, n = 0;
      else
        state.length -= n, state.awaitDrain = 0;
      if (state.length === 0) {
        if (!state.ended)
          state.needReadable = true;
        if (nOrig !== n && state.ended)
          endReadable(this);
      }
      if (ret !== null)
        this.emit("data", ret);
      return ret;
    };
    function onEofChunk(stream, state) {
      if (debug("onEofChunk"), state.ended)
        return;
      if (state.decoder) {
        var chunk = state.decoder.end();
        if (chunk && chunk.length)
          state.buffer.push(chunk), state.length += state.objectMode ? 1 : chunk.length;
      }
      if (state.ended = true, state.sync)
        emitReadable(stream);
      else if (state.needReadable = false, !state.emittedReadable)
        state.emittedReadable = true, emitReadable_(stream);
    }
    function emitReadable(stream) {
      var state = stream._readableState;
      if (debug("emitReadable", state.needReadable, state.emittedReadable), state.needReadable = false, !state.emittedReadable)
        debug("emitReadable", state.flowing), state.emittedReadable = true, process.nextTick(emitReadable_, stream);
    }
    function emitReadable_(stream) {
      var state = stream._readableState;
      if (debug("emitReadable_", state.destroyed, state.length, state.ended), !state.destroyed && (state.length || state.ended))
        stream.emit("readable"), state.emittedReadable = false;
      state.needReadable = !state.flowing && !state.ended && state.length <= state.highWaterMark, flow(stream);
    }
    function maybeReadMore(stream, state) {
      if (!state.readingMore)
        state.readingMore = true, process.nextTick(maybeReadMore_, stream, state);
    }
    function maybeReadMore_(stream, state) {
      while (!state.reading && !state.ended && (state.length < state.highWaterMark || state.flowing && state.length === 0)) {
        var len2 = state.length;
        if (debug("maybeReadMore read 0"), stream.read(0), len2 === state.length)
          break;
      }
      state.readingMore = false;
    }
    Readable.prototype._read = function(n) {
      errorOrDestroy(this, new ERR_METHOD_NOT_IMPLEMENTED("_read()"));
    };
    Readable.prototype.pipe = function(dest, pipeOpts) {
      var src = this, state = this._readableState;
      switch (state.pipesCount) {
        case 0:
          state.pipes = dest;
          break;
        case 1:
          state.pipes = [state.pipes, dest];
          break;
        default:
          state.pipes.push(dest);
          break;
      }
      state.pipesCount += 1, debug("pipe count=%d opts=%j", state.pipesCount, pipeOpts);
      var doEnd = (!pipeOpts || pipeOpts.end !== false) && dest !== process.stdout && dest !== process.stderr, endFn = doEnd ? onend : unpipe;
      if (state.endEmitted)
        process.nextTick(endFn);
      else
        src.once("end", endFn);
      dest.on("unpipe", onunpipe);
      function onunpipe(readable, unpipeInfo) {
        if (debug("onunpipe"), readable === src) {
          if (unpipeInfo && unpipeInfo.hasUnpiped === false)
            unpipeInfo.hasUnpiped = true, cleanup();
        }
      }
      function onend() {
        debug("onend"), dest.end();
      }
      var ondrain = pipeOnDrain(src);
      dest.on("drain", ondrain);
      var cleanedUp = false;
      function cleanup() {
        if (debug("cleanup"), dest.removeListener("close", onclose), dest.removeListener("finish", onfinish), dest.removeListener("drain", ondrain), dest.removeListener("error", onerror), dest.removeListener("unpipe", onunpipe), src.removeListener("end", onend), src.removeListener("end", unpipe), src.removeListener("data", ondata), cleanedUp = true, state.awaitDrain && (!dest._writableState || dest._writableState.needDrain))
          ondrain();
      }
      src.on("data", ondata);
      function ondata(chunk) {
        debug("ondata");
        var ret = dest.write(chunk);
        if (debug("dest.write", ret), ret === false) {
          if ((state.pipesCount === 1 && state.pipes === dest || state.pipesCount > 1 && indexOf(state.pipes, dest) !== -1) && !cleanedUp)
            debug("false write response, pause", state.awaitDrain), state.awaitDrain++;
          src.pause();
        }
      }
      function onerror(er) {
        if (debug("onerror", er), unpipe(), dest.removeListener("error", onerror), EElistenerCount(dest, "error") === 0)
          errorOrDestroy(dest, er);
      }
      prependListener(dest, "error", onerror);
      function onclose() {
        dest.removeListener("finish", onfinish), unpipe();
      }
      dest.once("close", onclose);
      function onfinish() {
        debug("onfinish"), dest.removeListener("close", onclose), unpipe();
      }
      dest.once("finish", onfinish);
      function unpipe() {
        debug("unpipe"), src.unpipe(dest);
      }
      if (dest.emit("pipe", src), !state.flowing)
        debug("pipe resume"), src.resume();
      return dest;
    };
    function pipeOnDrain(src) {
      return function() {
        var state = src._readableState;
        if (debug("pipeOnDrain", state.awaitDrain), state.awaitDrain)
          state.awaitDrain--;
        if (state.awaitDrain === 0 && EElistenerCount(src, "data"))
          state.flowing = true, flow(src);
      };
    }
    Readable.prototype.unpipe = function(dest) {
      var state = this._readableState, unpipeInfo = { hasUnpiped: false };
      if (state.pipesCount === 0)
        return this;
      if (state.pipesCount === 1) {
        if (dest && dest !== state.pipes)
          return this;
        if (!dest)
          dest = state.pipes;
        if (state.pipes = null, state.pipesCount = 0, state.flowing = false, dest)
          dest.emit("unpipe", this, unpipeInfo);
        return this;
      }
      if (!dest) {
        var { pipes: dests, pipesCount: len2 } = state;
        state.pipes = null, state.pipesCount = 0, state.flowing = false;
        for (var i2 = 0;i2 < len2; i2++)
          dests[i2].emit("unpipe", this, { hasUnpiped: false });
        return this;
      }
      var index = indexOf(state.pipes, dest);
      if (index === -1)
        return this;
      if (state.pipes.splice(index, 1), state.pipesCount -= 1, state.pipesCount === 1)
        state.pipes = state.pipes[0];
      return dest.emit("unpipe", this, unpipeInfo), this;
    };
    Readable.prototype.on = function(ev, fn) {
      var res = Stream.prototype.on.call(this, ev, fn), state = this._readableState;
      if (ev === "data") {
        if (state.readableListening = this.listenerCount("readable") > 0, state.flowing !== false)
          this.resume();
      } else if (ev === "readable") {
        if (!state.endEmitted && !state.readableListening) {
          if (state.readableListening = state.needReadable = true, state.flowing = false, state.emittedReadable = false, debug("on readable", state.length, state.reading), state.length)
            emitReadable(this);
          else if (!state.reading)
            process.nextTick(nReadingNextTick, this);
        }
      }
      return res;
    };
    Readable.prototype.addListener = Readable.prototype.on;
    Readable.prototype.removeListener = function(ev, fn) {
      var res = Stream.prototype.removeListener.call(this, ev, fn);
      if (ev === "readable")
        process.nextTick(updateReadableListening, this);
      return res;
    };
    Readable.prototype.removeAllListeners = function(ev) {
      var res = Stream.prototype.removeAllListeners.apply(this, arguments);
      if (ev === "readable" || ev === undefined)
        process.nextTick(updateReadableListening, this);
      return res;
    };
    function updateReadableListening(self2) {
      var state = self2._readableState;
      if (state.readableListening = self2.listenerCount("readable") > 0, state.resumeScheduled && !state.paused)
        state.flowing = true;
      else if (self2.listenerCount("data") > 0)
        self2.resume();
    }
    function nReadingNextTick(self2) {
      debug("readable nexttick read 0"), self2.read(0);
    }
    Readable.prototype.resume = function() {
      var state = this._readableState;
      if (!state.flowing)
        debug("resume"), state.flowing = !state.readableListening, resume(this, state);
      return state.paused = false, this;
    };
    function resume(stream, state) {
      if (!state.resumeScheduled)
        state.resumeScheduled = true, process.nextTick(resume_, stream, state);
    }
    function resume_(stream, state) {
      if (debug("resume", state.reading), !state.reading)
        stream.read(0);
      if (state.resumeScheduled = false, stream.emit("resume"), flow(stream), state.flowing && !state.reading)
        stream.read(0);
    }
    Readable.prototype.pause = function() {
      if (debug("call pause flowing=%j", this._readableState.flowing), this._readableState.flowing !== false)
        debug("pause"), this._readableState.flowing = false, this.emit("pause");
      return this._readableState.paused = true, this;
    };
    function flow(stream) {
      var state = stream._readableState;
      debug("flow", state.flowing);
      while (state.flowing && stream.read() !== null)
        ;
    }
    Readable.prototype.wrap = function(stream) {
      var _this = this, state = this._readableState, paused = false;
      stream.on("end", function() {
        if (debug("wrapped end"), state.decoder && !state.ended) {
          var chunk = state.decoder.end();
          if (chunk && chunk.length)
            _this.push(chunk);
        }
        _this.push(null);
      }), stream.on("data", function(chunk) {
        if (debug("wrapped data"), state.decoder)
          chunk = state.decoder.write(chunk);
        if (state.objectMode && (chunk === null || chunk === undefined))
          return;
        else if (!state.objectMode && (!chunk || !chunk.length))
          return;
        var ret = _this.push(chunk);
        if (!ret)
          paused = true, stream.pause();
      });
      for (var i2 in stream)
        if (this[i2] === undefined && typeof stream[i2] === "function")
          this[i2] = function(method) {
            return function() {
              return stream[method].apply(stream, arguments);
            };
          }(i2);
      for (var n = 0;n < kProxyEvents.length; n++)
        stream.on(kProxyEvents[n], this.emit.bind(this, kProxyEvents[n]));
      return this._read = function(n2) {
        if (debug("wrapped _read", n2), paused)
          paused = false, stream.resume();
      }, this;
    };
    if (typeof Symbol === "function")
      Readable.prototype[Symbol.asyncIterator] = function() {
        if (createReadableStreamAsyncIterator === undefined)
          createReadableStreamAsyncIterator = require_async_iterator();
        return createReadableStreamAsyncIterator(this);
      };
    Object.defineProperty(Readable.prototype, "readableHighWaterMark", { enumerable: false, get: function() {
      return this._readableState.highWaterMark;
    } });
    Object.defineProperty(Readable.prototype, "readableBuffer", { enumerable: false, get: function() {
      return this._readableState && this._readableState.buffer;
    } });
    Object.defineProperty(Readable.prototype, "readableFlowing", { enumerable: false, get: function() {
      return this._readableState.flowing;
    }, set: function(state) {
      if (this._readableState)
        this._readableState.flowing = state;
    } });
    Readable._fromList = fromList;
    Object.defineProperty(Readable.prototype, "readableLength", { enumerable: false, get: function() {
      return this._readableState.length;
    } });
    function fromList(n, state) {
      if (state.length === 0)
        return null;
      var ret;
      if (state.objectMode)
        ret = state.buffer.shift();
      else if (!n || n >= state.length) {
        if (state.decoder)
          ret = state.buffer.join("");
        else if (state.buffer.length === 1)
          ret = state.buffer.first();
        else
          ret = state.buffer.concat(state.length);
        state.buffer.clear();
      } else
        ret = state.buffer.consume(n, state.decoder);
      return ret;
    }
    function endReadable(stream) {
      var state = stream._readableState;
      if (debug("endReadable", state.endEmitted), !state.endEmitted)
        state.ended = true, process.nextTick(endReadableNT, state, stream);
    }
    function endReadableNT(state, stream) {
      if (debug("endReadableNT", state.endEmitted, state.length), !state.endEmitted && state.length === 0) {
        if (state.endEmitted = true, stream.readable = false, stream.emit("end"), state.autoDestroy) {
          var wState = stream._writableState;
          if (!wState || wState.autoDestroy && wState.finished)
            stream.destroy();
        }
      }
    }
    if (typeof Symbol === "function")
      Readable.from = function(iterable, opts) {
        if (from2 === undefined)
          from2 = require_from();
        return from2(Readable, iterable, opts);
      };
    function indexOf(xs, x) {
      for (var i2 = 0, l = xs.length;i2 < l; i2++)
        if (xs[i2] === x)
          return i2;
      return -1;
    }
  });
  require__stream_transform = __commonJS2((exports2, module2) => {
    module2.exports = Transform;
    var _require$codes = require_errors().codes, ERR_METHOD_NOT_IMPLEMENTED = _require$codes.ERR_METHOD_NOT_IMPLEMENTED, ERR_MULTIPLE_CALLBACK = _require$codes.ERR_MULTIPLE_CALLBACK, ERR_TRANSFORM_ALREADY_TRANSFORMING = _require$codes.ERR_TRANSFORM_ALREADY_TRANSFORMING, ERR_TRANSFORM_WITH_LENGTH_0 = _require$codes.ERR_TRANSFORM_WITH_LENGTH_0, Duplex = require__stream_duplex();
    require_inherits()(Transform, Duplex);
    function afterTransform(er, data) {
      var ts = this._transformState;
      ts.transforming = false;
      var cb = ts.writecb;
      if (cb === null)
        return this.emit("error", new ERR_MULTIPLE_CALLBACK);
      if (ts.writechunk = null, ts.writecb = null, data != null)
        this.push(data);
      cb(er);
      var rs = this._readableState;
      if (rs.reading = false, rs.needReadable || rs.length < rs.highWaterMark)
        this._read(rs.highWaterMark);
    }
    function Transform(options) {
      if (!(this instanceof Transform))
        return new Transform(options);
      if (Duplex.call(this, options), this._transformState = { afterTransform: afterTransform.bind(this), needTransform: false, transforming: false, writecb: null, writechunk: null, writeencoding: null }, this._readableState.needReadable = true, this._readableState.sync = false, options) {
        if (typeof options.transform === "function")
          this._transform = options.transform;
        if (typeof options.flush === "function")
          this._flush = options.flush;
      }
      this.on("prefinish", prefinish);
    }
    function prefinish() {
      var _this = this;
      if (typeof this._flush === "function" && !this._readableState.destroyed)
        this._flush(function(er, data) {
          done(_this, er, data);
        });
      else
        done(this, null, null);
    }
    Transform.prototype.push = function(chunk, encoding) {
      return this._transformState.needTransform = false, Duplex.prototype.push.call(this, chunk, encoding);
    };
    Transform.prototype._transform = function(chunk, encoding, cb) {
      cb(new ERR_METHOD_NOT_IMPLEMENTED("_transform()"));
    };
    Transform.prototype._write = function(chunk, encoding, cb) {
      var ts = this._transformState;
      if (ts.writecb = cb, ts.writechunk = chunk, ts.writeencoding = encoding, !ts.transforming) {
        var rs = this._readableState;
        if (ts.needTransform || rs.needReadable || rs.length < rs.highWaterMark)
          this._read(rs.highWaterMark);
      }
    };
    Transform.prototype._read = function(n) {
      var ts = this._transformState;
      if (ts.writechunk !== null && !ts.transforming)
        ts.transforming = true, this._transform(ts.writechunk, ts.writeencoding, ts.afterTransform);
      else
        ts.needTransform = true;
    };
    Transform.prototype._destroy = function(err, cb) {
      Duplex.prototype._destroy.call(this, err, function(err2) {
        cb(err2);
      });
    };
    function done(stream, er, data) {
      if (er)
        return stream.emit("error", er);
      if (data != null)
        stream.push(data);
      if (stream._writableState.length)
        throw new ERR_TRANSFORM_WITH_LENGTH_0;
      if (stream._transformState.transforming)
        throw new ERR_TRANSFORM_ALREADY_TRANSFORMING;
      return stream.push(null);
    }
  });
  require__stream_passthrough = __commonJS2((exports2, module2) => {
    module2.exports = PassThrough;
    var Transform = require__stream_transform();
    require_inherits()(PassThrough, Transform);
    function PassThrough(options) {
      if (!(this instanceof PassThrough))
        return new PassThrough(options);
      Transform.call(this, options);
    }
    PassThrough.prototype._transform = function(chunk, encoding, cb) {
      cb(null, chunk);
    };
  });
  require_pipeline = __commonJS2((exports2, module2) => {
    var eos;
    function once(callback) {
      var called = false;
      return function() {
        if (called)
          return;
        called = true, callback.apply(undefined, arguments);
      };
    }
    var _require$codes = require_errors().codes, ERR_MISSING_ARGS = _require$codes.ERR_MISSING_ARGS, ERR_STREAM_DESTROYED = _require$codes.ERR_STREAM_DESTROYED;
    function noop2(err) {
      if (err)
        throw err;
    }
    function isRequest2(stream) {
      return stream.setHeader && typeof stream.abort === "function";
    }
    function destroyer(stream, reading, writing, callback) {
      callback = once(callback);
      var closed = false;
      if (stream.on("close", function() {
        closed = true;
      }), eos === undefined)
        eos = require_end_of_stream();
      eos(stream, { readable: reading, writable: writing }, function(err) {
        if (err)
          return callback(err);
        closed = true, callback();
      });
      var destroyed = false;
      return function(err) {
        if (closed)
          return;
        if (destroyed)
          return;
        if (destroyed = true, isRequest2(stream))
          return stream.abort();
        if (typeof stream.destroy === "function")
          return stream.destroy();
        callback(err || new ERR_STREAM_DESTROYED("pipe"));
      };
    }
    function call(fn) {
      fn();
    }
    function pipe(from2, to) {
      return from2.pipe(to);
    }
    function popCallback(streams) {
      if (!streams.length)
        return noop2;
      if (typeof streams[streams.length - 1] !== "function")
        return noop2;
      return streams.pop();
    }
    function pipeline() {
      for (var _len = arguments.length, streams = Array(_len), _key = 0;_key < _len; _key++)
        streams[_key] = arguments[_key];
      var callback = popCallback(streams);
      if (Array.isArray(streams[0]))
        streams = streams[0];
      if (streams.length < 2)
        throw new ERR_MISSING_ARGS("streams");
      var error, destroys = streams.map(function(stream, i2) {
        var reading = i2 < streams.length - 1, writing = i2 > 0;
        return destroyer(stream, reading, writing, function(err) {
          if (!error)
            error = err;
          if (err)
            destroys.forEach(call);
          if (reading)
            return;
          destroys.forEach(call), callback(error);
        });
      });
      return streams.reduce(pipe);
    }
    module2.exports = pipeline;
  });
  require_readable = __commonJS2((exports2, module2) => {
    var Stream = require_stream();
    exports2 = module2.exports = require__stream_readable(), exports2.Stream = Stream || exports2, exports2.Readable = exports2, exports2.Writable = require__stream_writable(), exports2.Duplex = require__stream_duplex(), exports2.Transform = require__stream_transform(), exports2.PassThrough = require__stream_passthrough(), exports2.finished = require_end_of_stream(), exports2.pipeline = require_pipeline();
  });
  require_response = __commonJS2((exports2) => {
    var capability = require_capability(), inherits3 = require_inherits(), stream = require_readable(), rStates = exports2.readyStates = { UNSENT: 0, OPENED: 1, HEADERS_RECEIVED: 2, LOADING: 3, DONE: 4 }, IncomingMessage = exports2.IncomingMessage = function(xhr, response, mode, resetTimers) {
      var self2 = this;
      if (stream.Readable.call(self2), self2._mode = mode, self2.headers = {}, self2.rawHeaders = [], self2.trailers = {}, self2.rawTrailers = [], self2.on("end", function() {
        process.nextTick(function() {
          self2.emit("close");
        });
      }), mode === "fetch") {
        let read22 = function() {
          reader.read().then(function(result) {
            if (self2._destroyed)
              return;
            if (resetTimers(result.done), result.done) {
              self2.push(null);
              return;
            }
            self2.push(Buffer.from(result.value)), read22();
          }).catch(function(err) {
            if (resetTimers(true), !self2._destroyed)
              self2.emit("error", err);
          });
        };
        var read2 = read22;
        if (self2._fetchResponse = response, self2.url = response.url, self2.statusCode = response.status, self2.statusMessage = response.statusText, response.headers.forEach(function(header, key) {
          self2.headers[key.toLowerCase()] = header, self2.rawHeaders.push(key, header);
        }), capability.writableStream) {
          var writable = new WritableStream({ write: function(chunk) {
            return resetTimers(false), new Promise(function(resolve, reject) {
              if (self2._destroyed)
                reject();
              else if (self2.push(Buffer.from(chunk)))
                resolve();
              else
                self2._resumeFetch = resolve;
            });
          }, close: function() {
            if (resetTimers(true), !self2._destroyed)
              self2.push(null);
          }, abort: function(err) {
            if (resetTimers(true), !self2._destroyed)
              self2.emit("error", err);
          } });
          try {
            response.body.pipeTo(writable).catch(function(err) {
              if (resetTimers(true), !self2._destroyed)
                self2.emit("error", err);
            });
            return;
          } catch (e) {}
        }
        var reader = response.body.getReader();
        read22();
      } else {
        self2._xhr = xhr, self2._pos = 0, self2.url = xhr.responseURL, self2.statusCode = xhr.status, self2.statusMessage = xhr.statusText;
        var headers = xhr.getAllResponseHeaders().split(/\r?\n/);
        if (headers.forEach(function(header) {
          var matches = header.match(/^([^:]+):\s*(.*)/);
          if (matches) {
            var key = matches[1].toLowerCase();
            if (key === "set-cookie") {
              if (self2.headers[key] === undefined)
                self2.headers[key] = [];
              self2.headers[key].push(matches[2]);
            } else if (self2.headers[key] !== undefined)
              self2.headers[key] += ", " + matches[2];
            else
              self2.headers[key] = matches[2];
            self2.rawHeaders.push(matches[1], matches[2]);
          }
        }), self2._charset = "x-user-defined", !capability.overrideMimeType) {
          var mimeType = self2.rawHeaders["mime-type"];
          if (mimeType) {
            var charsetMatch = mimeType.match(/;\s*charset=([^;])(;|$)/);
            if (charsetMatch)
              self2._charset = charsetMatch[1].toLowerCase();
          }
          if (!self2._charset)
            self2._charset = "utf-8";
        }
      }
    };
    inherits3(IncomingMessage, stream.Readable);
    IncomingMessage.prototype._read = function() {
      var self2 = this, resolve = self2._resumeFetch;
      if (resolve)
        self2._resumeFetch = null, resolve();
    };
    IncomingMessage.prototype._onXHRProgress = function(resetTimers) {
      var self2 = this, xhr = self2._xhr, response = null;
      switch (self2._mode) {
        case "text":
          if (response = xhr.responseText, response.length > self2._pos) {
            var newData = response.substr(self2._pos);
            if (self2._charset === "x-user-defined") {
              var buffer = Buffer.alloc(newData.length);
              for (var i2 = 0;i2 < newData.length; i2++)
                buffer[i2] = newData.charCodeAt(i2) & 255;
              self2.push(buffer);
            } else
              self2.push(newData, self2._charset);
            self2._pos = response.length;
          }
          break;
        case "arraybuffer":
          if (xhr.readyState !== rStates.DONE || !xhr.response)
            break;
          response = xhr.response, self2.push(Buffer.from(new Uint8Array(response)));
          break;
        case "moz-chunked-arraybuffer":
          if (response = xhr.response, xhr.readyState !== rStates.LOADING || !response)
            break;
          self2.push(Buffer.from(new Uint8Array(response)));
          break;
        case "ms-stream":
          if (response = xhr.response, xhr.readyState !== rStates.LOADING)
            break;
          var reader = new globalThis.MSStreamReader;
          reader.onprogress = function() {
            if (reader.result.byteLength > self2._pos)
              self2.push(Buffer.from(new Uint8Array(reader.result.slice(self2._pos)))), self2._pos = reader.result.byteLength;
          }, reader.onload = function() {
            resetTimers(true), self2.push(null);
          }, reader.readAsArrayBuffer(response);
          break;
      }
      if (self2._xhr.readyState === rStates.DONE && self2._mode !== "ms-stream")
        resetTimers(true), self2.push(null);
    };
  });
  require_request = __commonJS2((exports2, module2) => {
    var capability = require_capability(), inherits3 = require_inherits(), response = require_response(), stream = require_readable(), IncomingMessage = response.IncomingMessage, rStates = response.readyStates;
    function decideMode(preferBinary, useFetch) {
      if (capability.fetch && useFetch)
        return "fetch";
      else if (capability.mozchunkedarraybuffer)
        return "moz-chunked-arraybuffer";
      else if (capability.msstream)
        return "ms-stream";
      else if (capability.arraybuffer && preferBinary)
        return "arraybuffer";
      else
        return "text";
    }
    var ClientRequest = module2.exports = function(opts) {
      var self2 = this;
      if (stream.Writable.call(self2), self2._opts = opts, self2._body = [], self2._headers = {}, opts.auth)
        self2.setHeader("Authorization", "Basic " + Buffer.from(opts.auth).toString("base64"));
      Object.keys(opts.headers).forEach(function(name) {
        self2.setHeader(name, opts.headers[name]);
      });
      var preferBinary, useFetch = true;
      if (opts.mode === "disable-fetch" || "requestTimeout" in opts && !capability.abortController)
        useFetch = false, preferBinary = true;
      else if (opts.mode === "prefer-streaming")
        preferBinary = false;
      else if (opts.mode === "allow-wrong-content-type")
        preferBinary = !capability.overrideMimeType;
      else if (!opts.mode || opts.mode === "default" || opts.mode === "prefer-fast")
        preferBinary = true;
      else
        throw Error("Invalid value for opts.mode");
      self2._mode = decideMode(preferBinary, useFetch), self2._fetchTimer = null, self2._socketTimeout = null, self2._socketTimer = null, self2.on("finish", function() {
        self2._onFinish();
      });
    };
    inherits3(ClientRequest, stream.Writable);
    ClientRequest.prototype.setHeader = function(name, value) {
      var self2 = this, lowerName = name.toLowerCase();
      if (unsafeHeaders.indexOf(lowerName) !== -1)
        return;
      self2._headers[lowerName] = { name, value };
    };
    ClientRequest.prototype.getHeader = function(name) {
      var header = this._headers[name.toLowerCase()];
      if (header)
        return header.value;
      return null;
    };
    ClientRequest.prototype.removeHeader = function(name) {
      var self2 = this;
      delete self2._headers[name.toLowerCase()];
    };
    ClientRequest.prototype._onFinish = function() {
      var self2 = this;
      if (self2._destroyed)
        return;
      var opts = self2._opts;
      if ("timeout" in opts && opts.timeout !== 0)
        self2.setTimeout(opts.timeout);
      var headersObj = self2._headers, body = null;
      if (opts.method !== "GET" && opts.method !== "HEAD")
        body = new Blob(self2._body, { type: (headersObj["content-type"] || {}).value || "" });
      var headersList = [];
      if (Object.keys(headersObj).forEach(function(keyName) {
        var name = headersObj[keyName].name, value = headersObj[keyName].value;
        if (Array.isArray(value))
          value.forEach(function(v) {
            headersList.push([name, v]);
          });
        else
          headersList.push([name, value]);
      }), self2._mode === "fetch") {
        var signal = null;
        if (capability.abortController) {
          var controller = new AbortController;
          if (signal = controller.signal, self2._fetchAbortController = controller, "requestTimeout" in opts && opts.requestTimeout !== 0)
            self2._fetchTimer = globalThis.setTimeout(function() {
              if (self2.emit("requestTimeout"), self2._fetchAbortController)
                self2._fetchAbortController.abort();
            }, opts.requestTimeout);
        }
        globalThis.fetch(self2._opts.url, { method: self2._opts.method, headers: headersList, body: body || undefined, mode: "cors", credentials: opts.withCredentials ? "include" : "same-origin", signal }).then(function(response2) {
          self2._fetchResponse = response2, self2._resetTimers(false), self2._connect();
        }, function(reason) {
          if (self2._resetTimers(true), !self2._destroyed)
            self2.emit("error", reason);
        });
      } else {
        var xhr = self2._xhr = new globalThis.XMLHttpRequest;
        try {
          xhr.open(self2._opts.method, self2._opts.url, true);
        } catch (err) {
          process.nextTick(function() {
            self2.emit("error", err);
          });
          return;
        }
        if ("responseType" in xhr)
          xhr.responseType = self2._mode;
        if ("withCredentials" in xhr)
          xhr.withCredentials = !!opts.withCredentials;
        if (self2._mode === "text" && "overrideMimeType" in xhr)
          xhr.overrideMimeType("text/plain; charset=x-user-defined");
        if ("requestTimeout" in opts)
          xhr.timeout = opts.requestTimeout, xhr.ontimeout = function() {
            self2.emit("requestTimeout");
          };
        if (headersList.forEach(function(header) {
          xhr.setRequestHeader(header[0], header[1]);
        }), self2._response = null, xhr.onreadystatechange = function() {
          switch (xhr.readyState) {
            case rStates.LOADING:
            case rStates.DONE:
              self2._onXHRProgress();
              break;
          }
        }, self2._mode === "moz-chunked-arraybuffer")
          xhr.onprogress = function() {
            self2._onXHRProgress();
          };
        xhr.onerror = function() {
          if (self2._destroyed)
            return;
          self2._resetTimers(true), self2.emit("error", Error("XHR error"));
        };
        try {
          xhr.send(body);
        } catch (err) {
          process.nextTick(function() {
            self2.emit("error", err);
          });
          return;
        }
      }
    };
    function statusValid(xhr) {
      try {
        var status = xhr.status;
        return status !== null && status !== 0;
      } catch (e) {
        return false;
      }
    }
    ClientRequest.prototype._onXHRProgress = function() {
      var self2 = this;
      if (self2._resetTimers(false), !statusValid(self2._xhr) || self2._destroyed)
        return;
      if (!self2._response)
        self2._connect();
      self2._response._onXHRProgress(self2._resetTimers.bind(self2));
    };
    ClientRequest.prototype._connect = function() {
      var self2 = this;
      if (self2._destroyed)
        return;
      self2._response = new IncomingMessage(self2._xhr, self2._fetchResponse, self2._mode, self2._resetTimers.bind(self2)), self2._response.on("error", function(err) {
        self2.emit("error", err);
      }), self2.emit("response", self2._response);
    };
    ClientRequest.prototype._write = function(chunk, encoding, cb) {
      var self2 = this;
      self2._body.push(chunk), cb();
    };
    ClientRequest.prototype._resetTimers = function(done) {
      var self2 = this;
      if (globalThis.clearTimeout(self2._socketTimer), self2._socketTimer = null, done)
        globalThis.clearTimeout(self2._fetchTimer), self2._fetchTimer = null;
      else if (self2._socketTimeout)
        self2._socketTimer = globalThis.setTimeout(function() {
          self2.emit("timeout");
        }, self2._socketTimeout);
    };
    ClientRequest.prototype.abort = ClientRequest.prototype.destroy = function(err) {
      var self2 = this;
      if (self2._destroyed = true, self2._resetTimers(true), self2._response)
        self2._response._destroyed = true;
      if (self2._xhr)
        self2._xhr.abort();
      else if (self2._fetchAbortController)
        self2._fetchAbortController.abort();
      if (err)
        self2.emit("error", err);
    };
    ClientRequest.prototype.end = function(data, encoding, cb) {
      var self2 = this;
      if (typeof data === "function")
        cb = data, data = undefined;
      stream.Writable.prototype.end.call(self2, data, encoding, cb);
    };
    ClientRequest.prototype.setTimeout = function(timeout, cb) {
      var self2 = this;
      if (cb)
        self2.once("timeout", cb);
      self2._socketTimeout = timeout, self2._resetTimers(false);
    };
    ClientRequest.prototype.flushHeaders = function() {};
    ClientRequest.prototype.setNoDelay = function() {};
    ClientRequest.prototype.setSocketKeepAlive = function() {};
    var unsafeHeaders = ["accept-charset", "accept-encoding", "access-control-request-headers", "access-control-request-method", "connection", "content-length", "cookie", "cookie2", "date", "dnt", "expect", "host", "keep-alive", "origin", "referer", "te", "trailer", "transfer-encoding", "upgrade", "via"];
  });
  require_immutable = __commonJS2((exports2, module2) => {
    module2.exports = extend2;
    var hasOwnProperty3 = Object.prototype.hasOwnProperty;
    function extend2() {
      var target = {};
      for (var i2 = 0;i2 < arguments.length; i2++) {
        var source = arguments[i2];
        for (var key in source)
          if (hasOwnProperty3.call(source, key))
            target[key] = source[key];
      }
      return target;
    }
  });
  require_builtin_status_codes = __commonJS2((exports2, module2) => {
    module2.exports = (init_http(), __toCommonJS(exports_http)).STATUS_CODES;
  });
  require_stream_http = __commonJS2((exports2) => {
    var ClientRequest = require_request(), response = require_response(), extend2 = require_immutable(), statusCodes = require_builtin_status_codes(), url = (init_url(), __toCommonJS(exports_url)), http = exports2;
    http.request = function(opts, cb) {
      if (typeof opts === "string")
        opts = url.parse(opts);
      else
        opts = extend2(opts);
      var defaultProtocol = globalThis.location.protocol.search(/^https?:$/) === -1 ? "http:" : "", protocol = opts.protocol || defaultProtocol, host = opts.hostname || opts.host, port = opts.port, path = opts.path || "/";
      if (host && host.indexOf(":") !== -1)
        host = "[" + host + "]";
      opts.url = (host ? protocol + "//" + host : "") + (port ? ":" + port : "") + path, opts.method = (opts.method || "GET").toUpperCase(), opts.headers = opts.headers || {};
      var req = new ClientRequest(opts);
      if (cb)
        req.on("response", cb);
      return req;
    };
    http.get = function(opts, cb) {
      var req = http.request(opts, cb);
      return req.end(), req;
    };
    http.ClientRequest = ClientRequest;
    http.IncomingMessage = response.IncomingMessage;
    http.Agent = function() {};
    http.Agent.defaultMaxSockets = 4;
    http.globalAgent = new http.Agent;
    http.STATUS_CODES = statusCodes;
    http.METHODS = ["CHECKOUT", "CONNECT", "COPY", "DELETE", "GET", "HEAD", "LOCK", "M-SEARCH", "MERGE", "MKACTIVITY", "MKCOL", "MOVE", "NOTIFY", "OPTIONS", "PATCH", "POST", "PROPFIND", "PROPPATCH", "PURGE", "PUT", "REPORT", "SEARCH", "SUBSCRIBE", "TRACE", "UNLOCK", "UNSUBSCRIBE"];
  });
  import_stream_http = __toESM(require_stream_http(), 1);
  ({ request, get, ClientRequest, IncomingMessage, Agent, globalAgent, STATUS_CODES, METHODS } = import_stream_http.default);
  http_default = import_stream_http.default;
});

// src/extension.ts
var exports_extension = {};
__export(exports_extension, {
  deactivate: () => deactivate,
  activate: () => activate
});
module.exports = __toCommonJS(exports_extension);

// src/watchdog.ts
var import_vscode4 = require("vscode");

// node_modules/axios/lib/helpers/bind.js
function bind(fn, thisArg) {
  return function wrap() {
    return fn.apply(thisArg, arguments);
  };
}

// node_modules/axios/lib/utils.js
var { toString } = Object.prototype;
var { getPrototypeOf } = Object;
var { iterator, toStringTag } = Symbol;
var kindOf = ((cache) => (thing) => {
  const str = toString.call(thing);
  return cache[str] || (cache[str] = str.slice(8, -1).toLowerCase());
})(Object.create(null));
var kindOfTest = (type) => {
  type = type.toLowerCase();
  return (thing) => kindOf(thing) === type;
};
var typeOfTest = (type) => (thing) => typeof thing === type;
var { isArray } = Array;
var isUndefined = typeOfTest("undefined");
function isBuffer(val) {
  return val !== null && !isUndefined(val) && val.constructor !== null && !isUndefined(val.constructor) && isFunction(val.constructor.isBuffer) && val.constructor.isBuffer(val);
}
var isArrayBuffer = kindOfTest("ArrayBuffer");
function isArrayBufferView(val) {
  let result;
  if (typeof ArrayBuffer !== "undefined" && ArrayBuffer.isView) {
    result = ArrayBuffer.isView(val);
  } else {
    result = val && val.buffer && isArrayBuffer(val.buffer);
  }
  return result;
}
var isString = typeOfTest("string");
var isFunction = typeOfTest("function");
var isNumber = typeOfTest("number");
var isObject = (thing) => thing !== null && typeof thing === "object";
var isBoolean = (thing) => thing === true || thing === false;
var isPlainObject = (val) => {
  if (kindOf(val) !== "object") {
    return false;
  }
  const prototype = getPrototypeOf(val);
  return (prototype === null || prototype === Object.prototype || Object.getPrototypeOf(prototype) === null) && !(toStringTag in val) && !(iterator in val);
};
var isEmptyObject = (val) => {
  if (!isObject(val) || isBuffer(val)) {
    return false;
  }
  try {
    return Object.keys(val).length === 0 && Object.getPrototypeOf(val) === Object.prototype;
  } catch (e) {
    return false;
  }
};
var isDate = kindOfTest("Date");
var isFile = kindOfTest("File");
var isBlob = kindOfTest("Blob");
var isFileList = kindOfTest("FileList");
var isStream = (val) => isObject(val) && isFunction(val.pipe);
var isFormData = (thing) => {
  let kind;
  return thing && (typeof FormData === "function" && thing instanceof FormData || isFunction(thing.append) && ((kind = kindOf(thing)) === "formdata" || kind === "object" && isFunction(thing.toString) && thing.toString() === "[object FormData]"));
};
var isURLSearchParams = kindOfTest("URLSearchParams");
var [isReadableStream, isRequest, isResponse, isHeaders] = [
  "ReadableStream",
  "Request",
  "Response",
  "Headers"
].map(kindOfTest);
var trim = (str) => str.trim ? str.trim() : str.replace(/^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g, "");
function forEach(obj, fn, { allOwnKeys = false } = {}) {
  if (obj === null || typeof obj === "undefined") {
    return;
  }
  let i;
  let l;
  if (typeof obj !== "object") {
    obj = [obj];
  }
  if (isArray(obj)) {
    for (i = 0, l = obj.length;i < l; i++) {
      fn.call(null, obj[i], i, obj);
    }
  } else {
    if (isBuffer(obj)) {
      return;
    }
    const keys = allOwnKeys ? Object.getOwnPropertyNames(obj) : Object.keys(obj);
    const len = keys.length;
    let key;
    for (i = 0;i < len; i++) {
      key = keys[i];
      fn.call(null, obj[key], key, obj);
    }
  }
}
function findKey(obj, key) {
  if (isBuffer(obj)) {
    return null;
  }
  key = key.toLowerCase();
  const keys = Object.keys(obj);
  let i = keys.length;
  let _key;
  while (i-- > 0) {
    _key = keys[i];
    if (key === _key.toLowerCase()) {
      return _key;
    }
  }
  return null;
}
var _global = (() => {
  if (typeof globalThis !== "undefined")
    return globalThis;
  return typeof self !== "undefined" ? self : typeof window !== "undefined" ? window : global;
})();
var isContextDefined = (context) => !isUndefined(context) && context !== _global;
function merge() {
  const { caseless, skipUndefined } = isContextDefined(this) && this || {};
  const result = {};
  const assignValue = (val, key) => {
    if (key === "__proto__" || key === "constructor" || key === "prototype") {
      return;
    }
    const targetKey = caseless && findKey(result, key) || key;
    if (isPlainObject(result[targetKey]) && isPlainObject(val)) {
      result[targetKey] = merge(result[targetKey], val);
    } else if (isPlainObject(val)) {
      result[targetKey] = merge({}, val);
    } else if (isArray(val)) {
      result[targetKey] = val.slice();
    } else if (!skipUndefined || !isUndefined(val)) {
      result[targetKey] = val;
    }
  };
  for (let i = 0, l = arguments.length;i < l; i++) {
    arguments[i] && forEach(arguments[i], assignValue);
  }
  return result;
}
var extend = (a, b, thisArg, { allOwnKeys } = {}) => {
  forEach(b, (val, key) => {
    if (thisArg && isFunction(val)) {
      Object.defineProperty(a, key, {
        value: bind(val, thisArg),
        writable: true,
        enumerable: true,
        configurable: true
      });
    } else {
      Object.defineProperty(a, key, {
        value: val,
        writable: true,
        enumerable: true,
        configurable: true
      });
    }
  }, { allOwnKeys });
  return a;
};
var stripBOM = (content) => {
  if (content.charCodeAt(0) === 65279) {
    content = content.slice(1);
  }
  return content;
};
var inherits = (constructor, superConstructor, props, descriptors) => {
  constructor.prototype = Object.create(superConstructor.prototype, descriptors);
  Object.defineProperty(constructor.prototype, "constructor", {
    value: constructor,
    writable: true,
    enumerable: false,
    configurable: true
  });
  Object.defineProperty(constructor, "super", {
    value: superConstructor.prototype
  });
  props && Object.assign(constructor.prototype, props);
};
var toFlatObject = (sourceObj, destObj, filter, propFilter) => {
  let props;
  let i;
  let prop;
  const merged = {};
  destObj = destObj || {};
  if (sourceObj == null)
    return destObj;
  do {
    props = Object.getOwnPropertyNames(sourceObj);
    i = props.length;
    while (i-- > 0) {
      prop = props[i];
      if ((!propFilter || propFilter(prop, sourceObj, destObj)) && !merged[prop]) {
        destObj[prop] = sourceObj[prop];
        merged[prop] = true;
      }
    }
    sourceObj = filter !== false && getPrototypeOf(sourceObj);
  } while (sourceObj && (!filter || filter(sourceObj, destObj)) && sourceObj !== Object.prototype);
  return destObj;
};
var endsWith = (str, searchString, position) => {
  str = String(str);
  if (position === undefined || position > str.length) {
    position = str.length;
  }
  position -= searchString.length;
  const lastIndex = str.indexOf(searchString, position);
  return lastIndex !== -1 && lastIndex === position;
};
var toArray = (thing) => {
  if (!thing)
    return null;
  if (isArray(thing))
    return thing;
  let i = thing.length;
  if (!isNumber(i))
    return null;
  const arr = new Array(i);
  while (i-- > 0) {
    arr[i] = thing[i];
  }
  return arr;
};
var isTypedArray = ((TypedArray) => {
  return (thing) => {
    return TypedArray && thing instanceof TypedArray;
  };
})(typeof Uint8Array !== "undefined" && getPrototypeOf(Uint8Array));
var forEachEntry = (obj, fn) => {
  const generator = obj && obj[iterator];
  const _iterator = generator.call(obj);
  let result;
  while ((result = _iterator.next()) && !result.done) {
    const pair = result.value;
    fn.call(obj, pair[0], pair[1]);
  }
};
var matchAll = (regExp, str) => {
  let matches;
  const arr = [];
  while ((matches = regExp.exec(str)) !== null) {
    arr.push(matches);
  }
  return arr;
};
var isHTMLForm = kindOfTest("HTMLFormElement");
var toCamelCase = (str) => {
  return str.toLowerCase().replace(/[-_\s]([a-z\d])(\w*)/g, function replacer(m, p1, p2) {
    return p1.toUpperCase() + p2;
  });
};
var hasOwnProperty = (({ hasOwnProperty: hasOwnProperty2 }) => (obj, prop) => hasOwnProperty2.call(obj, prop))(Object.prototype);
var isRegExp = kindOfTest("RegExp");
var reduceDescriptors = (obj, reducer) => {
  const descriptors = Object.getOwnPropertyDescriptors(obj);
  const reducedDescriptors = {};
  forEach(descriptors, (descriptor, name) => {
    let ret;
    if ((ret = reducer(descriptor, name, obj)) !== false) {
      reducedDescriptors[name] = ret || descriptor;
    }
  });
  Object.defineProperties(obj, reducedDescriptors);
};
var freezeMethods = (obj) => {
  reduceDescriptors(obj, (descriptor, name) => {
    if (isFunction(obj) && ["arguments", "caller", "callee"].indexOf(name) !== -1) {
      return false;
    }
    const value = obj[name];
    if (!isFunction(value))
      return;
    descriptor.enumerable = false;
    if ("writable" in descriptor) {
      descriptor.writable = false;
      return;
    }
    if (!descriptor.set) {
      descriptor.set = () => {
        throw Error("Can not rewrite read-only method '" + name + "'");
      };
    }
  });
};
var toObjectSet = (arrayOrString, delimiter) => {
  const obj = {};
  const define = (arr) => {
    arr.forEach((value) => {
      obj[value] = true;
    });
  };
  isArray(arrayOrString) ? define(arrayOrString) : define(String(arrayOrString).split(delimiter));
  return obj;
};
var noop = () => {};
var toFiniteNumber = (value, defaultValue) => {
  return value != null && Number.isFinite(value = +value) ? value : defaultValue;
};
function isSpecCompliantForm(thing) {
  return !!(thing && isFunction(thing.append) && thing[toStringTag] === "FormData" && thing[iterator]);
}
var toJSONObject = (obj) => {
  const stack = new Array(10);
  const visit = (source, i) => {
    if (isObject(source)) {
      if (stack.indexOf(source) >= 0) {
        return;
      }
      if (isBuffer(source)) {
        return source;
      }
      if (!("toJSON" in source)) {
        stack[i] = source;
        const target = isArray(source) ? [] : {};
        forEach(source, (value, key) => {
          const reducedValue = visit(value, i + 1);
          !isUndefined(reducedValue) && (target[key] = reducedValue);
        });
        stack[i] = undefined;
        return target;
      }
    }
    return source;
  };
  return visit(obj, 0);
};
var isAsyncFn = kindOfTest("AsyncFunction");
var isThenable = (thing) => thing && (isObject(thing) || isFunction(thing)) && isFunction(thing.then) && isFunction(thing.catch);
var _setImmediate = ((setImmediateSupported, postMessageSupported) => {
  if (setImmediateSupported) {
    return setImmediate;
  }
  return postMessageSupported ? ((token, callbacks) => {
    _global.addEventListener("message", ({ source, data }) => {
      if (source === _global && data === token) {
        callbacks.length && callbacks.shift()();
      }
    }, false);
    return (cb) => {
      callbacks.push(cb);
      _global.postMessage(token, "*");
    };
  })(`axios@${Math.random()}`, []) : (cb) => setTimeout(cb);
})(typeof setImmediate === "function", isFunction(_global.postMessage));
var asap = typeof queueMicrotask !== "undefined" ? queueMicrotask.bind(_global) : typeof process !== "undefined" && process.nextTick || _setImmediate;
var isIterable = (thing) => thing != null && isFunction(thing[iterator]);
var utils_default = {
  isArray,
  isArrayBuffer,
  isBuffer,
  isFormData,
  isArrayBufferView,
  isString,
  isNumber,
  isBoolean,
  isObject,
  isPlainObject,
  isEmptyObject,
  isReadableStream,
  isRequest,
  isResponse,
  isHeaders,
  isUndefined,
  isDate,
  isFile,
  isBlob,
  isRegExp,
  isFunction,
  isStream,
  isURLSearchParams,
  isTypedArray,
  isFileList,
  forEach,
  merge,
  extend,
  trim,
  stripBOM,
  inherits,
  toFlatObject,
  kindOf,
  kindOfTest,
  endsWith,
  toArray,
  forEachEntry,
  matchAll,
  isHTMLForm,
  hasOwnProperty,
  hasOwnProp: hasOwnProperty,
  reduceDescriptors,
  freezeMethods,
  toObjectSet,
  toCamelCase,
  noop,
  toFiniteNumber,
  findKey,
  global: _global,
  isContextDefined,
  isSpecCompliantForm,
  toJSONObject,
  isAsyncFn,
  isThenable,
  setImmediate: _setImmediate,
  asap,
  isIterable
};

// node_modules/axios/lib/core/AxiosError.js
class AxiosError extends Error {
  static from(error, code, config, request, response, customProps) {
    const axiosError = new AxiosError(error.message, code || error.code, config, request, response);
    axiosError.cause = error;
    axiosError.name = error.name;
    customProps && Object.assign(axiosError, customProps);
    return axiosError;
  }
  constructor(message, code, config, request, response) {
    super(message);
    this.name = "AxiosError";
    this.isAxiosError = true;
    code && (this.code = code);
    config && (this.config = config);
    request && (this.request = request);
    if (response) {
      this.response = response;
      this.status = response.status;
    }
  }
  toJSON() {
    return {
      message: this.message,
      name: this.name,
      description: this.description,
      number: this.number,
      fileName: this.fileName,
      lineNumber: this.lineNumber,
      columnNumber: this.columnNumber,
      stack: this.stack,
      config: utils_default.toJSONObject(this.config),
      code: this.code,
      status: this.status
    };
  }
}
AxiosError.ERR_BAD_OPTION_VALUE = "ERR_BAD_OPTION_VALUE";
AxiosError.ERR_BAD_OPTION = "ERR_BAD_OPTION";
AxiosError.ECONNABORTED = "ECONNABORTED";
AxiosError.ETIMEDOUT = "ETIMEDOUT";
AxiosError.ERR_NETWORK = "ERR_NETWORK";
AxiosError.ERR_FR_TOO_MANY_REDIRECTS = "ERR_FR_TOO_MANY_REDIRECTS";
AxiosError.ERR_DEPRECATED = "ERR_DEPRECATED";
AxiosError.ERR_BAD_RESPONSE = "ERR_BAD_RESPONSE";
AxiosError.ERR_BAD_REQUEST = "ERR_BAD_REQUEST";
AxiosError.ERR_CANCELED = "ERR_CANCELED";
AxiosError.ERR_NOT_SUPPORT = "ERR_NOT_SUPPORT";
AxiosError.ERR_INVALID_URL = "ERR_INVALID_URL";
var AxiosError_default = AxiosError;

// node_modules/axios/lib/helpers/null.js
var null_default = null;

// node_modules/axios/lib/helpers/toFormData.js
function isVisitable(thing) {
  return utils_default.isPlainObject(thing) || utils_default.isArray(thing);
}
function removeBrackets(key) {
  return utils_default.endsWith(key, "[]") ? key.slice(0, -2) : key;
}
function renderKey(path, key, dots) {
  if (!path)
    return key;
  return path.concat(key).map(function each(token, i) {
    token = removeBrackets(token);
    return !dots && i ? "[" + token + "]" : token;
  }).join(dots ? "." : "");
}
function isFlatArray(arr) {
  return utils_default.isArray(arr) && !arr.some(isVisitable);
}
var predicates = utils_default.toFlatObject(utils_default, {}, null, function filter(prop) {
  return /^is[A-Z]/.test(prop);
});
function toFormData(obj, formData, options) {
  if (!utils_default.isObject(obj)) {
    throw new TypeError("target must be an object");
  }
  formData = formData || new (null_default || FormData);
  options = utils_default.toFlatObject(options, {
    metaTokens: true,
    dots: false,
    indexes: false
  }, false, function defined(option, source) {
    return !utils_default.isUndefined(source[option]);
  });
  const metaTokens = options.metaTokens;
  const visitor = options.visitor || defaultVisitor;
  const dots = options.dots;
  const indexes = options.indexes;
  const _Blob = options.Blob || typeof Blob !== "undefined" && Blob;
  const useBlob = _Blob && utils_default.isSpecCompliantForm(formData);
  if (!utils_default.isFunction(visitor)) {
    throw new TypeError("visitor must be a function");
  }
  function convertValue(value) {
    if (value === null)
      return "";
    if (utils_default.isDate(value)) {
      return value.toISOString();
    }
    if (utils_default.isBoolean(value)) {
      return value.toString();
    }
    if (!useBlob && utils_default.isBlob(value)) {
      throw new AxiosError_default("Blob is not supported. Use a Buffer instead.");
    }
    if (utils_default.isArrayBuffer(value) || utils_default.isTypedArray(value)) {
      return useBlob && typeof Blob === "function" ? new Blob([value]) : Buffer.from(value);
    }
    return value;
  }
  function defaultVisitor(value, key, path) {
    let arr = value;
    if (value && !path && typeof value === "object") {
      if (utils_default.endsWith(key, "{}")) {
        key = metaTokens ? key : key.slice(0, -2);
        value = JSON.stringify(value);
      } else if (utils_default.isArray(value) && isFlatArray(value) || (utils_default.isFileList(value) || utils_default.endsWith(key, "[]")) && (arr = utils_default.toArray(value))) {
        key = removeBrackets(key);
        arr.forEach(function each(el, index) {
          !(utils_default.isUndefined(el) || el === null) && formData.append(indexes === true ? renderKey([key], index, dots) : indexes === null ? key : key + "[]", convertValue(el));
        });
        return false;
      }
    }
    if (isVisitable(value)) {
      return true;
    }
    formData.append(renderKey(path, key, dots), convertValue(value));
    return false;
  }
  const stack = [];
  const exposedHelpers = Object.assign(predicates, {
    defaultVisitor,
    convertValue,
    isVisitable
  });
  function build(value, path) {
    if (utils_default.isUndefined(value))
      return;
    if (stack.indexOf(value) !== -1) {
      throw Error("Circular reference detected in " + path.join("."));
    }
    stack.push(value);
    utils_default.forEach(value, function each(el, key) {
      const result = !(utils_default.isUndefined(el) || el === null) && visitor.call(formData, el, utils_default.isString(key) ? key.trim() : key, path, exposedHelpers);
      if (result === true) {
        build(el, path ? path.concat(key) : [key]);
      }
    });
    stack.pop();
  }
  if (!utils_default.isObject(obj)) {
    throw new TypeError("data must be an object");
  }
  build(obj);
  return formData;
}
var toFormData_default = toFormData;

// node_modules/axios/lib/helpers/AxiosURLSearchParams.js
function encode(str) {
  const charMap = {
    "!": "%21",
    "'": "%27",
    "(": "%28",
    ")": "%29",
    "~": "%7E",
    "%20": "+",
    "%00": "\x00"
  };
  return encodeURIComponent(str).replace(/[!'()~]|%20|%00/g, function replacer(match) {
    return charMap[match];
  });
}
function AxiosURLSearchParams(params, options) {
  this._pairs = [];
  params && toFormData_default(params, this, options);
}
var prototype = AxiosURLSearchParams.prototype;
prototype.append = function append(name, value) {
  this._pairs.push([name, value]);
};
prototype.toString = function toString2(encoder) {
  const _encode = encoder ? function(value) {
    return encoder.call(this, value, encode);
  } : encode;
  return this._pairs.map(function each(pair) {
    return _encode(pair[0]) + "=" + _encode(pair[1]);
  }, "").join("&");
};
var AxiosURLSearchParams_default = AxiosURLSearchParams;

// node_modules/axios/lib/helpers/buildURL.js
function encode2(val) {
  return encodeURIComponent(val).replace(/%3A/gi, ":").replace(/%24/g, "$").replace(/%2C/gi, ",").replace(/%20/g, "+");
}
function buildURL(url, params, options) {
  if (!params) {
    return url;
  }
  const _encode = options && options.encode || encode2;
  const _options = utils_default.isFunction(options) ? {
    serialize: options
  } : options;
  const serializeFn = _options && _options.serialize;
  let serializedParams;
  if (serializeFn) {
    serializedParams = serializeFn(params, _options);
  } else {
    serializedParams = utils_default.isURLSearchParams(params) ? params.toString() : new AxiosURLSearchParams_default(params, _options).toString(_encode);
  }
  if (serializedParams) {
    const hashmarkIndex = url.indexOf("#");
    if (hashmarkIndex !== -1) {
      url = url.slice(0, hashmarkIndex);
    }
    url += (url.indexOf("?") === -1 ? "?" : "&") + serializedParams;
  }
  return url;
}

// node_modules/axios/lib/core/InterceptorManager.js
class InterceptorManager {
  constructor() {
    this.handlers = [];
  }
  use(fulfilled, rejected, options) {
    this.handlers.push({
      fulfilled,
      rejected,
      synchronous: options ? options.synchronous : false,
      runWhen: options ? options.runWhen : null
    });
    return this.handlers.length - 1;
  }
  eject(id) {
    if (this.handlers[id]) {
      this.handlers[id] = null;
    }
  }
  clear() {
    if (this.handlers) {
      this.handlers = [];
    }
  }
  forEach(fn) {
    utils_default.forEach(this.handlers, function forEachHandler(h) {
      if (h !== null) {
        fn(h);
      }
    });
  }
}
var InterceptorManager_default = InterceptorManager;

// node_modules/axios/lib/defaults/transitional.js
var transitional_default = {
  silentJSONParsing: true,
  forcedJSONParsing: true,
  clarifyTimeoutError: false,
  legacyInterceptorReqResOrdering: true
};

// node_modules/axios/lib/platform/browser/classes/URLSearchParams.js
var URLSearchParams_default = typeof URLSearchParams !== "undefined" ? URLSearchParams : AxiosURLSearchParams_default;

// node_modules/axios/lib/platform/browser/classes/FormData.js
var FormData_default = typeof FormData !== "undefined" ? FormData : null;

// node_modules/axios/lib/platform/browser/classes/Blob.js
var Blob_default = typeof Blob !== "undefined" ? Blob : null;

// node_modules/axios/lib/platform/browser/index.js
var browser_default = {
  isBrowser: true,
  classes: {
    URLSearchParams: URLSearchParams_default,
    FormData: FormData_default,
    Blob: Blob_default
  },
  protocols: ["http", "https", "file", "blob", "url", "data"]
};

// node_modules/axios/lib/platform/common/utils.js
var exports_utils = {};
__export(exports_utils, {
  origin: () => origin,
  navigator: () => _navigator,
  hasStandardBrowserWebWorkerEnv: () => hasStandardBrowserWebWorkerEnv,
  hasStandardBrowserEnv: () => hasStandardBrowserEnv,
  hasBrowserEnv: () => hasBrowserEnv
});
var hasBrowserEnv = typeof window !== "undefined" && typeof document !== "undefined";
var _navigator = typeof navigator === "object" && navigator || undefined;
var hasStandardBrowserEnv = hasBrowserEnv && (!_navigator || ["ReactNative", "NativeScript", "NS"].indexOf(_navigator.product) < 0);
var hasStandardBrowserWebWorkerEnv = (() => {
  return typeof WorkerGlobalScope !== "undefined" && self instanceof WorkerGlobalScope && typeof self.importScripts === "function";
})();
var origin = hasBrowserEnv && window.location.href || "http://localhost";

// node_modules/axios/lib/platform/index.js
var platform_default = {
  ...exports_utils,
  ...browser_default
};

// node_modules/axios/lib/helpers/toURLEncodedForm.js
function toURLEncodedForm(data, options) {
  return toFormData_default(data, new platform_default.classes.URLSearchParams, {
    visitor: function(value, key, path, helpers) {
      if (platform_default.isNode && utils_default.isBuffer(value)) {
        this.append(key, value.toString("base64"));
        return false;
      }
      return helpers.defaultVisitor.apply(this, arguments);
    },
    ...options
  });
}

// node_modules/axios/lib/helpers/formDataToJSON.js
function parsePropPath(name) {
  return utils_default.matchAll(/\w+|\[(\w*)]/g, name).map((match) => {
    return match[0] === "[]" ? "" : match[1] || match[0];
  });
}
function arrayToObject(arr) {
  const obj = {};
  const keys = Object.keys(arr);
  let i;
  const len = keys.length;
  let key;
  for (i = 0;i < len; i++) {
    key = keys[i];
    obj[key] = arr[key];
  }
  return obj;
}
function formDataToJSON(formData) {
  function buildPath(path, value, target, index) {
    let name = path[index++];
    if (name === "__proto__")
      return true;
    const isNumericKey = Number.isFinite(+name);
    const isLast = index >= path.length;
    name = !name && utils_default.isArray(target) ? target.length : name;
    if (isLast) {
      if (utils_default.hasOwnProp(target, name)) {
        target[name] = [target[name], value];
      } else {
        target[name] = value;
      }
      return !isNumericKey;
    }
    if (!target[name] || !utils_default.isObject(target[name])) {
      target[name] = [];
    }
    const result = buildPath(path, value, target[name], index);
    if (result && utils_default.isArray(target[name])) {
      target[name] = arrayToObject(target[name]);
    }
    return !isNumericKey;
  }
  if (utils_default.isFormData(formData) && utils_default.isFunction(formData.entries)) {
    const obj = {};
    utils_default.forEachEntry(formData, (name, value) => {
      buildPath(parsePropPath(name), value, obj, 0);
    });
    return obj;
  }
  return null;
}
var formDataToJSON_default = formDataToJSON;

// node_modules/axios/lib/defaults/index.js
function stringifySafely(rawValue, parser, encoder) {
  if (utils_default.isString(rawValue)) {
    try {
      (parser || JSON.parse)(rawValue);
      return utils_default.trim(rawValue);
    } catch (e) {
      if (e.name !== "SyntaxError") {
        throw e;
      }
    }
  }
  return (encoder || JSON.stringify)(rawValue);
}
var defaults = {
  transitional: transitional_default,
  adapter: ["xhr", "http", "fetch"],
  transformRequest: [function transformRequest(data, headers) {
    const contentType = headers.getContentType() || "";
    const hasJSONContentType = contentType.indexOf("application/json") > -1;
    const isObjectPayload = utils_default.isObject(data);
    if (isObjectPayload && utils_default.isHTMLForm(data)) {
      data = new FormData(data);
    }
    const isFormData2 = utils_default.isFormData(data);
    if (isFormData2) {
      return hasJSONContentType ? JSON.stringify(formDataToJSON_default(data)) : data;
    }
    if (utils_default.isArrayBuffer(data) || utils_default.isBuffer(data) || utils_default.isStream(data) || utils_default.isFile(data) || utils_default.isBlob(data) || utils_default.isReadableStream(data)) {
      return data;
    }
    if (utils_default.isArrayBufferView(data)) {
      return data.buffer;
    }
    if (utils_default.isURLSearchParams(data)) {
      headers.setContentType("application/x-www-form-urlencoded;charset=utf-8", false);
      return data.toString();
    }
    let isFileList2;
    if (isObjectPayload) {
      if (contentType.indexOf("application/x-www-form-urlencoded") > -1) {
        return toURLEncodedForm(data, this.formSerializer).toString();
      }
      if ((isFileList2 = utils_default.isFileList(data)) || contentType.indexOf("multipart/form-data") > -1) {
        const _FormData = this.env && this.env.FormData;
        return toFormData_default(isFileList2 ? { "files[]": data } : data, _FormData && new _FormData, this.formSerializer);
      }
    }
    if (isObjectPayload || hasJSONContentType) {
      headers.setContentType("application/json", false);
      return stringifySafely(data);
    }
    return data;
  }],
  transformResponse: [function transformResponse(data) {
    const transitional = this.transitional || defaults.transitional;
    const forcedJSONParsing = transitional && transitional.forcedJSONParsing;
    const JSONRequested = this.responseType === "json";
    if (utils_default.isResponse(data) || utils_default.isReadableStream(data)) {
      return data;
    }
    if (data && utils_default.isString(data) && (forcedJSONParsing && !this.responseType || JSONRequested)) {
      const silentJSONParsing = transitional && transitional.silentJSONParsing;
      const strictJSONParsing = !silentJSONParsing && JSONRequested;
      try {
        return JSON.parse(data, this.parseReviver);
      } catch (e) {
        if (strictJSONParsing) {
          if (e.name === "SyntaxError") {
            throw AxiosError_default.from(e, AxiosError_default.ERR_BAD_RESPONSE, this, null, this.response);
          }
          throw e;
        }
      }
    }
    return data;
  }],
  timeout: 0,
  xsrfCookieName: "XSRF-TOKEN",
  xsrfHeaderName: "X-XSRF-TOKEN",
  maxContentLength: -1,
  maxBodyLength: -1,
  env: {
    FormData: platform_default.classes.FormData,
    Blob: platform_default.classes.Blob
  },
  validateStatus: function validateStatus(status) {
    return status >= 200 && status < 300;
  },
  headers: {
    common: {
      Accept: "application/json, text/plain, */*",
      "Content-Type": undefined
    }
  }
};
utils_default.forEach(["delete", "get", "head", "post", "put", "patch"], (method) => {
  defaults.headers[method] = {};
});
var defaults_default = defaults;

// node_modules/axios/lib/helpers/parseHeaders.js
var ignoreDuplicateOf = utils_default.toObjectSet([
  "age",
  "authorization",
  "content-length",
  "content-type",
  "etag",
  "expires",
  "from",
  "host",
  "if-modified-since",
  "if-unmodified-since",
  "last-modified",
  "location",
  "max-forwards",
  "proxy-authorization",
  "referer",
  "retry-after",
  "user-agent"
]);
var parseHeaders_default = (rawHeaders) => {
  const parsed = {};
  let key;
  let val;
  let i;
  rawHeaders && rawHeaders.split(`
`).forEach(function parser(line) {
    i = line.indexOf(":");
    key = line.substring(0, i).trim().toLowerCase();
    val = line.substring(i + 1).trim();
    if (!key || parsed[key] && ignoreDuplicateOf[key]) {
      return;
    }
    if (key === "set-cookie") {
      if (parsed[key]) {
        parsed[key].push(val);
      } else {
        parsed[key] = [val];
      }
    } else {
      parsed[key] = parsed[key] ? parsed[key] + ", " + val : val;
    }
  });
  return parsed;
};

// node_modules/axios/lib/core/AxiosHeaders.js
var $internals = Symbol("internals");
function normalizeHeader(header) {
  return header && String(header).trim().toLowerCase();
}
function normalizeValue(value) {
  if (value === false || value == null) {
    return value;
  }
  return utils_default.isArray(value) ? value.map(normalizeValue) : String(value);
}
function parseTokens(str) {
  const tokens = Object.create(null);
  const tokensRE = /([^\s,;=]+)\s*(?:=\s*([^,;]+))?/g;
  let match;
  while (match = tokensRE.exec(str)) {
    tokens[match[1]] = match[2];
  }
  return tokens;
}
var isValidHeaderName = (str) => /^[-_a-zA-Z0-9^`|~,!#$%&'*+.]+$/.test(str.trim());
function matchHeaderValue(context, value, header, filter2, isHeaderNameFilter) {
  if (utils_default.isFunction(filter2)) {
    return filter2.call(this, value, header);
  }
  if (isHeaderNameFilter) {
    value = header;
  }
  if (!utils_default.isString(value))
    return;
  if (utils_default.isString(filter2)) {
    return value.indexOf(filter2) !== -1;
  }
  if (utils_default.isRegExp(filter2)) {
    return filter2.test(value);
  }
}
function formatHeader(header) {
  return header.trim().toLowerCase().replace(/([a-z\d])(\w*)/g, (w, char, str) => {
    return char.toUpperCase() + str;
  });
}
function buildAccessors(obj, header) {
  const accessorName = utils_default.toCamelCase(" " + header);
  ["get", "set", "has"].forEach((methodName) => {
    Object.defineProperty(obj, methodName + accessorName, {
      value: function(arg1, arg2, arg3) {
        return this[methodName].call(this, header, arg1, arg2, arg3);
      },
      configurable: true
    });
  });
}

class AxiosHeaders {
  constructor(headers) {
    headers && this.set(headers);
  }
  set(header, valueOrRewrite, rewrite) {
    const self2 = this;
    function setHeader(_value, _header, _rewrite) {
      const lHeader = normalizeHeader(_header);
      if (!lHeader) {
        throw new Error("header name must be a non-empty string");
      }
      const key = utils_default.findKey(self2, lHeader);
      if (!key || self2[key] === undefined || _rewrite === true || _rewrite === undefined && self2[key] !== false) {
        self2[key || _header] = normalizeValue(_value);
      }
    }
    const setHeaders = (headers, _rewrite) => utils_default.forEach(headers, (_value, _header) => setHeader(_value, _header, _rewrite));
    if (utils_default.isPlainObject(header) || header instanceof this.constructor) {
      setHeaders(header, valueOrRewrite);
    } else if (utils_default.isString(header) && (header = header.trim()) && !isValidHeaderName(header)) {
      setHeaders(parseHeaders_default(header), valueOrRewrite);
    } else if (utils_default.isObject(header) && utils_default.isIterable(header)) {
      let obj = {}, dest, key;
      for (const entry of header) {
        if (!utils_default.isArray(entry)) {
          throw TypeError("Object iterator must return a key-value pair");
        }
        obj[key = entry[0]] = (dest = obj[key]) ? utils_default.isArray(dest) ? [...dest, entry[1]] : [dest, entry[1]] : entry[1];
      }
      setHeaders(obj, valueOrRewrite);
    } else {
      header != null && setHeader(valueOrRewrite, header, rewrite);
    }
    return this;
  }
  get(header, parser) {
    header = normalizeHeader(header);
    if (header) {
      const key = utils_default.findKey(this, header);
      if (key) {
        const value = this[key];
        if (!parser) {
          return value;
        }
        if (parser === true) {
          return parseTokens(value);
        }
        if (utils_default.isFunction(parser)) {
          return parser.call(this, value, key);
        }
        if (utils_default.isRegExp(parser)) {
          return parser.exec(value);
        }
        throw new TypeError("parser must be boolean|regexp|function");
      }
    }
  }
  has(header, matcher) {
    header = normalizeHeader(header);
    if (header) {
      const key = utils_default.findKey(this, header);
      return !!(key && this[key] !== undefined && (!matcher || matchHeaderValue(this, this[key], key, matcher)));
    }
    return false;
  }
  delete(header, matcher) {
    const self2 = this;
    let deleted = false;
    function deleteHeader(_header) {
      _header = normalizeHeader(_header);
      if (_header) {
        const key = utils_default.findKey(self2, _header);
        if (key && (!matcher || matchHeaderValue(self2, self2[key], key, matcher))) {
          delete self2[key];
          deleted = true;
        }
      }
    }
    if (utils_default.isArray(header)) {
      header.forEach(deleteHeader);
    } else {
      deleteHeader(header);
    }
    return deleted;
  }
  clear(matcher) {
    const keys = Object.keys(this);
    let i = keys.length;
    let deleted = false;
    while (i--) {
      const key = keys[i];
      if (!matcher || matchHeaderValue(this, this[key], key, matcher, true)) {
        delete this[key];
        deleted = true;
      }
    }
    return deleted;
  }
  normalize(format) {
    const self2 = this;
    const headers = {};
    utils_default.forEach(this, (value, header) => {
      const key = utils_default.findKey(headers, header);
      if (key) {
        self2[key] = normalizeValue(value);
        delete self2[header];
        return;
      }
      const normalized = format ? formatHeader(header) : String(header).trim();
      if (normalized !== header) {
        delete self2[header];
      }
      self2[normalized] = normalizeValue(value);
      headers[normalized] = true;
    });
    return this;
  }
  concat(...targets) {
    return this.constructor.concat(this, ...targets);
  }
  toJSON(asStrings) {
    const obj = Object.create(null);
    utils_default.forEach(this, (value, header) => {
      value != null && value !== false && (obj[header] = asStrings && utils_default.isArray(value) ? value.join(", ") : value);
    });
    return obj;
  }
  [Symbol.iterator]() {
    return Object.entries(this.toJSON())[Symbol.iterator]();
  }
  toString() {
    return Object.entries(this.toJSON()).map(([header, value]) => header + ": " + value).join(`
`);
  }
  getSetCookie() {
    return this.get("set-cookie") || [];
  }
  get [Symbol.toStringTag]() {
    return "AxiosHeaders";
  }
  static from(thing) {
    return thing instanceof this ? thing : new this(thing);
  }
  static concat(first, ...targets) {
    const computed = new this(first);
    targets.forEach((target) => computed.set(target));
    return computed;
  }
  static accessor(header) {
    const internals = this[$internals] = this[$internals] = {
      accessors: {}
    };
    const accessors = internals.accessors;
    const prototype2 = this.prototype;
    function defineAccessor(_header) {
      const lHeader = normalizeHeader(_header);
      if (!accessors[lHeader]) {
        buildAccessors(prototype2, _header);
        accessors[lHeader] = true;
      }
    }
    utils_default.isArray(header) ? header.forEach(defineAccessor) : defineAccessor(header);
    return this;
  }
}
AxiosHeaders.accessor(["Content-Type", "Content-Length", "Accept", "Accept-Encoding", "User-Agent", "Authorization"]);
utils_default.reduceDescriptors(AxiosHeaders.prototype, ({ value }, key) => {
  let mapped = key[0].toUpperCase() + key.slice(1);
  return {
    get: () => value,
    set(headerValue) {
      this[mapped] = headerValue;
    }
  };
});
utils_default.freezeMethods(AxiosHeaders);
var AxiosHeaders_default = AxiosHeaders;

// node_modules/axios/lib/core/transformData.js
function transformData(fns, response) {
  const config = this || defaults_default;
  const context = response || config;
  const headers = AxiosHeaders_default.from(context.headers);
  let data = context.data;
  utils_default.forEach(fns, function transform(fn) {
    data = fn.call(config, data, headers.normalize(), response ? response.status : undefined);
  });
  headers.normalize();
  return data;
}

// node_modules/axios/lib/cancel/isCancel.js
function isCancel(value) {
  return !!(value && value.__CANCEL__);
}

// node_modules/axios/lib/cancel/CanceledError.js
class CanceledError extends AxiosError_default {
  constructor(message, config, request) {
    super(message == null ? "canceled" : message, AxiosError_default.ERR_CANCELED, config, request);
    this.name = "CanceledError";
    this.__CANCEL__ = true;
  }
}
var CanceledError_default = CanceledError;

// node_modules/axios/lib/core/settle.js
function settle(resolve, reject, response) {
  const validateStatus2 = response.config.validateStatus;
  if (!response.status || !validateStatus2 || validateStatus2(response.status)) {
    resolve(response);
  } else {
    reject(new AxiosError_default("Request failed with status code " + response.status, [AxiosError_default.ERR_BAD_REQUEST, AxiosError_default.ERR_BAD_RESPONSE][Math.floor(response.status / 100) - 4], response.config, response.request, response));
  }
}

// node_modules/axios/lib/helpers/parseProtocol.js
function parseProtocol(url) {
  const match = /^([-+\w]{1,25})(:?\/\/|:)/.exec(url);
  return match && match[1] || "";
}

// node_modules/axios/lib/helpers/speedometer.js
function speedometer(samplesCount, min) {
  samplesCount = samplesCount || 10;
  const bytes = new Array(samplesCount);
  const timestamps = new Array(samplesCount);
  let head = 0;
  let tail = 0;
  let firstSampleTS;
  min = min !== undefined ? min : 1000;
  return function push(chunkLength) {
    const now = Date.now();
    const startedAt = timestamps[tail];
    if (!firstSampleTS) {
      firstSampleTS = now;
    }
    bytes[head] = chunkLength;
    timestamps[head] = now;
    let i = tail;
    let bytesCount = 0;
    while (i !== head) {
      bytesCount += bytes[i++];
      i = i % samplesCount;
    }
    head = (head + 1) % samplesCount;
    if (head === tail) {
      tail = (tail + 1) % samplesCount;
    }
    if (now - firstSampleTS < min) {
      return;
    }
    const passed = startedAt && now - startedAt;
    return passed ? Math.round(bytesCount * 1000 / passed) : undefined;
  };
}
var speedometer_default = speedometer;

// node_modules/axios/lib/helpers/throttle.js
function throttle(fn, freq) {
  let timestamp = 0;
  let threshold = 1000 / freq;
  let lastArgs;
  let timer;
  const invoke = (args, now = Date.now()) => {
    timestamp = now;
    lastArgs = null;
    if (timer) {
      clearTimeout(timer);
      timer = null;
    }
    fn(...args);
  };
  const throttled = (...args) => {
    const now = Date.now();
    const passed = now - timestamp;
    if (passed >= threshold) {
      invoke(args, now);
    } else {
      lastArgs = args;
      if (!timer) {
        timer = setTimeout(() => {
          timer = null;
          invoke(lastArgs);
        }, threshold - passed);
      }
    }
  };
  const flush = () => lastArgs && invoke(lastArgs);
  return [throttled, flush];
}
var throttle_default = throttle;

// node_modules/axios/lib/helpers/progressEventReducer.js
var progressEventReducer = (listener, isDownloadStream, freq = 3) => {
  let bytesNotified = 0;
  const _speedometer = speedometer_default(50, 250);
  return throttle_default((e) => {
    const loaded = e.loaded;
    const total = e.lengthComputable ? e.total : undefined;
    const progressBytes = loaded - bytesNotified;
    const rate = _speedometer(progressBytes);
    const inRange = loaded <= total;
    bytesNotified = loaded;
    const data = {
      loaded,
      total,
      progress: total ? loaded / total : undefined,
      bytes: progressBytes,
      rate: rate ? rate : undefined,
      estimated: rate && total && inRange ? (total - loaded) / rate : undefined,
      event: e,
      lengthComputable: total != null,
      [isDownloadStream ? "download" : "upload"]: true
    };
    listener(data);
  }, freq);
};
var progressEventDecorator = (total, throttled) => {
  const lengthComputable = total != null;
  return [(loaded) => throttled[0]({
    lengthComputable,
    total,
    loaded
  }), throttled[1]];
};
var asyncDecorator = (fn) => (...args) => utils_default.asap(() => fn(...args));

// node_modules/axios/lib/helpers/isURLSameOrigin.js
var isURLSameOrigin_default = platform_default.hasStandardBrowserEnv ? ((origin2, isMSIE) => (url) => {
  url = new URL(url, platform_default.origin);
  return origin2.protocol === url.protocol && origin2.host === url.host && (isMSIE || origin2.port === url.port);
})(new URL(platform_default.origin), platform_default.navigator && /(msie|trident)/i.test(platform_default.navigator.userAgent)) : () => true;

// node_modules/axios/lib/helpers/cookies.js
var cookies_default = platform_default.hasStandardBrowserEnv ? {
  write(name, value, expires, path, domain, secure, sameSite) {
    if (typeof document === "undefined")
      return;
    const cookie = [`${name}=${encodeURIComponent(value)}`];
    if (utils_default.isNumber(expires)) {
      cookie.push(`expires=${new Date(expires).toUTCString()}`);
    }
    if (utils_default.isString(path)) {
      cookie.push(`path=${path}`);
    }
    if (utils_default.isString(domain)) {
      cookie.push(`domain=${domain}`);
    }
    if (secure === true) {
      cookie.push("secure");
    }
    if (utils_default.isString(sameSite)) {
      cookie.push(`SameSite=${sameSite}`);
    }
    document.cookie = cookie.join("; ");
  },
  read(name) {
    if (typeof document === "undefined")
      return null;
    const match = document.cookie.match(new RegExp("(?:^|; )" + name + "=([^;]*)"));
    return match ? decodeURIComponent(match[1]) : null;
  },
  remove(name) {
    this.write(name, "", Date.now() - 86400000, "/");
  }
} : {
  write() {},
  read() {
    return null;
  },
  remove() {}
};

// node_modules/axios/lib/helpers/isAbsoluteURL.js
function isAbsoluteURL(url) {
  if (typeof url !== "string") {
    return false;
  }
  return /^([a-z][a-z\d+\-.]*:)?\/\//i.test(url);
}

// node_modules/axios/lib/helpers/combineURLs.js
function combineURLs(baseURL, relativeURL) {
  return relativeURL ? baseURL.replace(/\/?\/$/, "") + "/" + relativeURL.replace(/^\/+/, "") : baseURL;
}

// node_modules/axios/lib/core/buildFullPath.js
function buildFullPath(baseURL, requestedURL, allowAbsoluteUrls) {
  let isRelativeUrl = !isAbsoluteURL(requestedURL);
  if (baseURL && (isRelativeUrl || allowAbsoluteUrls == false)) {
    return combineURLs(baseURL, requestedURL);
  }
  return requestedURL;
}

// node_modules/axios/lib/core/mergeConfig.js
var headersToObject = (thing) => thing instanceof AxiosHeaders_default ? { ...thing } : thing;
function mergeConfig(config1, config2) {
  config2 = config2 || {};
  const config = {};
  function getMergedValue(target, source, prop, caseless) {
    if (utils_default.isPlainObject(target) && utils_default.isPlainObject(source)) {
      return utils_default.merge.call({ caseless }, target, source);
    } else if (utils_default.isPlainObject(source)) {
      return utils_default.merge({}, source);
    } else if (utils_default.isArray(source)) {
      return source.slice();
    }
    return source;
  }
  function mergeDeepProperties(a, b, prop, caseless) {
    if (!utils_default.isUndefined(b)) {
      return getMergedValue(a, b, prop, caseless);
    } else if (!utils_default.isUndefined(a)) {
      return getMergedValue(undefined, a, prop, caseless);
    }
  }
  function valueFromConfig2(a, b) {
    if (!utils_default.isUndefined(b)) {
      return getMergedValue(undefined, b);
    }
  }
  function defaultToConfig2(a, b) {
    if (!utils_default.isUndefined(b)) {
      return getMergedValue(undefined, b);
    } else if (!utils_default.isUndefined(a)) {
      return getMergedValue(undefined, a);
    }
  }
  function mergeDirectKeys(a, b, prop) {
    if (prop in config2) {
      return getMergedValue(a, b);
    } else if (prop in config1) {
      return getMergedValue(undefined, a);
    }
  }
  const mergeMap = {
    url: valueFromConfig2,
    method: valueFromConfig2,
    data: valueFromConfig2,
    baseURL: defaultToConfig2,
    transformRequest: defaultToConfig2,
    transformResponse: defaultToConfig2,
    paramsSerializer: defaultToConfig2,
    timeout: defaultToConfig2,
    timeoutMessage: defaultToConfig2,
    withCredentials: defaultToConfig2,
    withXSRFToken: defaultToConfig2,
    adapter: defaultToConfig2,
    responseType: defaultToConfig2,
    xsrfCookieName: defaultToConfig2,
    xsrfHeaderName: defaultToConfig2,
    onUploadProgress: defaultToConfig2,
    onDownloadProgress: defaultToConfig2,
    decompress: defaultToConfig2,
    maxContentLength: defaultToConfig2,
    maxBodyLength: defaultToConfig2,
    beforeRedirect: defaultToConfig2,
    transport: defaultToConfig2,
    httpAgent: defaultToConfig2,
    httpsAgent: defaultToConfig2,
    cancelToken: defaultToConfig2,
    socketPath: defaultToConfig2,
    responseEncoding: defaultToConfig2,
    validateStatus: mergeDirectKeys,
    headers: (a, b, prop) => mergeDeepProperties(headersToObject(a), headersToObject(b), prop, true)
  };
  utils_default.forEach(Object.keys({ ...config1, ...config2 }), function computeConfigValue(prop) {
    if (prop === "__proto__" || prop === "constructor" || prop === "prototype")
      return;
    const merge2 = utils_default.hasOwnProp(mergeMap, prop) ? mergeMap[prop] : mergeDeepProperties;
    const configValue = merge2(config1[prop], config2[prop], prop);
    utils_default.isUndefined(configValue) && merge2 !== mergeDirectKeys || (config[prop] = configValue);
  });
  return config;
}

// node_modules/axios/lib/helpers/resolveConfig.js
var resolveConfig_default = (config) => {
  const newConfig = mergeConfig({}, config);
  let { data, withXSRFToken, xsrfHeaderName, xsrfCookieName, headers, auth } = newConfig;
  newConfig.headers = headers = AxiosHeaders_default.from(headers);
  newConfig.url = buildURL(buildFullPath(newConfig.baseURL, newConfig.url, newConfig.allowAbsoluteUrls), config.params, config.paramsSerializer);
  if (auth) {
    headers.set("Authorization", "Basic " + btoa((auth.username || "") + ":" + (auth.password ? unescape(encodeURIComponent(auth.password)) : "")));
  }
  if (utils_default.isFormData(data)) {
    if (platform_default.hasStandardBrowserEnv || platform_default.hasStandardBrowserWebWorkerEnv) {
      headers.setContentType(undefined);
    } else if (utils_default.isFunction(data.getHeaders)) {
      const formHeaders = data.getHeaders();
      const allowedHeaders = ["content-type", "content-length"];
      Object.entries(formHeaders).forEach(([key, val]) => {
        if (allowedHeaders.includes(key.toLowerCase())) {
          headers.set(key, val);
        }
      });
    }
  }
  if (platform_default.hasStandardBrowserEnv) {
    withXSRFToken && utils_default.isFunction(withXSRFToken) && (withXSRFToken = withXSRFToken(newConfig));
    if (withXSRFToken || withXSRFToken !== false && isURLSameOrigin_default(newConfig.url)) {
      const xsrfValue = xsrfHeaderName && xsrfCookieName && cookies_default.read(xsrfCookieName);
      if (xsrfValue) {
        headers.set(xsrfHeaderName, xsrfValue);
      }
    }
  }
  return newConfig;
};

// node_modules/axios/lib/adapters/xhr.js
var isXHRAdapterSupported = typeof XMLHttpRequest !== "undefined";
var xhr_default = isXHRAdapterSupported && function(config) {
  return new Promise(function dispatchXhrRequest(resolve, reject) {
    const _config = resolveConfig_default(config);
    let requestData = _config.data;
    const requestHeaders = AxiosHeaders_default.from(_config.headers).normalize();
    let { responseType, onUploadProgress, onDownloadProgress } = _config;
    let onCanceled;
    let uploadThrottled, downloadThrottled;
    let flushUpload, flushDownload;
    function done() {
      flushUpload && flushUpload();
      flushDownload && flushDownload();
      _config.cancelToken && _config.cancelToken.unsubscribe(onCanceled);
      _config.signal && _config.signal.removeEventListener("abort", onCanceled);
    }
    let request = new XMLHttpRequest;
    request.open(_config.method.toUpperCase(), _config.url, true);
    request.timeout = _config.timeout;
    function onloadend() {
      if (!request) {
        return;
      }
      const responseHeaders = AxiosHeaders_default.from("getAllResponseHeaders" in request && request.getAllResponseHeaders());
      const responseData = !responseType || responseType === "text" || responseType === "json" ? request.responseText : request.response;
      const response = {
        data: responseData,
        status: request.status,
        statusText: request.statusText,
        headers: responseHeaders,
        config,
        request
      };
      settle(function _resolve(value) {
        resolve(value);
        done();
      }, function _reject(err) {
        reject(err);
        done();
      }, response);
      request = null;
    }
    if ("onloadend" in request) {
      request.onloadend = onloadend;
    } else {
      request.onreadystatechange = function handleLoad() {
        if (!request || request.readyState !== 4) {
          return;
        }
        if (request.status === 0 && !(request.responseURL && request.responseURL.indexOf("file:") === 0)) {
          return;
        }
        setTimeout(onloadend);
      };
    }
    request.onabort = function handleAbort() {
      if (!request) {
        return;
      }
      reject(new AxiosError_default("Request aborted", AxiosError_default.ECONNABORTED, config, request));
      request = null;
    };
    request.onerror = function handleError(event) {
      const msg = event && event.message ? event.message : "Network Error";
      const err = new AxiosError_default(msg, AxiosError_default.ERR_NETWORK, config, request);
      err.event = event || null;
      reject(err);
      request = null;
    };
    request.ontimeout = function handleTimeout() {
      let timeoutErrorMessage = _config.timeout ? "timeout of " + _config.timeout + "ms exceeded" : "timeout exceeded";
      const transitional = _config.transitional || transitional_default;
      if (_config.timeoutErrorMessage) {
        timeoutErrorMessage = _config.timeoutErrorMessage;
      }
      reject(new AxiosError_default(timeoutErrorMessage, transitional.clarifyTimeoutError ? AxiosError_default.ETIMEDOUT : AxiosError_default.ECONNABORTED, config, request));
      request = null;
    };
    requestData === undefined && requestHeaders.setContentType(null);
    if ("setRequestHeader" in request) {
      utils_default.forEach(requestHeaders.toJSON(), function setRequestHeader(val, key) {
        request.setRequestHeader(key, val);
      });
    }
    if (!utils_default.isUndefined(_config.withCredentials)) {
      request.withCredentials = !!_config.withCredentials;
    }
    if (responseType && responseType !== "json") {
      request.responseType = _config.responseType;
    }
    if (onDownloadProgress) {
      [downloadThrottled, flushDownload] = progressEventReducer(onDownloadProgress, true);
      request.addEventListener("progress", downloadThrottled);
    }
    if (onUploadProgress && request.upload) {
      [uploadThrottled, flushUpload] = progressEventReducer(onUploadProgress);
      request.upload.addEventListener("progress", uploadThrottled);
      request.upload.addEventListener("loadend", flushUpload);
    }
    if (_config.cancelToken || _config.signal) {
      onCanceled = (cancel) => {
        if (!request) {
          return;
        }
        reject(!cancel || cancel.type ? new CanceledError_default(null, config, request) : cancel);
        request.abort();
        request = null;
      };
      _config.cancelToken && _config.cancelToken.subscribe(onCanceled);
      if (_config.signal) {
        _config.signal.aborted ? onCanceled() : _config.signal.addEventListener("abort", onCanceled);
      }
    }
    const protocol = parseProtocol(_config.url);
    if (protocol && platform_default.protocols.indexOf(protocol) === -1) {
      reject(new AxiosError_default("Unsupported protocol " + protocol + ":", AxiosError_default.ERR_BAD_REQUEST, config));
      return;
    }
    request.send(requestData || null);
  });
};

// node_modules/axios/lib/helpers/composeSignals.js
var composeSignals = (signals, timeout) => {
  const { length } = signals = signals ? signals.filter(Boolean) : [];
  if (timeout || length) {
    let controller = new AbortController;
    let aborted;
    const onabort = function(reason) {
      if (!aborted) {
        aborted = true;
        unsubscribe();
        const err = reason instanceof Error ? reason : this.reason;
        controller.abort(err instanceof AxiosError_default ? err : new CanceledError_default(err instanceof Error ? err.message : err));
      }
    };
    let timer = timeout && setTimeout(() => {
      timer = null;
      onabort(new AxiosError_default(`timeout of ${timeout}ms exceeded`, AxiosError_default.ETIMEDOUT));
    }, timeout);
    const unsubscribe = () => {
      if (signals) {
        timer && clearTimeout(timer);
        timer = null;
        signals.forEach((signal2) => {
          signal2.unsubscribe ? signal2.unsubscribe(onabort) : signal2.removeEventListener("abort", onabort);
        });
        signals = null;
      }
    };
    signals.forEach((signal2) => signal2.addEventListener("abort", onabort));
    const { signal } = controller;
    signal.unsubscribe = () => utils_default.asap(unsubscribe);
    return signal;
  }
};
var composeSignals_default = composeSignals;

// node_modules/axios/lib/helpers/trackStream.js
var streamChunk = function* (chunk, chunkSize) {
  let len = chunk.byteLength;
  if (!chunkSize || len < chunkSize) {
    yield chunk;
    return;
  }
  let pos = 0;
  let end;
  while (pos < len) {
    end = pos + chunkSize;
    yield chunk.slice(pos, end);
    pos = end;
  }
};
var readBytes = async function* (iterable, chunkSize) {
  for await (const chunk of readStream(iterable)) {
    yield* streamChunk(chunk, chunkSize);
  }
};
var readStream = async function* (stream) {
  if (stream[Symbol.asyncIterator]) {
    yield* stream;
    return;
  }
  const reader = stream.getReader();
  try {
    for (;; ) {
      const { done, value } = await reader.read();
      if (done) {
        break;
      }
      yield value;
    }
  } finally {
    await reader.cancel();
  }
};
var trackStream = (stream, chunkSize, onProgress, onFinish) => {
  const iterator2 = readBytes(stream, chunkSize);
  let bytes = 0;
  let done;
  let _onFinish = (e) => {
    if (!done) {
      done = true;
      onFinish && onFinish(e);
    }
  };
  return new ReadableStream({
    async pull(controller) {
      try {
        const { done: done2, value } = await iterator2.next();
        if (done2) {
          _onFinish();
          controller.close();
          return;
        }
        let len = value.byteLength;
        if (onProgress) {
          let loadedBytes = bytes += len;
          onProgress(loadedBytes);
        }
        controller.enqueue(new Uint8Array(value));
      } catch (err) {
        _onFinish(err);
        throw err;
      }
    },
    cancel(reason) {
      _onFinish(reason);
      return iterator2.return();
    }
  }, {
    highWaterMark: 2
  });
};

// node_modules/axios/lib/adapters/fetch.js
var DEFAULT_CHUNK_SIZE = 64 * 1024;
var { isFunction: isFunction2 } = utils_default;
var globalFetchAPI = (({ Request, Response }) => ({
  Request,
  Response
}))(utils_default.global);
var {
  ReadableStream: ReadableStream2,
  TextEncoder: TextEncoder2
} = utils_default.global;
var test = (fn, ...args) => {
  try {
    return !!fn(...args);
  } catch (e) {
    return false;
  }
};
var factory = (env) => {
  env = utils_default.merge.call({
    skipUndefined: true
  }, globalFetchAPI, env);
  const { fetch: envFetch, Request, Response } = env;
  const isFetchSupported = envFetch ? isFunction2(envFetch) : typeof fetch === "function";
  const isRequestSupported = isFunction2(Request);
  const isResponseSupported = isFunction2(Response);
  if (!isFetchSupported) {
    return false;
  }
  const isReadableStreamSupported = isFetchSupported && isFunction2(ReadableStream2);
  const encodeText = isFetchSupported && (typeof TextEncoder2 === "function" ? ((encoder) => (str) => encoder.encode(str))(new TextEncoder2) : async (str) => new Uint8Array(await new Request(str).arrayBuffer()));
  const supportsRequestStream = isRequestSupported && isReadableStreamSupported && test(() => {
    let duplexAccessed = false;
    const hasContentType = new Request(platform_default.origin, {
      body: new ReadableStream2,
      method: "POST",
      get duplex() {
        duplexAccessed = true;
        return "half";
      }
    }).headers.has("Content-Type");
    return duplexAccessed && !hasContentType;
  });
  const supportsResponseStream = isResponseSupported && isReadableStreamSupported && test(() => utils_default.isReadableStream(new Response("").body));
  const resolvers = {
    stream: supportsResponseStream && ((res) => res.body)
  };
  isFetchSupported && (() => {
    ["text", "arrayBuffer", "blob", "formData", "stream"].forEach((type) => {
      !resolvers[type] && (resolvers[type] = (res, config) => {
        let method = res && res[type];
        if (method) {
          return method.call(res);
        }
        throw new AxiosError_default(`Response type '${type}' is not supported`, AxiosError_default.ERR_NOT_SUPPORT, config);
      });
    });
  })();
  const getBodyLength = async (body) => {
    if (body == null) {
      return 0;
    }
    if (utils_default.isBlob(body)) {
      return body.size;
    }
    if (utils_default.isSpecCompliantForm(body)) {
      const _request = new Request(platform_default.origin, {
        method: "POST",
        body
      });
      return (await _request.arrayBuffer()).byteLength;
    }
    if (utils_default.isArrayBufferView(body) || utils_default.isArrayBuffer(body)) {
      return body.byteLength;
    }
    if (utils_default.isURLSearchParams(body)) {
      body = body + "";
    }
    if (utils_default.isString(body)) {
      return (await encodeText(body)).byteLength;
    }
  };
  const resolveBodyLength = async (headers, body) => {
    const length = utils_default.toFiniteNumber(headers.getContentLength());
    return length == null ? getBodyLength(body) : length;
  };
  return async (config) => {
    let {
      url,
      method,
      data,
      signal,
      cancelToken,
      timeout,
      onDownloadProgress,
      onUploadProgress,
      responseType,
      headers,
      withCredentials = "same-origin",
      fetchOptions
    } = resolveConfig_default(config);
    let _fetch = envFetch || fetch;
    responseType = responseType ? (responseType + "").toLowerCase() : "text";
    let composedSignal = composeSignals_default([signal, cancelToken && cancelToken.toAbortSignal()], timeout);
    let request = null;
    const unsubscribe = composedSignal && composedSignal.unsubscribe && (() => {
      composedSignal.unsubscribe();
    });
    let requestContentLength;
    try {
      if (onUploadProgress && supportsRequestStream && method !== "get" && method !== "head" && (requestContentLength = await resolveBodyLength(headers, data)) !== 0) {
        let _request = new Request(url, {
          method: "POST",
          body: data,
          duplex: "half"
        });
        let contentTypeHeader;
        if (utils_default.isFormData(data) && (contentTypeHeader = _request.headers.get("content-type"))) {
          headers.setContentType(contentTypeHeader);
        }
        if (_request.body) {
          const [onProgress, flush] = progressEventDecorator(requestContentLength, progressEventReducer(asyncDecorator(onUploadProgress)));
          data = trackStream(_request.body, DEFAULT_CHUNK_SIZE, onProgress, flush);
        }
      }
      if (!utils_default.isString(withCredentials)) {
        withCredentials = withCredentials ? "include" : "omit";
      }
      const isCredentialsSupported = isRequestSupported && "credentials" in Request.prototype;
      const resolvedOptions = {
        ...fetchOptions,
        signal: composedSignal,
        method: method.toUpperCase(),
        headers: headers.normalize().toJSON(),
        body: data,
        duplex: "half",
        credentials: isCredentialsSupported ? withCredentials : undefined
      };
      request = isRequestSupported && new Request(url, resolvedOptions);
      let response = await (isRequestSupported ? _fetch(request, fetchOptions) : _fetch(url, resolvedOptions));
      const isStreamResponse = supportsResponseStream && (responseType === "stream" || responseType === "response");
      if (supportsResponseStream && (onDownloadProgress || isStreamResponse && unsubscribe)) {
        const options = {};
        ["status", "statusText", "headers"].forEach((prop) => {
          options[prop] = response[prop];
        });
        const responseContentLength = utils_default.toFiniteNumber(response.headers.get("content-length"));
        const [onProgress, flush] = onDownloadProgress && progressEventDecorator(responseContentLength, progressEventReducer(asyncDecorator(onDownloadProgress), true)) || [];
        response = new Response(trackStream(response.body, DEFAULT_CHUNK_SIZE, onProgress, () => {
          flush && flush();
          unsubscribe && unsubscribe();
        }), options);
      }
      responseType = responseType || "text";
      let responseData = await resolvers[utils_default.findKey(resolvers, responseType) || "text"](response, config);
      !isStreamResponse && unsubscribe && unsubscribe();
      return await new Promise((resolve, reject) => {
        settle(resolve, reject, {
          data: responseData,
          headers: AxiosHeaders_default.from(response.headers),
          status: response.status,
          statusText: response.statusText,
          config,
          request
        });
      });
    } catch (err) {
      unsubscribe && unsubscribe();
      if (err && err.name === "TypeError" && /Load failed|fetch/i.test(err.message)) {
        throw Object.assign(new AxiosError_default("Network Error", AxiosError_default.ERR_NETWORK, config, request, err && err.response), {
          cause: err.cause || err
        });
      }
      throw AxiosError_default.from(err, err && err.code, config, request, err && err.response);
    }
  };
};
var seedCache = new Map;
var getFetch = (config) => {
  let env = config && config.env || {};
  const { fetch: fetch2, Request, Response } = env;
  const seeds = [
    Request,
    Response,
    fetch2
  ];
  let len = seeds.length, i = len, seed, target, map = seedCache;
  while (i--) {
    seed = seeds[i];
    target = map.get(seed);
    target === undefined && map.set(seed, target = i ? new Map : factory(env));
    map = target;
  }
  return target;
};
var adapter = getFetch();

// node_modules/axios/lib/adapters/adapters.js
var knownAdapters = {
  http: null_default,
  xhr: xhr_default,
  fetch: {
    get: getFetch
  }
};
utils_default.forEach(knownAdapters, (fn, value) => {
  if (fn) {
    try {
      Object.defineProperty(fn, "name", { value });
    } catch (e) {}
    Object.defineProperty(fn, "adapterName", { value });
  }
});
var renderReason = (reason) => `- ${reason}`;
var isResolvedHandle = (adapter2) => utils_default.isFunction(adapter2) || adapter2 === null || adapter2 === false;
function getAdapter(adapters, config) {
  adapters = utils_default.isArray(adapters) ? adapters : [adapters];
  const { length } = adapters;
  let nameOrAdapter;
  let adapter2;
  const rejectedReasons = {};
  for (let i = 0;i < length; i++) {
    nameOrAdapter = adapters[i];
    let id;
    adapter2 = nameOrAdapter;
    if (!isResolvedHandle(nameOrAdapter)) {
      adapter2 = knownAdapters[(id = String(nameOrAdapter)).toLowerCase()];
      if (adapter2 === undefined) {
        throw new AxiosError_default(`Unknown adapter '${id}'`);
      }
    }
    if (adapter2 && (utils_default.isFunction(adapter2) || (adapter2 = adapter2.get(config)))) {
      break;
    }
    rejectedReasons[id || "#" + i] = adapter2;
  }
  if (!adapter2) {
    const reasons = Object.entries(rejectedReasons).map(([id, state]) => `adapter ${id} ` + (state === false ? "is not supported by the environment" : "is not available in the build"));
    let s = length ? reasons.length > 1 ? `since :
` + reasons.map(renderReason).join(`
`) : " " + renderReason(reasons[0]) : "as no adapter specified";
    throw new AxiosError_default(`There is no suitable adapter to dispatch the request ` + s, "ERR_NOT_SUPPORT");
  }
  return adapter2;
}
var adapters_default = {
  getAdapter,
  adapters: knownAdapters
};

// node_modules/axios/lib/core/dispatchRequest.js
function throwIfCancellationRequested(config) {
  if (config.cancelToken) {
    config.cancelToken.throwIfRequested();
  }
  if (config.signal && config.signal.aborted) {
    throw new CanceledError_default(null, config);
  }
}
function dispatchRequest(config) {
  throwIfCancellationRequested(config);
  config.headers = AxiosHeaders_default.from(config.headers);
  config.data = transformData.call(config, config.transformRequest);
  if (["post", "put", "patch"].indexOf(config.method) !== -1) {
    config.headers.setContentType("application/x-www-form-urlencoded", false);
  }
  const adapter2 = adapters_default.getAdapter(config.adapter || defaults_default.adapter, config);
  return adapter2(config).then(function onAdapterResolution(response) {
    throwIfCancellationRequested(config);
    response.data = transformData.call(config, config.transformResponse, response);
    response.headers = AxiosHeaders_default.from(response.headers);
    return response;
  }, function onAdapterRejection(reason) {
    if (!isCancel(reason)) {
      throwIfCancellationRequested(config);
      if (reason && reason.response) {
        reason.response.data = transformData.call(config, config.transformResponse, reason.response);
        reason.response.headers = AxiosHeaders_default.from(reason.response.headers);
      }
    }
    return Promise.reject(reason);
  });
}

// node_modules/axios/lib/env/data.js
var VERSION = "1.13.5";

// node_modules/axios/lib/helpers/validator.js
var validators = {};
["object", "boolean", "number", "function", "string", "symbol"].forEach((type, i) => {
  validators[type] = function validator(thing) {
    return typeof thing === type || "a" + (i < 1 ? "n " : " ") + type;
  };
});
var deprecatedWarnings = {};
validators.transitional = function transitional(validator, version, message) {
  function formatMessage(opt, desc) {
    return "[Axios v" + VERSION + "] Transitional option '" + opt + "'" + desc + (message ? ". " + message : "");
  }
  return (value, opt, opts) => {
    if (validator === false) {
      throw new AxiosError_default(formatMessage(opt, " has been removed" + (version ? " in " + version : "")), AxiosError_default.ERR_DEPRECATED);
    }
    if (version && !deprecatedWarnings[opt]) {
      deprecatedWarnings[opt] = true;
      console.warn(formatMessage(opt, " has been deprecated since v" + version + " and will be removed in the near future"));
    }
    return validator ? validator(value, opt, opts) : true;
  };
};
validators.spelling = function spelling(correctSpelling) {
  return (value, opt) => {
    console.warn(`${opt} is likely a misspelling of ${correctSpelling}`);
    return true;
  };
};
function assertOptions(options, schema, allowUnknown) {
  if (typeof options !== "object") {
    throw new AxiosError_default("options must be an object", AxiosError_default.ERR_BAD_OPTION_VALUE);
  }
  const keys = Object.keys(options);
  let i = keys.length;
  while (i-- > 0) {
    const opt = keys[i];
    const validator = schema[opt];
    if (validator) {
      const value = options[opt];
      const result = value === undefined || validator(value, opt, options);
      if (result !== true) {
        throw new AxiosError_default("option " + opt + " must be " + result, AxiosError_default.ERR_BAD_OPTION_VALUE);
      }
      continue;
    }
    if (allowUnknown !== true) {
      throw new AxiosError_default("Unknown option " + opt, AxiosError_default.ERR_BAD_OPTION);
    }
  }
}
var validator_default = {
  assertOptions,
  validators
};

// node_modules/axios/lib/core/Axios.js
var validators2 = validator_default.validators;

class Axios {
  constructor(instanceConfig) {
    this.defaults = instanceConfig || {};
    this.interceptors = {
      request: new InterceptorManager_default,
      response: new InterceptorManager_default
    };
  }
  async request(configOrUrl, config) {
    try {
      return await this._request(configOrUrl, config);
    } catch (err) {
      if (err instanceof Error) {
        let dummy = {};
        Error.captureStackTrace ? Error.captureStackTrace(dummy) : dummy = new Error;
        const stack = dummy.stack ? dummy.stack.replace(/^.+\n/, "") : "";
        try {
          if (!err.stack) {
            err.stack = stack;
          } else if (stack && !String(err.stack).endsWith(stack.replace(/^.+\n.+\n/, ""))) {
            err.stack += `
` + stack;
          }
        } catch (e) {}
      }
      throw err;
    }
  }
  _request(configOrUrl, config) {
    if (typeof configOrUrl === "string") {
      config = config || {};
      config.url = configOrUrl;
    } else {
      config = configOrUrl || {};
    }
    config = mergeConfig(this.defaults, config);
    const { transitional: transitional2, paramsSerializer, headers } = config;
    if (transitional2 !== undefined) {
      validator_default.assertOptions(transitional2, {
        silentJSONParsing: validators2.transitional(validators2.boolean),
        forcedJSONParsing: validators2.transitional(validators2.boolean),
        clarifyTimeoutError: validators2.transitional(validators2.boolean),
        legacyInterceptorReqResOrdering: validators2.transitional(validators2.boolean)
      }, false);
    }
    if (paramsSerializer != null) {
      if (utils_default.isFunction(paramsSerializer)) {
        config.paramsSerializer = {
          serialize: paramsSerializer
        };
      } else {
        validator_default.assertOptions(paramsSerializer, {
          encode: validators2.function,
          serialize: validators2.function
        }, true);
      }
    }
    if (config.allowAbsoluteUrls !== undefined) {} else if (this.defaults.allowAbsoluteUrls !== undefined) {
      config.allowAbsoluteUrls = this.defaults.allowAbsoluteUrls;
    } else {
      config.allowAbsoluteUrls = true;
    }
    validator_default.assertOptions(config, {
      baseUrl: validators2.spelling("baseURL"),
      withXsrfToken: validators2.spelling("withXSRFToken")
    }, true);
    config.method = (config.method || this.defaults.method || "get").toLowerCase();
    let contextHeaders = headers && utils_default.merge(headers.common, headers[config.method]);
    headers && utils_default.forEach(["delete", "get", "head", "post", "put", "patch", "common"], (method) => {
      delete headers[method];
    });
    config.headers = AxiosHeaders_default.concat(contextHeaders, headers);
    const requestInterceptorChain = [];
    let synchronousRequestInterceptors = true;
    this.interceptors.request.forEach(function unshiftRequestInterceptors(interceptor) {
      if (typeof interceptor.runWhen === "function" && interceptor.runWhen(config) === false) {
        return;
      }
      synchronousRequestInterceptors = synchronousRequestInterceptors && interceptor.synchronous;
      const transitional3 = config.transitional || transitional_default;
      const legacyInterceptorReqResOrdering = transitional3 && transitional3.legacyInterceptorReqResOrdering;
      if (legacyInterceptorReqResOrdering) {
        requestInterceptorChain.unshift(interceptor.fulfilled, interceptor.rejected);
      } else {
        requestInterceptorChain.push(interceptor.fulfilled, interceptor.rejected);
      }
    });
    const responseInterceptorChain = [];
    this.interceptors.response.forEach(function pushResponseInterceptors(interceptor) {
      responseInterceptorChain.push(interceptor.fulfilled, interceptor.rejected);
    });
    let promise;
    let i = 0;
    let len;
    if (!synchronousRequestInterceptors) {
      const chain = [dispatchRequest.bind(this), undefined];
      chain.unshift(...requestInterceptorChain);
      chain.push(...responseInterceptorChain);
      len = chain.length;
      promise = Promise.resolve(config);
      while (i < len) {
        promise = promise.then(chain[i++], chain[i++]);
      }
      return promise;
    }
    len = requestInterceptorChain.length;
    let newConfig = config;
    while (i < len) {
      const onFulfilled = requestInterceptorChain[i++];
      const onRejected = requestInterceptorChain[i++];
      try {
        newConfig = onFulfilled(newConfig);
      } catch (error) {
        onRejected.call(this, error);
        break;
      }
    }
    try {
      promise = dispatchRequest.call(this, newConfig);
    } catch (error) {
      return Promise.reject(error);
    }
    i = 0;
    len = responseInterceptorChain.length;
    while (i < len) {
      promise = promise.then(responseInterceptorChain[i++], responseInterceptorChain[i++]);
    }
    return promise;
  }
  getUri(config) {
    config = mergeConfig(this.defaults, config);
    const fullPath = buildFullPath(config.baseURL, config.url, config.allowAbsoluteUrls);
    return buildURL(fullPath, config.params, config.paramsSerializer);
  }
}
utils_default.forEach(["delete", "get", "head", "options"], function forEachMethodNoData(method) {
  Axios.prototype[method] = function(url, config) {
    return this.request(mergeConfig(config || {}, {
      method,
      url,
      data: (config || {}).data
    }));
  };
});
utils_default.forEach(["post", "put", "patch"], function forEachMethodWithData(method) {
  function generateHTTPMethod(isForm) {
    return function httpMethod(url, data, config) {
      return this.request(mergeConfig(config || {}, {
        method,
        headers: isForm ? {
          "Content-Type": "multipart/form-data"
        } : {},
        url,
        data
      }));
    };
  }
  Axios.prototype[method] = generateHTTPMethod();
  Axios.prototype[method + "Form"] = generateHTTPMethod(true);
});
var Axios_default = Axios;

// node_modules/axios/lib/cancel/CancelToken.js
class CancelToken {
  constructor(executor) {
    if (typeof executor !== "function") {
      throw new TypeError("executor must be a function.");
    }
    let resolvePromise;
    this.promise = new Promise(function promiseExecutor(resolve) {
      resolvePromise = resolve;
    });
    const token = this;
    this.promise.then((cancel) => {
      if (!token._listeners)
        return;
      let i = token._listeners.length;
      while (i-- > 0) {
        token._listeners[i](cancel);
      }
      token._listeners = null;
    });
    this.promise.then = (onfulfilled) => {
      let _resolve;
      const promise = new Promise((resolve) => {
        token.subscribe(resolve);
        _resolve = resolve;
      }).then(onfulfilled);
      promise.cancel = function reject() {
        token.unsubscribe(_resolve);
      };
      return promise;
    };
    executor(function cancel(message, config, request) {
      if (token.reason) {
        return;
      }
      token.reason = new CanceledError_default(message, config, request);
      resolvePromise(token.reason);
    });
  }
  throwIfRequested() {
    if (this.reason) {
      throw this.reason;
    }
  }
  subscribe(listener) {
    if (this.reason) {
      listener(this.reason);
      return;
    }
    if (this._listeners) {
      this._listeners.push(listener);
    } else {
      this._listeners = [listener];
    }
  }
  unsubscribe(listener) {
    if (!this._listeners) {
      return;
    }
    const index = this._listeners.indexOf(listener);
    if (index !== -1) {
      this._listeners.splice(index, 1);
    }
  }
  toAbortSignal() {
    const controller = new AbortController;
    const abort = (err) => {
      controller.abort(err);
    };
    this.subscribe(abort);
    controller.signal.unsubscribe = () => this.unsubscribe(abort);
    return controller.signal;
  }
  static source() {
    let cancel;
    const token = new CancelToken(function executor(c) {
      cancel = c;
    });
    return {
      token,
      cancel
    };
  }
}
var CancelToken_default = CancelToken;

// node_modules/axios/lib/helpers/spread.js
function spread(callback) {
  return function wrap(arr) {
    return callback.apply(null, arr);
  };
}

// node_modules/axios/lib/helpers/isAxiosError.js
function isAxiosError(payload) {
  return utils_default.isObject(payload) && payload.isAxiosError === true;
}

// node_modules/axios/lib/helpers/HttpStatusCode.js
var HttpStatusCode = {
  Continue: 100,
  SwitchingProtocols: 101,
  Processing: 102,
  EarlyHints: 103,
  Ok: 200,
  Created: 201,
  Accepted: 202,
  NonAuthoritativeInformation: 203,
  NoContent: 204,
  ResetContent: 205,
  PartialContent: 206,
  MultiStatus: 207,
  AlreadyReported: 208,
  ImUsed: 226,
  MultipleChoices: 300,
  MovedPermanently: 301,
  Found: 302,
  SeeOther: 303,
  NotModified: 304,
  UseProxy: 305,
  Unused: 306,
  TemporaryRedirect: 307,
  PermanentRedirect: 308,
  BadRequest: 400,
  Unauthorized: 401,
  PaymentRequired: 402,
  Forbidden: 403,
  NotFound: 404,
  MethodNotAllowed: 405,
  NotAcceptable: 406,
  ProxyAuthenticationRequired: 407,
  RequestTimeout: 408,
  Conflict: 409,
  Gone: 410,
  LengthRequired: 411,
  PreconditionFailed: 412,
  PayloadTooLarge: 413,
  UriTooLong: 414,
  UnsupportedMediaType: 415,
  RangeNotSatisfiable: 416,
  ExpectationFailed: 417,
  ImATeapot: 418,
  MisdirectedRequest: 421,
  UnprocessableEntity: 422,
  Locked: 423,
  FailedDependency: 424,
  TooEarly: 425,
  UpgradeRequired: 426,
  PreconditionRequired: 428,
  TooManyRequests: 429,
  RequestHeaderFieldsTooLarge: 431,
  UnavailableForLegalReasons: 451,
  InternalServerError: 500,
  NotImplemented: 501,
  BadGateway: 502,
  ServiceUnavailable: 503,
  GatewayTimeout: 504,
  HttpVersionNotSupported: 505,
  VariantAlsoNegotiates: 506,
  InsufficientStorage: 507,
  LoopDetected: 508,
  NotExtended: 510,
  NetworkAuthenticationRequired: 511,
  WebServerIsDown: 521,
  ConnectionTimedOut: 522,
  OriginIsUnreachable: 523,
  TimeoutOccurred: 524,
  SslHandshakeFailed: 525,
  InvalidSslCertificate: 526
};
Object.entries(HttpStatusCode).forEach(([key, value]) => {
  HttpStatusCode[value] = key;
});
var HttpStatusCode_default = HttpStatusCode;

// node_modules/axios/lib/axios.js
function createInstance(defaultConfig) {
  const context = new Axios_default(defaultConfig);
  const instance = bind(Axios_default.prototype.request, context);
  utils_default.extend(instance, Axios_default.prototype, context, { allOwnKeys: true });
  utils_default.extend(instance, context, null, { allOwnKeys: true });
  instance.create = function create(instanceConfig) {
    return createInstance(mergeConfig(defaultConfig, instanceConfig));
  };
  return instance;
}
var axios = createInstance(defaults_default);
axios.Axios = Axios_default;
axios.CanceledError = CanceledError_default;
axios.CancelToken = CancelToken_default;
axios.isCancel = isCancel;
axios.VERSION = VERSION;
axios.toFormData = toFormData_default;
axios.AxiosError = AxiosError_default;
axios.Cancel = axios.CanceledError;
axios.all = function all(promises) {
  return Promise.all(promises);
};
axios.spread = spread;
axios.isAxiosError = isAxiosError;
axios.mergeConfig = mergeConfig;
axios.AxiosHeaders = AxiosHeaders_default;
axios.formToJSON = (thing) => formDataToJSON_default(utils_default.isHTMLForm(thing) ? new FormData(thing) : thing);
axios.getAdapter = adapters_default.getAdapter;
axios.HttpStatusCode = HttpStatusCode_default;
axios.default = axios;
var axios_default = axios;

// node_modules/axios/index.js
var {
  Axios: Axios2,
  AxiosError: AxiosError2,
  CanceledError: CanceledError2,
  isCancel: isCancel2,
  CancelToken: CancelToken2,
  VERSION: VERSION2,
  all: all2,
  Cancel,
  isAxiosError: isAxiosError2,
  spread: spread2,
  toFormData: toFormData2,
  AxiosHeaders: AxiosHeaders2,
  HttpStatusCode: HttpStatusCode2,
  formToJSON,
  getAdapter: getAdapter2,
  mergeConfig: mergeConfig2
} = axios_default;

// src/shared.ts
var import_vscode = require("vscode");
var Extension = {
  shortName: "TikBook",
  name: "TikBook for RouterOS"
};
var log = import_vscode.window.createOutputChannel(Extension.name, { log: true });
log.info(`<shared> Logging started on ${log.name} at level ${log.logLevel}`);
function initializeLogging() {
  return [
    log.onDidChangeLogLevel((e) => log.info(`<shared> Log level changed to ${import_vscode.LogLevel[e]}`))
  ];
}

// src/config.ts
var import_vscode2 = require("vscode");
function getSettings() {
  const vsconf = import_vscode2.workspace.getConfiguration("tikbook", null);
  return {
    username: vsconf.get("username") || "admin",
    password: vsconf.get("password") || "",
    baseUrl: vsconf.get("baseUrl") || "http://192.168.88.1",
    apiTimeout: vsconf.get("apiTimeout") || 15,
    sshCommand: vsconf.get("sshCommand") || "ssh",
    provideLspServerCredentials: vsconf.get("provideLspServerCredentials"),
    checkCertificates: vsconf.get("checkCertificates") || false
  };
}
function getConnectionUrlString() {
  const settings = getSettings();
  const url = URL.parse(settings.baseUrl);
  if (url) {
    url.username = settings.username;
    return `${url.protocol}//${url.username}@${url.host}`;
  } else {
    return "";
  }
}

class SecretManager {
  static SECRET_KEY = "tikbook.password.default";
  context;
  keyname;
  disposables = [];
  _onSecretChange = new import_vscode2.EventEmitter;
  onSecretChange = this._onSecretChange.event;
  static default;
  static start(context) {
    return SecretManager.default = new SecretManager(context, SecretManager.SECRET_KEY);
  }
  constructor(context, keyname) {
    this.context = context;
    this.keyname = keyname;
    this.disposables.push(this.context.secrets.onDidChange(async (e) => {
      if (e.key === this.keyname)
        await this.updatePasswordStatus();
    }));
    this.updatePasswordStatus();
    import_vscode2.workspace.onDidChangeConfiguration((e) => {
      if (e.affectsConfiguration("tikbook.passwordInfo")) {
        log.debug("<SecretManager> {onDidChangeConfiguration} use edited status, should replaced");
        this.updatePasswordStatus();
      }
    });
  }
  async initialize() {
    await this.updatePasswordStatus();
  }
  dispose() {
    this.disposables.forEach((e) => e.dispose());
  }
  async setPassword(back) {
    const password = await import_vscode2.window.showInputBox({
      prompt: "Enter password for RouterOS",
      password: true,
      placeHolder: `Password for ${getSettings().baseUrl}`,
      ignoreFocusOut: true
    });
    if (password) {
      await this.context.secrets.store(SecretManager.SECRET_KEY, password);
      await this.updatePasswordStatus();
      const msg = "Saved. Password using secret in SecretStore";
      import_vscode2.window.showInformationMessage(msg);
      log.info(`<SecretManager> {setPassword} called and notified ${msg}`);
    }
    if (back) {
      log.trace("<SecretManager> returning back to menu", back);
      import_vscode2.commands.executeCommand(back);
    }
  }
  async clearPassword(back) {
    await this.context.secrets.delete(SecretManager.SECRET_KEY);
    await this.updatePasswordStatus();
    const msg = "Cleared. Password using plain text from Settings";
    import_vscode2.window.showWarningMessage(msg);
    log.warn(`<SecretManager> {clearPassword} called and warned user '${msg}'`);
    if (back) {
      import_vscode2.commands.executeCommand(back);
    }
  }
  async getPassword() {
    return await this.context.secrets.get(SecretManager.SECRET_KEY);
  }
  async updatePasswordStatus() {
    const config = import_vscode2.workspace.getConfiguration("tikbook");
    const hasPassword = !!await this.getPassword();
    await import_vscode2.commands.executeCommand("setContext", "tikbook.usingSecrets", hasPassword);
    await config.update("passwordInfo", hasPassword ? "✓ Password using secret in SecretStore" : "⚠ Password using plain text from Settings", import_vscode2.ConfigurationTarget.Global);
  }
}

// src/routeros.ts
var import_vscode3 = require("vscode");

// node:https
var __create2 = Object.create;
var { getPrototypeOf: __getProtoOf2, defineProperty: __defProp3, getOwnPropertyNames: __getOwnPropNames3 } = Object;
var __hasOwnProp3 = Object.prototype.hasOwnProperty;
var __toESM2 = (mod, isNodeMode, target) => {
  target = mod != null ? __create2(__getProtoOf2(mod)) : {};
  let to = isNodeMode || !mod || !mod.__esModule ? __defProp3(target, "default", { value: mod, enumerable: true }) : target;
  for (let key of __getOwnPropNames3(mod))
    if (!__hasOwnProp3.call(to, key))
      __defProp3(to, key, { get: () => mod[key], enumerable: true });
  return to;
};
var __commonJS3 = (cb, mod) => () => (mod || cb((mod = { exports: {} }).exports, mod), mod.exports);
var require_https_browserify = __commonJS3((exports2, module2) => {
  var http = (init_http(), __toCommonJS(exports_http)), url = (init_url(), __toCommonJS(exports_url)), https = exports2;
  for (key in http)
    if (http.hasOwnProperty(key))
      https[key] = http[key];
  var key;
  https.request = function(params, cb) {
    return params = validateParams(params), http.request.call(this, params, cb);
  };
  https.get = function(params, cb) {
    return params = validateParams(params), http.get.call(this, params, cb);
  };
  function validateParams(params) {
    if (typeof params === "string")
      params = url.parse(params);
    if (!params.protocol)
      params.protocol = "https:";
    if (params.protocol !== "https:")
      throw Error('Protocol "' + params.protocol + '" not supported. Expected "https:"');
    return params;
  }
});
var https = __toESM2(require_https_browserify(), 1);
var { Agent: Agent2, ClientRequest: ClientRequest2, IncomingMessage: IncomingMessage2, METHODS: METHODS2, OutgoingMessage, STATUS_CODES: STATUS_CODES2, Server, ServerResponse, createServer, get: get2, globalAgent: globalAgent2, maxHeaderSize, request: request2, setMaxIdleHTTPParsers, validateHeaderName, validateHeaderValue } = https;

// src/routeros.ts
var _httpsNoCheckCertificates;
function getHttpsAgent() {
  const shouldCheckCertificates = getSettings().checkCertificates;
  if (import_vscode3.env.uiKind === import_vscode3.UIKind.Web)
    return;
  if (shouldCheckCertificates)
    return;
  if (_httpsNoCheckCertificates)
    return _httpsNoCheckCertificates;
  return _httpsNoCheckCertificates = new Agent2({
    rejectUnauthorized: false
  });
}

class RouterRestClient {
  static #default = undefined;
  static get default() {
    log.trace("<RouterRestClient> {{get default}}");
    if (RouterRestClient.#default) {
      return RouterRestClient.#default;
    } else {
      log.info("<RouterRestClient> created NEW {{default}} client");
      RouterRestClient.#default = new RouterRestClient;
      return RouterRestClient.#default;
    }
  }
  _onHttpResponseSuccess = new import_vscode3.EventEmitter;
  _onHttpResponseError = new import_vscode3.EventEmitter;
  _onHttpRequestSuccess = new import_vscode3.EventEmitter;
  _onHttpRequestError = new import_vscode3.EventEmitter;
  onHttpResponseSuccess = this._onHttpResponseSuccess.event;
  onHttpResponseError = this._onHttpResponseError.event;
  onHttpRequestSuccess = this._onHttpRequestSuccess.event;
  onHttpRequestError = this._onHttpRequestError.event;
  constructor() {
    log.trace("<RouterRestClient> {constructor} noop");
  }
  dispose() {
    log.info("<RouterRestClient> {dispose} invoked");
    this._onHttpResponseError.dispose();
    this._onHttpResponseSuccess.dispose();
    this._onHttpRequestError.dispose();
    this._onHttpRequestSuccess.dispose();
  }
  get httpClient() {
    log.trace("<RouterRestClient> {httpClient}");
    const client = axios_default.create({
      headers: { "Content-Type": "application/json" },
      withCredentials: true
    });
    client.interceptors.request.use(async (req) => {
      const password = await SecretManager.default.getPassword();
      const settings = getSettings();
      req.auth = {
        username: settings.username,
        password: password || settings.password || ""
      };
      req.baseURL = `${settings.baseUrl}/rest`;
      req.timeout = settings.apiTimeout * 1000;
      if (import_vscode3.env.uiKind === import_vscode3.UIKind.Desktop)
        req.httpsAgent = getHttpsAgent();
      return req;
    });
    client.interceptors.request.use((req) => this.pipelineRequestSuccess(req), (error) => this.pipelineRequestError(error));
    client.interceptors.response.use((resp) => this.pipelineResponseSuccess(resp), (error) => this.pipelineResponseError(error));
    return client;
  }
  pipelineRequestSuccess(req) {
    log.info("<RouterRestClient> request incoming", req.method, req.url);
    this._onHttpRequestSuccess.fire(req);
    return req;
  }
  pipelineRequestError(error) {
    if (isAxiosError2(error)) {
      log.warn("<RouterRestClient> axios error _before_ sending", `${error.config?.url} ${error.code} '${error.message}' baseUrl ${error.config?.baseURL} user ${error.config?.auth?.username}`);
      this._onHttpRequestError.fire(error);
    } else {
      log.error("<RouterRestClient> cannot send request", error);
    }
    return Promise.reject(error);
  }
  pipelineResponseSuccess(resp) {
    log.info("<RouterRestClient> done successfully", resp.config.url);
    this._onHttpResponseSuccess.fire(resp);
    return resp;
  }
  pipelineResponseError(error) {
    if (isAxiosError2(error)) {
      log.warn("<RouterRestClient> axios error _before_ sending", `${error.config?.url} ${error.code} '${error.message}' baseUrl ${error.config?.baseURL} user ${error.config?.auth?.username}`);
      this._onHttpRequestError.fire(error);
    } else {
      log.error("<RouterRestClient> request failed", error);
    }
    return Promise.reject(error);
  }
  async _execute(cmd, signal) {
    log.trace("<RouterRestClient> [_execute] ");
    return await this.httpClient.post("/execute", {
      "as-string": true,
      script: cmd
    }, signal ? { signal } : {}).then((resp) => resp?.data?.ret);
  }
  async _asCSV(cmd, signal, _options) {
    return this._execute(`:put [:serialize to=dsv delimiter=, options=dsv.remap [${cmd} as-value]]`, signal);
  }
  async _asJSON(cmd, signal, _pretty) {
    return this._execute(`:put [:serialize to=json [${cmd} as-value]]`, signal);
  }
  async _inspect(request3, input, path) {
    log.trace("<RouterRestClient> [_inspect] ");
    return await this.httpClient.post("/console/inspect", {
      request: request3,
      input,
      path
    }).then((resp) => resp?.data);
  }
  async run(cmd, signal) {
    return this._execute(cmd, signal);
  }
  inspectHighligh = (input, path) => {
    return this._inspect("highlight", new RouterScriptPreprocessor(input).unicodeCharReplace("_"), path);
  };
  inspectSyntax = (input, path) => {
    return this._inspect("syntax", input, path);
  };
  inspectCompletion = (input, path) => {
    return this._inspect("completion", input, path);
  };
  inspectChild = (input, path) => {
    return this._inspect("child", input, path);
  };
  exportConfig = (type, token) => {
    log.info(`<RouterRestClient> [exportConfig] ${type}`);
    return this.run(`:export ${type}`, token);
  };
  scriptEnvironment = () => {
    return this.httpClient.post("/system/script/environment/print", {}).then((resp) => resp.data);
  };
  get systemScripts() {
    return this.httpClient.post("/system/script/print", {}).then((resp) => resp.data);
  }
  get defaultConfiguration() {
    return this.httpClient.post("/system/default-configuration/print", {}).then((resp) => resp.data?.[0]);
  }
  getSystemScript = (name) => {
    return this.httpClient.get(`/system/script/${encodeURIComponent(name)}`).then((resp) => resp.data);
  };
  getIdentity = () => {
    return this.httpClient.get("/system/identity").then((resp) => resp.data?.name);
  };
  getRawIdentity = () => {
    return this.httpClient.get("/system/identity");
  };
  getSystemResources() {
    return this.httpClient.get("/system/resource").then((resp) => resp.data);
  }
  getNeighbors(format2 = "csv") {
    if (format2 !== "csv")
      throw new Error("not implemented");
    return this._asCSV("/ip/neighbor print detail");
  }
}

class RouterScriptPreprocessor {
  text = "";
  unicodeCharReplace(replace = "_") {
    let result = "";
    for (let i2 = 0;i2 < this.text.length; i2++) {
      const charCode = this.text.charCodeAt(i2);
      if (charCode >= 0 && charCode <= 127) {
        result += this.text.charAt(i2);
      } else {
        result += replace;
      }
    }
    return result;
  }
  constructor(text) {
    this.text = text;
  }
}

// node_modules/luxon/build/es6/luxon.mjs
class LuxonError extends Error {
}

class InvalidDateTimeError extends LuxonError {
  constructor(reason) {
    super(`Invalid DateTime: ${reason.toMessage()}`);
  }
}

class InvalidIntervalError extends LuxonError {
  constructor(reason) {
    super(`Invalid Interval: ${reason.toMessage()}`);
  }
}

class InvalidDurationError extends LuxonError {
  constructor(reason) {
    super(`Invalid Duration: ${reason.toMessage()}`);
  }
}

class ConflictingSpecificationError extends LuxonError {
}

class InvalidUnitError extends LuxonError {
  constructor(unit) {
    super(`Invalid unit ${unit}`);
  }
}

class InvalidArgumentError extends LuxonError {
}

class ZoneIsAbstractError extends LuxonError {
  constructor() {
    super("Zone is an abstract class");
  }
}
var n = "numeric";
var s = "short";
var l = "long";
var DATE_SHORT = {
  year: n,
  month: n,
  day: n
};
var DATE_MED = {
  year: n,
  month: s,
  day: n
};
var DATE_MED_WITH_WEEKDAY = {
  year: n,
  month: s,
  day: n,
  weekday: s
};
var DATE_FULL = {
  year: n,
  month: l,
  day: n
};
var DATE_HUGE = {
  year: n,
  month: l,
  day: n,
  weekday: l
};
var TIME_SIMPLE = {
  hour: n,
  minute: n
};
var TIME_WITH_SECONDS = {
  hour: n,
  minute: n,
  second: n
};
var TIME_WITH_SHORT_OFFSET = {
  hour: n,
  minute: n,
  second: n,
  timeZoneName: s
};
var TIME_WITH_LONG_OFFSET = {
  hour: n,
  minute: n,
  second: n,
  timeZoneName: l
};
var TIME_24_SIMPLE = {
  hour: n,
  minute: n,
  hourCycle: "h23"
};
var TIME_24_WITH_SECONDS = {
  hour: n,
  minute: n,
  second: n,
  hourCycle: "h23"
};
var TIME_24_WITH_SHORT_OFFSET = {
  hour: n,
  minute: n,
  second: n,
  hourCycle: "h23",
  timeZoneName: s
};
var TIME_24_WITH_LONG_OFFSET = {
  hour: n,
  minute: n,
  second: n,
  hourCycle: "h23",
  timeZoneName: l
};
var DATETIME_SHORT = {
  year: n,
  month: n,
  day: n,
  hour: n,
  minute: n
};
var DATETIME_SHORT_WITH_SECONDS = {
  year: n,
  month: n,
  day: n,
  hour: n,
  minute: n,
  second: n
};
var DATETIME_MED = {
  year: n,
  month: s,
  day: n,
  hour: n,
  minute: n
};
var DATETIME_MED_WITH_SECONDS = {
  year: n,
  month: s,
  day: n,
  hour: n,
  minute: n,
  second: n
};
var DATETIME_MED_WITH_WEEKDAY = {
  year: n,
  month: s,
  day: n,
  weekday: s,
  hour: n,
  minute: n
};
var DATETIME_FULL = {
  year: n,
  month: l,
  day: n,
  hour: n,
  minute: n,
  timeZoneName: s
};
var DATETIME_FULL_WITH_SECONDS = {
  year: n,
  month: l,
  day: n,
  hour: n,
  minute: n,
  second: n,
  timeZoneName: s
};
var DATETIME_HUGE = {
  year: n,
  month: l,
  day: n,
  weekday: l,
  hour: n,
  minute: n,
  timeZoneName: l
};
var DATETIME_HUGE_WITH_SECONDS = {
  year: n,
  month: l,
  day: n,
  weekday: l,
  hour: n,
  minute: n,
  second: n,
  timeZoneName: l
};

class Zone {
  get type() {
    throw new ZoneIsAbstractError;
  }
  get name() {
    throw new ZoneIsAbstractError;
  }
  get ianaName() {
    return this.name;
  }
  get isUniversal() {
    throw new ZoneIsAbstractError;
  }
  offsetName(ts, opts) {
    throw new ZoneIsAbstractError;
  }
  formatOffset(ts, format2) {
    throw new ZoneIsAbstractError;
  }
  offset(ts) {
    throw new ZoneIsAbstractError;
  }
  equals(otherZone) {
    throw new ZoneIsAbstractError;
  }
  get isValid() {
    throw new ZoneIsAbstractError;
  }
}
var singleton$1 = null;

class SystemZone extends Zone {
  static get instance() {
    if (singleton$1 === null) {
      singleton$1 = new SystemZone;
    }
    return singleton$1;
  }
  get type() {
    return "system";
  }
  get name() {
    return new Intl.DateTimeFormat().resolvedOptions().timeZone;
  }
  get isUniversal() {
    return false;
  }
  offsetName(ts, { format: format2, locale }) {
    return parseZoneInfo(ts, format2, locale);
  }
  formatOffset(ts, format2) {
    return formatOffset(this.offset(ts), format2);
  }
  offset(ts) {
    return -new Date(ts).getTimezoneOffset();
  }
  equals(otherZone) {
    return otherZone.type === "system";
  }
  get isValid() {
    return true;
  }
}
var dtfCache = new Map;
function makeDTF(zoneName) {
  let dtf = dtfCache.get(zoneName);
  if (dtf === undefined) {
    dtf = new Intl.DateTimeFormat("en-US", {
      hour12: false,
      timeZone: zoneName,
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
      era: "short"
    });
    dtfCache.set(zoneName, dtf);
  }
  return dtf;
}
var typeToPos = {
  year: 0,
  month: 1,
  day: 2,
  era: 3,
  hour: 4,
  minute: 5,
  second: 6
};
function hackyOffset(dtf, date) {
  const formatted = dtf.format(date).replace(/\u200E/g, ""), parsed = /(\d+)\/(\d+)\/(\d+) (AD|BC),? (\d+):(\d+):(\d+)/.exec(formatted), [, fMonth, fDay, fYear, fadOrBc, fHour, fMinute, fSecond] = parsed;
  return [fYear, fMonth, fDay, fadOrBc, fHour, fMinute, fSecond];
}
function partsOffset(dtf, date) {
  const formatted = dtf.formatToParts(date);
  const filled = [];
  for (let i2 = 0;i2 < formatted.length; i2++) {
    const { type, value } = formatted[i2];
    const pos = typeToPos[type];
    if (type === "era") {
      filled[pos] = value;
    } else if (!isUndefined3(pos)) {
      filled[pos] = parseInt(value, 10);
    }
  }
  return filled;
}
var ianaZoneCache = new Map;

class IANAZone extends Zone {
  static create(name) {
    let zone = ianaZoneCache.get(name);
    if (zone === undefined) {
      ianaZoneCache.set(name, zone = new IANAZone(name));
    }
    return zone;
  }
  static resetCache() {
    ianaZoneCache.clear();
    dtfCache.clear();
  }
  static isValidSpecifier(s2) {
    return this.isValidZone(s2);
  }
  static isValidZone(zone) {
    if (!zone) {
      return false;
    }
    try {
      new Intl.DateTimeFormat("en-US", { timeZone: zone }).format();
      return true;
    } catch (e) {
      return false;
    }
  }
  constructor(name) {
    super();
    this.zoneName = name;
    this.valid = IANAZone.isValidZone(name);
  }
  get type() {
    return "iana";
  }
  get name() {
    return this.zoneName;
  }
  get isUniversal() {
    return false;
  }
  offsetName(ts, { format: format2, locale }) {
    return parseZoneInfo(ts, format2, locale, this.name);
  }
  formatOffset(ts, format2) {
    return formatOffset(this.offset(ts), format2);
  }
  offset(ts) {
    if (!this.valid)
      return NaN;
    const date = new Date(ts);
    if (isNaN(date))
      return NaN;
    const dtf = makeDTF(this.name);
    let [year, month, day, adOrBc, hour, minute, second] = dtf.formatToParts ? partsOffset(dtf, date) : hackyOffset(dtf, date);
    if (adOrBc === "BC") {
      year = -Math.abs(year) + 1;
    }
    const adjustedHour = hour === 24 ? 0 : hour;
    const asUTC = objToLocalTS({
      year,
      month,
      day,
      hour: adjustedHour,
      minute,
      second,
      millisecond: 0
    });
    let asTS = +date;
    const over = asTS % 1000;
    asTS -= over >= 0 ? over : 1000 + over;
    return (asUTC - asTS) / (60 * 1000);
  }
  equals(otherZone) {
    return otherZone.type === "iana" && otherZone.name === this.name;
  }
  get isValid() {
    return this.valid;
  }
}
var intlLFCache = {};
function getCachedLF(locString, opts = {}) {
  const key = JSON.stringify([locString, opts]);
  let dtf = intlLFCache[key];
  if (!dtf) {
    dtf = new Intl.ListFormat(locString, opts);
    intlLFCache[key] = dtf;
  }
  return dtf;
}
var intlDTCache = new Map;
function getCachedDTF(locString, opts = {}) {
  const key = JSON.stringify([locString, opts]);
  let dtf = intlDTCache.get(key);
  if (dtf === undefined) {
    dtf = new Intl.DateTimeFormat(locString, opts);
    intlDTCache.set(key, dtf);
  }
  return dtf;
}
var intlNumCache = new Map;
function getCachedINF(locString, opts = {}) {
  const key = JSON.stringify([locString, opts]);
  let inf = intlNumCache.get(key);
  if (inf === undefined) {
    inf = new Intl.NumberFormat(locString, opts);
    intlNumCache.set(key, inf);
  }
  return inf;
}
var intlRelCache = new Map;
function getCachedRTF(locString, opts = {}) {
  const { base, ...cacheKeyOpts } = opts;
  const key = JSON.stringify([locString, cacheKeyOpts]);
  let inf = intlRelCache.get(key);
  if (inf === undefined) {
    inf = new Intl.RelativeTimeFormat(locString, opts);
    intlRelCache.set(key, inf);
  }
  return inf;
}
var sysLocaleCache = null;
function systemLocale() {
  if (sysLocaleCache) {
    return sysLocaleCache;
  } else {
    sysLocaleCache = new Intl.DateTimeFormat().resolvedOptions().locale;
    return sysLocaleCache;
  }
}
var intlResolvedOptionsCache = new Map;
function getCachedIntResolvedOptions(locString) {
  let opts = intlResolvedOptionsCache.get(locString);
  if (opts === undefined) {
    opts = new Intl.DateTimeFormat(locString).resolvedOptions();
    intlResolvedOptionsCache.set(locString, opts);
  }
  return opts;
}
var weekInfoCache = new Map;
function getCachedWeekInfo(locString) {
  let data = weekInfoCache.get(locString);
  if (!data) {
    const locale = new Intl.Locale(locString);
    data = "getWeekInfo" in locale ? locale.getWeekInfo() : locale.weekInfo;
    if (!("minimalDays" in data)) {
      data = { ...fallbackWeekSettings, ...data };
    }
    weekInfoCache.set(locString, data);
  }
  return data;
}
function parseLocaleString(localeStr) {
  const xIndex = localeStr.indexOf("-x-");
  if (xIndex !== -1) {
    localeStr = localeStr.substring(0, xIndex);
  }
  const uIndex = localeStr.indexOf("-u-");
  if (uIndex === -1) {
    return [localeStr];
  } else {
    let options;
    let selectedStr;
    try {
      options = getCachedDTF(localeStr).resolvedOptions();
      selectedStr = localeStr;
    } catch (e) {
      const smaller = localeStr.substring(0, uIndex);
      options = getCachedDTF(smaller).resolvedOptions();
      selectedStr = smaller;
    }
    const { numberingSystem, calendar } = options;
    return [selectedStr, numberingSystem, calendar];
  }
}
function intlConfigString(localeStr, numberingSystem, outputCalendar) {
  if (outputCalendar || numberingSystem) {
    if (!localeStr.includes("-u-")) {
      localeStr += "-u";
    }
    if (outputCalendar) {
      localeStr += `-ca-${outputCalendar}`;
    }
    if (numberingSystem) {
      localeStr += `-nu-${numberingSystem}`;
    }
    return localeStr;
  } else {
    return localeStr;
  }
}
function mapMonths(f) {
  const ms = [];
  for (let i2 = 1;i2 <= 12; i2++) {
    const dt = DateTime.utc(2009, i2, 1);
    ms.push(f(dt));
  }
  return ms;
}
function mapWeekdays(f) {
  const ms = [];
  for (let i2 = 1;i2 <= 7; i2++) {
    const dt = DateTime.utc(2016, 11, 13 + i2);
    ms.push(f(dt));
  }
  return ms;
}
function listStuff(loc, length, englishFn, intlFn) {
  const mode = loc.listingMode();
  if (mode === "error") {
    return null;
  } else if (mode === "en") {
    return englishFn(length);
  } else {
    return intlFn(length);
  }
}
function supportsFastNumbers(loc) {
  if (loc.numberingSystem && loc.numberingSystem !== "latn") {
    return false;
  } else {
    return loc.numberingSystem === "latn" || !loc.locale || loc.locale.startsWith("en") || getCachedIntResolvedOptions(loc.locale).numberingSystem === "latn";
  }
}

class PolyNumberFormatter {
  constructor(intl, forceSimple, opts) {
    this.padTo = opts.padTo || 0;
    this.floor = opts.floor || false;
    const { padTo, floor, ...otherOpts } = opts;
    if (!forceSimple || Object.keys(otherOpts).length > 0) {
      const intlOpts = { useGrouping: false, ...opts };
      if (opts.padTo > 0)
        intlOpts.minimumIntegerDigits = opts.padTo;
      this.inf = getCachedINF(intl, intlOpts);
    }
  }
  format(i2) {
    if (this.inf) {
      const fixed = this.floor ? Math.floor(i2) : i2;
      return this.inf.format(fixed);
    } else {
      const fixed = this.floor ? Math.floor(i2) : roundTo(i2, 3);
      return padStart(fixed, this.padTo);
    }
  }
}

class PolyDateFormatter {
  constructor(dt, intl, opts) {
    this.opts = opts;
    this.originalZone = undefined;
    let z = undefined;
    if (this.opts.timeZone) {
      this.dt = dt;
    } else if (dt.zone.type === "fixed") {
      const gmtOffset = -1 * (dt.offset / 60);
      const offsetZ = gmtOffset >= 0 ? `Etc/GMT+${gmtOffset}` : `Etc/GMT${gmtOffset}`;
      if (dt.offset !== 0 && IANAZone.create(offsetZ).valid) {
        z = offsetZ;
        this.dt = dt;
      } else {
        z = "UTC";
        this.dt = dt.offset === 0 ? dt : dt.setZone("UTC").plus({ minutes: dt.offset });
        this.originalZone = dt.zone;
      }
    } else if (dt.zone.type === "system") {
      this.dt = dt;
    } else if (dt.zone.type === "iana") {
      this.dt = dt;
      z = dt.zone.name;
    } else {
      z = "UTC";
      this.dt = dt.setZone("UTC").plus({ minutes: dt.offset });
      this.originalZone = dt.zone;
    }
    const intlOpts = { ...this.opts };
    intlOpts.timeZone = intlOpts.timeZone || z;
    this.dtf = getCachedDTF(intl, intlOpts);
  }
  format() {
    if (this.originalZone) {
      return this.formatToParts().map(({ value }) => value).join("");
    }
    return this.dtf.format(this.dt.toJSDate());
  }
  formatToParts() {
    const parts = this.dtf.formatToParts(this.dt.toJSDate());
    if (this.originalZone) {
      return parts.map((part) => {
        if (part.type === "timeZoneName") {
          const offsetName = this.originalZone.offsetName(this.dt.ts, {
            locale: this.dt.locale,
            format: this.opts.timeZoneName
          });
          return {
            ...part,
            value: offsetName
          };
        } else {
          return part;
        }
      });
    }
    return parts;
  }
  resolvedOptions() {
    return this.dtf.resolvedOptions();
  }
}

class PolyRelFormatter {
  constructor(intl, isEnglish, opts) {
    this.opts = { style: "long", ...opts };
    if (!isEnglish && hasRelative()) {
      this.rtf = getCachedRTF(intl, opts);
    }
  }
  format(count, unit) {
    if (this.rtf) {
      return this.rtf.format(count, unit);
    } else {
      return formatRelativeTime(unit, count, this.opts.numeric, this.opts.style !== "long");
    }
  }
  formatToParts(count, unit) {
    if (this.rtf) {
      return this.rtf.formatToParts(count, unit);
    } else {
      return [];
    }
  }
}
var fallbackWeekSettings = {
  firstDay: 1,
  minimalDays: 4,
  weekend: [6, 7]
};

class Locale {
  static fromOpts(opts) {
    return Locale.create(opts.locale, opts.numberingSystem, opts.outputCalendar, opts.weekSettings, opts.defaultToEN);
  }
  static create(locale, numberingSystem, outputCalendar, weekSettings, defaultToEN = false) {
    const specifiedLocale = locale || Settings.defaultLocale;
    const localeR = specifiedLocale || (defaultToEN ? "en-US" : systemLocale());
    const numberingSystemR = numberingSystem || Settings.defaultNumberingSystem;
    const outputCalendarR = outputCalendar || Settings.defaultOutputCalendar;
    const weekSettingsR = validateWeekSettings(weekSettings) || Settings.defaultWeekSettings;
    return new Locale(localeR, numberingSystemR, outputCalendarR, weekSettingsR, specifiedLocale);
  }
  static resetCache() {
    sysLocaleCache = null;
    intlDTCache.clear();
    intlNumCache.clear();
    intlRelCache.clear();
    intlResolvedOptionsCache.clear();
    weekInfoCache.clear();
  }
  static fromObject({ locale, numberingSystem, outputCalendar, weekSettings } = {}) {
    return Locale.create(locale, numberingSystem, outputCalendar, weekSettings);
  }
  constructor(locale, numbering, outputCalendar, weekSettings, specifiedLocale) {
    const [parsedLocale, parsedNumberingSystem, parsedOutputCalendar] = parseLocaleString(locale);
    this.locale = parsedLocale;
    this.numberingSystem = numbering || parsedNumberingSystem || null;
    this.outputCalendar = outputCalendar || parsedOutputCalendar || null;
    this.weekSettings = weekSettings;
    this.intl = intlConfigString(this.locale, this.numberingSystem, this.outputCalendar);
    this.weekdaysCache = { format: {}, standalone: {} };
    this.monthsCache = { format: {}, standalone: {} };
    this.meridiemCache = null;
    this.eraCache = {};
    this.specifiedLocale = specifiedLocale;
    this.fastNumbersCached = null;
  }
  get fastNumbers() {
    if (this.fastNumbersCached == null) {
      this.fastNumbersCached = supportsFastNumbers(this);
    }
    return this.fastNumbersCached;
  }
  listingMode() {
    const isActuallyEn = this.isEnglish();
    const hasNoWeirdness = (this.numberingSystem === null || this.numberingSystem === "latn") && (this.outputCalendar === null || this.outputCalendar === "gregory");
    return isActuallyEn && hasNoWeirdness ? "en" : "intl";
  }
  clone(alts) {
    if (!alts || Object.getOwnPropertyNames(alts).length === 0) {
      return this;
    } else {
      return Locale.create(alts.locale || this.specifiedLocale, alts.numberingSystem || this.numberingSystem, alts.outputCalendar || this.outputCalendar, validateWeekSettings(alts.weekSettings) || this.weekSettings, alts.defaultToEN || false);
    }
  }
  redefaultToEN(alts = {}) {
    return this.clone({ ...alts, defaultToEN: true });
  }
  redefaultToSystem(alts = {}) {
    return this.clone({ ...alts, defaultToEN: false });
  }
  months(length, format2 = false) {
    return listStuff(this, length, months2, () => {
      const monthSpecialCase = this.intl === "ja" || this.intl.startsWith("ja-");
      format2 &= !monthSpecialCase;
      const intl = format2 ? { month: length, day: "numeric" } : { month: length }, formatStr = format2 ? "format" : "standalone";
      if (!this.monthsCache[formatStr][length]) {
        const mapper = !monthSpecialCase ? (dt) => this.extract(dt, intl, "month") : (dt) => this.dtFormatter(dt, intl).format();
        this.monthsCache[formatStr][length] = mapMonths(mapper);
      }
      return this.monthsCache[formatStr][length];
    });
  }
  weekdays(length, format2 = false) {
    return listStuff(this, length, weekdays, () => {
      const intl = format2 ? { weekday: length, year: "numeric", month: "long", day: "numeric" } : { weekday: length }, formatStr = format2 ? "format" : "standalone";
      if (!this.weekdaysCache[formatStr][length]) {
        this.weekdaysCache[formatStr][length] = mapWeekdays((dt) => this.extract(dt, intl, "weekday"));
      }
      return this.weekdaysCache[formatStr][length];
    });
  }
  meridiems() {
    return listStuff(this, undefined, () => meridiems, () => {
      if (!this.meridiemCache) {
        const intl = { hour: "numeric", hourCycle: "h12" };
        this.meridiemCache = [DateTime.utc(2016, 11, 13, 9), DateTime.utc(2016, 11, 13, 19)].map((dt) => this.extract(dt, intl, "dayperiod"));
      }
      return this.meridiemCache;
    });
  }
  eras(length) {
    return listStuff(this, length, eras, () => {
      const intl = { era: length };
      if (!this.eraCache[length]) {
        this.eraCache[length] = [DateTime.utc(-40, 1, 1), DateTime.utc(2017, 1, 1)].map((dt) => this.extract(dt, intl, "era"));
      }
      return this.eraCache[length];
    });
  }
  extract(dt, intlOpts, field) {
    const df = this.dtFormatter(dt, intlOpts), results = df.formatToParts(), matching = results.find((m) => m.type.toLowerCase() === field);
    return matching ? matching.value : null;
  }
  numberFormatter(opts = {}) {
    return new PolyNumberFormatter(this.intl, opts.forceSimple || this.fastNumbers, opts);
  }
  dtFormatter(dt, intlOpts = {}) {
    return new PolyDateFormatter(dt, this.intl, intlOpts);
  }
  relFormatter(opts = {}) {
    return new PolyRelFormatter(this.intl, this.isEnglish(), opts);
  }
  listFormatter(opts = {}) {
    return getCachedLF(this.intl, opts);
  }
  isEnglish() {
    return this.locale === "en" || this.locale.toLowerCase() === "en-us" || getCachedIntResolvedOptions(this.intl).locale.startsWith("en-us");
  }
  getWeekSettings() {
    if (this.weekSettings) {
      return this.weekSettings;
    } else if (!hasLocaleWeekInfo()) {
      return fallbackWeekSettings;
    } else {
      return getCachedWeekInfo(this.locale);
    }
  }
  getStartOfWeek() {
    return this.getWeekSettings().firstDay;
  }
  getMinDaysInFirstWeek() {
    return this.getWeekSettings().minimalDays;
  }
  getWeekendDays() {
    return this.getWeekSettings().weekend;
  }
  equals(other) {
    return this.locale === other.locale && this.numberingSystem === other.numberingSystem && this.outputCalendar === other.outputCalendar;
  }
  toString() {
    return `Locale(${this.locale}, ${this.numberingSystem}, ${this.outputCalendar})`;
  }
}
var singleton = null;

class FixedOffsetZone extends Zone {
  static get utcInstance() {
    if (singleton === null) {
      singleton = new FixedOffsetZone(0);
    }
    return singleton;
  }
  static instance(offset) {
    return offset === 0 ? FixedOffsetZone.utcInstance : new FixedOffsetZone(offset);
  }
  static parseSpecifier(s2) {
    if (s2) {
      const r = s2.match(/^utc(?:([+-]\d{1,2})(?::(\d{2}))?)?$/i);
      if (r) {
        return new FixedOffsetZone(signedOffset(r[1], r[2]));
      }
    }
    return null;
  }
  constructor(offset) {
    super();
    this.fixed = offset;
  }
  get type() {
    return "fixed";
  }
  get name() {
    return this.fixed === 0 ? "UTC" : `UTC${formatOffset(this.fixed, "narrow")}`;
  }
  get ianaName() {
    if (this.fixed === 0) {
      return "Etc/UTC";
    } else {
      return `Etc/GMT${formatOffset(-this.fixed, "narrow")}`;
    }
  }
  offsetName() {
    return this.name;
  }
  formatOffset(ts, format2) {
    return formatOffset(this.fixed, format2);
  }
  get isUniversal() {
    return true;
  }
  offset() {
    return this.fixed;
  }
  equals(otherZone) {
    return otherZone.type === "fixed" && otherZone.fixed === this.fixed;
  }
  get isValid() {
    return true;
  }
}

class InvalidZone extends Zone {
  constructor(zoneName) {
    super();
    this.zoneName = zoneName;
  }
  get type() {
    return "invalid";
  }
  get name() {
    return this.zoneName;
  }
  get isUniversal() {
    return false;
  }
  offsetName() {
    return null;
  }
  formatOffset() {
    return "";
  }
  offset() {
    return NaN;
  }
  equals() {
    return false;
  }
  get isValid() {
    return false;
  }
}
function normalizeZone(input, defaultZone) {
  if (isUndefined3(input) || input === null) {
    return defaultZone;
  } else if (input instanceof Zone) {
    return input;
  } else if (isString3(input)) {
    const lowered = input.toLowerCase();
    if (lowered === "default")
      return defaultZone;
    else if (lowered === "local" || lowered === "system")
      return SystemZone.instance;
    else if (lowered === "utc" || lowered === "gmt")
      return FixedOffsetZone.utcInstance;
    else
      return FixedOffsetZone.parseSpecifier(lowered) || IANAZone.create(input);
  } else if (isNumber3(input)) {
    return FixedOffsetZone.instance(input);
  } else if (typeof input === "object" && "offset" in input && typeof input.offset === "function") {
    return input;
  } else {
    return new InvalidZone(input);
  }
}
var numberingSystems = {
  arab: "[٠-٩]",
  arabext: "[۰-۹]",
  bali: "[᭐-᭙]",
  beng: "[০-৯]",
  deva: "[०-९]",
  fullwide: "[０-９]",
  gujr: "[૦-૯]",
  hanidec: "[〇|一|二|三|四|五|六|七|八|九]",
  khmr: "[០-៩]",
  knda: "[೦-೯]",
  laoo: "[໐-໙]",
  limb: "[᥆-᥏]",
  mlym: "[൦-൯]",
  mong: "[᠐-᠙]",
  mymr: "[၀-၉]",
  orya: "[୦-୯]",
  tamldec: "[௦-௯]",
  telu: "[౦-౯]",
  thai: "[๐-๙]",
  tibt: "[༠-༩]",
  latn: "\\d"
};
var numberingSystemsUTF16 = {
  arab: [1632, 1641],
  arabext: [1776, 1785],
  bali: [6992, 7001],
  beng: [2534, 2543],
  deva: [2406, 2415],
  fullwide: [65296, 65303],
  gujr: [2790, 2799],
  khmr: [6112, 6121],
  knda: [3302, 3311],
  laoo: [3792, 3801],
  limb: [6470, 6479],
  mlym: [3430, 3439],
  mong: [6160, 6169],
  mymr: [4160, 4169],
  orya: [2918, 2927],
  tamldec: [3046, 3055],
  telu: [3174, 3183],
  thai: [3664, 3673],
  tibt: [3872, 3881]
};
var hanidecChars = numberingSystems.hanidec.replace(/[\[|\]]/g, "").split("");
function parseDigits(str) {
  let value = parseInt(str, 10);
  if (isNaN(value)) {
    value = "";
    for (let i2 = 0;i2 < str.length; i2++) {
      const code2 = str.charCodeAt(i2);
      if (str[i2].search(numberingSystems.hanidec) !== -1) {
        value += hanidecChars.indexOf(str[i2]);
      } else {
        for (const key in numberingSystemsUTF16) {
          const [min, max] = numberingSystemsUTF16[key];
          if (code2 >= min && code2 <= max) {
            value += code2 - min;
          }
        }
      }
    }
    return parseInt(value, 10);
  } else {
    return value;
  }
}
var digitRegexCache = new Map;
function resetDigitRegexCache() {
  digitRegexCache.clear();
}
function digitRegex({ numberingSystem }, append2 = "") {
  const ns = numberingSystem || "latn";
  let appendCache = digitRegexCache.get(ns);
  if (appendCache === undefined) {
    appendCache = new Map;
    digitRegexCache.set(ns, appendCache);
  }
  let regex = appendCache.get(append2);
  if (regex === undefined) {
    regex = new RegExp(`${numberingSystems[ns]}${append2}`);
    appendCache.set(append2, regex);
  }
  return regex;
}
var now = () => Date.now();
var defaultZone = "system";
var defaultLocale = null;
var defaultNumberingSystem = null;
var defaultOutputCalendar = null;
var twoDigitCutoffYear = 60;
var throwOnInvalid;
var defaultWeekSettings = null;

class Settings {
  static get now() {
    return now;
  }
  static set now(n2) {
    now = n2;
  }
  static set defaultZone(zone) {
    defaultZone = zone;
  }
  static get defaultZone() {
    return normalizeZone(defaultZone, SystemZone.instance);
  }
  static get defaultLocale() {
    return defaultLocale;
  }
  static set defaultLocale(locale) {
    defaultLocale = locale;
  }
  static get defaultNumberingSystem() {
    return defaultNumberingSystem;
  }
  static set defaultNumberingSystem(numberingSystem) {
    defaultNumberingSystem = numberingSystem;
  }
  static get defaultOutputCalendar() {
    return defaultOutputCalendar;
  }
  static set defaultOutputCalendar(outputCalendar) {
    defaultOutputCalendar = outputCalendar;
  }
  static get defaultWeekSettings() {
    return defaultWeekSettings;
  }
  static set defaultWeekSettings(weekSettings) {
    defaultWeekSettings = validateWeekSettings(weekSettings);
  }
  static get twoDigitCutoffYear() {
    return twoDigitCutoffYear;
  }
  static set twoDigitCutoffYear(cutoffYear) {
    twoDigitCutoffYear = cutoffYear % 100;
  }
  static get throwOnInvalid() {
    return throwOnInvalid;
  }
  static set throwOnInvalid(t) {
    throwOnInvalid = t;
  }
  static resetCaches() {
    Locale.resetCache();
    IANAZone.resetCache();
    DateTime.resetCache();
    resetDigitRegexCache();
  }
}

class Invalid {
  constructor(reason, explanation) {
    this.reason = reason;
    this.explanation = explanation;
  }
  toMessage() {
    if (this.explanation) {
      return `${this.reason}: ${this.explanation}`;
    } else {
      return this.reason;
    }
  }
}
var nonLeapLadder = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334];
var leapLadder = [0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335];
function unitOutOfRange(unit, value) {
  return new Invalid("unit out of range", `you specified ${value} (of type ${typeof value}) as a ${unit}, which is invalid`);
}
function dayOfWeek(year, month, day) {
  const d = new Date(Date.UTC(year, month - 1, day));
  if (year < 100 && year >= 0) {
    d.setUTCFullYear(d.getUTCFullYear() - 1900);
  }
  const js = d.getUTCDay();
  return js === 0 ? 7 : js;
}
function computeOrdinal(year, month, day) {
  return day + (isLeapYear(year) ? leapLadder : nonLeapLadder)[month - 1];
}
function uncomputeOrdinal(year, ordinal) {
  const table = isLeapYear(year) ? leapLadder : nonLeapLadder, month0 = table.findIndex((i2) => i2 < ordinal), day = ordinal - table[month0];
  return { month: month0 + 1, day };
}
function isoWeekdayToLocal(isoWeekday, startOfWeek) {
  return (isoWeekday - startOfWeek + 7) % 7 + 1;
}
function gregorianToWeek(gregObj, minDaysInFirstWeek = 4, startOfWeek = 1) {
  const { year, month, day } = gregObj, ordinal = computeOrdinal(year, month, day), weekday = isoWeekdayToLocal(dayOfWeek(year, month, day), startOfWeek);
  let weekNumber = Math.floor((ordinal - weekday + 14 - minDaysInFirstWeek) / 7), weekYear;
  if (weekNumber < 1) {
    weekYear = year - 1;
    weekNumber = weeksInWeekYear(weekYear, minDaysInFirstWeek, startOfWeek);
  } else if (weekNumber > weeksInWeekYear(year, minDaysInFirstWeek, startOfWeek)) {
    weekYear = year + 1;
    weekNumber = 1;
  } else {
    weekYear = year;
  }
  return { weekYear, weekNumber, weekday, ...timeObject(gregObj) };
}
function weekToGregorian(weekData, minDaysInFirstWeek = 4, startOfWeek = 1) {
  const { weekYear, weekNumber, weekday } = weekData, weekdayOfJan4 = isoWeekdayToLocal(dayOfWeek(weekYear, 1, minDaysInFirstWeek), startOfWeek), yearInDays = daysInYear(weekYear);
  let ordinal = weekNumber * 7 + weekday - weekdayOfJan4 - 7 + minDaysInFirstWeek, year;
  if (ordinal < 1) {
    year = weekYear - 1;
    ordinal += daysInYear(year);
  } else if (ordinal > yearInDays) {
    year = weekYear + 1;
    ordinal -= daysInYear(weekYear);
  } else {
    year = weekYear;
  }
  const { month, day } = uncomputeOrdinal(year, ordinal);
  return { year, month, day, ...timeObject(weekData) };
}
function gregorianToOrdinal(gregData) {
  const { year, month, day } = gregData;
  const ordinal = computeOrdinal(year, month, day);
  return { year, ordinal, ...timeObject(gregData) };
}
function ordinalToGregorian(ordinalData) {
  const { year, ordinal } = ordinalData;
  const { month, day } = uncomputeOrdinal(year, ordinal);
  return { year, month, day, ...timeObject(ordinalData) };
}
function usesLocalWeekValues(obj, loc) {
  const hasLocaleWeekData = !isUndefined3(obj.localWeekday) || !isUndefined3(obj.localWeekNumber) || !isUndefined3(obj.localWeekYear);
  if (hasLocaleWeekData) {
    const hasIsoWeekData = !isUndefined3(obj.weekday) || !isUndefined3(obj.weekNumber) || !isUndefined3(obj.weekYear);
    if (hasIsoWeekData) {
      throw new ConflictingSpecificationError("Cannot mix locale-based week fields with ISO-based week fields");
    }
    if (!isUndefined3(obj.localWeekday))
      obj.weekday = obj.localWeekday;
    if (!isUndefined3(obj.localWeekNumber))
      obj.weekNumber = obj.localWeekNumber;
    if (!isUndefined3(obj.localWeekYear))
      obj.weekYear = obj.localWeekYear;
    delete obj.localWeekday;
    delete obj.localWeekNumber;
    delete obj.localWeekYear;
    return {
      minDaysInFirstWeek: loc.getMinDaysInFirstWeek(),
      startOfWeek: loc.getStartOfWeek()
    };
  } else {
    return { minDaysInFirstWeek: 4, startOfWeek: 1 };
  }
}
function hasInvalidWeekData(obj, minDaysInFirstWeek = 4, startOfWeek = 1) {
  const validYear = isInteger(obj.weekYear), validWeek = integerBetween(obj.weekNumber, 1, weeksInWeekYear(obj.weekYear, minDaysInFirstWeek, startOfWeek)), validWeekday = integerBetween(obj.weekday, 1, 7);
  if (!validYear) {
    return unitOutOfRange("weekYear", obj.weekYear);
  } else if (!validWeek) {
    return unitOutOfRange("week", obj.weekNumber);
  } else if (!validWeekday) {
    return unitOutOfRange("weekday", obj.weekday);
  } else
    return false;
}
function hasInvalidOrdinalData(obj) {
  const validYear = isInteger(obj.year), validOrdinal = integerBetween(obj.ordinal, 1, daysInYear(obj.year));
  if (!validYear) {
    return unitOutOfRange("year", obj.year);
  } else if (!validOrdinal) {
    return unitOutOfRange("ordinal", obj.ordinal);
  } else
    return false;
}
function hasInvalidGregorianData(obj) {
  const validYear = isInteger(obj.year), validMonth = integerBetween(obj.month, 1, 12), validDay = integerBetween(obj.day, 1, daysInMonth(obj.year, obj.month));
  if (!validYear) {
    return unitOutOfRange("year", obj.year);
  } else if (!validMonth) {
    return unitOutOfRange("month", obj.month);
  } else if (!validDay) {
    return unitOutOfRange("day", obj.day);
  } else
    return false;
}
function hasInvalidTimeData(obj) {
  const { hour, minute, second, millisecond } = obj;
  const validHour = integerBetween(hour, 0, 23) || hour === 24 && minute === 0 && second === 0 && millisecond === 0, validMinute = integerBetween(minute, 0, 59), validSecond = integerBetween(second, 0, 59), validMillisecond = integerBetween(millisecond, 0, 999);
  if (!validHour) {
    return unitOutOfRange("hour", hour);
  } else if (!validMinute) {
    return unitOutOfRange("minute", minute);
  } else if (!validSecond) {
    return unitOutOfRange("second", second);
  } else if (!validMillisecond) {
    return unitOutOfRange("millisecond", millisecond);
  } else
    return false;
}
function isUndefined3(o) {
  return typeof o === "undefined";
}
function isNumber3(o) {
  return typeof o === "number";
}
function isInteger(o) {
  return typeof o === "number" && o % 1 === 0;
}
function isString3(o) {
  return typeof o === "string";
}
function isDate3(o) {
  return Object.prototype.toString.call(o) === "[object Date]";
}
function hasRelative() {
  try {
    return typeof Intl !== "undefined" && !!Intl.RelativeTimeFormat;
  } catch (e) {
    return false;
  }
}
function hasLocaleWeekInfo() {
  try {
    return typeof Intl !== "undefined" && !!Intl.Locale && (("weekInfo" in Intl.Locale.prototype) || ("getWeekInfo" in Intl.Locale.prototype));
  } catch (e) {
    return false;
  }
}
function maybeArray(thing) {
  return Array.isArray(thing) ? thing : [thing];
}
function bestBy(arr, by, compare) {
  if (arr.length === 0) {
    return;
  }
  return arr.reduce((best, next) => {
    const pair = [by(next), next];
    if (!best) {
      return pair;
    } else if (compare(best[0], pair[0]) === best[0]) {
      return best;
    } else {
      return pair;
    }
  }, null)[1];
}
function pick(obj, keys) {
  return keys.reduce((a, k) => {
    a[k] = obj[k];
    return a;
  }, {});
}
function hasOwnProperty3(obj, prop) {
  return Object.prototype.hasOwnProperty.call(obj, prop);
}
function validateWeekSettings(settings) {
  if (settings == null) {
    return null;
  } else if (typeof settings !== "object") {
    throw new InvalidArgumentError("Week settings must be an object");
  } else {
    if (!integerBetween(settings.firstDay, 1, 7) || !integerBetween(settings.minimalDays, 1, 7) || !Array.isArray(settings.weekend) || settings.weekend.some((v) => !integerBetween(v, 1, 7))) {
      throw new InvalidArgumentError("Invalid week settings");
    }
    return {
      firstDay: settings.firstDay,
      minimalDays: settings.minimalDays,
      weekend: Array.from(settings.weekend)
    };
  }
}
function integerBetween(thing, bottom, top) {
  return isInteger(thing) && thing >= bottom && thing <= top;
}
function floorMod(x, n2) {
  return x - n2 * Math.floor(x / n2);
}
function padStart(input, n2 = 2) {
  const isNeg = input < 0;
  let padded;
  if (isNeg) {
    padded = "-" + ("" + -input).padStart(n2, "0");
  } else {
    padded = ("" + input).padStart(n2, "0");
  }
  return padded;
}
function parseInteger(string) {
  if (isUndefined3(string) || string === null || string === "") {
    return;
  } else {
    return parseInt(string, 10);
  }
}
function parseFloating(string) {
  if (isUndefined3(string) || string === null || string === "") {
    return;
  } else {
    return parseFloat(string);
  }
}
function parseMillis(fraction) {
  if (isUndefined3(fraction) || fraction === null || fraction === "") {
    return;
  } else {
    const f = parseFloat("0." + fraction) * 1000;
    return Math.floor(f);
  }
}
function roundTo(number, digits, rounding = "round") {
  const factor = 10 ** digits;
  switch (rounding) {
    case "expand":
      return number > 0 ? Math.ceil(number * factor) / factor : Math.floor(number * factor) / factor;
    case "trunc":
      return Math.trunc(number * factor) / factor;
    case "round":
      return Math.round(number * factor) / factor;
    case "floor":
      return Math.floor(number * factor) / factor;
    case "ceil":
      return Math.ceil(number * factor) / factor;
    default:
      throw new RangeError(`Value rounding ${rounding} is out of range`);
  }
}
function isLeapYear(year) {
  return year % 4 === 0 && (year % 100 !== 0 || year % 400 === 0);
}
function daysInYear(year) {
  return isLeapYear(year) ? 366 : 365;
}
function daysInMonth(year, month) {
  const modMonth = floorMod(month - 1, 12) + 1, modYear = year + (month - modMonth) / 12;
  if (modMonth === 2) {
    return isLeapYear(modYear) ? 29 : 28;
  } else {
    return [31, null, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][modMonth - 1];
  }
}
function objToLocalTS(obj) {
  let d = Date.UTC(obj.year, obj.month - 1, obj.day, obj.hour, obj.minute, obj.second, obj.millisecond);
  if (obj.year < 100 && obj.year >= 0) {
    d = new Date(d);
    d.setUTCFullYear(obj.year, obj.month - 1, obj.day);
  }
  return +d;
}
function firstWeekOffset(year, minDaysInFirstWeek, startOfWeek) {
  const fwdlw = isoWeekdayToLocal(dayOfWeek(year, 1, minDaysInFirstWeek), startOfWeek);
  return -fwdlw + minDaysInFirstWeek - 1;
}
function weeksInWeekYear(weekYear, minDaysInFirstWeek = 4, startOfWeek = 1) {
  const weekOffset = firstWeekOffset(weekYear, minDaysInFirstWeek, startOfWeek);
  const weekOffsetNext = firstWeekOffset(weekYear + 1, minDaysInFirstWeek, startOfWeek);
  return (daysInYear(weekYear) - weekOffset + weekOffsetNext) / 7;
}
function untruncateYear(year) {
  if (year > 99) {
    return year;
  } else
    return year > Settings.twoDigitCutoffYear ? 1900 + year : 2000 + year;
}
function parseZoneInfo(ts, offsetFormat, locale, timeZone = null) {
  const date = new Date(ts), intlOpts = {
    hourCycle: "h23",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit"
  };
  if (timeZone) {
    intlOpts.timeZone = timeZone;
  }
  const modified = { timeZoneName: offsetFormat, ...intlOpts };
  const parsed = new Intl.DateTimeFormat(locale, modified).formatToParts(date).find((m) => m.type.toLowerCase() === "timezonename");
  return parsed ? parsed.value : null;
}
function signedOffset(offHourStr, offMinuteStr) {
  let offHour = parseInt(offHourStr, 10);
  if (Number.isNaN(offHour)) {
    offHour = 0;
  }
  const offMin = parseInt(offMinuteStr, 10) || 0, offMinSigned = offHour < 0 || Object.is(offHour, -0) ? -offMin : offMin;
  return offHour * 60 + offMinSigned;
}
function asNumber(value) {
  const numericValue = Number(value);
  if (typeof value === "boolean" || value === "" || !Number.isFinite(numericValue))
    throw new InvalidArgumentError(`Invalid unit value ${value}`);
  return numericValue;
}
function normalizeObject(obj, normalizer) {
  const normalized = {};
  for (const u in obj) {
    if (hasOwnProperty3(obj, u)) {
      const v = obj[u];
      if (v === undefined || v === null)
        continue;
      normalized[normalizer(u)] = asNumber(v);
    }
  }
  return normalized;
}
function formatOffset(offset, format2) {
  const hours = Math.trunc(Math.abs(offset / 60)), minutes = Math.trunc(Math.abs(offset % 60)), sign = offset >= 0 ? "+" : "-";
  switch (format2) {
    case "short":
      return `${sign}${padStart(hours, 2)}:${padStart(minutes, 2)}`;
    case "narrow":
      return `${sign}${hours}${minutes > 0 ? `:${minutes}` : ""}`;
    case "techie":
      return `${sign}${padStart(hours, 2)}${padStart(minutes, 2)}`;
    default:
      throw new RangeError(`Value format ${format2} is out of range for property format`);
  }
}
function timeObject(obj) {
  return pick(obj, ["hour", "minute", "second", "millisecond"]);
}
var monthsLong = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December"
];
var monthsShort = [
  "Jan",
  "Feb",
  "Mar",
  "Apr",
  "May",
  "Jun",
  "Jul",
  "Aug",
  "Sep",
  "Oct",
  "Nov",
  "Dec"
];
var monthsNarrow = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"];
function months2(length) {
  switch (length) {
    case "narrow":
      return [...monthsNarrow];
    case "short":
      return [...monthsShort];
    case "long":
      return [...monthsLong];
    case "numeric":
      return ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"];
    case "2-digit":
      return ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"];
    default:
      return null;
  }
}
var weekdaysLong = [
  "Monday",
  "Tuesday",
  "Wednesday",
  "Thursday",
  "Friday",
  "Saturday",
  "Sunday"
];
var weekdaysShort = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
var weekdaysNarrow = ["M", "T", "W", "T", "F", "S", "S"];
function weekdays(length) {
  switch (length) {
    case "narrow":
      return [...weekdaysNarrow];
    case "short":
      return [...weekdaysShort];
    case "long":
      return [...weekdaysLong];
    case "numeric":
      return ["1", "2", "3", "4", "5", "6", "7"];
    default:
      return null;
  }
}
var meridiems = ["AM", "PM"];
var erasLong = ["Before Christ", "Anno Domini"];
var erasShort = ["BC", "AD"];
var erasNarrow = ["B", "A"];
function eras(length) {
  switch (length) {
    case "narrow":
      return [...erasNarrow];
    case "short":
      return [...erasShort];
    case "long":
      return [...erasLong];
    default:
      return null;
  }
}
function meridiemForDateTime(dt) {
  return meridiems[dt.hour < 12 ? 0 : 1];
}
function weekdayForDateTime(dt, length) {
  return weekdays(length)[dt.weekday - 1];
}
function monthForDateTime(dt, length) {
  return months2(length)[dt.month - 1];
}
function eraForDateTime(dt, length) {
  return eras(length)[dt.year < 0 ? 0 : 1];
}
function formatRelativeTime(unit, count, numeric = "always", narrow = false) {
  const units = {
    years: ["year", "yr."],
    quarters: ["quarter", "qtr."],
    months: ["month", "mo."],
    weeks: ["week", "wk."],
    days: ["day", "day", "days"],
    hours: ["hour", "hr."],
    minutes: ["minute", "min."],
    seconds: ["second", "sec."]
  };
  const lastable = ["hours", "minutes", "seconds"].indexOf(unit) === -1;
  if (numeric === "auto" && lastable) {
    const isDay = unit === "days";
    switch (count) {
      case 1:
        return isDay ? "tomorrow" : `next ${units[unit][0]}`;
      case -1:
        return isDay ? "yesterday" : `last ${units[unit][0]}`;
      case 0:
        return isDay ? "today" : `this ${units[unit][0]}`;
    }
  }
  const isInPast = Object.is(count, -0) || count < 0, fmtValue = Math.abs(count), singular = fmtValue === 1, lilUnits = units[unit], fmtUnit = narrow ? singular ? lilUnits[1] : lilUnits[2] || lilUnits[1] : singular ? units[unit][0] : unit;
  return isInPast ? `${fmtValue} ${fmtUnit} ago` : `in ${fmtValue} ${fmtUnit}`;
}
function stringifyTokens(splits, tokenToString) {
  let s2 = "";
  for (const token of splits) {
    if (token.literal) {
      s2 += token.val;
    } else {
      s2 += tokenToString(token.val);
    }
  }
  return s2;
}
var macroTokenToFormatOpts = {
  D: DATE_SHORT,
  DD: DATE_MED,
  DDD: DATE_FULL,
  DDDD: DATE_HUGE,
  t: TIME_SIMPLE,
  tt: TIME_WITH_SECONDS,
  ttt: TIME_WITH_SHORT_OFFSET,
  tttt: TIME_WITH_LONG_OFFSET,
  T: TIME_24_SIMPLE,
  TT: TIME_24_WITH_SECONDS,
  TTT: TIME_24_WITH_SHORT_OFFSET,
  TTTT: TIME_24_WITH_LONG_OFFSET,
  f: DATETIME_SHORT,
  ff: DATETIME_MED,
  fff: DATETIME_FULL,
  ffff: DATETIME_HUGE,
  F: DATETIME_SHORT_WITH_SECONDS,
  FF: DATETIME_MED_WITH_SECONDS,
  FFF: DATETIME_FULL_WITH_SECONDS,
  FFFF: DATETIME_HUGE_WITH_SECONDS
};

class Formatter {
  static create(locale, opts = {}) {
    return new Formatter(locale, opts);
  }
  static parseFormat(fmt) {
    let current = null, currentFull = "", bracketed = false;
    const splits = [];
    for (let i2 = 0;i2 < fmt.length; i2++) {
      const c = fmt.charAt(i2);
      if (c === "'") {
        if (currentFull.length > 0 || bracketed) {
          splits.push({
            literal: bracketed || /^\s+$/.test(currentFull),
            val: currentFull === "" ? "'" : currentFull
          });
        }
        current = null;
        currentFull = "";
        bracketed = !bracketed;
      } else if (bracketed) {
        currentFull += c;
      } else if (c === current) {
        currentFull += c;
      } else {
        if (currentFull.length > 0) {
          splits.push({ literal: /^\s+$/.test(currentFull), val: currentFull });
        }
        currentFull = c;
        current = c;
      }
    }
    if (currentFull.length > 0) {
      splits.push({ literal: bracketed || /^\s+$/.test(currentFull), val: currentFull });
    }
    return splits;
  }
  static macroTokenToFormatOpts(token) {
    return macroTokenToFormatOpts[token];
  }
  constructor(locale, formatOpts) {
    this.opts = formatOpts;
    this.loc = locale;
    this.systemLoc = null;
  }
  formatWithSystemDefault(dt, opts) {
    if (this.systemLoc === null) {
      this.systemLoc = this.loc.redefaultToSystem();
    }
    const df = this.systemLoc.dtFormatter(dt, { ...this.opts, ...opts });
    return df.format();
  }
  dtFormatter(dt, opts = {}) {
    return this.loc.dtFormatter(dt, { ...this.opts, ...opts });
  }
  formatDateTime(dt, opts) {
    return this.dtFormatter(dt, opts).format();
  }
  formatDateTimeParts(dt, opts) {
    return this.dtFormatter(dt, opts).formatToParts();
  }
  formatInterval(interval, opts) {
    const df = this.dtFormatter(interval.start, opts);
    return df.dtf.formatRange(interval.start.toJSDate(), interval.end.toJSDate());
  }
  resolvedOptions(dt, opts) {
    return this.dtFormatter(dt, opts).resolvedOptions();
  }
  num(n2, p = 0, signDisplay = undefined) {
    if (this.opts.forceSimple) {
      return padStart(n2, p);
    }
    const opts = { ...this.opts };
    if (p > 0) {
      opts.padTo = p;
    }
    if (signDisplay) {
      opts.signDisplay = signDisplay;
    }
    return this.loc.numberFormatter(opts).format(n2);
  }
  formatDateTimeFromString(dt, fmt) {
    const knownEnglish = this.loc.listingMode() === "en", useDateTimeFormatter = this.loc.outputCalendar && this.loc.outputCalendar !== "gregory", string = (opts, extract) => this.loc.extract(dt, opts, extract), formatOffset2 = (opts) => {
      if (dt.isOffsetFixed && dt.offset === 0 && opts.allowZ) {
        return "Z";
      }
      return dt.isValid ? dt.zone.formatOffset(dt.ts, opts.format) : "";
    }, meridiem = () => knownEnglish ? meridiemForDateTime(dt) : string({ hour: "numeric", hourCycle: "h12" }, "dayperiod"), month = (length, standalone) => knownEnglish ? monthForDateTime(dt, length) : string(standalone ? { month: length } : { month: length, day: "numeric" }, "month"), weekday = (length, standalone) => knownEnglish ? weekdayForDateTime(dt, length) : string(standalone ? { weekday: length } : { weekday: length, month: "long", day: "numeric" }, "weekday"), maybeMacro = (token) => {
      const formatOpts = Formatter.macroTokenToFormatOpts(token);
      if (formatOpts) {
        return this.formatWithSystemDefault(dt, formatOpts);
      } else {
        return token;
      }
    }, era = (length) => knownEnglish ? eraForDateTime(dt, length) : string({ era: length }, "era"), tokenToString = (token) => {
      switch (token) {
        case "S":
          return this.num(dt.millisecond);
        case "u":
        case "SSS":
          return this.num(dt.millisecond, 3);
        case "s":
          return this.num(dt.second);
        case "ss":
          return this.num(dt.second, 2);
        case "uu":
          return this.num(Math.floor(dt.millisecond / 10), 2);
        case "uuu":
          return this.num(Math.floor(dt.millisecond / 100));
        case "m":
          return this.num(dt.minute);
        case "mm":
          return this.num(dt.minute, 2);
        case "h":
          return this.num(dt.hour % 12 === 0 ? 12 : dt.hour % 12);
        case "hh":
          return this.num(dt.hour % 12 === 0 ? 12 : dt.hour % 12, 2);
        case "H":
          return this.num(dt.hour);
        case "HH":
          return this.num(dt.hour, 2);
        case "Z":
          return formatOffset2({ format: "narrow", allowZ: this.opts.allowZ });
        case "ZZ":
          return formatOffset2({ format: "short", allowZ: this.opts.allowZ });
        case "ZZZ":
          return formatOffset2({ format: "techie", allowZ: this.opts.allowZ });
        case "ZZZZ":
          return dt.zone.offsetName(dt.ts, { format: "short", locale: this.loc.locale });
        case "ZZZZZ":
          return dt.zone.offsetName(dt.ts, { format: "long", locale: this.loc.locale });
        case "z":
          return dt.zoneName;
        case "a":
          return meridiem();
        case "d":
          return useDateTimeFormatter ? string({ day: "numeric" }, "day") : this.num(dt.day);
        case "dd":
          return useDateTimeFormatter ? string({ day: "2-digit" }, "day") : this.num(dt.day, 2);
        case "c":
          return this.num(dt.weekday);
        case "ccc":
          return weekday("short", true);
        case "cccc":
          return weekday("long", true);
        case "ccccc":
          return weekday("narrow", true);
        case "E":
          return this.num(dt.weekday);
        case "EEE":
          return weekday("short", false);
        case "EEEE":
          return weekday("long", false);
        case "EEEEE":
          return weekday("narrow", false);
        case "L":
          return useDateTimeFormatter ? string({ month: "numeric", day: "numeric" }, "month") : this.num(dt.month);
        case "LL":
          return useDateTimeFormatter ? string({ month: "2-digit", day: "numeric" }, "month") : this.num(dt.month, 2);
        case "LLL":
          return month("short", true);
        case "LLLL":
          return month("long", true);
        case "LLLLL":
          return month("narrow", true);
        case "M":
          return useDateTimeFormatter ? string({ month: "numeric" }, "month") : this.num(dt.month);
        case "MM":
          return useDateTimeFormatter ? string({ month: "2-digit" }, "month") : this.num(dt.month, 2);
        case "MMM":
          return month("short", false);
        case "MMMM":
          return month("long", false);
        case "MMMMM":
          return month("narrow", false);
        case "y":
          return useDateTimeFormatter ? string({ year: "numeric" }, "year") : this.num(dt.year);
        case "yy":
          return useDateTimeFormatter ? string({ year: "2-digit" }, "year") : this.num(dt.year.toString().slice(-2), 2);
        case "yyyy":
          return useDateTimeFormatter ? string({ year: "numeric" }, "year") : this.num(dt.year, 4);
        case "yyyyyy":
          return useDateTimeFormatter ? string({ year: "numeric" }, "year") : this.num(dt.year, 6);
        case "G":
          return era("short");
        case "GG":
          return era("long");
        case "GGGGG":
          return era("narrow");
        case "kk":
          return this.num(dt.weekYear.toString().slice(-2), 2);
        case "kkkk":
          return this.num(dt.weekYear, 4);
        case "W":
          return this.num(dt.weekNumber);
        case "WW":
          return this.num(dt.weekNumber, 2);
        case "n":
          return this.num(dt.localWeekNumber);
        case "nn":
          return this.num(dt.localWeekNumber, 2);
        case "ii":
          return this.num(dt.localWeekYear.toString().slice(-2), 2);
        case "iiii":
          return this.num(dt.localWeekYear, 4);
        case "o":
          return this.num(dt.ordinal);
        case "ooo":
          return this.num(dt.ordinal, 3);
        case "q":
          return this.num(dt.quarter);
        case "qq":
          return this.num(dt.quarter, 2);
        case "X":
          return this.num(Math.floor(dt.ts / 1000));
        case "x":
          return this.num(dt.ts);
        default:
          return maybeMacro(token);
      }
    };
    return stringifyTokens(Formatter.parseFormat(fmt), tokenToString);
  }
  formatDurationFromString(dur, fmt) {
    const invertLargest = this.opts.signMode === "negativeLargestOnly" ? -1 : 1;
    const tokenToField = (token) => {
      switch (token[0]) {
        case "S":
          return "milliseconds";
        case "s":
          return "seconds";
        case "m":
          return "minutes";
        case "h":
          return "hours";
        case "d":
          return "days";
        case "w":
          return "weeks";
        case "M":
          return "months";
        case "y":
          return "years";
        default:
          return null;
      }
    }, tokenToString = (lildur, info) => (token) => {
      const mapped = tokenToField(token);
      if (mapped) {
        const inversionFactor = info.isNegativeDuration && mapped !== info.largestUnit ? invertLargest : 1;
        let signDisplay;
        if (this.opts.signMode === "negativeLargestOnly" && mapped !== info.largestUnit) {
          signDisplay = "never";
        } else if (this.opts.signMode === "all") {
          signDisplay = "always";
        } else {
          signDisplay = "auto";
        }
        return this.num(lildur.get(mapped) * inversionFactor, token.length, signDisplay);
      } else {
        return token;
      }
    }, tokens = Formatter.parseFormat(fmt), realTokens = tokens.reduce((found, { literal, val }) => literal ? found : found.concat(val), []), collapsed = dur.shiftTo(...realTokens.map(tokenToField).filter((t) => t)), durationInfo = {
      isNegativeDuration: collapsed < 0,
      largestUnit: Object.keys(collapsed.values)[0]
    };
    return stringifyTokens(tokens, tokenToString(collapsed, durationInfo));
  }
}
var ianaRegex = /[A-Za-z_+-]{1,256}(?::?\/[A-Za-z0-9_+-]{1,256}(?:\/[A-Za-z0-9_+-]{1,256})?)?/;
function combineRegexes(...regexes) {
  const full = regexes.reduce((f, r) => f + r.source, "");
  return RegExp(`^${full}$`);
}
function combineExtractors(...extractors) {
  return (m) => extractors.reduce(([mergedVals, mergedZone, cursor], ex) => {
    const [val, zone, next] = ex(m, cursor);
    return [{ ...mergedVals, ...val }, zone || mergedZone, next];
  }, [{}, null, 1]).slice(0, 2);
}
function parse(s2, ...patterns) {
  if (s2 == null) {
    return [null, null];
  }
  for (const [regex, extractor] of patterns) {
    const m = regex.exec(s2);
    if (m) {
      return extractor(m);
    }
  }
  return [null, null];
}
function simpleParse(...keys) {
  return (match, cursor) => {
    const ret = {};
    let i2;
    for (i2 = 0;i2 < keys.length; i2++) {
      ret[keys[i2]] = parseInteger(match[cursor + i2]);
    }
    return [ret, null, cursor + i2];
  };
}
var offsetRegex = /(?:([Zz])|([+-]\d\d)(?::?(\d\d))?)/;
var isoExtendedZone = `(?:${offsetRegex.source}?(?:\\[(${ianaRegex.source})\\])?)?`;
var isoTimeBaseRegex = /(\d\d)(?::?(\d\d)(?::?(\d\d)(?:[.,](\d{1,30}))?)?)?/;
var isoTimeRegex = RegExp(`${isoTimeBaseRegex.source}${isoExtendedZone}`);
var isoTimeExtensionRegex = RegExp(`(?:[Tt]${isoTimeRegex.source})?`);
var isoYmdRegex = /([+-]\d{6}|\d{4})(?:-?(\d\d)(?:-?(\d\d))?)?/;
var isoWeekRegex = /(\d{4})-?W(\d\d)(?:-?(\d))?/;
var isoOrdinalRegex = /(\d{4})-?(\d{3})/;
var extractISOWeekData = simpleParse("weekYear", "weekNumber", "weekDay");
var extractISOOrdinalData = simpleParse("year", "ordinal");
var sqlYmdRegex = /(\d{4})-(\d\d)-(\d\d)/;
var sqlTimeRegex = RegExp(`${isoTimeBaseRegex.source} ?(?:${offsetRegex.source}|(${ianaRegex.source}))?`);
var sqlTimeExtensionRegex = RegExp(`(?: ${sqlTimeRegex.source})?`);
function int(match, pos, fallback) {
  const m = match[pos];
  return isUndefined3(m) ? fallback : parseInteger(m);
}
function extractISOYmd(match, cursor) {
  const item = {
    year: int(match, cursor),
    month: int(match, cursor + 1, 1),
    day: int(match, cursor + 2, 1)
  };
  return [item, null, cursor + 3];
}
function extractISOTime(match, cursor) {
  const item = {
    hours: int(match, cursor, 0),
    minutes: int(match, cursor + 1, 0),
    seconds: int(match, cursor + 2, 0),
    milliseconds: parseMillis(match[cursor + 3])
  };
  return [item, null, cursor + 4];
}
function extractISOOffset(match, cursor) {
  const local = !match[cursor] && !match[cursor + 1], fullOffset = signedOffset(match[cursor + 1], match[cursor + 2]), zone = local ? null : FixedOffsetZone.instance(fullOffset);
  return [{}, zone, cursor + 3];
}
function extractIANAZone(match, cursor) {
  const zone = match[cursor] ? IANAZone.create(match[cursor]) : null;
  return [{}, zone, cursor + 1];
}
var isoTimeOnly = RegExp(`^T?${isoTimeBaseRegex.source}$`);
var isoDuration = /^-?P(?:(?:(-?\d{1,20}(?:\.\d{1,20})?)Y)?(?:(-?\d{1,20}(?:\.\d{1,20})?)M)?(?:(-?\d{1,20}(?:\.\d{1,20})?)W)?(?:(-?\d{1,20}(?:\.\d{1,20})?)D)?(?:T(?:(-?\d{1,20}(?:\.\d{1,20})?)H)?(?:(-?\d{1,20}(?:\.\d{1,20})?)M)?(?:(-?\d{1,20})(?:[.,](-?\d{1,20}))?S)?)?)$/;
function extractISODuration(match) {
  const [s2, yearStr, monthStr, weekStr, dayStr, hourStr, minuteStr, secondStr, millisecondsStr] = match;
  const hasNegativePrefix = s2[0] === "-";
  const negativeSeconds = secondStr && secondStr[0] === "-";
  const maybeNegate = (num, force = false) => num !== undefined && (force || num && hasNegativePrefix) ? -num : num;
  return [
    {
      years: maybeNegate(parseFloating(yearStr)),
      months: maybeNegate(parseFloating(monthStr)),
      weeks: maybeNegate(parseFloating(weekStr)),
      days: maybeNegate(parseFloating(dayStr)),
      hours: maybeNegate(parseFloating(hourStr)),
      minutes: maybeNegate(parseFloating(minuteStr)),
      seconds: maybeNegate(parseFloating(secondStr), secondStr === "-0"),
      milliseconds: maybeNegate(parseMillis(millisecondsStr), negativeSeconds)
    }
  ];
}
var obsOffsets = {
  GMT: 0,
  EDT: -4 * 60,
  EST: -5 * 60,
  CDT: -5 * 60,
  CST: -6 * 60,
  MDT: -6 * 60,
  MST: -7 * 60,
  PDT: -7 * 60,
  PST: -8 * 60
};
function fromStrings(weekdayStr, yearStr, monthStr, dayStr, hourStr, minuteStr, secondStr) {
  const result = {
    year: yearStr.length === 2 ? untruncateYear(parseInteger(yearStr)) : parseInteger(yearStr),
    month: monthsShort.indexOf(monthStr) + 1,
    day: parseInteger(dayStr),
    hour: parseInteger(hourStr),
    minute: parseInteger(minuteStr)
  };
  if (secondStr)
    result.second = parseInteger(secondStr);
  if (weekdayStr) {
    result.weekday = weekdayStr.length > 3 ? weekdaysLong.indexOf(weekdayStr) + 1 : weekdaysShort.indexOf(weekdayStr) + 1;
  }
  return result;
}
var rfc2822 = /^(?:(Mon|Tue|Wed|Thu|Fri|Sat|Sun),\s)?(\d{1,2})\s(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s(\d{2,4})\s(\d\d):(\d\d)(?::(\d\d))?\s(?:(UT|GMT|[ECMP][SD]T)|([Zz])|(?:([+-]\d\d)(\d\d)))$/;
function extractRFC2822(match) {
  const [
    ,
    weekdayStr,
    dayStr,
    monthStr,
    yearStr,
    hourStr,
    minuteStr,
    secondStr,
    obsOffset,
    milOffset,
    offHourStr,
    offMinuteStr
  ] = match, result = fromStrings(weekdayStr, yearStr, monthStr, dayStr, hourStr, minuteStr, secondStr);
  let offset;
  if (obsOffset) {
    offset = obsOffsets[obsOffset];
  } else if (milOffset) {
    offset = 0;
  } else {
    offset = signedOffset(offHourStr, offMinuteStr);
  }
  return [result, new FixedOffsetZone(offset)];
}
function preprocessRFC2822(s2) {
  return s2.replace(/\([^()]*\)|[\n\t]/g, " ").replace(/(\s\s+)/g, " ").trim();
}
var rfc1123 = /^(Mon|Tue|Wed|Thu|Fri|Sat|Sun), (\d\d) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (\d{4}) (\d\d):(\d\d):(\d\d) GMT$/;
var rfc850 = /^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday), (\d\d)-(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-(\d\d) (\d\d):(\d\d):(\d\d) GMT$/;
var ascii = /^(Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) ( \d|\d\d) (\d\d):(\d\d):(\d\d) (\d{4})$/;
function extractRFC1123Or850(match) {
  const [, weekdayStr, dayStr, monthStr, yearStr, hourStr, minuteStr, secondStr] = match, result = fromStrings(weekdayStr, yearStr, monthStr, dayStr, hourStr, minuteStr, secondStr);
  return [result, FixedOffsetZone.utcInstance];
}
function extractASCII(match) {
  const [, weekdayStr, monthStr, dayStr, hourStr, minuteStr, secondStr, yearStr] = match, result = fromStrings(weekdayStr, yearStr, monthStr, dayStr, hourStr, minuteStr, secondStr);
  return [result, FixedOffsetZone.utcInstance];
}
var isoYmdWithTimeExtensionRegex = combineRegexes(isoYmdRegex, isoTimeExtensionRegex);
var isoWeekWithTimeExtensionRegex = combineRegexes(isoWeekRegex, isoTimeExtensionRegex);
var isoOrdinalWithTimeExtensionRegex = combineRegexes(isoOrdinalRegex, isoTimeExtensionRegex);
var isoTimeCombinedRegex = combineRegexes(isoTimeRegex);
var extractISOYmdTimeAndOffset = combineExtractors(extractISOYmd, extractISOTime, extractISOOffset, extractIANAZone);
var extractISOWeekTimeAndOffset = combineExtractors(extractISOWeekData, extractISOTime, extractISOOffset, extractIANAZone);
var extractISOOrdinalDateAndTime = combineExtractors(extractISOOrdinalData, extractISOTime, extractISOOffset, extractIANAZone);
var extractISOTimeAndOffset = combineExtractors(extractISOTime, extractISOOffset, extractIANAZone);
function parseISODate(s2) {
  return parse(s2, [isoYmdWithTimeExtensionRegex, extractISOYmdTimeAndOffset], [isoWeekWithTimeExtensionRegex, extractISOWeekTimeAndOffset], [isoOrdinalWithTimeExtensionRegex, extractISOOrdinalDateAndTime], [isoTimeCombinedRegex, extractISOTimeAndOffset]);
}
function parseRFC2822Date(s2) {
  return parse(preprocessRFC2822(s2), [rfc2822, extractRFC2822]);
}
function parseHTTPDate(s2) {
  return parse(s2, [rfc1123, extractRFC1123Or850], [rfc850, extractRFC1123Or850], [ascii, extractASCII]);
}
function parseISODuration(s2) {
  return parse(s2, [isoDuration, extractISODuration]);
}
var extractISOTimeOnly = combineExtractors(extractISOTime);
function parseISOTimeOnly(s2) {
  return parse(s2, [isoTimeOnly, extractISOTimeOnly]);
}
var sqlYmdWithTimeExtensionRegex = combineRegexes(sqlYmdRegex, sqlTimeExtensionRegex);
var sqlTimeCombinedRegex = combineRegexes(sqlTimeRegex);
var extractISOTimeOffsetAndIANAZone = combineExtractors(extractISOTime, extractISOOffset, extractIANAZone);
function parseSQL(s2) {
  return parse(s2, [sqlYmdWithTimeExtensionRegex, extractISOYmdTimeAndOffset], [sqlTimeCombinedRegex, extractISOTimeOffsetAndIANAZone]);
}
var INVALID$2 = "Invalid Duration";
var lowOrderMatrix = {
  weeks: {
    days: 7,
    hours: 7 * 24,
    minutes: 7 * 24 * 60,
    seconds: 7 * 24 * 60 * 60,
    milliseconds: 7 * 24 * 60 * 60 * 1000
  },
  days: {
    hours: 24,
    minutes: 24 * 60,
    seconds: 24 * 60 * 60,
    milliseconds: 24 * 60 * 60 * 1000
  },
  hours: { minutes: 60, seconds: 60 * 60, milliseconds: 60 * 60 * 1000 },
  minutes: { seconds: 60, milliseconds: 60 * 1000 },
  seconds: { milliseconds: 1000 }
};
var casualMatrix = {
  years: {
    quarters: 4,
    months: 12,
    weeks: 52,
    days: 365,
    hours: 365 * 24,
    minutes: 365 * 24 * 60,
    seconds: 365 * 24 * 60 * 60,
    milliseconds: 365 * 24 * 60 * 60 * 1000
  },
  quarters: {
    months: 3,
    weeks: 13,
    days: 91,
    hours: 91 * 24,
    minutes: 91 * 24 * 60,
    seconds: 91 * 24 * 60 * 60,
    milliseconds: 91 * 24 * 60 * 60 * 1000
  },
  months: {
    weeks: 4,
    days: 30,
    hours: 30 * 24,
    minutes: 30 * 24 * 60,
    seconds: 30 * 24 * 60 * 60,
    milliseconds: 30 * 24 * 60 * 60 * 1000
  },
  ...lowOrderMatrix
};
var daysInYearAccurate = 146097 / 400;
var daysInMonthAccurate = 146097 / 4800;
var accurateMatrix = {
  years: {
    quarters: 4,
    months: 12,
    weeks: daysInYearAccurate / 7,
    days: daysInYearAccurate,
    hours: daysInYearAccurate * 24,
    minutes: daysInYearAccurate * 24 * 60,
    seconds: daysInYearAccurate * 24 * 60 * 60,
    milliseconds: daysInYearAccurate * 24 * 60 * 60 * 1000
  },
  quarters: {
    months: 3,
    weeks: daysInYearAccurate / 28,
    days: daysInYearAccurate / 4,
    hours: daysInYearAccurate * 24 / 4,
    minutes: daysInYearAccurate * 24 * 60 / 4,
    seconds: daysInYearAccurate * 24 * 60 * 60 / 4,
    milliseconds: daysInYearAccurate * 24 * 60 * 60 * 1000 / 4
  },
  months: {
    weeks: daysInMonthAccurate / 7,
    days: daysInMonthAccurate,
    hours: daysInMonthAccurate * 24,
    minutes: daysInMonthAccurate * 24 * 60,
    seconds: daysInMonthAccurate * 24 * 60 * 60,
    milliseconds: daysInMonthAccurate * 24 * 60 * 60 * 1000
  },
  ...lowOrderMatrix
};
var orderedUnits$1 = [
  "years",
  "quarters",
  "months",
  "weeks",
  "days",
  "hours",
  "minutes",
  "seconds",
  "milliseconds"
];
var reverseUnits = orderedUnits$1.slice(0).reverse();
function clone$1(dur, alts, clear = false) {
  const conf = {
    values: clear ? alts.values : { ...dur.values, ...alts.values || {} },
    loc: dur.loc.clone(alts.loc),
    conversionAccuracy: alts.conversionAccuracy || dur.conversionAccuracy,
    matrix: alts.matrix || dur.matrix
  };
  return new Duration(conf);
}
function durationToMillis(matrix, vals) {
  let sum = vals.milliseconds ?? 0;
  for (const unit of reverseUnits.slice(1)) {
    if (vals[unit]) {
      sum += vals[unit] * matrix[unit]["milliseconds"];
    }
  }
  return sum;
}
function normalizeValues(matrix, vals) {
  const factor = durationToMillis(matrix, vals) < 0 ? -1 : 1;
  orderedUnits$1.reduceRight((previous, current) => {
    if (!isUndefined3(vals[current])) {
      if (previous) {
        const previousVal = vals[previous] * factor;
        const conv = matrix[current][previous];
        const rollUp = Math.floor(previousVal / conv);
        vals[current] += rollUp * factor;
        vals[previous] -= rollUp * conv * factor;
      }
      return current;
    } else {
      return previous;
    }
  }, null);
  orderedUnits$1.reduce((previous, current) => {
    if (!isUndefined3(vals[current])) {
      if (previous) {
        const fraction = vals[previous] % 1;
        vals[previous] -= fraction;
        vals[current] += fraction * matrix[previous][current];
      }
      return current;
    } else {
      return previous;
    }
  }, null);
}
function removeZeroes(vals) {
  const newVals = {};
  for (const [key, value] of Object.entries(vals)) {
    if (value !== 0) {
      newVals[key] = value;
    }
  }
  return newVals;
}

class Duration {
  constructor(config) {
    const accurate = config.conversionAccuracy === "longterm" || false;
    let matrix = accurate ? accurateMatrix : casualMatrix;
    if (config.matrix) {
      matrix = config.matrix;
    }
    this.values = config.values;
    this.loc = config.loc || Locale.create();
    this.conversionAccuracy = accurate ? "longterm" : "casual";
    this.invalid = config.invalid || null;
    this.matrix = matrix;
    this.isLuxonDuration = true;
  }
  static fromMillis(count, opts) {
    return Duration.fromObject({ milliseconds: count }, opts);
  }
  static fromObject(obj, opts = {}) {
    if (obj == null || typeof obj !== "object") {
      throw new InvalidArgumentError(`Duration.fromObject: argument expected to be an object, got ${obj === null ? "null" : typeof obj}`);
    }
    return new Duration({
      values: normalizeObject(obj, Duration.normalizeUnit),
      loc: Locale.fromObject(opts),
      conversionAccuracy: opts.conversionAccuracy,
      matrix: opts.matrix
    });
  }
  static fromDurationLike(durationLike) {
    if (isNumber3(durationLike)) {
      return Duration.fromMillis(durationLike);
    } else if (Duration.isDuration(durationLike)) {
      return durationLike;
    } else if (typeof durationLike === "object") {
      return Duration.fromObject(durationLike);
    } else {
      throw new InvalidArgumentError(`Unknown duration argument ${durationLike} of type ${typeof durationLike}`);
    }
  }
  static fromISO(text, opts) {
    const [parsed] = parseISODuration(text);
    if (parsed) {
      return Duration.fromObject(parsed, opts);
    } else {
      return Duration.invalid("unparsable", `the input "${text}" can't be parsed as ISO 8601`);
    }
  }
  static fromISOTime(text, opts) {
    const [parsed] = parseISOTimeOnly(text);
    if (parsed) {
      return Duration.fromObject(parsed, opts);
    } else {
      return Duration.invalid("unparsable", `the input "${text}" can't be parsed as ISO 8601`);
    }
  }
  static invalid(reason, explanation = null) {
    if (!reason) {
      throw new InvalidArgumentError("need to specify a reason the Duration is invalid");
    }
    const invalid = reason instanceof Invalid ? reason : new Invalid(reason, explanation);
    if (Settings.throwOnInvalid) {
      throw new InvalidDurationError(invalid);
    } else {
      return new Duration({ invalid });
    }
  }
  static normalizeUnit(unit) {
    const normalized = {
      year: "years",
      years: "years",
      quarter: "quarters",
      quarters: "quarters",
      month: "months",
      months: "months",
      week: "weeks",
      weeks: "weeks",
      day: "days",
      days: "days",
      hour: "hours",
      hours: "hours",
      minute: "minutes",
      minutes: "minutes",
      second: "seconds",
      seconds: "seconds",
      millisecond: "milliseconds",
      milliseconds: "milliseconds"
    }[unit ? unit.toLowerCase() : unit];
    if (!normalized)
      throw new InvalidUnitError(unit);
    return normalized;
  }
  static isDuration(o) {
    return o && o.isLuxonDuration || false;
  }
  get locale() {
    return this.isValid ? this.loc.locale : null;
  }
  get numberingSystem() {
    return this.isValid ? this.loc.numberingSystem : null;
  }
  toFormat(fmt, opts = {}) {
    const fmtOpts = {
      ...opts,
      floor: opts.round !== false && opts.floor !== false
    };
    return this.isValid ? Formatter.create(this.loc, fmtOpts).formatDurationFromString(this, fmt) : INVALID$2;
  }
  toHuman(opts = {}) {
    if (!this.isValid)
      return INVALID$2;
    const showZeros = opts.showZeros !== false;
    const l2 = orderedUnits$1.map((unit) => {
      const val = this.values[unit];
      if (isUndefined3(val) || val === 0 && !showZeros) {
        return null;
      }
      return this.loc.numberFormatter({ style: "unit", unitDisplay: "long", ...opts, unit: unit.slice(0, -1) }).format(val);
    }).filter((n2) => n2);
    return this.loc.listFormatter({ type: "conjunction", style: opts.listStyle || "narrow", ...opts }).format(l2);
  }
  toObject() {
    if (!this.isValid)
      return {};
    return { ...this.values };
  }
  toISO() {
    if (!this.isValid)
      return null;
    let s2 = "P";
    if (this.years !== 0)
      s2 += this.years + "Y";
    if (this.months !== 0 || this.quarters !== 0)
      s2 += this.months + this.quarters * 3 + "M";
    if (this.weeks !== 0)
      s2 += this.weeks + "W";
    if (this.days !== 0)
      s2 += this.days + "D";
    if (this.hours !== 0 || this.minutes !== 0 || this.seconds !== 0 || this.milliseconds !== 0)
      s2 += "T";
    if (this.hours !== 0)
      s2 += this.hours + "H";
    if (this.minutes !== 0)
      s2 += this.minutes + "M";
    if (this.seconds !== 0 || this.milliseconds !== 0)
      s2 += roundTo(this.seconds + this.milliseconds / 1000, 3) + "S";
    if (s2 === "P")
      s2 += "T0S";
    return s2;
  }
  toISOTime(opts = {}) {
    if (!this.isValid)
      return null;
    const millis = this.toMillis();
    if (millis < 0 || millis >= 86400000)
      return null;
    opts = {
      suppressMilliseconds: false,
      suppressSeconds: false,
      includePrefix: false,
      format: "extended",
      ...opts,
      includeOffset: false
    };
    const dateTime = DateTime.fromMillis(millis, { zone: "UTC" });
    return dateTime.toISOTime(opts);
  }
  toJSON() {
    return this.toISO();
  }
  toString() {
    return this.toISO();
  }
  [Symbol.for("nodejs.util.inspect.custom")]() {
    if (this.isValid) {
      return `Duration { values: ${JSON.stringify(this.values)} }`;
    } else {
      return `Duration { Invalid, reason: ${this.invalidReason} }`;
    }
  }
  toMillis() {
    if (!this.isValid)
      return NaN;
    return durationToMillis(this.matrix, this.values);
  }
  valueOf() {
    return this.toMillis();
  }
  plus(duration) {
    if (!this.isValid)
      return this;
    const dur = Duration.fromDurationLike(duration), result = {};
    for (const k of orderedUnits$1) {
      if (hasOwnProperty3(dur.values, k) || hasOwnProperty3(this.values, k)) {
        result[k] = dur.get(k) + this.get(k);
      }
    }
    return clone$1(this, { values: result }, true);
  }
  minus(duration) {
    if (!this.isValid)
      return this;
    const dur = Duration.fromDurationLike(duration);
    return this.plus(dur.negate());
  }
  mapUnits(fn) {
    if (!this.isValid)
      return this;
    const result = {};
    for (const k of Object.keys(this.values)) {
      result[k] = asNumber(fn(this.values[k], k));
    }
    return clone$1(this, { values: result }, true);
  }
  get(unit) {
    return this[Duration.normalizeUnit(unit)];
  }
  set(values) {
    if (!this.isValid)
      return this;
    const mixed = { ...this.values, ...normalizeObject(values, Duration.normalizeUnit) };
    return clone$1(this, { values: mixed });
  }
  reconfigure({ locale, numberingSystem, conversionAccuracy, matrix } = {}) {
    const loc = this.loc.clone({ locale, numberingSystem });
    const opts = { loc, matrix, conversionAccuracy };
    return clone$1(this, opts);
  }
  as(unit) {
    return this.isValid ? this.shiftTo(unit).get(unit) : NaN;
  }
  normalize() {
    if (!this.isValid)
      return this;
    const vals = this.toObject();
    normalizeValues(this.matrix, vals);
    return clone$1(this, { values: vals }, true);
  }
  rescale() {
    if (!this.isValid)
      return this;
    const vals = removeZeroes(this.normalize().shiftToAll().toObject());
    return clone$1(this, { values: vals }, true);
  }
  shiftTo(...units) {
    if (!this.isValid)
      return this;
    if (units.length === 0) {
      return this;
    }
    units = units.map((u) => Duration.normalizeUnit(u));
    const built = {}, accumulated = {}, vals = this.toObject();
    let lastUnit;
    for (const k of orderedUnits$1) {
      if (units.indexOf(k) >= 0) {
        lastUnit = k;
        let own = 0;
        for (const ak in accumulated) {
          own += this.matrix[ak][k] * accumulated[ak];
          accumulated[ak] = 0;
        }
        if (isNumber3(vals[k])) {
          own += vals[k];
        }
        const i2 = Math.trunc(own);
        built[k] = i2;
        accumulated[k] = (own * 1000 - i2 * 1000) / 1000;
      } else if (isNumber3(vals[k])) {
        accumulated[k] = vals[k];
      }
    }
    for (const key in accumulated) {
      if (accumulated[key] !== 0) {
        built[lastUnit] += key === lastUnit ? accumulated[key] : accumulated[key] / this.matrix[lastUnit][key];
      }
    }
    normalizeValues(this.matrix, built);
    return clone$1(this, { values: built }, true);
  }
  shiftToAll() {
    if (!this.isValid)
      return this;
    return this.shiftTo("years", "months", "weeks", "days", "hours", "minutes", "seconds", "milliseconds");
  }
  negate() {
    if (!this.isValid)
      return this;
    const negated = {};
    for (const k of Object.keys(this.values)) {
      negated[k] = this.values[k] === 0 ? 0 : -this.values[k];
    }
    return clone$1(this, { values: negated }, true);
  }
  removeZeros() {
    if (!this.isValid)
      return this;
    const vals = removeZeroes(this.values);
    return clone$1(this, { values: vals }, true);
  }
  get years() {
    return this.isValid ? this.values.years || 0 : NaN;
  }
  get quarters() {
    return this.isValid ? this.values.quarters || 0 : NaN;
  }
  get months() {
    return this.isValid ? this.values.months || 0 : NaN;
  }
  get weeks() {
    return this.isValid ? this.values.weeks || 0 : NaN;
  }
  get days() {
    return this.isValid ? this.values.days || 0 : NaN;
  }
  get hours() {
    return this.isValid ? this.values.hours || 0 : NaN;
  }
  get minutes() {
    return this.isValid ? this.values.minutes || 0 : NaN;
  }
  get seconds() {
    return this.isValid ? this.values.seconds || 0 : NaN;
  }
  get milliseconds() {
    return this.isValid ? this.values.milliseconds || 0 : NaN;
  }
  get isValid() {
    return this.invalid === null;
  }
  get invalidReason() {
    return this.invalid ? this.invalid.reason : null;
  }
  get invalidExplanation() {
    return this.invalid ? this.invalid.explanation : null;
  }
  equals(other) {
    if (!this.isValid || !other.isValid) {
      return false;
    }
    if (!this.loc.equals(other.loc)) {
      return false;
    }
    function eq(v1, v2) {
      if (v1 === undefined || v1 === 0)
        return v2 === undefined || v2 === 0;
      return v1 === v2;
    }
    for (const u of orderedUnits$1) {
      if (!eq(this.values[u], other.values[u])) {
        return false;
      }
    }
    return true;
  }
}
var INVALID$1 = "Invalid Interval";
function validateStartEnd(start, end) {
  if (!start || !start.isValid) {
    return Interval.invalid("missing or invalid start");
  } else if (!end || !end.isValid) {
    return Interval.invalid("missing or invalid end");
  } else if (end < start) {
    return Interval.invalid("end before start", `The end of an interval must be after its start, but you had start=${start.toISO()} and end=${end.toISO()}`);
  } else {
    return null;
  }
}

class Interval {
  constructor(config) {
    this.s = config.start;
    this.e = config.end;
    this.invalid = config.invalid || null;
    this.isLuxonInterval = true;
  }
  static invalid(reason, explanation = null) {
    if (!reason) {
      throw new InvalidArgumentError("need to specify a reason the Interval is invalid");
    }
    const invalid = reason instanceof Invalid ? reason : new Invalid(reason, explanation);
    if (Settings.throwOnInvalid) {
      throw new InvalidIntervalError(invalid);
    } else {
      return new Interval({ invalid });
    }
  }
  static fromDateTimes(start, end) {
    const builtStart = friendlyDateTime(start), builtEnd = friendlyDateTime(end);
    const validateError = validateStartEnd(builtStart, builtEnd);
    if (validateError == null) {
      return new Interval({
        start: builtStart,
        end: builtEnd
      });
    } else {
      return validateError;
    }
  }
  static after(start, duration) {
    const dur = Duration.fromDurationLike(duration), dt = friendlyDateTime(start);
    return Interval.fromDateTimes(dt, dt.plus(dur));
  }
  static before(end, duration) {
    const dur = Duration.fromDurationLike(duration), dt = friendlyDateTime(end);
    return Interval.fromDateTimes(dt.minus(dur), dt);
  }
  static fromISO(text, opts) {
    const [s2, e] = (text || "").split("/", 2);
    if (s2 && e) {
      let start, startIsValid;
      try {
        start = DateTime.fromISO(s2, opts);
        startIsValid = start.isValid;
      } catch (e2) {
        startIsValid = false;
      }
      let end, endIsValid;
      try {
        end = DateTime.fromISO(e, opts);
        endIsValid = end.isValid;
      } catch (e2) {
        endIsValid = false;
      }
      if (startIsValid && endIsValid) {
        return Interval.fromDateTimes(start, end);
      }
      if (startIsValid) {
        const dur = Duration.fromISO(e, opts);
        if (dur.isValid) {
          return Interval.after(start, dur);
        }
      } else if (endIsValid) {
        const dur = Duration.fromISO(s2, opts);
        if (dur.isValid) {
          return Interval.before(end, dur);
        }
      }
    }
    return Interval.invalid("unparsable", `the input "${text}" can't be parsed as ISO 8601`);
  }
  static isInterval(o) {
    return o && o.isLuxonInterval || false;
  }
  get start() {
    return this.isValid ? this.s : null;
  }
  get end() {
    return this.isValid ? this.e : null;
  }
  get lastDateTime() {
    return this.isValid ? this.e ? this.e.minus(1) : null : null;
  }
  get isValid() {
    return this.invalidReason === null;
  }
  get invalidReason() {
    return this.invalid ? this.invalid.reason : null;
  }
  get invalidExplanation() {
    return this.invalid ? this.invalid.explanation : null;
  }
  length(unit = "milliseconds") {
    return this.isValid ? this.toDuration(...[unit]).get(unit) : NaN;
  }
  count(unit = "milliseconds", opts) {
    if (!this.isValid)
      return NaN;
    const start = this.start.startOf(unit, opts);
    let end;
    if (opts?.useLocaleWeeks) {
      end = this.end.reconfigure({ locale: start.locale });
    } else {
      end = this.end;
    }
    end = end.startOf(unit, opts);
    return Math.floor(end.diff(start, unit).get(unit)) + (end.valueOf() !== this.end.valueOf());
  }
  hasSame(unit) {
    return this.isValid ? this.isEmpty() || this.e.minus(1).hasSame(this.s, unit) : false;
  }
  isEmpty() {
    return this.s.valueOf() === this.e.valueOf();
  }
  isAfter(dateTime) {
    if (!this.isValid)
      return false;
    return this.s > dateTime;
  }
  isBefore(dateTime) {
    if (!this.isValid)
      return false;
    return this.e <= dateTime;
  }
  contains(dateTime) {
    if (!this.isValid)
      return false;
    return this.s <= dateTime && this.e > dateTime;
  }
  set({ start, end } = {}) {
    if (!this.isValid)
      return this;
    return Interval.fromDateTimes(start || this.s, end || this.e);
  }
  splitAt(...dateTimes) {
    if (!this.isValid)
      return [];
    const sorted = dateTimes.map(friendlyDateTime).filter((d) => this.contains(d)).sort((a, b) => a.toMillis() - b.toMillis()), results = [];
    let { s: s2 } = this, i2 = 0;
    while (s2 < this.e) {
      const added = sorted[i2] || this.e, next = +added > +this.e ? this.e : added;
      results.push(Interval.fromDateTimes(s2, next));
      s2 = next;
      i2 += 1;
    }
    return results;
  }
  splitBy(duration) {
    const dur = Duration.fromDurationLike(duration);
    if (!this.isValid || !dur.isValid || dur.as("milliseconds") === 0) {
      return [];
    }
    let { s: s2 } = this, idx = 1, next;
    const results = [];
    while (s2 < this.e) {
      const added = this.start.plus(dur.mapUnits((x) => x * idx));
      next = +added > +this.e ? this.e : added;
      results.push(Interval.fromDateTimes(s2, next));
      s2 = next;
      idx += 1;
    }
    return results;
  }
  divideEqually(numberOfParts) {
    if (!this.isValid)
      return [];
    return this.splitBy(this.length() / numberOfParts).slice(0, numberOfParts);
  }
  overlaps(other) {
    return this.e > other.s && this.s < other.e;
  }
  abutsStart(other) {
    if (!this.isValid)
      return false;
    return +this.e === +other.s;
  }
  abutsEnd(other) {
    if (!this.isValid)
      return false;
    return +other.e === +this.s;
  }
  engulfs(other) {
    if (!this.isValid)
      return false;
    return this.s <= other.s && this.e >= other.e;
  }
  equals(other) {
    if (!this.isValid || !other.isValid) {
      return false;
    }
    return this.s.equals(other.s) && this.e.equals(other.e);
  }
  intersection(other) {
    if (!this.isValid)
      return this;
    const s2 = this.s > other.s ? this.s : other.s, e = this.e < other.e ? this.e : other.e;
    if (s2 >= e) {
      return null;
    } else {
      return Interval.fromDateTimes(s2, e);
    }
  }
  union(other) {
    if (!this.isValid)
      return this;
    const s2 = this.s < other.s ? this.s : other.s, e = this.e > other.e ? this.e : other.e;
    return Interval.fromDateTimes(s2, e);
  }
  static merge(intervals) {
    const [found, final] = intervals.sort((a, b) => a.s - b.s).reduce(([sofar, current], item) => {
      if (!current) {
        return [sofar, item];
      } else if (current.overlaps(item) || current.abutsStart(item)) {
        return [sofar, current.union(item)];
      } else {
        return [sofar.concat([current]), item];
      }
    }, [[], null]);
    if (final) {
      found.push(final);
    }
    return found;
  }
  static xor(intervals) {
    let start = null, currentCount = 0;
    const results = [], ends = intervals.map((i2) => [
      { time: i2.s, type: "s" },
      { time: i2.e, type: "e" }
    ]), flattened = Array.prototype.concat(...ends), arr = flattened.sort((a, b) => a.time - b.time);
    for (const i2 of arr) {
      currentCount += i2.type === "s" ? 1 : -1;
      if (currentCount === 1) {
        start = i2.time;
      } else {
        if (start && +start !== +i2.time) {
          results.push(Interval.fromDateTimes(start, i2.time));
        }
        start = null;
      }
    }
    return Interval.merge(results);
  }
  difference(...intervals) {
    return Interval.xor([this].concat(intervals)).map((i2) => this.intersection(i2)).filter((i2) => i2 && !i2.isEmpty());
  }
  toString() {
    if (!this.isValid)
      return INVALID$1;
    return `[${this.s.toISO()} – ${this.e.toISO()})`;
  }
  [Symbol.for("nodejs.util.inspect.custom")]() {
    if (this.isValid) {
      return `Interval { start: ${this.s.toISO()}, end: ${this.e.toISO()} }`;
    } else {
      return `Interval { Invalid, reason: ${this.invalidReason} }`;
    }
  }
  toLocaleString(formatOpts = DATE_SHORT, opts = {}) {
    return this.isValid ? Formatter.create(this.s.loc.clone(opts), formatOpts).formatInterval(this) : INVALID$1;
  }
  toISO(opts) {
    if (!this.isValid)
      return INVALID$1;
    return `${this.s.toISO(opts)}/${this.e.toISO(opts)}`;
  }
  toISODate() {
    if (!this.isValid)
      return INVALID$1;
    return `${this.s.toISODate()}/${this.e.toISODate()}`;
  }
  toISOTime(opts) {
    if (!this.isValid)
      return INVALID$1;
    return `${this.s.toISOTime(opts)}/${this.e.toISOTime(opts)}`;
  }
  toFormat(dateFormat, { separator = " – " } = {}) {
    if (!this.isValid)
      return INVALID$1;
    return `${this.s.toFormat(dateFormat)}${separator}${this.e.toFormat(dateFormat)}`;
  }
  toDuration(unit, opts) {
    if (!this.isValid) {
      return Duration.invalid(this.invalidReason);
    }
    return this.e.diff(this.s, unit, opts);
  }
  mapEndpoints(mapFn) {
    return Interval.fromDateTimes(mapFn(this.s), mapFn(this.e));
  }
}

class Info {
  static hasDST(zone = Settings.defaultZone) {
    const proto = DateTime.now().setZone(zone).set({ month: 12 });
    return !zone.isUniversal && proto.offset !== proto.set({ month: 6 }).offset;
  }
  static isValidIANAZone(zone) {
    return IANAZone.isValidZone(zone);
  }
  static normalizeZone(input) {
    return normalizeZone(input, Settings.defaultZone);
  }
  static getStartOfWeek({ locale = null, locObj = null } = {}) {
    return (locObj || Locale.create(locale)).getStartOfWeek();
  }
  static getMinimumDaysInFirstWeek({ locale = null, locObj = null } = {}) {
    return (locObj || Locale.create(locale)).getMinDaysInFirstWeek();
  }
  static getWeekendWeekdays({ locale = null, locObj = null } = {}) {
    return (locObj || Locale.create(locale)).getWeekendDays().slice();
  }
  static months(length = "long", { locale = null, numberingSystem = null, locObj = null, outputCalendar = "gregory" } = {}) {
    return (locObj || Locale.create(locale, numberingSystem, outputCalendar)).months(length);
  }
  static monthsFormat(length = "long", { locale = null, numberingSystem = null, locObj = null, outputCalendar = "gregory" } = {}) {
    return (locObj || Locale.create(locale, numberingSystem, outputCalendar)).months(length, true);
  }
  static weekdays(length = "long", { locale = null, numberingSystem = null, locObj = null } = {}) {
    return (locObj || Locale.create(locale, numberingSystem, null)).weekdays(length);
  }
  static weekdaysFormat(length = "long", { locale = null, numberingSystem = null, locObj = null } = {}) {
    return (locObj || Locale.create(locale, numberingSystem, null)).weekdays(length, true);
  }
  static meridiems({ locale = null } = {}) {
    return Locale.create(locale).meridiems();
  }
  static eras(length = "short", { locale = null } = {}) {
    return Locale.create(locale, null, "gregory").eras(length);
  }
  static features() {
    return { relative: hasRelative(), localeWeek: hasLocaleWeekInfo() };
  }
}
function dayDiff(earlier, later) {
  const utcDayStart = (dt) => dt.toUTC(0, { keepLocalTime: true }).startOf("day").valueOf(), ms = utcDayStart(later) - utcDayStart(earlier);
  return Math.floor(Duration.fromMillis(ms).as("days"));
}
function highOrderDiffs(cursor, later, units) {
  const differs = [
    ["years", (a, b) => b.year - a.year],
    ["quarters", (a, b) => b.quarter - a.quarter + (b.year - a.year) * 4],
    ["months", (a, b) => b.month - a.month + (b.year - a.year) * 12],
    [
      "weeks",
      (a, b) => {
        const days = dayDiff(a, b);
        return (days - days % 7) / 7;
      }
    ],
    ["days", dayDiff]
  ];
  const results = {};
  const earlier = cursor;
  let lowestOrder, highWater;
  for (const [unit, differ] of differs) {
    if (units.indexOf(unit) >= 0) {
      lowestOrder = unit;
      results[unit] = differ(cursor, later);
      highWater = earlier.plus(results);
      if (highWater > later) {
        results[unit]--;
        cursor = earlier.plus(results);
        if (cursor > later) {
          highWater = cursor;
          results[unit]--;
          cursor = earlier.plus(results);
        }
      } else {
        cursor = highWater;
      }
    }
  }
  return [cursor, results, highWater, lowestOrder];
}
function diff(earlier, later, units, opts) {
  let [cursor, results, highWater, lowestOrder] = highOrderDiffs(earlier, later, units);
  const remainingMillis = later - cursor;
  const lowerOrderUnits = units.filter((u) => ["hours", "minutes", "seconds", "milliseconds"].indexOf(u) >= 0);
  if (lowerOrderUnits.length === 0) {
    if (highWater < later) {
      highWater = cursor.plus({ [lowestOrder]: 1 });
    }
    if (highWater !== cursor) {
      results[lowestOrder] = (results[lowestOrder] || 0) + remainingMillis / (highWater - cursor);
    }
  }
  const duration = Duration.fromObject(results, opts);
  if (lowerOrderUnits.length > 0) {
    return Duration.fromMillis(remainingMillis, opts).shiftTo(...lowerOrderUnits).plus(duration);
  } else {
    return duration;
  }
}
var MISSING_FTP = "missing Intl.DateTimeFormat.formatToParts support";
function intUnit(regex, post = (i2) => i2) {
  return { regex, deser: ([s2]) => post(parseDigits(s2)) };
}
var NBSP = String.fromCharCode(160);
var spaceOrNBSP = `[ ${NBSP}]`;
var spaceOrNBSPRegExp = new RegExp(spaceOrNBSP, "g");
function fixListRegex(s2) {
  return s2.replace(/\./g, "\\.?").replace(spaceOrNBSPRegExp, spaceOrNBSP);
}
function stripInsensitivities(s2) {
  return s2.replace(/\./g, "").replace(spaceOrNBSPRegExp, " ").toLowerCase();
}
function oneOf(strings, startIndex) {
  if (strings === null) {
    return null;
  } else {
    return {
      regex: RegExp(strings.map(fixListRegex).join("|")),
      deser: ([s2]) => strings.findIndex((i2) => stripInsensitivities(s2) === stripInsensitivities(i2)) + startIndex
    };
  }
}
function offset(regex, groups) {
  return { regex, deser: ([, h, m]) => signedOffset(h, m), groups };
}
function simple(regex) {
  return { regex, deser: ([s2]) => s2 };
}
function escapeToken(value) {
  return value.replace(/[\-\[\]{}()*+?.,\\\^$|#\s]/g, "\\$&");
}
function unitForToken(token, loc) {
  const one = digitRegex(loc), two = digitRegex(loc, "{2}"), three = digitRegex(loc, "{3}"), four = digitRegex(loc, "{4}"), six = digitRegex(loc, "{6}"), oneOrTwo = digitRegex(loc, "{1,2}"), oneToThree = digitRegex(loc, "{1,3}"), oneToSix = digitRegex(loc, "{1,6}"), oneToNine = digitRegex(loc, "{1,9}"), twoToFour = digitRegex(loc, "{2,4}"), fourToSix = digitRegex(loc, "{4,6}"), literal = (t) => ({ regex: RegExp(escapeToken(t.val)), deser: ([s2]) => s2, literal: true }), unitate = (t) => {
    if (token.literal) {
      return literal(t);
    }
    switch (t.val) {
      case "G":
        return oneOf(loc.eras("short"), 0);
      case "GG":
        return oneOf(loc.eras("long"), 0);
      case "y":
        return intUnit(oneToSix);
      case "yy":
        return intUnit(twoToFour, untruncateYear);
      case "yyyy":
        return intUnit(four);
      case "yyyyy":
        return intUnit(fourToSix);
      case "yyyyyy":
        return intUnit(six);
      case "M":
        return intUnit(oneOrTwo);
      case "MM":
        return intUnit(two);
      case "MMM":
        return oneOf(loc.months("short", true), 1);
      case "MMMM":
        return oneOf(loc.months("long", true), 1);
      case "L":
        return intUnit(oneOrTwo);
      case "LL":
        return intUnit(two);
      case "LLL":
        return oneOf(loc.months("short", false), 1);
      case "LLLL":
        return oneOf(loc.months("long", false), 1);
      case "d":
        return intUnit(oneOrTwo);
      case "dd":
        return intUnit(two);
      case "o":
        return intUnit(oneToThree);
      case "ooo":
        return intUnit(three);
      case "HH":
        return intUnit(two);
      case "H":
        return intUnit(oneOrTwo);
      case "hh":
        return intUnit(two);
      case "h":
        return intUnit(oneOrTwo);
      case "mm":
        return intUnit(two);
      case "m":
        return intUnit(oneOrTwo);
      case "q":
        return intUnit(oneOrTwo);
      case "qq":
        return intUnit(two);
      case "s":
        return intUnit(oneOrTwo);
      case "ss":
        return intUnit(two);
      case "S":
        return intUnit(oneToThree);
      case "SSS":
        return intUnit(three);
      case "u":
        return simple(oneToNine);
      case "uu":
        return simple(oneOrTwo);
      case "uuu":
        return intUnit(one);
      case "a":
        return oneOf(loc.meridiems(), 0);
      case "kkkk":
        return intUnit(four);
      case "kk":
        return intUnit(twoToFour, untruncateYear);
      case "W":
        return intUnit(oneOrTwo);
      case "WW":
        return intUnit(two);
      case "E":
      case "c":
        return intUnit(one);
      case "EEE":
        return oneOf(loc.weekdays("short", false), 1);
      case "EEEE":
        return oneOf(loc.weekdays("long", false), 1);
      case "ccc":
        return oneOf(loc.weekdays("short", true), 1);
      case "cccc":
        return oneOf(loc.weekdays("long", true), 1);
      case "Z":
      case "ZZ":
        return offset(new RegExp(`([+-]${oneOrTwo.source})(?::(${two.source}))?`), 2);
      case "ZZZ":
        return offset(new RegExp(`([+-]${oneOrTwo.source})(${two.source})?`), 2);
      case "z":
        return simple(/[a-z_+-/]{1,256}?/i);
      case " ":
        return simple(/[^\S\n\r]/);
      default:
        return literal(t);
    }
  };
  const unit = unitate(token) || {
    invalidReason: MISSING_FTP
  };
  unit.token = token;
  return unit;
}
var partTypeStyleToTokenVal = {
  year: {
    "2-digit": "yy",
    numeric: "yyyyy"
  },
  month: {
    numeric: "M",
    "2-digit": "MM",
    short: "MMM",
    long: "MMMM"
  },
  day: {
    numeric: "d",
    "2-digit": "dd"
  },
  weekday: {
    short: "EEE",
    long: "EEEE"
  },
  dayperiod: "a",
  dayPeriod: "a",
  hour12: {
    numeric: "h",
    "2-digit": "hh"
  },
  hour24: {
    numeric: "H",
    "2-digit": "HH"
  },
  minute: {
    numeric: "m",
    "2-digit": "mm"
  },
  second: {
    numeric: "s",
    "2-digit": "ss"
  },
  timeZoneName: {
    long: "ZZZZZ",
    short: "ZZZ"
  }
};
function tokenForPart(part, formatOpts, resolvedOpts) {
  const { type, value } = part;
  if (type === "literal") {
    const isSpace = /^\s+$/.test(value);
    return {
      literal: !isSpace,
      val: isSpace ? " " : value
    };
  }
  const style = formatOpts[type];
  let actualType = type;
  if (type === "hour") {
    if (formatOpts.hour12 != null) {
      actualType = formatOpts.hour12 ? "hour12" : "hour24";
    } else if (formatOpts.hourCycle != null) {
      if (formatOpts.hourCycle === "h11" || formatOpts.hourCycle === "h12") {
        actualType = "hour12";
      } else {
        actualType = "hour24";
      }
    } else {
      actualType = resolvedOpts.hour12 ? "hour12" : "hour24";
    }
  }
  let val = partTypeStyleToTokenVal[actualType];
  if (typeof val === "object") {
    val = val[style];
  }
  if (val) {
    return {
      literal: false,
      val
    };
  }
  return;
}
function buildRegex(units) {
  const re = units.map((u) => u.regex).reduce((f, r) => `${f}(${r.source})`, "");
  return [`^${re}$`, units];
}
function match(input, regex, handlers) {
  const matches = input.match(regex);
  if (matches) {
    const all3 = {};
    let matchIndex = 1;
    for (const i2 in handlers) {
      if (hasOwnProperty3(handlers, i2)) {
        const h = handlers[i2], groups = h.groups ? h.groups + 1 : 1;
        if (!h.literal && h.token) {
          all3[h.token.val[0]] = h.deser(matches.slice(matchIndex, matchIndex + groups));
        }
        matchIndex += groups;
      }
    }
    return [matches, all3];
  } else {
    return [matches, {}];
  }
}
function dateTimeFromMatches(matches) {
  const toField = (token) => {
    switch (token) {
      case "S":
        return "millisecond";
      case "s":
        return "second";
      case "m":
        return "minute";
      case "h":
      case "H":
        return "hour";
      case "d":
        return "day";
      case "o":
        return "ordinal";
      case "L":
      case "M":
        return "month";
      case "y":
        return "year";
      case "E":
      case "c":
        return "weekday";
      case "W":
        return "weekNumber";
      case "k":
        return "weekYear";
      case "q":
        return "quarter";
      default:
        return null;
    }
  };
  let zone = null;
  let specificOffset;
  if (!isUndefined3(matches.z)) {
    zone = IANAZone.create(matches.z);
  }
  if (!isUndefined3(matches.Z)) {
    if (!zone) {
      zone = new FixedOffsetZone(matches.Z);
    }
    specificOffset = matches.Z;
  }
  if (!isUndefined3(matches.q)) {
    matches.M = (matches.q - 1) * 3 + 1;
  }
  if (!isUndefined3(matches.h)) {
    if (matches.h < 12 && matches.a === 1) {
      matches.h += 12;
    } else if (matches.h === 12 && matches.a === 0) {
      matches.h = 0;
    }
  }
  if (matches.G === 0 && matches.y) {
    matches.y = -matches.y;
  }
  if (!isUndefined3(matches.u)) {
    matches.S = parseMillis(matches.u);
  }
  const vals = Object.keys(matches).reduce((r, k) => {
    const f = toField(k);
    if (f) {
      r[f] = matches[k];
    }
    return r;
  }, {});
  return [vals, zone, specificOffset];
}
var dummyDateTimeCache = null;
function getDummyDateTime() {
  if (!dummyDateTimeCache) {
    dummyDateTimeCache = DateTime.fromMillis(1555555555555);
  }
  return dummyDateTimeCache;
}
function maybeExpandMacroToken(token, locale) {
  if (token.literal) {
    return token;
  }
  const formatOpts = Formatter.macroTokenToFormatOpts(token.val);
  const tokens = formatOptsToTokens(formatOpts, locale);
  if (tokens == null || tokens.includes(undefined)) {
    return token;
  }
  return tokens;
}
function expandMacroTokens(tokens, locale) {
  return Array.prototype.concat(...tokens.map((t) => maybeExpandMacroToken(t, locale)));
}

class TokenParser {
  constructor(locale, format2) {
    this.locale = locale;
    this.format = format2;
    this.tokens = expandMacroTokens(Formatter.parseFormat(format2), locale);
    this.units = this.tokens.map((t) => unitForToken(t, locale));
    this.disqualifyingUnit = this.units.find((t) => t.invalidReason);
    if (!this.disqualifyingUnit) {
      const [regexString, handlers] = buildRegex(this.units);
      this.regex = RegExp(regexString, "i");
      this.handlers = handlers;
    }
  }
  explainFromTokens(input) {
    if (!this.isValid) {
      return { input, tokens: this.tokens, invalidReason: this.invalidReason };
    } else {
      const [rawMatches, matches] = match(input, this.regex, this.handlers), [result, zone, specificOffset] = matches ? dateTimeFromMatches(matches) : [null, null, undefined];
      if (hasOwnProperty3(matches, "a") && hasOwnProperty3(matches, "H")) {
        throw new ConflictingSpecificationError("Can't include meridiem when specifying 24-hour format");
      }
      return {
        input,
        tokens: this.tokens,
        regex: this.regex,
        rawMatches,
        matches,
        result,
        zone,
        specificOffset
      };
    }
  }
  get isValid() {
    return !this.disqualifyingUnit;
  }
  get invalidReason() {
    return this.disqualifyingUnit ? this.disqualifyingUnit.invalidReason : null;
  }
}
function explainFromTokens(locale, input, format2) {
  const parser = new TokenParser(locale, format2);
  return parser.explainFromTokens(input);
}
function parseFromTokens(locale, input, format2) {
  const { result, zone, specificOffset, invalidReason } = explainFromTokens(locale, input, format2);
  return [result, zone, specificOffset, invalidReason];
}
function formatOptsToTokens(formatOpts, locale) {
  if (!formatOpts) {
    return null;
  }
  const formatter = Formatter.create(locale, formatOpts);
  const df = formatter.dtFormatter(getDummyDateTime());
  const parts = df.formatToParts();
  const resolvedOpts = df.resolvedOptions();
  return parts.map((p) => tokenForPart(p, formatOpts, resolvedOpts));
}
var INVALID = "Invalid DateTime";
var MAX_DATE = 8640000000000000;
function unsupportedZone(zone) {
  return new Invalid("unsupported zone", `the zone "${zone.name}" is not supported`);
}
function possiblyCachedWeekData(dt) {
  if (dt.weekData === null) {
    dt.weekData = gregorianToWeek(dt.c);
  }
  return dt.weekData;
}
function possiblyCachedLocalWeekData(dt) {
  if (dt.localWeekData === null) {
    dt.localWeekData = gregorianToWeek(dt.c, dt.loc.getMinDaysInFirstWeek(), dt.loc.getStartOfWeek());
  }
  return dt.localWeekData;
}
function clone(inst, alts) {
  const current = {
    ts: inst.ts,
    zone: inst.zone,
    c: inst.c,
    o: inst.o,
    loc: inst.loc,
    invalid: inst.invalid
  };
  return new DateTime({ ...current, ...alts, old: current });
}
function fixOffset(localTS, o, tz) {
  let utcGuess = localTS - o * 60 * 1000;
  const o2 = tz.offset(utcGuess);
  if (o === o2) {
    return [utcGuess, o];
  }
  utcGuess -= (o2 - o) * 60 * 1000;
  const o3 = tz.offset(utcGuess);
  if (o2 === o3) {
    return [utcGuess, o2];
  }
  return [localTS - Math.min(o2, o3) * 60 * 1000, Math.max(o2, o3)];
}
function tsToObj(ts, offset2) {
  ts += offset2 * 60 * 1000;
  const d = new Date(ts);
  return {
    year: d.getUTCFullYear(),
    month: d.getUTCMonth() + 1,
    day: d.getUTCDate(),
    hour: d.getUTCHours(),
    minute: d.getUTCMinutes(),
    second: d.getUTCSeconds(),
    millisecond: d.getUTCMilliseconds()
  };
}
function objToTS(obj, offset2, zone) {
  return fixOffset(objToLocalTS(obj), offset2, zone);
}
function adjustTime(inst, dur) {
  const oPre = inst.o, year = inst.c.year + Math.trunc(dur.years), month = inst.c.month + Math.trunc(dur.months) + Math.trunc(dur.quarters) * 3, c = {
    ...inst.c,
    year,
    month,
    day: Math.min(inst.c.day, daysInMonth(year, month)) + Math.trunc(dur.days) + Math.trunc(dur.weeks) * 7
  }, millisToAdd = Duration.fromObject({
    years: dur.years - Math.trunc(dur.years),
    quarters: dur.quarters - Math.trunc(dur.quarters),
    months: dur.months - Math.trunc(dur.months),
    weeks: dur.weeks - Math.trunc(dur.weeks),
    days: dur.days - Math.trunc(dur.days),
    hours: dur.hours,
    minutes: dur.minutes,
    seconds: dur.seconds,
    milliseconds: dur.milliseconds
  }).as("milliseconds"), localTS = objToLocalTS(c);
  let [ts, o] = fixOffset(localTS, oPre, inst.zone);
  if (millisToAdd !== 0) {
    ts += millisToAdd;
    o = inst.zone.offset(ts);
  }
  return { ts, o };
}
function parseDataToDateTime(parsed, parsedZone, opts, format2, text, specificOffset) {
  const { setZone, zone } = opts;
  if (parsed && Object.keys(parsed).length !== 0 || parsedZone) {
    const interpretationZone = parsedZone || zone, inst = DateTime.fromObject(parsed, {
      ...opts,
      zone: interpretationZone,
      specificOffset
    });
    return setZone ? inst : inst.setZone(zone);
  } else {
    return DateTime.invalid(new Invalid("unparsable", `the input "${text}" can't be parsed as ${format2}`));
  }
}
function toTechFormat(dt, format2, allowZ = true) {
  return dt.isValid ? Formatter.create(Locale.create("en-US"), {
    allowZ,
    forceSimple: true
  }).formatDateTimeFromString(dt, format2) : null;
}
function toISODate(o, extended, precision) {
  const longFormat = o.c.year > 9999 || o.c.year < 0;
  let c = "";
  if (longFormat && o.c.year >= 0)
    c += "+";
  c += padStart(o.c.year, longFormat ? 6 : 4);
  if (precision === "year")
    return c;
  if (extended) {
    c += "-";
    c += padStart(o.c.month);
    if (precision === "month")
      return c;
    c += "-";
  } else {
    c += padStart(o.c.month);
    if (precision === "month")
      return c;
  }
  c += padStart(o.c.day);
  return c;
}
function toISOTime(o, extended, suppressSeconds, suppressMilliseconds, includeOffset, extendedZone, precision) {
  let showSeconds = !suppressSeconds || o.c.millisecond !== 0 || o.c.second !== 0, c = "";
  switch (precision) {
    case "day":
    case "month":
    case "year":
      break;
    default:
      c += padStart(o.c.hour);
      if (precision === "hour")
        break;
      if (extended) {
        c += ":";
        c += padStart(o.c.minute);
        if (precision === "minute")
          break;
        if (showSeconds) {
          c += ":";
          c += padStart(o.c.second);
        }
      } else {
        c += padStart(o.c.minute);
        if (precision === "minute")
          break;
        if (showSeconds) {
          c += padStart(o.c.second);
        }
      }
      if (precision === "second")
        break;
      if (showSeconds && (!suppressMilliseconds || o.c.millisecond !== 0)) {
        c += ".";
        c += padStart(o.c.millisecond, 3);
      }
  }
  if (includeOffset) {
    if (o.isOffsetFixed && o.offset === 0 && !extendedZone) {
      c += "Z";
    } else if (o.o < 0) {
      c += "-";
      c += padStart(Math.trunc(-o.o / 60));
      c += ":";
      c += padStart(Math.trunc(-o.o % 60));
    } else {
      c += "+";
      c += padStart(Math.trunc(o.o / 60));
      c += ":";
      c += padStart(Math.trunc(o.o % 60));
    }
  }
  if (extendedZone) {
    c += "[" + o.zone.ianaName + "]";
  }
  return c;
}
var defaultUnitValues = {
  month: 1,
  day: 1,
  hour: 0,
  minute: 0,
  second: 0,
  millisecond: 0
};
var defaultWeekUnitValues = {
  weekNumber: 1,
  weekday: 1,
  hour: 0,
  minute: 0,
  second: 0,
  millisecond: 0
};
var defaultOrdinalUnitValues = {
  ordinal: 1,
  hour: 0,
  minute: 0,
  second: 0,
  millisecond: 0
};
var orderedUnits = ["year", "month", "day", "hour", "minute", "second", "millisecond"];
var orderedWeekUnits = [
  "weekYear",
  "weekNumber",
  "weekday",
  "hour",
  "minute",
  "second",
  "millisecond"
];
var orderedOrdinalUnits = ["year", "ordinal", "hour", "minute", "second", "millisecond"];
function normalizeUnit(unit) {
  const normalized = {
    year: "year",
    years: "year",
    month: "month",
    months: "month",
    day: "day",
    days: "day",
    hour: "hour",
    hours: "hour",
    minute: "minute",
    minutes: "minute",
    quarter: "quarter",
    quarters: "quarter",
    second: "second",
    seconds: "second",
    millisecond: "millisecond",
    milliseconds: "millisecond",
    weekday: "weekday",
    weekdays: "weekday",
    weeknumber: "weekNumber",
    weeksnumber: "weekNumber",
    weeknumbers: "weekNumber",
    weekyear: "weekYear",
    weekyears: "weekYear",
    ordinal: "ordinal"
  }[unit.toLowerCase()];
  if (!normalized)
    throw new InvalidUnitError(unit);
  return normalized;
}
function normalizeUnitWithLocalWeeks(unit) {
  switch (unit.toLowerCase()) {
    case "localweekday":
    case "localweekdays":
      return "localWeekday";
    case "localweeknumber":
    case "localweeknumbers":
      return "localWeekNumber";
    case "localweekyear":
    case "localweekyears":
      return "localWeekYear";
    default:
      return normalizeUnit(unit);
  }
}
function guessOffsetForZone(zone) {
  if (zoneOffsetTs === undefined) {
    zoneOffsetTs = Settings.now();
  }
  if (zone.type !== "iana") {
    return zone.offset(zoneOffsetTs);
  }
  const zoneName = zone.name;
  let offsetGuess = zoneOffsetGuessCache.get(zoneName);
  if (offsetGuess === undefined) {
    offsetGuess = zone.offset(zoneOffsetTs);
    zoneOffsetGuessCache.set(zoneName, offsetGuess);
  }
  return offsetGuess;
}
function quickDT(obj, opts) {
  const zone = normalizeZone(opts.zone, Settings.defaultZone);
  if (!zone.isValid) {
    return DateTime.invalid(unsupportedZone(zone));
  }
  const loc = Locale.fromObject(opts);
  let ts, o;
  if (!isUndefined3(obj.year)) {
    for (const u of orderedUnits) {
      if (isUndefined3(obj[u])) {
        obj[u] = defaultUnitValues[u];
      }
    }
    const invalid = hasInvalidGregorianData(obj) || hasInvalidTimeData(obj);
    if (invalid) {
      return DateTime.invalid(invalid);
    }
    const offsetProvis = guessOffsetForZone(zone);
    [ts, o] = objToTS(obj, offsetProvis, zone);
  } else {
    ts = Settings.now();
  }
  return new DateTime({ ts, zone, loc, o });
}
function diffRelative(start, end, opts) {
  const round = isUndefined3(opts.round) ? true : opts.round, rounding = isUndefined3(opts.rounding) ? "trunc" : opts.rounding, format2 = (c, unit) => {
    c = roundTo(c, round || opts.calendary ? 0 : 2, opts.calendary ? "round" : rounding);
    const formatter = end.loc.clone(opts).relFormatter(opts);
    return formatter.format(c, unit);
  }, differ = (unit) => {
    if (opts.calendary) {
      if (!end.hasSame(start, unit)) {
        return end.startOf(unit).diff(start.startOf(unit), unit).get(unit);
      } else
        return 0;
    } else {
      return end.diff(start, unit).get(unit);
    }
  };
  if (opts.unit) {
    return format2(differ(opts.unit), opts.unit);
  }
  for (const unit of opts.units) {
    const count = differ(unit);
    if (Math.abs(count) >= 1) {
      return format2(count, unit);
    }
  }
  return format2(start > end ? -0 : 0, opts.units[opts.units.length - 1]);
}
function lastOpts(argList) {
  let opts = {}, args;
  if (argList.length > 0 && typeof argList[argList.length - 1] === "object") {
    opts = argList[argList.length - 1];
    args = Array.from(argList).slice(0, argList.length - 1);
  } else {
    args = Array.from(argList);
  }
  return [opts, args];
}
var zoneOffsetTs;
var zoneOffsetGuessCache = new Map;

class DateTime {
  constructor(config) {
    const zone = config.zone || Settings.defaultZone;
    let invalid = config.invalid || (Number.isNaN(config.ts) ? new Invalid("invalid input") : null) || (!zone.isValid ? unsupportedZone(zone) : null);
    this.ts = isUndefined3(config.ts) ? Settings.now() : config.ts;
    let c = null, o = null;
    if (!invalid) {
      const unchanged = config.old && config.old.ts === this.ts && config.old.zone.equals(zone);
      if (unchanged) {
        [c, o] = [config.old.c, config.old.o];
      } else {
        const ot = isNumber3(config.o) && !config.old ? config.o : zone.offset(this.ts);
        c = tsToObj(this.ts, ot);
        invalid = Number.isNaN(c.year) ? new Invalid("invalid input") : null;
        c = invalid ? null : c;
        o = invalid ? null : ot;
      }
    }
    this._zone = zone;
    this.loc = config.loc || Locale.create();
    this.invalid = invalid;
    this.weekData = null;
    this.localWeekData = null;
    this.c = c;
    this.o = o;
    this.isLuxonDateTime = true;
  }
  static now() {
    return new DateTime({});
  }
  static local() {
    const [opts, args] = lastOpts(arguments), [year, month, day, hour, minute, second, millisecond] = args;
    return quickDT({ year, month, day, hour, minute, second, millisecond }, opts);
  }
  static utc() {
    const [opts, args] = lastOpts(arguments), [year, month, day, hour, minute, second, millisecond] = args;
    opts.zone = FixedOffsetZone.utcInstance;
    return quickDT({ year, month, day, hour, minute, second, millisecond }, opts);
  }
  static fromJSDate(date, options = {}) {
    const ts = isDate3(date) ? date.valueOf() : NaN;
    if (Number.isNaN(ts)) {
      return DateTime.invalid("invalid input");
    }
    const zoneToUse = normalizeZone(options.zone, Settings.defaultZone);
    if (!zoneToUse.isValid) {
      return DateTime.invalid(unsupportedZone(zoneToUse));
    }
    return new DateTime({
      ts,
      zone: zoneToUse,
      loc: Locale.fromObject(options)
    });
  }
  static fromMillis(milliseconds, options = {}) {
    if (!isNumber3(milliseconds)) {
      throw new InvalidArgumentError(`fromMillis requires a numerical input, but received a ${typeof milliseconds} with value ${milliseconds}`);
    } else if (milliseconds < -MAX_DATE || milliseconds > MAX_DATE) {
      return DateTime.invalid("Timestamp out of range");
    } else {
      return new DateTime({
        ts: milliseconds,
        zone: normalizeZone(options.zone, Settings.defaultZone),
        loc: Locale.fromObject(options)
      });
    }
  }
  static fromSeconds(seconds, options = {}) {
    if (!isNumber3(seconds)) {
      throw new InvalidArgumentError("fromSeconds requires a numerical input");
    } else {
      return new DateTime({
        ts: seconds * 1000,
        zone: normalizeZone(options.zone, Settings.defaultZone),
        loc: Locale.fromObject(options)
      });
    }
  }
  static fromObject(obj, opts = {}) {
    obj = obj || {};
    const zoneToUse = normalizeZone(opts.zone, Settings.defaultZone);
    if (!zoneToUse.isValid) {
      return DateTime.invalid(unsupportedZone(zoneToUse));
    }
    const loc = Locale.fromObject(opts);
    const normalized = normalizeObject(obj, normalizeUnitWithLocalWeeks);
    const { minDaysInFirstWeek, startOfWeek } = usesLocalWeekValues(normalized, loc);
    const tsNow = Settings.now(), offsetProvis = !isUndefined3(opts.specificOffset) ? opts.specificOffset : zoneToUse.offset(tsNow), containsOrdinal = !isUndefined3(normalized.ordinal), containsGregorYear = !isUndefined3(normalized.year), containsGregorMD = !isUndefined3(normalized.month) || !isUndefined3(normalized.day), containsGregor = containsGregorYear || containsGregorMD, definiteWeekDef = normalized.weekYear || normalized.weekNumber;
    if ((containsGregor || containsOrdinal) && definiteWeekDef) {
      throw new ConflictingSpecificationError("Can't mix weekYear/weekNumber units with year/month/day or ordinals");
    }
    if (containsGregorMD && containsOrdinal) {
      throw new ConflictingSpecificationError("Can't mix ordinal dates with month/day");
    }
    const useWeekData = definiteWeekDef || normalized.weekday && !containsGregor;
    let units, defaultValues, objNow = tsToObj(tsNow, offsetProvis);
    if (useWeekData) {
      units = orderedWeekUnits;
      defaultValues = defaultWeekUnitValues;
      objNow = gregorianToWeek(objNow, minDaysInFirstWeek, startOfWeek);
    } else if (containsOrdinal) {
      units = orderedOrdinalUnits;
      defaultValues = defaultOrdinalUnitValues;
      objNow = gregorianToOrdinal(objNow);
    } else {
      units = orderedUnits;
      defaultValues = defaultUnitValues;
    }
    let foundFirst = false;
    for (const u of units) {
      const v = normalized[u];
      if (!isUndefined3(v)) {
        foundFirst = true;
      } else if (foundFirst) {
        normalized[u] = defaultValues[u];
      } else {
        normalized[u] = objNow[u];
      }
    }
    const higherOrderInvalid = useWeekData ? hasInvalidWeekData(normalized, minDaysInFirstWeek, startOfWeek) : containsOrdinal ? hasInvalidOrdinalData(normalized) : hasInvalidGregorianData(normalized), invalid = higherOrderInvalid || hasInvalidTimeData(normalized);
    if (invalid) {
      return DateTime.invalid(invalid);
    }
    const gregorian = useWeekData ? weekToGregorian(normalized, minDaysInFirstWeek, startOfWeek) : containsOrdinal ? ordinalToGregorian(normalized) : normalized, [tsFinal, offsetFinal] = objToTS(gregorian, offsetProvis, zoneToUse), inst = new DateTime({
      ts: tsFinal,
      zone: zoneToUse,
      o: offsetFinal,
      loc
    });
    if (normalized.weekday && containsGregor && obj.weekday !== inst.weekday) {
      return DateTime.invalid("mismatched weekday", `you can't specify both a weekday of ${normalized.weekday} and a date of ${inst.toISO()}`);
    }
    if (!inst.isValid) {
      return DateTime.invalid(inst.invalid);
    }
    return inst;
  }
  static fromISO(text, opts = {}) {
    const [vals, parsedZone] = parseISODate(text);
    return parseDataToDateTime(vals, parsedZone, opts, "ISO 8601", text);
  }
  static fromRFC2822(text, opts = {}) {
    const [vals, parsedZone] = parseRFC2822Date(text);
    return parseDataToDateTime(vals, parsedZone, opts, "RFC 2822", text);
  }
  static fromHTTP(text, opts = {}) {
    const [vals, parsedZone] = parseHTTPDate(text);
    return parseDataToDateTime(vals, parsedZone, opts, "HTTP", opts);
  }
  static fromFormat(text, fmt, opts = {}) {
    if (isUndefined3(text) || isUndefined3(fmt)) {
      throw new InvalidArgumentError("fromFormat requires an input string and a format");
    }
    const { locale = null, numberingSystem = null } = opts, localeToUse = Locale.fromOpts({
      locale,
      numberingSystem,
      defaultToEN: true
    }), [vals, parsedZone, specificOffset, invalid] = parseFromTokens(localeToUse, text, fmt);
    if (invalid) {
      return DateTime.invalid(invalid);
    } else {
      return parseDataToDateTime(vals, parsedZone, opts, `format ${fmt}`, text, specificOffset);
    }
  }
  static fromString(text, fmt, opts = {}) {
    return DateTime.fromFormat(text, fmt, opts);
  }
  static fromSQL(text, opts = {}) {
    const [vals, parsedZone] = parseSQL(text);
    return parseDataToDateTime(vals, parsedZone, opts, "SQL", text);
  }
  static invalid(reason, explanation = null) {
    if (!reason) {
      throw new InvalidArgumentError("need to specify a reason the DateTime is invalid");
    }
    const invalid = reason instanceof Invalid ? reason : new Invalid(reason, explanation);
    if (Settings.throwOnInvalid) {
      throw new InvalidDateTimeError(invalid);
    } else {
      return new DateTime({ invalid });
    }
  }
  static isDateTime(o) {
    return o && o.isLuxonDateTime || false;
  }
  static parseFormatForOpts(formatOpts, localeOpts = {}) {
    const tokenList = formatOptsToTokens(formatOpts, Locale.fromObject(localeOpts));
    return !tokenList ? null : tokenList.map((t) => t ? t.val : null).join("");
  }
  static expandFormat(fmt, localeOpts = {}) {
    const expanded = expandMacroTokens(Formatter.parseFormat(fmt), Locale.fromObject(localeOpts));
    return expanded.map((t) => t.val).join("");
  }
  static resetCache() {
    zoneOffsetTs = undefined;
    zoneOffsetGuessCache.clear();
  }
  get(unit) {
    return this[unit];
  }
  get isValid() {
    return this.invalid === null;
  }
  get invalidReason() {
    return this.invalid ? this.invalid.reason : null;
  }
  get invalidExplanation() {
    return this.invalid ? this.invalid.explanation : null;
  }
  get locale() {
    return this.isValid ? this.loc.locale : null;
  }
  get numberingSystem() {
    return this.isValid ? this.loc.numberingSystem : null;
  }
  get outputCalendar() {
    return this.isValid ? this.loc.outputCalendar : null;
  }
  get zone() {
    return this._zone;
  }
  get zoneName() {
    return this.isValid ? this.zone.name : null;
  }
  get year() {
    return this.isValid ? this.c.year : NaN;
  }
  get quarter() {
    return this.isValid ? Math.ceil(this.c.month / 3) : NaN;
  }
  get month() {
    return this.isValid ? this.c.month : NaN;
  }
  get day() {
    return this.isValid ? this.c.day : NaN;
  }
  get hour() {
    return this.isValid ? this.c.hour : NaN;
  }
  get minute() {
    return this.isValid ? this.c.minute : NaN;
  }
  get second() {
    return this.isValid ? this.c.second : NaN;
  }
  get millisecond() {
    return this.isValid ? this.c.millisecond : NaN;
  }
  get weekYear() {
    return this.isValid ? possiblyCachedWeekData(this).weekYear : NaN;
  }
  get weekNumber() {
    return this.isValid ? possiblyCachedWeekData(this).weekNumber : NaN;
  }
  get weekday() {
    return this.isValid ? possiblyCachedWeekData(this).weekday : NaN;
  }
  get isWeekend() {
    return this.isValid && this.loc.getWeekendDays().includes(this.weekday);
  }
  get localWeekday() {
    return this.isValid ? possiblyCachedLocalWeekData(this).weekday : NaN;
  }
  get localWeekNumber() {
    return this.isValid ? possiblyCachedLocalWeekData(this).weekNumber : NaN;
  }
  get localWeekYear() {
    return this.isValid ? possiblyCachedLocalWeekData(this).weekYear : NaN;
  }
  get ordinal() {
    return this.isValid ? gregorianToOrdinal(this.c).ordinal : NaN;
  }
  get monthShort() {
    return this.isValid ? Info.months("short", { locObj: this.loc })[this.month - 1] : null;
  }
  get monthLong() {
    return this.isValid ? Info.months("long", { locObj: this.loc })[this.month - 1] : null;
  }
  get weekdayShort() {
    return this.isValid ? Info.weekdays("short", { locObj: this.loc })[this.weekday - 1] : null;
  }
  get weekdayLong() {
    return this.isValid ? Info.weekdays("long", { locObj: this.loc })[this.weekday - 1] : null;
  }
  get offset() {
    return this.isValid ? +this.o : NaN;
  }
  get offsetNameShort() {
    if (this.isValid) {
      return this.zone.offsetName(this.ts, {
        format: "short",
        locale: this.locale
      });
    } else {
      return null;
    }
  }
  get offsetNameLong() {
    if (this.isValid) {
      return this.zone.offsetName(this.ts, {
        format: "long",
        locale: this.locale
      });
    } else {
      return null;
    }
  }
  get isOffsetFixed() {
    return this.isValid ? this.zone.isUniversal : null;
  }
  get isInDST() {
    if (this.isOffsetFixed) {
      return false;
    } else {
      return this.offset > this.set({ month: 1, day: 1 }).offset || this.offset > this.set({ month: 5 }).offset;
    }
  }
  getPossibleOffsets() {
    if (!this.isValid || this.isOffsetFixed) {
      return [this];
    }
    const dayMs = 86400000;
    const minuteMs = 60000;
    const localTS = objToLocalTS(this.c);
    const oEarlier = this.zone.offset(localTS - dayMs);
    const oLater = this.zone.offset(localTS + dayMs);
    const o1 = this.zone.offset(localTS - oEarlier * minuteMs);
    const o2 = this.zone.offset(localTS - oLater * minuteMs);
    if (o1 === o2) {
      return [this];
    }
    const ts1 = localTS - o1 * minuteMs;
    const ts2 = localTS - o2 * minuteMs;
    const c1 = tsToObj(ts1, o1);
    const c2 = tsToObj(ts2, o2);
    if (c1.hour === c2.hour && c1.minute === c2.minute && c1.second === c2.second && c1.millisecond === c2.millisecond) {
      return [clone(this, { ts: ts1 }), clone(this, { ts: ts2 })];
    }
    return [this];
  }
  get isInLeapYear() {
    return isLeapYear(this.year);
  }
  get daysInMonth() {
    return daysInMonth(this.year, this.month);
  }
  get daysInYear() {
    return this.isValid ? daysInYear(this.year) : NaN;
  }
  get weeksInWeekYear() {
    return this.isValid ? weeksInWeekYear(this.weekYear) : NaN;
  }
  get weeksInLocalWeekYear() {
    return this.isValid ? weeksInWeekYear(this.localWeekYear, this.loc.getMinDaysInFirstWeek(), this.loc.getStartOfWeek()) : NaN;
  }
  resolvedLocaleOptions(opts = {}) {
    const { locale, numberingSystem, calendar } = Formatter.create(this.loc.clone(opts), opts).resolvedOptions(this);
    return { locale, numberingSystem, outputCalendar: calendar };
  }
  toUTC(offset2 = 0, opts = {}) {
    return this.setZone(FixedOffsetZone.instance(offset2), opts);
  }
  toLocal() {
    return this.setZone(Settings.defaultZone);
  }
  setZone(zone, { keepLocalTime = false, keepCalendarTime = false } = {}) {
    zone = normalizeZone(zone, Settings.defaultZone);
    if (zone.equals(this.zone)) {
      return this;
    } else if (!zone.isValid) {
      return DateTime.invalid(unsupportedZone(zone));
    } else {
      let newTS = this.ts;
      if (keepLocalTime || keepCalendarTime) {
        const offsetGuess = zone.offset(this.ts);
        const asObj = this.toObject();
        [newTS] = objToTS(asObj, offsetGuess, zone);
      }
      return clone(this, { ts: newTS, zone });
    }
  }
  reconfigure({ locale, numberingSystem, outputCalendar } = {}) {
    const loc = this.loc.clone({ locale, numberingSystem, outputCalendar });
    return clone(this, { loc });
  }
  setLocale(locale) {
    return this.reconfigure({ locale });
  }
  set(values) {
    if (!this.isValid)
      return this;
    const normalized = normalizeObject(values, normalizeUnitWithLocalWeeks);
    const { minDaysInFirstWeek, startOfWeek } = usesLocalWeekValues(normalized, this.loc);
    const settingWeekStuff = !isUndefined3(normalized.weekYear) || !isUndefined3(normalized.weekNumber) || !isUndefined3(normalized.weekday), containsOrdinal = !isUndefined3(normalized.ordinal), containsGregorYear = !isUndefined3(normalized.year), containsGregorMD = !isUndefined3(normalized.month) || !isUndefined3(normalized.day), containsGregor = containsGregorYear || containsGregorMD, definiteWeekDef = normalized.weekYear || normalized.weekNumber;
    if ((containsGregor || containsOrdinal) && definiteWeekDef) {
      throw new ConflictingSpecificationError("Can't mix weekYear/weekNumber units with year/month/day or ordinals");
    }
    if (containsGregorMD && containsOrdinal) {
      throw new ConflictingSpecificationError("Can't mix ordinal dates with month/day");
    }
    let mixed;
    if (settingWeekStuff) {
      mixed = weekToGregorian({ ...gregorianToWeek(this.c, minDaysInFirstWeek, startOfWeek), ...normalized }, minDaysInFirstWeek, startOfWeek);
    } else if (!isUndefined3(normalized.ordinal)) {
      mixed = ordinalToGregorian({ ...gregorianToOrdinal(this.c), ...normalized });
    } else {
      mixed = { ...this.toObject(), ...normalized };
      if (isUndefined3(normalized.day)) {
        mixed.day = Math.min(daysInMonth(mixed.year, mixed.month), mixed.day);
      }
    }
    const [ts, o] = objToTS(mixed, this.o, this.zone);
    return clone(this, { ts, o });
  }
  plus(duration) {
    if (!this.isValid)
      return this;
    const dur = Duration.fromDurationLike(duration);
    return clone(this, adjustTime(this, dur));
  }
  minus(duration) {
    if (!this.isValid)
      return this;
    const dur = Duration.fromDurationLike(duration).negate();
    return clone(this, adjustTime(this, dur));
  }
  startOf(unit, { useLocaleWeeks = false } = {}) {
    if (!this.isValid)
      return this;
    const o = {}, normalizedUnit = Duration.normalizeUnit(unit);
    switch (normalizedUnit) {
      case "years":
        o.month = 1;
      case "quarters":
      case "months":
        o.day = 1;
      case "weeks":
      case "days":
        o.hour = 0;
      case "hours":
        o.minute = 0;
      case "minutes":
        o.second = 0;
      case "seconds":
        o.millisecond = 0;
        break;
    }
    if (normalizedUnit === "weeks") {
      if (useLocaleWeeks) {
        const startOfWeek = this.loc.getStartOfWeek();
        const { weekday } = this;
        if (weekday < startOfWeek) {
          o.weekNumber = this.weekNumber - 1;
        }
        o.weekday = startOfWeek;
      } else {
        o.weekday = 1;
      }
    }
    if (normalizedUnit === "quarters") {
      const q = Math.ceil(this.month / 3);
      o.month = (q - 1) * 3 + 1;
    }
    return this.set(o);
  }
  endOf(unit, opts) {
    return this.isValid ? this.plus({ [unit]: 1 }).startOf(unit, opts).minus(1) : this;
  }
  toFormat(fmt, opts = {}) {
    return this.isValid ? Formatter.create(this.loc.redefaultToEN(opts)).formatDateTimeFromString(this, fmt) : INVALID;
  }
  toLocaleString(formatOpts = DATE_SHORT, opts = {}) {
    return this.isValid ? Formatter.create(this.loc.clone(opts), formatOpts).formatDateTime(this) : INVALID;
  }
  toLocaleParts(opts = {}) {
    return this.isValid ? Formatter.create(this.loc.clone(opts), opts).formatDateTimeParts(this) : [];
  }
  toISO({
    format: format2 = "extended",
    suppressSeconds = false,
    suppressMilliseconds = false,
    includeOffset = true,
    extendedZone = false,
    precision = "milliseconds"
  } = {}) {
    if (!this.isValid) {
      return null;
    }
    precision = normalizeUnit(precision);
    const ext = format2 === "extended";
    let c = toISODate(this, ext, precision);
    if (orderedUnits.indexOf(precision) >= 3)
      c += "T";
    c += toISOTime(this, ext, suppressSeconds, suppressMilliseconds, includeOffset, extendedZone, precision);
    return c;
  }
  toISODate({ format: format2 = "extended", precision = "day" } = {}) {
    if (!this.isValid) {
      return null;
    }
    return toISODate(this, format2 === "extended", normalizeUnit(precision));
  }
  toISOWeekDate() {
    return toTechFormat(this, "kkkk-'W'WW-c");
  }
  toISOTime({
    suppressMilliseconds = false,
    suppressSeconds = false,
    includeOffset = true,
    includePrefix = false,
    extendedZone = false,
    format: format2 = "extended",
    precision = "milliseconds"
  } = {}) {
    if (!this.isValid) {
      return null;
    }
    precision = normalizeUnit(precision);
    let c = includePrefix && orderedUnits.indexOf(precision) >= 3 ? "T" : "";
    return c + toISOTime(this, format2 === "extended", suppressSeconds, suppressMilliseconds, includeOffset, extendedZone, precision);
  }
  toRFC2822() {
    return toTechFormat(this, "EEE, dd LLL yyyy HH:mm:ss ZZZ", false);
  }
  toHTTP() {
    return toTechFormat(this.toUTC(), "EEE, dd LLL yyyy HH:mm:ss 'GMT'");
  }
  toSQLDate() {
    if (!this.isValid) {
      return null;
    }
    return toISODate(this, true);
  }
  toSQLTime({ includeOffset = true, includeZone = false, includeOffsetSpace = true } = {}) {
    let fmt = "HH:mm:ss.SSS";
    if (includeZone || includeOffset) {
      if (includeOffsetSpace) {
        fmt += " ";
      }
      if (includeZone) {
        fmt += "z";
      } else if (includeOffset) {
        fmt += "ZZ";
      }
    }
    return toTechFormat(this, fmt, true);
  }
  toSQL(opts = {}) {
    if (!this.isValid) {
      return null;
    }
    return `${this.toSQLDate()} ${this.toSQLTime(opts)}`;
  }
  toString() {
    return this.isValid ? this.toISO() : INVALID;
  }
  [Symbol.for("nodejs.util.inspect.custom")]() {
    if (this.isValid) {
      return `DateTime { ts: ${this.toISO()}, zone: ${this.zone.name}, locale: ${this.locale} }`;
    } else {
      return `DateTime { Invalid, reason: ${this.invalidReason} }`;
    }
  }
  valueOf() {
    return this.toMillis();
  }
  toMillis() {
    return this.isValid ? this.ts : NaN;
  }
  toSeconds() {
    return this.isValid ? this.ts / 1000 : NaN;
  }
  toUnixInteger() {
    return this.isValid ? Math.floor(this.ts / 1000) : NaN;
  }
  toJSON() {
    return this.toISO();
  }
  toBSON() {
    return this.toJSDate();
  }
  toObject(opts = {}) {
    if (!this.isValid)
      return {};
    const base = { ...this.c };
    if (opts.includeConfig) {
      base.outputCalendar = this.outputCalendar;
      base.numberingSystem = this.loc.numberingSystem;
      base.locale = this.loc.locale;
    }
    return base;
  }
  toJSDate() {
    return new Date(this.isValid ? this.ts : NaN);
  }
  diff(otherDateTime, unit = "milliseconds", opts = {}) {
    if (!this.isValid || !otherDateTime.isValid) {
      return Duration.invalid("created by diffing an invalid DateTime");
    }
    const durOpts = { locale: this.locale, numberingSystem: this.numberingSystem, ...opts };
    const units = maybeArray(unit).map(Duration.normalizeUnit), otherIsLater = otherDateTime.valueOf() > this.valueOf(), earlier = otherIsLater ? this : otherDateTime, later = otherIsLater ? otherDateTime : this, diffed = diff(earlier, later, units, durOpts);
    return otherIsLater ? diffed.negate() : diffed;
  }
  diffNow(unit = "milliseconds", opts = {}) {
    return this.diff(DateTime.now(), unit, opts);
  }
  until(otherDateTime) {
    return this.isValid ? Interval.fromDateTimes(this, otherDateTime) : this;
  }
  hasSame(otherDateTime, unit, opts) {
    if (!this.isValid)
      return false;
    const inputMs = otherDateTime.valueOf();
    const adjustedToZone = this.setZone(otherDateTime.zone, { keepLocalTime: true });
    return adjustedToZone.startOf(unit, opts) <= inputMs && inputMs <= adjustedToZone.endOf(unit, opts);
  }
  equals(other) {
    return this.isValid && other.isValid && this.valueOf() === other.valueOf() && this.zone.equals(other.zone) && this.loc.equals(other.loc);
  }
  toRelative(options = {}) {
    if (!this.isValid)
      return null;
    const base = options.base || DateTime.fromObject({}, { zone: this.zone }), padding = options.padding ? this < base ? -options.padding : options.padding : 0;
    let units = ["years", "months", "days", "hours", "minutes", "seconds"];
    let unit = options.unit;
    if (Array.isArray(options.unit)) {
      units = options.unit;
      unit = undefined;
    }
    return diffRelative(base, this.plus(padding), {
      ...options,
      numeric: "always",
      units,
      unit
    });
  }
  toRelativeCalendar(options = {}) {
    if (!this.isValid)
      return null;
    return diffRelative(options.base || DateTime.fromObject({}, { zone: this.zone }), this, {
      ...options,
      numeric: "auto",
      units: ["years", "months", "days"],
      calendary: true
    });
  }
  static min(...dateTimes) {
    if (!dateTimes.every(DateTime.isDateTime)) {
      throw new InvalidArgumentError("min requires all arguments be DateTimes");
    }
    return bestBy(dateTimes, (i2) => i2.valueOf(), Math.min);
  }
  static max(...dateTimes) {
    if (!dateTimes.every(DateTime.isDateTime)) {
      throw new InvalidArgumentError("max requires all arguments be DateTimes");
    }
    return bestBy(dateTimes, (i2) => i2.valueOf(), Math.max);
  }
  static fromFormatExplain(text, fmt, options = {}) {
    const { locale = null, numberingSystem = null } = options, localeToUse = Locale.fromOpts({
      locale,
      numberingSystem,
      defaultToEN: true
    });
    return explainFromTokens(localeToUse, text, fmt);
  }
  static fromStringExplain(text, fmt, options = {}) {
    return DateTime.fromFormatExplain(text, fmt, options);
  }
  static buildFormatParser(fmt, options = {}) {
    const { locale = null, numberingSystem = null } = options, localeToUse = Locale.fromOpts({
      locale,
      numberingSystem,
      defaultToEN: true
    });
    return new TokenParser(localeToUse, fmt);
  }
  static fromFormatParser(text, formatParser, opts = {}) {
    if (isUndefined3(text) || isUndefined3(formatParser)) {
      throw new InvalidArgumentError("fromFormatParser requires an input string and a format parser");
    }
    const { locale = null, numberingSystem = null } = opts, localeToUse = Locale.fromOpts({
      locale,
      numberingSystem,
      defaultToEN: true
    });
    if (!localeToUse.equals(formatParser.locale)) {
      throw new InvalidArgumentError(`fromFormatParser called with a locale of ${localeToUse}, ` + `but the format parser was created for ${formatParser.locale}`);
    }
    const { result, zone, specificOffset, invalidReason } = formatParser.explainFromTokens(text);
    if (invalidReason) {
      return DateTime.invalid(invalidReason);
    } else {
      return parseDataToDateTime(result, zone, opts, `format ${formatParser.format}`, text, specificOffset);
    }
  }
  static get DATE_SHORT() {
    return DATE_SHORT;
  }
  static get DATE_MED() {
    return DATE_MED;
  }
  static get DATE_MED_WITH_WEEKDAY() {
    return DATE_MED_WITH_WEEKDAY;
  }
  static get DATE_FULL() {
    return DATE_FULL;
  }
  static get DATE_HUGE() {
    return DATE_HUGE;
  }
  static get TIME_SIMPLE() {
    return TIME_SIMPLE;
  }
  static get TIME_WITH_SECONDS() {
    return TIME_WITH_SECONDS;
  }
  static get TIME_WITH_SHORT_OFFSET() {
    return TIME_WITH_SHORT_OFFSET;
  }
  static get TIME_WITH_LONG_OFFSET() {
    return TIME_WITH_LONG_OFFSET;
  }
  static get TIME_24_SIMPLE() {
    return TIME_24_SIMPLE;
  }
  static get TIME_24_WITH_SECONDS() {
    return TIME_24_WITH_SECONDS;
  }
  static get TIME_24_WITH_SHORT_OFFSET() {
    return TIME_24_WITH_SHORT_OFFSET;
  }
  static get TIME_24_WITH_LONG_OFFSET() {
    return TIME_24_WITH_LONG_OFFSET;
  }
  static get DATETIME_SHORT() {
    return DATETIME_SHORT;
  }
  static get DATETIME_SHORT_WITH_SECONDS() {
    return DATETIME_SHORT_WITH_SECONDS;
  }
  static get DATETIME_MED() {
    return DATETIME_MED;
  }
  static get DATETIME_MED_WITH_SECONDS() {
    return DATETIME_MED_WITH_SECONDS;
  }
  static get DATETIME_MED_WITH_WEEKDAY() {
    return DATETIME_MED_WITH_WEEKDAY;
  }
  static get DATETIME_FULL() {
    return DATETIME_FULL;
  }
  static get DATETIME_FULL_WITH_SECONDS() {
    return DATETIME_FULL_WITH_SECONDS;
  }
  static get DATETIME_HUGE() {
    return DATETIME_HUGE;
  }
  static get DATETIME_HUGE_WITH_SECONDS() {
    return DATETIME_HUGE_WITH_SECONDS;
  }
}
function friendlyDateTime(dateTimeish) {
  if (DateTime.isDateTime(dateTimeish)) {
    return dateTimeish;
  } else if (dateTimeish && dateTimeish.valueOf && isNumber3(dateTimeish.valueOf())) {
    return DateTime.fromJSDate(dateTimeish);
  } else if (dateTimeish && typeof dateTimeish === "object") {
    return DateTime.fromObject(dateTimeish);
  } else {
    throw new InvalidArgumentError(`Unknown datetime argument: ${dateTimeish}, of type ${typeof dateTimeish}`);
  }
}

// src/watchdog.ts
class StatusWatchdog {
  statusConnectedRouter;
  lastUpdate = DateTime.now();
  client;
  lastRouterName = " ... ";
  state = "none";
  static command = "tikbook.cmd.connected-router.configure";
  pollInterval;
  lastRouterResources;
  lastStatusMessage;
  lastLspConnectionUrl;
  toolTipStyles = {
    error: {
      backgroundColor: new import_vscode4.ThemeColor("statusBarItem.errorBackground"),
      color: new import_vscode4.ThemeColor("statusBarItem.errorForeground")
    },
    "http error": {
      backgroundColor: new import_vscode4.ThemeColor("statusBarItem.errorBackground"),
      color: new import_vscode4.ThemeColor("statusBarItem.errorForeground")
    },
    inflight: {
      backgroundColor: new import_vscode4.ThemeColor("statusBarItem.warningBackground"),
      color: new import_vscode4.ThemeColor("statusBarItem.warningForeground")
    },
    normal: {},
    none: {}
  };
  constructor(context) {
    this.client = RouterRestClient.default;
    context.subscriptions.push(import_vscode4.commands.registerCommand(StatusWatchdog.command, () => this.onClick()));
    this.statusConnectedRouter = import_vscode4.window.createStatusBarItem(import_vscode4.StatusBarAlignment.Left, 100);
    this.statusConnectedRouter.command = StatusWatchdog.command;
    context.subscriptions.push(this.onConfigurationChange(), this.statusConnectedRouter, RouterRestClient.default.onHttpResponseError((e) => {
      this.triggerUpdate("error", e);
    }), RouterRestClient.default.onHttpRequestError((e) => {
      this.triggerUpdate("http error", e);
    }), RouterRestClient.default.onHttpRequestSuccess((e) => this.triggerUpdate("inflight", `${e.method?.toUpperCase()} ${e.url}`)), RouterRestClient.default.onHttpResponseSuccess((e) => this.triggerUpdate("normal", e.statusText)));
    this.triggerUpdate("none", "Initializing...");
    setTimeout(() => this.checkRouter(), 1000);
    this.pollInterval = setInterval(() => {
      if (this.state != "normal")
        this.checkRouter();
      if (this.lastUpdate.diffNow() > Duration.fromMillis(0 - (getSettings().apiTimeout * 1000 * 2 + 1000)))
        this.checkRouter();
    }, getSettings().apiTimeout * 1000 + 1000);
  }
  dispose() {
    this.statusConnectedRouter.dispose();
    this.pollInterval.close();
  }
  onConfigurationChange() {
    return import_vscode4.workspace.onDidChangeConfiguration((e) => {
      if (e.affectsConfiguration("tikbook")) {
        log.info("<StatusWatchdog> relevant config change received");
        if (e.affectsConfiguration("tikbook.provideLspServerCredentials")) {
          if (import_vscode4.workspace.getConfiguration("tikbook").get("provideLspServerCredentials") === false) {
            import_vscode4.commands.executeCommand("routeroslsp.server.clearConnectionUrl").then((dirty) => log.info(`<StatusWatchdog> sent LSP [routeroslsp.server.clearConnectionUrl] successfully (dirty=${dirty})`), (error) => log.warn(`<StatusWatchdog> {onConfigurationChange} calling [routeroslsp.server.clearConnectionUrl] got exception`, error));
          }
        }
        this.checkRouter();
      }
    });
  }
  triggerUpdate(state, msg) {
    this.state = state;
    if (typeof msg === "object")
      msg = getTextFromError(msg);
    if (msg)
      this.lastStatusMessage = msg;
    this.setStatusBar(this.toolTipStyles[state]);
  }
  setStatusBar(style) {
    this.lastUpdate = DateTime.now();
    this.statusConnectedRouter.text = `$(mikrotik-icon-line) ${this.lastRouterName} `;
    this.statusConnectedRouter.tooltip = this.getStatusMarkdown();
    this.statusConnectedRouter.backgroundColor = style.backgroundColor;
    this.statusConnectedRouter.color = style.color;
    this.statusConnectedRouter.show();
  }
  getStatusMarkdown() {
    let mdStatus = "";
    mdStatus += `## RouterOS \`${this.lastRouterName}\`
`;
    const url = getConnectionUrlString();
    if (url) {
      mdStatus += `TikBook using **${url.toString()}**

`;
      if (this.lastLspConnectionUrl) {
        mdStatus += `RouterOS LSP using **${this.lastLspConnectionUrl}**

`;
      }
      mdStatus += `
`;
      if (this.lastRouterResources) {
        mdStatus += `### System Resources
`;
        mdStatus += `| | |
| ---: | :--- |
`;
        Object.keys(this.lastRouterResources).map((e) => `| **${e}**: | ${this.lastRouterResources[e]}|`).forEach((t) => mdStatus += `${t}
`);
      }
    } else {
      mdStatus += `### **INVALID SETTINGS**
`;
      mdStatus += `Setting \`baseUri\` is not valid.  RouterOS device must be configured and online for many features.

`;
    }
    if (this.state !== "normal") {
      mdStatus += `### **${this.state.toUpperCase()}**
`;
      if (this.lastStatusMessage) {
        mdStatus += `\`\`\`
${this.lastStatusMessage.toString().replace("`", "\\`")}
\`\`\`

`;
      }
    }
    mdStatus += `
_last updated ${this.lastUpdate.toLocaleString(DateTime.DATETIME_SHORT)}_
`;
    return new import_vscode4.MarkdownString(mdStatus);
  }
  async onClick() {
    this.checkRouter();
    if (this.state == "normal")
      import_vscode4.commands.executeCommand("tikbook.show.menu.main");
    else
      import_vscode4.commands.executeCommand("tikbook.show.menu.setup");
  }
  async updateLspConnectionUrl() {
    const routeroslspExtension = import_vscode4.extensions.getExtension("TIKOCI.lsp-routeros-ts");
    if (routeroslspExtension) {
      import_vscode4.commands.executeCommand("routeroslsp.server.getConnectionUrl").then((urlString) => this.lastLspConnectionUrl = urlString, (error) => log.warn(`<StatusWatchdog> {getLspConnectionurl} failed: ${error}`));
    }
  }
  async syncLspConnectionUrl() {
    const { baseUrl, username, password, apiTimeout, provideLspServerCredentials, checkCertificates } = getSettings();
    const routeroslspExtension = import_vscode4.extensions.getExtension("TIKOCI.lsp-routeros-ts");
    if (routeroslspExtension) {
      if (provideLspServerCredentials) {
        log.debug(`<StatusWatchdog> {syncLspConnectionUrl} invoked`);
        try {
          return await import_vscode4.commands.executeCommand("routeroslsp.server.useConnectionUrl", "TikBook", baseUrl, username, await SecretManager.default.getPassword() || password, apiTimeout, checkCertificates);
        } catch (error) {
          log.warn(`<StatusWatchdog> {syncLspConnectionUrl} exception from [routeroslsp.server.useConnectionUrl] ${JSON.stringify(error)}`);
        }
      }
    } else {
      log.warn(`<StatusWatchdog> {syncLspConnectionUrl} RouterOS LSP Extension not found`);
    }
    return false;
  }
  async checkRouter() {
    log.debug("<StatusWatchdog> checking router...");
    this.lastUpdate = DateTime.now();
    try {
      this.updateLspConnectionUrl();
      const axiosResponse = await this.client.getRawIdentity();
      this.lastRouterName = axiosResponse.data?.name;
      if (this.lastRouterName !== null) {
        this.lastRouterResources = await this.client.getSystemResources();
        this.triggerUpdate("normal", "Router connection check successful");
        if (await this.syncLspConnectionUrl()) {
          import_vscode4.commands.executeCommand("routeroslsp.cmd.testConnection");
        }
        log.info("<StatusWatchdog> check was successful for ", this.lastRouterName);
      } else {
        this.lastRouterResources = undefined;
        this.triggerUpdate("error", `Failed to get RouterOS name (/system/identity)

\${`);
      }
    } catch {
      this.lastRouterResources = undefined;
      log.error("<StatusWatchdog> check failed to ", getConnectionUrlString());
    }
  }
}
function getTextFromError(error) {
  let errText = "";
  if (error.code && error.message) {
    switch (error.code) {
      case "ECONNABORTED": {
        errText += `${error.code} No response (${error.message})`;
        break;
      }
      case "HOSTDOWN": {
        errText += `${error.code} No response (${error.message})`;
        break;
      }
      case "ECONNREFUSED": {
        errText += `${error.code} Perhaps wrong port number/protocol in Base Url? Or, firewall blocking? (${error.message})`;
        break;
      }
      case "ERR_TLS_CERT_ALTNAME_INVALID": {
        errText += `${error.code} Perhaps disable 'Check Certificates' in Settings? (${error.message})`;
        break;
      }
      case "ERR_BAD_REQUEST": {
        if (error.status) {
          switch (error.status) {
            case 401: {
              errText += `HTTP error ${error.status} - username or password are wrong`;
              break;
            }
            case 404: {
              errText += `HTTP error ${error.status} - either hostname is wrong or an additional path is bad.`;
              break;
            }
            default:
              errText += `HTTP unknown error ${error.status} ${error.code} ${error.message} )`;
              break;
          }
          break;
        }
        break;
      }
      default:
        errText += `${error.message} (${error.code})`;
    }
  } else if (error.message) {
    errText += `${error.message} ${error.name ? `(${error.name})` : ""}`;
  } else {
    errText += error.toString ? error.toString() : "Unknown error without data";
  }
  return errText;
}

// src/notebook.ts
var import_vscode5 = require("vscode");
var encoding = "utf-8";
function initializeNotebookEngines() {
  const killswitch = new import_vscode5.CancellationTokenSource;
  return [
    import_vscode5.workspace.registerNotebookSerializer("tikbook", new ScriptSerializer, {
      transientOutputs: true,
      transientCellMetadata: {
        inputCollapsed: true,
        outputCollapsed: true
      }
    }),
    import_vscode5.workspace.registerNotebookSerializer("routeros", new ScriptSerializer, {
      transientOutputs: true,
      transientCellMetadata: {
        inputCollapsed: true,
        outputCollapsed: true
      }
    }),
    import_vscode5.workspace.registerNotebookSerializer("markdown-routeros", new MarkdownSerializer, {
      transientOutputs: true,
      transientCellMetadata: {
        inputCollapsed: true,
        outputCollapsed: true
      }
    }),
    import_vscode5.workspace.registerNotebookSerializer("interactive", new ScriptSerializer, {
      transientOutputs: true,
      transientCellMetadata: {
        inputCollapsed: true,
        outputCollapsed: true
      }
    }),
    new TikbookController,
    new RscController,
    new ReplController,
    new MarkdownController,
    import_vscode5.commands.registerCommand("tikbook.new.notebook.markdown", () => import_vscode5.workspace.openNotebookDocument("markdown-routeros", new import_vscode5.NotebookData([])).then((nb) => import_vscode5.window.showNotebookDocument(nb))),
    import_vscode5.commands.registerCommand("tikbook.new.notebook", () => import_vscode5.workspace.openNotebookDocument("tikbook", new import_vscode5.NotebookData([])).then((nb) => import_vscode5.window.showNotebookDocument(nb))),
    import_vscode5.commands.registerCommand("tikbook.new.notebook.repl", async () => {
      await import_vscode5.commands.executeCommand("interactive.open", undefined, undefined, `lesnitsky.tikbook-easy-lens/interactive-tikbook`, undefined);
    }),
    import_vscode5.commands.registerCommand("tikbook.notebook.clone.routeros", async (uri) => {
      let nb;
      if (uri) {
        import_vscode5.workspace.openNotebookDocument("tikbook", await import_vscode5.commands.executeCommand("vscode.executeDataToNotebook", "routeros-markdown", new TextEncoder().encode((await import_vscode5.workspace.openTextDocument(uri)).getText())));
      } else {
        nb = import_vscode5.window.activeNotebookEditor?.notebook;
      }
      if (nb) {
        copyNotebookAs(nb, "tikbook");
      } else {
        log.error(`<notebook> [tikbook.notebook.clone.routeros] got no notebook`);
      }
    }),
    import_vscode5.commands.registerCommand("tikbook.notebook.clone.markdown", async (uri) => {
      let nb;
      if (uri) {
        import_vscode5.workspace.openNotebookDocument("markdown-routeros", await import_vscode5.commands.executeCommand("vscode.executeDataToNotebook", "tikbook", new TextEncoder().encode((await import_vscode5.workspace.openTextDocument(uri)).getText())));
      } else {
        nb = import_vscode5.window.activeNotebookEditor?.notebook;
      }
      if (nb) {
        copyNotebookAs(nb, "markdown-routeros");
      } else {
        log.error(`<notebook> [tikbook.notebook.clone.markdown] got no notebook`);
      }
    }),
    import_vscode5.commands.registerCommand("tikbook.new.notebook.router.scripts", async () => {
      const uri = import_vscode5.Uri.parse("rscena:all-scripts.md.rsc?scripts.tikbook");
      const textDocument = await import_vscode5.workspace.openTextDocument(uri);
      const content = textDocument.getText();
      const buffer = new TextEncoder().encode(content);
      const notebookData = await new ScriptSerializer().deserializeNotebook(buffer, killswitch.token);
      import_vscode5.window.showNotebookDocument(await import_vscode5.workspace.openNotebookDocument("tikbook", notebookData));
    }),
    import_vscode5.commands.registerCommand("tikbook.notebook.markdown.preview.markdown", async (_uri) => {
      import_vscode5.commands.executeCommand("markdown.showPreviewToSide", _uri);
    }),
    import_vscode5.commands.registerCommand("tikbook.notebook.reopen.routeros", async (uri) => {
      const targetUri = uri;
      if (!targetUri) {
        import_vscode5.window.showWarningMessage("No document is found to open in [tikbook.notebook.reopen.routeros] command");
        log.warn(`[tikbook.notebook.reopen.routeros] found no uri for vscode.openWith`);
        return;
      }
      if (import_vscode5.window.activeNotebookEditor?.notebook.isUntitled || import_vscode5.window.activeTextEditor?.document.isUntitled) {
        import_vscode5.window.showWarningMessage(`Untitled documents cannot previewed. Save file to enable RouterOS script view.`, "Save As...", "Cancel").then((selection) => {
          if (selection === "Save As...") {
            import_vscode5.commands.executeCommand("workbench.action.files.save").then((e) => log.info(JSON.stringify(e)));
          }
        });
        return;
      }
      try {
        import_vscode5.commands.executeCommand("vscode.openWith", uri, "default", import_vscode5.ViewColumn.Beside);
        log.debug(`[tikbook.notebook.reopen.routeros] vscode.openWith ${uri.toString(true)} called`);
      } catch (error) {
        log.warn("[tikbook.notebook.reopen.routeros] Error opening with notebook:", error);
        import_vscode5.window.showWarningMessage(`Exception opening text document from notebook using ${uri.toString()}`);
      }
    })
  ];
}
async function convertNotebookFormat(nb, newFormat) {
  const scriptSerializer = new ScriptSerializer;
  const markdownSerializer = new MarkdownSerializer;
  if (nb.isDirty || nb.isUntitled) {
    const msg = "Document must be saved before copy to new notebook format.";
    import_vscode5.window.showWarningMessage(msg);
    log.info(`<notebook.convertNotebookFormat> warned '${msg}'`, nb.uri.toString(), newFormat);
    return null;
  }
  const text = (await import_vscode5.workspace.openTextDocument(nb.uri)).getText();
  if (nb.notebookType == newFormat)
    return nb;
  const serializer = newFormat == "markdown-routeros" ? scriptSerializer : markdownSerializer;
  const killswitch = new import_vscode5.CancellationTokenSource;
  const notebookData = await serializer.deserializeNotebook(new TextEncoder().encode(text), killswitch.token);
  return import_vscode5.workspace.openNotebookDocument(newFormat, { cells: notebookData.cells, metadata: notebookData.metadata });
}
async function copyNotebookAs(notebook, newNotebookType) {
  if (notebook && notebook.notebookType) {
    log.debug("<notebook.copyNotebookAs> has notebook, prompting user to create copy", notebook.uri.toString(), newNotebookType);
    import_vscode5.window.showInformationMessage(`Create new copy in '${newNotebookType}' notebook format?`, { modal: true, detail: "Note: Future changes are not synced between notebook formats." }, "Create Copy").then(async (e) => {
      if (e === "Create Copy") {
        log.debug("<notebook.copyNotebookAs> attempting file copy+show after user confirm");
        const newNotebook = await convertNotebookFormat(notebook, newNotebookType);
        if (newNotebook)
          import_vscode5.window.showNotebookDocument(newNotebook);
      } else {
        log.debug("<notebook.createNotebookCopy> skipped", notebook.uri.toString(), newNotebookType);
      }
    });
  } else {
    const msg = "No notebook found to copy";
    import_vscode5.window.showWarningMessage(msg);
    log.debug(`<notebook.copyNotebookAs> warned user '${msg}'`, notebook.uri.toString(), newNotebookType);
  }
}

class MarkdownSerializer {
  serializeNotebook(data, _) {
    return new TextEncoder().encode(`[//]: #!tikbook

` + data.cells.map((c, i2, a) => {
      switch (c.kind) {
        case import_vscode5.NotebookCellKind.Code: {
          const code2 = c.value.trim();
          if (code2.match(/^[\s]+$/))
            return "";
          return `\`\`\`routeros
${code2}
\`\`\`

`;
        }
        case import_vscode5.NotebookCellKind.Markup: {
          const md = c.value.trim();
          if (md.match(/^[\s]+$/))
            return "";
          if (a[i2 - 1] && a[i2 - 1].kind === import_vscode5.NotebookCellKind.Markup) {
            return `[//]: #.

${md}

`;
          }
          return `${md}

`;
        }
      }
    }).join(""));
  }
  async deserializeNotebook(content, _token) {
    const lines = new TextDecoder(encoding).decode(content).split(`
`);
    const notebookCellData = [];
    let pending = "";
    const metadata = { shebang: false };
    let type = import_vscode5.NotebookCellKind.Markup;
    const commitPending = (lang, cellMetadata) => {
      if (pending) {
        const text = pending.trimEnd();
        if (text.length > 0) {
          const cellData = new import_vscode5.NotebookCellData(type, `${text}`, lang);
          if (cellMetadata)
            cellData.metadata = cellMetadata;
          notebookCellData.push(cellData);
        }
        pending = "";
      }
    };
    lines.forEach((c) => {
      c = c.trimEnd();
      const shebangParsed = c.match(/^[[][/][/][\]]: #!tikbook[ ]*(.*)$/);
      if (shebangParsed) {
        metadata.shebang = shebangParsed.groups?.[0] ? shebangParsed.groups[0] : true;
        return;
      }
      if (c.match(/^```routeros/)) {
        commitPending("markdown");
        type = import_vscode5.NotebookCellKind.Code;
        return;
      }
      if (c.match(/^```/) && type === import_vscode5.NotebookCellKind.Code) {
        commitPending("routeros");
        type = import_vscode5.NotebookCellKind.Markup;
        return;
      }
      const rawMetadataParsed = c.match(/^([\[][\/][\/][\]]: #[.])([ ][(](.*)[)])?/);
      if (rawMetadataParsed && type !== import_vscode5.NotebookCellKind.Code) {
        commitPending("markdown");
      }
      pending += `${c.trimEnd()}
`;
    });
    commitPending(type === import_vscode5.NotebookCellKind.Markup ? "markdown" : "routeros");
    const notebookData = new import_vscode5.NotebookData(notebookCellData);
    notebookData.metadata = metadata;
    return notebookData;
  }
}

class ScriptSerializer {
  serializeNotebook(data, _) {
    return new TextEncoder().encode(data.cells.reduce((M, V, I, A) => {
      if (V.value.trim().length === 0) {
        return M;
      }
      switch (V.kind) {
        case import_vscode5.NotebookCellKind.Code: {
          if (A[I - 1] && A[I - 1].kind === import_vscode5.NotebookCellKind.Code) {
            M += `#.

`;
          }
          return `${M}${V.value.trim()}

`;
        }
        case import_vscode5.NotebookCellKind.Markup: {
          return `${M}` + V.value.split(`
`).reduce((m, v) => {
            return `${m}#  ${v.trim()}
`;
          }, `#.markdown
`) + `#.

`;
        }
      }
    }, `#!tikbook

`));
  }
  deserializeNotebook(content, _) {
    const lines = new TextDecoder(encoding).decode(content).split(`
`);
    const notebookCellData = [];
    let pending = "";
    let type = import_vscode5.NotebookCellKind.Code;
    const commitPending = (type2) => {
      if (pending) {
        const text = pending.trim();
        if (text.length > 0) {
          notebookCellData.push(new import_vscode5.NotebookCellData(type2, `${text}`, type2 === import_vscode5.NotebookCellKind.Markup ? "markdown" : "routeros"));
        }
        pending = "";
      }
    };
    lines.forEach((C) => {
      const c = C.trimEnd();
      if (c.match(/^#!([\/].*)?tikbook/)) {
        return;
      }
      if (c.match(/^#.markdown/)) {
        commitPending(type);
        type = import_vscode5.NotebookCellKind.Markup;
        return;
      }
      if (c.match(/^#[.]/)) {
        commitPending(type);
        type = import_vscode5.NotebookCellKind.Code;
        return;
      }
      pending += type === import_vscode5.NotebookCellKind.Markup ? `${c.substring(3).trimEnd()}
` : `${c.trimEnd()}
`;
    });
    commitPending(type);
    return new import_vscode5.NotebookData(notebookCellData);
  }
}

class TikbookControllerBase {
  controllerId;
  notebookType;
  label;
  supportedLanguages = ["routeros"];
  _controller;
  _executionOrder = 0;
  dispose() {
    this._controller.dispose();
  }
  constructor(id, type, label) {
    this.controllerId = id;
    this.notebookType = type;
    this.label = label;
    this._controller = import_vscode5.notebooks.createNotebookController(this.controllerId, this.notebookType, this.label);
    this._controller.supportedLanguages = this.supportedLanguages;
    this._controller.supportsExecutionOrder = true;
    this._controller.description = `RouterOS kernel with '${this.notebookType}' serializer`;
    this._controller.executeHandler = this._execute.bind(this);
  }
  async _execute(cells, _notebook, _controller) {
    let hasError = false;
    for (const cell of cells) {
      if (hasError) {
        const execution = _controller.createNotebookCellExecution(cell);
        execution.start(Date.now());
        execution.end(false, Date.now());
        continue;
      }
      const success = await this._doExecution(cell);
      if (!success)
        hasError = true;
    }
  }
  async _doExecution(cell) {
    const execution = this._controller.createNotebookCellExecution(cell);
    execution.executionOrder = ++this._executionOrder;
    execution.start(Date.now());
    const codeText = cell.document.getText();
    const outputItems = [];
    try {
      const killswitch = new AbortController;
      let aborted = false;
      execution.token.onCancellationRequested((e) => {
        killswitch.abort(e);
        aborted = true;
        execution.replaceOutput([
          new import_vscode5.NotebookCellOutput([
            log.logLevel === import_vscode5.LogLevel.Trace ? import_vscode5.NotebookCellOutputItem.error(Error(e)) : import_vscode5.NotebookCellOutputItem.stderr("request cancelled")
          ])
        ]);
        execution.end(false, Date.now());
      });
      const response = await RouterRestClient.default.run(codeText, killswitch.signal);
      let json;
      try {
        json = JSON.parse(response);
      } catch {}
      if (typeof json === "object") {
        outputItems.push(import_vscode5.NotebookCellOutputItem.json(json));
      } else {
        if (response) {
          if (response.match(/^bad command.*/) || response.match(/^no such item.*/) || response.match(/^value of.*out of range.*/) || response.match(/^invalid value for argument.*/) || response.match(/^Script Error: .*/) || response.match(/^syntax error/) || response.match(/^expected end of command.*/)) {
            outputItems.push(import_vscode5.NotebookCellOutputItem.stderr(response));
          }
          outputItems.push(import_vscode5.NotebookCellOutputItem.text(response));
        }
      }
      if (outputItems.length > 0) {
        execution.replaceOutput(new import_vscode5.NotebookCellOutput(outputItems));
      } else {
        execution.clearOutput();
      }
      let success = true;
      if (outputItems.filter((e) => e.mime.match(/application\/vnd.code.notebook.(stderr|error)/g)).length > 0) {
        success = false;
      }
      if (!aborted)
        execution.end(success, Date.now());
      return success;
    } catch (error) {
      log.error(`<TikbookControllerBase> {_doExecution} got exception`, error);
      execution.replaceOutput([
        new import_vscode5.NotebookCellOutput([
          import_vscode5.NotebookCellOutputItem.error(error)
        ])
      ]);
      if (!execution.token.isCancellationRequested)
        execution.end(false, Date.now());
      return false;
    }
  }
}

class TikbookController extends TikbookControllerBase {
  static controllerId = "tikbook";
  static notebookType = "tikbook";
  static label = "RouterOS TikBook";
  constructor() {
    super(TikbookController.controllerId, TikbookController.notebookType, TikbookController.label);
  }
}

class RscController extends TikbookControllerBase {
  static controllerId = "routeros";
  static notebookType = "routeros";
  static label = "RouterOS Script";
  constructor() {
    super(RscController.controllerId, RscController.notebookType, RscController.label);
  }
}

class MarkdownController extends TikbookControllerBase {
  static controllerId = "markdown-routeros";
  static notebookType = "markdown-routeros";
  static label = "Markdown RouterOS";
  constructor() {
    super(MarkdownController.controllerId, MarkdownController.notebookType, MarkdownController.label);
  }
}

class ReplController extends TikbookControllerBase {
  static controllerId = "interactive-tikbook";
  static notebookType = "interactive";
  static label = "RouterOS REPL";
  constructor() {
    super(ReplController.controllerId, ReplController.notebookType, ReplController.label);
  }
}

// src/codelens.ts
var import_vscode6 = require("vscode");
class MarkdownHandlers {
  static log;
  output;
  killswitch = new AbortController;
  constructor(context) {
    if (!MarkdownHandlers.log) {
      MarkdownHandlers.log = this.output = import_vscode6.window.createOutputChannel("RouterOS Run", "markdown");
    } else {
      this.output = MarkdownHandlers.log;
    }
    context.subscriptions.push(import_vscode6.languages.registerCodeLensProvider({ language: "markdown" }, new MarkdownCodeFenceCodeLensProvider), import_vscode6.commands.registerCommand("tikbook.markdown.routeros.run.block", async (codeContent, fileName, range) => {
      log.info(`Run RouterOS from ${fileName}:${range.start.line}.  Check 'RouterOS Run' Output for results.`);
      const startTime = DateTime.now();
      this.output.appendLine(`## Run \`${fileName}\` ln ${range.start.line} at ${startTime.toLocaleString(DateTime.DATETIME_SHORT_WITH_SECONDS)}`);
      this.output.appendLine(`\`\`\`routeros`);
      this.output.appendLine(`${codeContent}`);
      this.output.appendLine(`\`\`\``);
      function timeTaken() {
        return DateTime.now().diff(startTime).toHuman({ unit: "seconds", unitDisplay: "short" });
      }
      try {
        const restout = await RouterRestClient.default.run(codeContent, this.killswitch.signal);
        this.output.appendLine(`> Completed in ${timeTaken()}`);
        if (restout.trim().length > 0) {
          this.output.appendLine(`\`\`\``);
          restout.split(`
`).forEach((e) => this.output.appendLine(`  ${e}`));
          this.output.appendLine(`\`\`\``);
        }
        this.output.appendLine("");
      } catch (err) {
        const error = err;
        this.output.appendLine(`> ### **ERROR** in ${timeTaken()}`);
        if (error?.cause)
          this.output.appendLine(`**${error.cause}**`);
        error.toString().split(`
`).forEach((e) => this.output.appendLine(`${e}`));
        this.output.appendLine("");
      }
      this.output.show();
    }));
  }
  dispose() {
    this.killswitch.abort();
  }
}

class MarkdownCodeFenceCodeLensProvider {
  provideCodeLenses(document2, _token) {
    const codeLenses = [];
    const text = document2.getText();
    const lines = text.split(`
`);
    let inRunnableCodeBlock = false;
    let codeBlockLanguage = null;
    let codeBlockStartLine = -1;
    for (let i2 = 0;i2 < lines.length; i2++) {
      const line = lines[i2];
      const fenceStartMatch = line.match(/^\s*```(\S*)\s*$/);
      if (fenceStartMatch && !inRunnableCodeBlock) {
        const lang = fenceStartMatch[1];
        if (lang === "routeros") {
          inRunnableCodeBlock = true;
          codeBlockLanguage = lang;
          codeBlockStartLine = i2;
        }
      } else if (line.trim() === "```" && inRunnableCodeBlock) {
        if (codeBlockLanguage === "routeros") {
          const range = new import_vscode6.Range(codeBlockStartLine, 0, codeBlockStartLine, line.length);
          const codeContentStartLine = codeBlockStartLine + 1;
          const codeContentEndLine = i2 - 1;
          const codeContentRange = new import_vscode6.Range(codeContentStartLine, 0, codeContentEndLine, document2.lineAt(codeContentEndLine).text.length);
          const codeContent = document2.getText(codeContentRange);
          codeLenses.push(new import_vscode6.CodeLens(range, {
            title: "$(play) RouterOS Run",
            command: "tikbook.markdown.routeros.run.block",
            arguments: [codeContent.trim(), document2.fileName, range]
          }));
        }
        inRunnableCodeBlock = false;
        codeBlockLanguage = null;
        codeBlockStartLine = -1;
      }
    }
    return codeLenses;
  }
}

// src/video.ts
var import_vscode7 = require("vscode");
class VideoViewer {
  context;
  static videoViewer;
  static default(context) {
    if (VideoViewer.videoViewer) {
      log.trace("<VideoViewer> {default} accessed using cache");
      return VideoViewer.videoViewer;
    }
    VideoViewer.videoViewer = new VideoViewer(context);
    log.trace("<VideoViewer> {default} created");
    return VideoViewer.videoViewer;
  }
  constructor(context) {
    this.context = context;
    this.activate();
  }
  activate() {
    log.trace("<VideoViewer> [activate]");
    this.context.subscriptions.push(import_vscode7.commands.registerCommand("tikbook.test.video.embedded", async (params) => {
      const repoUrl = params?.baseUrl || "https://tikoci.github.io/media/videos/";
      const repoGroup = params?.group || "test";
      const repoLanguages = params?.languages || ["en"];
      const videoBaseName = params?.name || "video";
      const videoDefaultLanguage = repoLanguages[0] || ["en"];
      const videoTitle = params?.name || "video";
      log.trace("<VideoViewer> [tikbook.test.video.embedded] start");
      const panel = import_vscode7.window.createWebviewPanel("tikbookVideoViewer", videoTitle, import_vscode7.ViewColumn.Two, {
        enableScripts: true,
        retainContextWhenHidden: true
      });
      const cspSource = panel.webview.cspSource;
      async function makeWebviewUrl(url, raw = true) {
        if (raw)
          return panel.webview.asWebviewUri(import_vscode7.Uri.parse(url));
        else {
          const vtttext = (await axios_default.get(url)).data;
          return import_vscode7.Uri.parse(`data:text/vtt;charset=utf-8,${encodeURIComponent(vtttext)}`);
        }
      }
      const jsUrl = panel.webview.asWebviewUri(import_vscode7.Uri.joinPath(this.context.extensionUri, "media", "web", "video.js"));
      const video = panel.webview.asWebviewUri(import_vscode7.Uri.parse(`${repoUrl}${repoGroup}/${videoBaseName}.mp3audio.mp4`));
      const subtitles = await makeWebviewUrl(`${repoUrl}${repoGroup}/${videoBaseName}.${videoDefaultLanguage}.vtt`);
      const chapters = await makeWebviewUrl(`${repoUrl}${repoGroup}/${videoBaseName}.chapters.vtt`);
      const csp = `default-src data: 'self' ${cspSource} vscode-resource:; style-src 'unsafe-inline'; img-src 'self' ${cspSource} https: vscode-resource:; script-src ${cspSource} 'self' vscode-resource: https:; media-src data: 'self' ${cspSource} https: vscode-resource:;`;
      panel.webview.html = this.generateHtmlPage(videoBaseName, csp, jsUrl, video, subtitles, chapters);
      log.trace("<VideoViewer> [tikbook.test.video.embedded] done");
    }));
  }
  dispose() {
    log.trace("<VideoViewer> {dispose}");
  }
  generateHtmlPage(title, csp, jsUrl, videoUrl, subtitlesUrl, chaptersUrl) {
    log.trace("<VideoViewer> {generateHtmlPage}");
    log.trace(`<VideoViewer> .csp ${csp}`);
    log.trace(`<VideoViewer> .jsUrl ${jsUrl}`);
    log.trace(`<VideoViewer> .videoUrl ${videoUrl}`);
    log.trace(`<VideoViewer> .subtitlesUrl ${subtitlesUrl}`);
    log.trace(`<VideoViewer> .chaptersUrl ${chaptersUrl}`);
    return `<html>
<head>
  <meta charset="UTF-8">
  <meta http-equiv="Content-Security-Policy"
    content="${csp}">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MikroTik Player</title>
  <style>
  :root {
      /* Use VSCode's theme colors */
      --bg-color: var(--vscode-editor-background);
      --text-color: var(--vscode-editor-foreground);
      --accent-color: var(--vscode-textLink-foreground);
      --secondary-text: var(--vscode-descriptionForeground);
      --hover-color: var(--vscode-textLink-activeForeground);
      --font-mono: var(--vscode-editor-font-family);
      
      /* Fallbacks for older VSCode versions */
      --bg-color: var(--vscode-editor-background, #1e1e1e);
      --text-color: var(--vscode-editor-foreground, #cccccc);
      --accent-color: var(--vscode-textLink-foreground, #4fc3f7);
      --secondary-text: var(--vscode-descriptionForeground, #808080);
      --hover-color: var(--vscode-textLink-activeForeground, #74b9ff);
    }
    * {
      box-sizing: border-box;
    }

    html,
    body {
      margin: 0;
      padding: 0;
      height: 100%;
      background: var(--bg-color);
      color: var(--text-color);
      font-family: var(--font-mono);
    }

    videoold {
      position: absolute;
      top: 50%;
      left: 50%;
      max-width: 100%;
      max-height: 100%;
      transform: translate(-50%, -50%);
    }

    video {
      position: absolute;
      top: 0;                           /* Changed from 50% */
      left: 50%;
      max-width: 100%;
      max-height: 100%;
      transform: translate(-50%, 0);    /* Changed from translate(-50%, -50%) */
      background: var(--bg-color);
    }

    /* Subtitle styling */
    video::cue {
      font-family: var(--font-mono);
      font-size: 0.8em;
      background: rgba(0, 0, 0, 0.8);
      color: #fff;
      text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
      padding: 0.2em 0.4em;
      border-radius: 2px;
    }

    video::cue(.narrator) {
      font-style: italic;
      color: #ccc;
    }

    .title,
    .chapter-selector {
      position: fixed;
      top: 16px;
      font-family: var(--font-mono);
      color: white; // var(--text-color);
      font-size: 0.9em;
    }

    .title {
      left: 16px;
      text-align: center;
    }

    .chapter-selector {
      right: 16px;
    }

    .activeChapter {
      color: var(--accent-color) !important;
      font-weight: bold !important;
    }

    a {
      color: inherit;
      text-decoration: none;
      transition: color 0.2s ease;
    }

    a:hover {
      color: var(--accent-color);
    }

    .videoStatsFooter {
      text-align: right;
      margin-top: 0.5em;
    }

    /* Ensure consistent styling across browsers */
    details summary {
      cursor: pointer;
      user-select: none;
    }

    ul {
      list-style: none;
      padding: 0;
      margin: 0;
    }

    li {
      padding: 0.2em 0;
    }
  </style>
</head>
<body>
<div class="video-container">
  <video id="video" crossorigin=anonymous controls preload="metadata">
    <source src="${videoUrl}" type="video/mp4">
    <track type="subtitles" src="${subtitlesUrl}" srclang="en"
      label="Subtitles" default>
    <track id="chapters" type="chapters" src="${chaptersUrl}"
      srclang="en" label="Chapters">
  </video>
  <div class="title">
    <span>${title}</span>
  </div>
  <div class="chapter-selector">
    <details class="dropdown">
      <summary id="activeChapter" class="outline">...</summary>
      <ul id="chaptersList"></ul>
      <footer>
        <div class="videoStatsFooter">
          <small>
            <i>pos </i><span id="currentTime"></span><br>
            <span id="nextChapterTime"><i>next </i><span id="nextChapterTimeDiff"></span></span>
          </small>
        </div>
      </footer>
    </details>
  </div>
  </div>
</div>
<script src="${jsUrl}"/>
</body>

</html>`;
  }
}

// src/virtualdocs.ts
var import_vscode8 = require("vscode");

// node:path
function assertPath(path) {
  if (typeof path !== "string")
    throw TypeError("Path must be a string. Received " + JSON.stringify(path));
}
function normalizeStringPosix(path, allowAboveRoot) {
  var res = "", lastSegmentLength = 0, lastSlash = -1, dots = 0, code2;
  for (var i2 = 0;i2 <= path.length; ++i2) {
    if (i2 < path.length)
      code2 = path.charCodeAt(i2);
    else if (code2 === 47)
      break;
    else
      code2 = 47;
    if (code2 === 47) {
      if (lastSlash === i2 - 1 || dots === 1)
        ;
      else if (lastSlash !== i2 - 1 && dots === 2) {
        if (res.length < 2 || lastSegmentLength !== 2 || res.charCodeAt(res.length - 1) !== 46 || res.charCodeAt(res.length - 2) !== 46) {
          if (res.length > 2) {
            var lastSlashIndex = res.lastIndexOf("/");
            if (lastSlashIndex !== res.length - 1) {
              if (lastSlashIndex === -1)
                res = "", lastSegmentLength = 0;
              else
                res = res.slice(0, lastSlashIndex), lastSegmentLength = res.length - 1 - res.lastIndexOf("/");
              lastSlash = i2, dots = 0;
              continue;
            }
          } else if (res.length === 2 || res.length === 1) {
            res = "", lastSegmentLength = 0, lastSlash = i2, dots = 0;
            continue;
          }
        }
        if (allowAboveRoot) {
          if (res.length > 0)
            res += "/..";
          else
            res = "..";
          lastSegmentLength = 2;
        }
      } else {
        if (res.length > 0)
          res += "/" + path.slice(lastSlash + 1, i2);
        else
          res = path.slice(lastSlash + 1, i2);
        lastSegmentLength = i2 - lastSlash - 1;
      }
      lastSlash = i2, dots = 0;
    } else if (code2 === 46 && dots !== -1)
      ++dots;
    else
      dots = -1;
  }
  return res;
}
function _format(sep, pathObject) {
  var dir = pathObject.dir || pathObject.root, base = pathObject.base || (pathObject.name || "") + (pathObject.ext || "");
  if (!dir)
    return base;
  if (dir === pathObject.root)
    return dir + base;
  return dir + sep + base;
}
function resolve() {
  var resolvedPath = "", resolvedAbsolute = false, cwd;
  for (var i2 = arguments.length - 1;i2 >= -1 && !resolvedAbsolute; i2--) {
    var path;
    if (i2 >= 0)
      path = arguments[i2];
    else {
      if (cwd === undefined)
        cwd = process.cwd();
      path = cwd;
    }
    if (assertPath(path), path.length === 0)
      continue;
    resolvedPath = path + "/" + resolvedPath, resolvedAbsolute = path.charCodeAt(0) === 47;
  }
  if (resolvedPath = normalizeStringPosix(resolvedPath, !resolvedAbsolute), resolvedAbsolute)
    if (resolvedPath.length > 0)
      return "/" + resolvedPath;
    else
      return "/";
  else if (resolvedPath.length > 0)
    return resolvedPath;
  else
    return ".";
}
function normalize(path) {
  if (assertPath(path), path.length === 0)
    return ".";
  var isAbsolute = path.charCodeAt(0) === 47, trailingSeparator = path.charCodeAt(path.length - 1) === 47;
  if (path = normalizeStringPosix(path, !isAbsolute), path.length === 0 && !isAbsolute)
    path = ".";
  if (path.length > 0 && trailingSeparator)
    path += "/";
  if (isAbsolute)
    return "/" + path;
  return path;
}
function isAbsolute(path) {
  return assertPath(path), path.length > 0 && path.charCodeAt(0) === 47;
}
function join() {
  if (arguments.length === 0)
    return ".";
  var joined;
  for (var i2 = 0;i2 < arguments.length; ++i2) {
    var arg = arguments[i2];
    if (assertPath(arg), arg.length > 0)
      if (joined === undefined)
        joined = arg;
      else
        joined += "/" + arg;
  }
  if (joined === undefined)
    return ".";
  return normalize(joined);
}
function relative(from2, to) {
  if (assertPath(from2), assertPath(to), from2 === to)
    return "";
  if (from2 = resolve(from2), to = resolve(to), from2 === to)
    return "";
  var fromStart = 1;
  for (;fromStart < from2.length; ++fromStart)
    if (from2.charCodeAt(fromStart) !== 47)
      break;
  var fromEnd = from2.length, fromLen = fromEnd - fromStart, toStart = 1;
  for (;toStart < to.length; ++toStart)
    if (to.charCodeAt(toStart) !== 47)
      break;
  var toEnd = to.length, toLen = toEnd - toStart, length = fromLen < toLen ? fromLen : toLen, lastCommonSep = -1, i2 = 0;
  for (;i2 <= length; ++i2) {
    if (i2 === length) {
      if (toLen > length) {
        if (to.charCodeAt(toStart + i2) === 47)
          return to.slice(toStart + i2 + 1);
        else if (i2 === 0)
          return to.slice(toStart + i2);
      } else if (fromLen > length) {
        if (from2.charCodeAt(fromStart + i2) === 47)
          lastCommonSep = i2;
        else if (i2 === 0)
          lastCommonSep = 0;
      }
      break;
    }
    var fromCode = from2.charCodeAt(fromStart + i2), toCode = to.charCodeAt(toStart + i2);
    if (fromCode !== toCode)
      break;
    else if (fromCode === 47)
      lastCommonSep = i2;
  }
  var out = "";
  for (i2 = fromStart + lastCommonSep + 1;i2 <= fromEnd; ++i2)
    if (i2 === fromEnd || from2.charCodeAt(i2) === 47)
      if (out.length === 0)
        out += "..";
      else
        out += "/..";
  if (out.length > 0)
    return out + to.slice(toStart + lastCommonSep);
  else {
    if (toStart += lastCommonSep, to.charCodeAt(toStart) === 47)
      ++toStart;
    return to.slice(toStart);
  }
}
function _makeLong(path) {
  return path;
}
function dirname(path) {
  if (assertPath(path), path.length === 0)
    return ".";
  var code2 = path.charCodeAt(0), hasRoot = code2 === 47, end = -1, matchedSlash = true;
  for (var i2 = path.length - 1;i2 >= 1; --i2)
    if (code2 = path.charCodeAt(i2), code2 === 47) {
      if (!matchedSlash) {
        end = i2;
        break;
      }
    } else
      matchedSlash = false;
  if (end === -1)
    return hasRoot ? "/" : ".";
  if (hasRoot && end === 1)
    return "//";
  return path.slice(0, end);
}
function basename(path, ext) {
  if (ext !== undefined && typeof ext !== "string")
    throw TypeError('"ext" argument must be a string');
  assertPath(path);
  var start = 0, end = -1, matchedSlash = true, i2;
  if (ext !== undefined && ext.length > 0 && ext.length <= path.length) {
    if (ext.length === path.length && ext === path)
      return "";
    var extIdx = ext.length - 1, firstNonSlashEnd = -1;
    for (i2 = path.length - 1;i2 >= 0; --i2) {
      var code2 = path.charCodeAt(i2);
      if (code2 === 47) {
        if (!matchedSlash) {
          start = i2 + 1;
          break;
        }
      } else {
        if (firstNonSlashEnd === -1)
          matchedSlash = false, firstNonSlashEnd = i2 + 1;
        if (extIdx >= 0)
          if (code2 === ext.charCodeAt(extIdx)) {
            if (--extIdx === -1)
              end = i2;
          } else
            extIdx = -1, end = firstNonSlashEnd;
      }
    }
    if (start === end)
      end = firstNonSlashEnd;
    else if (end === -1)
      end = path.length;
    return path.slice(start, end);
  } else {
    for (i2 = path.length - 1;i2 >= 0; --i2)
      if (path.charCodeAt(i2) === 47) {
        if (!matchedSlash) {
          start = i2 + 1;
          break;
        }
      } else if (end === -1)
        matchedSlash = false, end = i2 + 1;
    if (end === -1)
      return "";
    return path.slice(start, end);
  }
}
function extname(path) {
  assertPath(path);
  var startDot = -1, startPart = 0, end = -1, matchedSlash = true, preDotState = 0;
  for (var i2 = path.length - 1;i2 >= 0; --i2) {
    var code2 = path.charCodeAt(i2);
    if (code2 === 47) {
      if (!matchedSlash) {
        startPart = i2 + 1;
        break;
      }
      continue;
    }
    if (end === -1)
      matchedSlash = false, end = i2 + 1;
    if (code2 === 46) {
      if (startDot === -1)
        startDot = i2;
      else if (preDotState !== 1)
        preDotState = 1;
    } else if (startDot !== -1)
      preDotState = -1;
  }
  if (startDot === -1 || end === -1 || preDotState === 0 || preDotState === 1 && startDot === end - 1 && startDot === startPart + 1)
    return "";
  return path.slice(startDot, end);
}
function format2(pathObject) {
  if (pathObject === null || typeof pathObject !== "object")
    throw TypeError('The "pathObject" argument must be of type Object. Received type ' + typeof pathObject);
  return _format("/", pathObject);
}
function parse2(path) {
  assertPath(path);
  var ret = { root: "", dir: "", base: "", ext: "", name: "" };
  if (path.length === 0)
    return ret;
  var code2 = path.charCodeAt(0), isAbsolute2 = code2 === 47, start;
  if (isAbsolute2)
    ret.root = "/", start = 1;
  else
    start = 0;
  var startDot = -1, startPart = 0, end = -1, matchedSlash = true, i2 = path.length - 1, preDotState = 0;
  for (;i2 >= start; --i2) {
    if (code2 = path.charCodeAt(i2), code2 === 47) {
      if (!matchedSlash) {
        startPart = i2 + 1;
        break;
      }
      continue;
    }
    if (end === -1)
      matchedSlash = false, end = i2 + 1;
    if (code2 === 46) {
      if (startDot === -1)
        startDot = i2;
      else if (preDotState !== 1)
        preDotState = 1;
    } else if (startDot !== -1)
      preDotState = -1;
  }
  if (startDot === -1 || end === -1 || preDotState === 0 || preDotState === 1 && startDot === end - 1 && startDot === startPart + 1) {
    if (end !== -1)
      if (startPart === 0 && isAbsolute2)
        ret.base = ret.name = path.slice(1, end);
      else
        ret.base = ret.name = path.slice(startPart, end);
  } else {
    if (startPart === 0 && isAbsolute2)
      ret.name = path.slice(1, startDot), ret.base = path.slice(1, end);
    else
      ret.name = path.slice(startPart, startDot), ret.base = path.slice(startPart, end);
    ret.ext = path.slice(startDot, end);
  }
  if (startPart > 0)
    ret.dir = path.slice(0, startPart - 1);
  else if (isAbsolute2)
    ret.dir = "/";
  return ret;
}
var sep = "/";
var delimiter = ":";
var posix = ((p) => (p.posix = p, p))({ resolve, normalize, isAbsolute, join, relative, _makeLong, dirname, basename, extname, format: format2, parse: parse2, sep, delimiter, win32: null, posix: null });

// src/virtualdocs.ts
function initializeVirtualDocs() {
  const provider = new RouterConfigProvider;
  return [
    import_vscode8.workspace.registerTextDocumentContentProvider("rscena", provider),
    import_vscode8.commands.registerCommand("tikbook.view.markdown", async () => {
      const doc = import_vscode8.window.activeNotebookEditor ? import_vscode8.window.activeNotebookEditor?.notebook : import_vscode8.window.activeTextEditor?.document;
      if (!doc) {
        log.warn(`<vdoc> [tikbook.view.markdown] an active editor or notebook is required, but none was found, command aborted`);
        return;
      }
      if (doc.isUntitled) {
        import_vscode8.window.showWarningMessage(`Untitled documents cannot previewed. Save file to enable Markdown preview.`, "Save As...", "Cancel").then((selection) => {
          if (selection === "Save As...")
            import_vscode8.commands.executeCommand("workbench.action.files.save").then((e) => log.info(JSON.stringify(e)));
        });
        return;
      }
      const frag = import_vscode8.window.activeNotebookEditor ? "tikbook2md" : "rsc2md";
      await import_vscode8.workspace.openTextDocument(import_vscode8.Uri.parse(`rscena:${posix.basename(doc.uri.path)}-view.md/?${frag}#${doc.uri}`)).then((doc2) => {
        import_vscode8.window.showTextDocument(doc2, { preview: false, preserveFocus: false, viewColumn: import_vscode8.ViewColumn.Two });
      });
    }),
    import_vscode8.commands.registerCommand("tikbook.view.script", async () => {
      const nb = import_vscode8.window.activeNotebookEditor?.notebook;
      if (!nb) {
        log.warn(`<vdoc> [tikbook.view.script] found no active notebook`);
        return;
      }
      if (nb.isUntitled) {
        import_vscode8.window.showWarningMessage(`Untitled notebooks cannot previewed. Save file to enable RouterOS script preview.`, "Save As...", "Cancel").then((selection) => {
          if (selection === "Save As...")
            import_vscode8.commands.executeCommand("workbench.action.files.save").then((e) => log.info(JSON.stringify(e)));
        });
        return;
      }
      await import_vscode8.workspace.openTextDocument(import_vscode8.Uri.parse(`rscena:${posix.basename(nb.uri.path)}-view.rsc/?md2rsc#${nb.uri}`)).then((doc) => {
        import_vscode8.window.showTextDocument(doc, { preview: false, preserveFocus: false, viewColumn: import_vscode8.ViewColumn.Beside });
      });
    }),
    import_vscode8.commands.registerCommand("tikbook.open.router.export", async (type = "compact") => {
      await import_vscode8.workspace.openTextDocument(import_vscode8.Uri.parse(`rscena:export-${type}.rsc?export#${type}`)).then((doc) => import_vscode8.window.showTextDocument(doc, { preview: false }));
    }),
    import_vscode8.commands.registerCommand("tikbook.open.router.script", async (name, id) => {
      await import_vscode8.workspace.openTextDocument(import_vscode8.Uri.parse(`rscena:${encodeURIComponent(name)}.rsc?script#${encodeURIComponent(id)}`)).then((doc) => import_vscode8.window.showTextDocument(doc, { preview: false }));
    }),
    import_vscode8.commands.registerCommand("tikbook.open.router.scripts.globals", async () => {
      await import_vscode8.workspace.openTextDocument(import_vscode8.Uri.parse(`rscena:all-script-as-globals.rsc?scripts.globals`)).then((doc) => import_vscode8.window.showTextDocument(doc, { preview: false }));
    }),
    import_vscode8.commands.registerCommand("tikbook.open.router.scripts.tikbook", async () => {
      await import_vscode8.workspace.openTextDocument(import_vscode8.Uri.parse(`rscena:all-scripts.md.rsc?scripts.tikbook`)).then((doc) => import_vscode8.window.showTextDocument(doc, { preview: false }));
    }),
    import_vscode8.commands.registerCommand("tikbook.open.router.default-configuration.script", async () => {
      await import_vscode8.workspace.openTextDocument(import_vscode8.Uri.parse(`rscena:defconf.rsc?default-configuration#script`)).then((doc) => import_vscode8.window.showTextDocument(doc, { preview: false }));
    }),
    import_vscode8.commands.registerCommand("tikbook.open.router.default-configuration.caps-mode-script", async () => {
      await import_vscode8.workspace.openTextDocument(import_vscode8.Uri.parse(`rscena:defconf-capsman.rsc?default-configuration#caps-mode-script`)).then((doc) => import_vscode8.window.showTextDocument(doc, { preview: false }));
    }),
    import_vscode8.commands.registerCommand("tikbook.open.router.default-configuration.custom-script", async () => {
      await import_vscode8.workspace.openTextDocument(import_vscode8.Uri.parse(`rscena:defconf-custom.rsc?default-configuration#script`)).then((doc) => import_vscode8.window.showTextDocument(doc, { preview: false }));
    }),
    import_vscode8.commands.registerCommand("tikbook.open.router.ip.neighbor.print.detail.csv", async () => {
      await import_vscode8.workspace.openTextDocument(import_vscode8.Uri.parse(`rscena:ip-neighbor.csv?ip-neighbor#detail`)).then((doc) => import_vscode8.window.showTextDocument(doc, { preview: false }));
    }),
    import_vscode8.commands.registerCommand("tikbook.open.router.csv", async (cmd, name) => {
      await import_vscode8.workspace.openTextDocument(import_vscode8.Uri.parse(`rscena:${encodeURIComponent(name)}.csv?csv#${encodeURIComponent(cmd)}`)).then((doc) => import_vscode8.window.showTextDocument(doc, { preview: false }));
    }),
    import_vscode8.commands.registerCommand("tikbook.vdoc.refresh", async (uri) => {
      provider.refresh(uri);
    }),
    import_vscode8.commands.registerCommand("tikbook.vdoc.refresh.active", () => {
      const activeEditor = import_vscode8.window.activeTextEditor;
      if (activeEditor && activeEditor.document.uri.scheme === RouterConfigProvider.scheme) {
        import_vscode8.commands.executeCommand("tikbook.vdoc.refresh", activeEditor.document.uri);
      }
    }),
    import_vscode8.commands.registerCommand("tikbook.vdoc.refresh.all", () => {
      provider.refreshAll();
    })
  ];
}

class RouterConfigProvider {
  disposables = [];
  killswitch = new AbortController;
  onDidChangeEmitter = new import_vscode8.EventEmitter;
  onDidChange = this.onDidChangeEmitter.event;
  urimap = new BiMap;
  static scheme = "rscena";
  constructor() {
    this.disposables.push(import_vscode8.workspace.onDidCloseTextDocument((doc) => this.urimap.deleteByValue(doc.uri.toString())));
    this.disposables.push(import_vscode8.workspace.onDidSaveTextDocument((doc) => {
      const savedocuri = this.urimap.getValue(doc.uri.toString());
      if (savedocuri) {
        this.onDidChangeEmitter.fire(import_vscode8.Uri.parse(savedocuri));
      }
    }));
    this.disposables.push(import_vscode8.workspace.onDidCloseNotebookDocument((doc) => this.urimap.deleteByValue(doc.uri.toString())));
    this.disposables.push(import_vscode8.workspace.onDidSaveNotebookDocument((doc) => {
      const savedocuri = this.urimap.getValue(doc.uri.toString());
      if (savedocuri) {
        this.onDidChangeEmitter.fire(import_vscode8.Uri.parse(savedocuri));
      }
    }));
  }
  refresh(uri) {
    this.onDidChangeEmitter.fire(uri);
  }
  refreshAll() {
    this.urimap.rawKeys.forEach((k) => {
      this.refresh(import_vscode8.Uri.parse(k));
    });
  }
  async provideTextDocumentContent(uri, _token) {
    log.info(`<RouterConfigProvider> {provideTextDocumentContent} got request scheme ${uri.scheme} authority ${uri.authority} path ${uri.path} query ${uri.query} fragment ${uri.fragment}`);
    const client = RouterRestClient.default;
    switch (uri.query) {
      case "tikbook2md":
        this.urimap.set(import_vscode8.Uri.parse(uri.fragment).toString(), uri.toString());
        return await this.getMarkdownFromNotebook(import_vscode8.Uri.parse(uri.fragment));
      case "rsc2md":
        this.urimap.set(import_vscode8.Uri.parse(uri.fragment).toString(), uri.toString());
        return await this.getMarkdownFromScript(import_vscode8.Uri.parse(uri.fragment));
      case "md2rsc":
        this.urimap.set(import_vscode8.Uri.parse(uri.fragment).toString(), uri.toString());
        return await this.getScriptFromNotebook(import_vscode8.Uri.parse(uri.fragment));
      case "export":
        return await client.exportConfig(uri.fragment, this.killswitch.signal);
      case "script":
        return (await client.getSystemScript(uri.fragment)).source;
      case "scripts.tikbook":
        return (await client.systemScripts).map((script) => {
          return `
#.markdown
` + `#   ### ${script.name}
` + (script.comment ? `#   #### ${script.comment}
` : "") + `#   * **owner** ${script.owner}
` + `#   * **dont-require-permissions** ${script["dont-require-permissions"]}
` + `#   * **policy** ${script.policy}
` + `#   > _Script captured at_ ${DateTime.now().toLocaleString(DateTime.DATETIME_SHORT)}
` + `#.
` + `${script.source}
`;
        }).join(`
#.
`);
      case "scripts.globals":
        return (await client.systemScripts).map((script) => {
          return `
# ${script.name.toUpperCase()} - ${script.comment}
` + `#	owner=${script.owner} ${script["dont-require-permissions"] && script["dont-require-permissions"] === "yes" ? `dont-require-permissions=yes` : `policy=${script.policy}`}
` + `:global "run-${script.name}" do={
` + `${script.source?.split(`
`).join(`
    `)}
` + `}
`;
        }).join(`
#.
`);
      case "default-configuration":
        switch (uri.fragment) {
          case "caps-mode-script":
            return (await client.defaultConfiguration)["caps-mode-script"];
          case "custom":
            return (await client.defaultConfiguration).custom;
          default:
            return (await client.defaultConfiguration).script;
        }
      case "ip-neighbor": {
        return await client._asCSV("/ip/neighbor/print detail");
      }
      case "csv": {
        return await client._asCSV(uri.fragment);
      }
    }
  }
  dispose() {
    this.disposables.forEach((e) => e.dispose());
    this.killswitch.abort("killing export, disposed <RouterConfigProvider>");
  }
  async getMarkdownFromScript(uri) {
    if (!uri)
      throw new Error("URI must be to a valid notebook document");
    const killswitch = new import_vscode8.CancellationTokenSource;
    const text = (await import_vscode8.workspace.openTextDocument(uri)).getText();
    const scriptSerializer = new ScriptSerializer;
    const markdownSerializer = new MarkdownSerializer;
    return new TextDecoder().decode(await markdownSerializer.serializeNotebook(await scriptSerializer.deserializeNotebook(new TextEncoder().encode(text), killswitch.token), killswitch.token));
  }
  async getMarkdownFromNotebook(uri) {
    const nb = await import_vscode8.workspace.openNotebookDocument(uri);
    if (!nb)
      throw new Error("URI must be to a valid notebook document");
    const killswitch = new import_vscode8.CancellationTokenSource;
    const text = (await import_vscode8.workspace.openTextDocument(nb.uri)).getText();
    const scriptSerializer = new ScriptSerializer;
    const markdownSerializer = new MarkdownSerializer;
    switch (nb.notebookType) {
      case "tikbook":
      case "routeros":
        return new TextDecoder().decode(await markdownSerializer.serializeNotebook(await scriptSerializer.deserializeNotebook(new TextEncoder().encode(text), killswitch.token), killswitch.token));
      case "markdown-routeros":
        return text;
      default:
        log.error("<RouterConfigProvider> {getMarkdownFromNotebook} got invalid notebookType, throwing");
        throw new Error("Notebook must be a known type.  Currently TikBook or Markdown RouterOS");
    }
  }
  async getScriptFromNotebook(uri) {
    const nb = await import_vscode8.workspace.openNotebookDocument(uri);
    if (!nb)
      throw new Error("URI must be to a valid notebook document");
    const killswitch = new import_vscode8.CancellationTokenSource;
    const text = (await import_vscode8.workspace.openTextDocument(nb.uri)).getText();
    const scriptSerializer = new ScriptSerializer;
    const markdownSerializer = new MarkdownSerializer;
    switch (nb.notebookType) {
      case "tikbook":
      case "routeros":
        return text;
      case "markdown-routeros":
        return new TextDecoder().decode(await scriptSerializer.serializeNotebook(await markdownSerializer.deserializeNotebook(new TextEncoder().encode(text), killswitch.token), killswitch.token));
      default:
        log.error(`<getScriptFromNotebook> got invalid notebookType, throwing`, uri);
        throw new Error("Notebook must be a known type.  Currently TikBook or Markdown RouterOS");
    }
  }
}

class BiMap {
  keyToValue = new Map;
  valueToKey = new Map;
  get rawKeys() {
    return this.keyToValue;
  }
  set(key, value) {
    if (this.keyToValue.has(key)) {
      this.valueToKey.delete(this.keyToValue.get(key));
    }
    if (this.valueToKey.has(value)) {
      this.keyToValue.delete(this.valueToKey.get(value));
    }
    this.keyToValue.set(key, value);
    this.valueToKey.set(value, key);
  }
  getValue(key) {
    return this.keyToValue.get(key);
  }
  getKey(value) {
    return this.valueToKey.get(value);
  }
  deleteByKey(key) {
    const value = this.keyToValue.get(key);
    const deleted = this.keyToValue.delete(key);
    if (value !== undefined) {
      this.valueToKey.delete(value);
    }
    return deleted;
  }
  deleteByValue(value) {
    const key = this.valueToKey.get(value);
    const deleted = this.valueToKey.delete(value);
    if (key !== undefined) {
      this.keyToValue.delete(key);
    }
    return deleted;
  }
  hasKey(key) {
    return this.keyToValue.has(key);
  }
  hasValue(value) {
    return this.valueToKey.has(value);
  }
  keys() {
    return this.keyToValue.keys();
  }
  values() {
    return this.keyToValue.values();
  }
  clear() {
    this.keyToValue.clear();
    this.valueToKey.clear();
  }
  get size() {
    return this.keyToValue.size;
  }
}

// src/menus.ts
var import_vscode10 = require("vscode");

// src/remote.ts
var import_vscode9 = require("vscode");
function initializeSSH() {
  log.debug(`<SSH> {initalizeSSH}`);
  return [
    import_vscode9.commands.registerCommand("tikbook.open.terminal.router", () => openTerminalRouter())
  ];
}
function openTerminalRouter() {
  const settings = getSettings();
  const url = URL.parse(settings.baseUrl);
  if (!url) {
    log.error(`<openTerminalRouter> got no URL`);
    import_vscode9.window.showWarningMessage(`Could not open SSH terminal.  TikBook 'Base URL' setting is invalid.`);
    return;
  }
  const connuri = `${settings.username}@${url.hostname}`;
  const terminal = import_vscode9.window.createTerminal({
    name: `ssh ${connuri}`,
    iconPath: new import_vscode9.ThemeIcon("mikrotik-icon-line")
  });
  log.info(`<SSH> {openTerminalRouter} ${settings.sshCommand} ${connuri}`);
  terminal.sendText(`${settings.sshCommand} ${connuri}`);
  terminal.show(false);
}
async function fetchGitHubRepos(organization = "tikoci") {
  try {
    log.debug(`<fetchGitHubRepos> invoked ${organization}`);
    const response = await axios_default.get(`https://api.github.com/orgs/${organization}/repos`, {
      params: {
        type: "public",
        sort: "updated",
        per_page: 100
      },
      headers: {
        "User-Agent": "VSCode-Extension",
        Accept: "application/vnd.github.v3+json"
      },
      timeout: 1e4
    });
    return response.data;
  } catch (_error) {
    if (isAxiosError2(_error)) {
      const error = _error;
      if (error.response) {
        throw new Error(`GitHub API error: ${error.response.status} ${error.response.statusText}`, { cause: _error });
      } else if (error.request) {
        throw new Error("Network error: Unable to reach GitHub API", { cause: _error });
      } else if (error.code === "ECONNABORTED") {
        throw new Error("Request timeout: GitHub API is taking too long to respond", { cause: _error });
      } else {
        throw new Error(`Request error: ${error.message || "Unknown error occurred"}`, { cause: _error });
      }
    }
    throw new Error("Unknown error", { cause: _error });
  }
}

// src/menus.ts
function quickPickBack(where) {
  return [
    {
      label: "",
      kind: import_vscode10.QuickPickItemKind.Separator
    },
    {
      label: "$(debug-step-back)  Go Back",
      cmd: where
    }
  ];
}
function initializeMenus() {
  return [
    import_vscode10.commands.registerCommand("tikbook.show.menu.main", () => showMenuMain()),
    import_vscode10.commands.registerCommand("tikbook.show.menu.new", () => showMenuNew()),
    import_vscode10.commands.registerCommand("tikbook.show.menu.setup", () => showMenuConnection()),
    import_vscode10.commands.registerCommand("tikbook.show.menu.setup.baseurl", (_) => showSetupBaseUrl(_)),
    import_vscode10.commands.registerCommand("tikbook.show.menu.setup.username", (_) => showSetupUsername(_)),
    import_vscode10.commands.registerCommand("tikbook.show.menu.setup.apitimeout", (_) => showSetupApiTimeout(_)),
    import_vscode10.commands.registerCommand("tikbook.show.menu.setup.sshcommand", (_) => showSetupSshCommand(_)),
    import_vscode10.commands.registerCommand("tikbook.show.menu.outputs", () => showMenuOutputs()),
    import_vscode10.commands.registerCommand("tikbook.show.menu.router.admin", () => showRouterAdminMenu()),
    import_vscode10.commands.registerCommand("tikbook.show.menu.router.scripts", () => showScriptListMenu()),
    import_vscode10.commands.registerCommand("tikbook.show.menu.router.export", () => showConfigurationExportMenu()),
    import_vscode10.commands.registerCommand("tikbook.browse.mikrotik.help", () => showHelpMenu()),
    import_vscode10.commands.registerCommand("tikbook.show.menu.variables.global", () => showRouterVariableGlobalForClipboard()),
    import_vscode10.commands.registerCommand("tikbook.menu.showTikociRepoPicker", (back, browse) => showTikociRepoPicker(back, browse))
  ];
}
async function showMenuMain() {
  return import_vscode10.window.showQuickPick([
    {
      label: "$(mikrotik-icon-line)  New RouterOS Document",
      cmd: "tikbook.show.menu.new"
    },
    {
      label: "$(gear)  Setup Connection",
      cmd: "tikbook.show.menu.setup"
    },
    {
      label: "$(tools)  RouterOS Management",
      cmd: "tikbook.show.menu.router.admin"
    },
    {
      label: "$(question)  Help Resources",
      cmd: "tikbook.browse.mikrotik.help"
    },
    {
      label: "$(output)  Show TikBook Logs (Outputs)",
      description: "including extension and run logs",
      cmd: "tikbook.show.menu.outputs"
    }
  ], {
    title: "RouterOS TikBook"
  }).then((pickedItem) => {
    if (pickedItem?.cmd)
      import_vscode10.commands.executeCommand(pickedItem.cmd);
    else
      log.debug("<menus.showMenuMain> Main menu has no command to run");
  });
}
async function showMenuNew() {
  return import_vscode10.window.showQuickPick([
    {
      label: "$(mikrotik-icon-line)  New RouterOS Script File",
      description: "normal .rsc file",
      id: "routeros"
    },
    {
      label: "$(tikoci-tikbook)  New RouterOS Notebook",
      description: "TikBook using RouterOS script file",
      id: "tikbook"
    },
    {
      label: "$(markdown)  New Markdown Notebook",
      description: "TikBook using Markdown with runnable RouterOS",
      id: "markdown-routeros"
    },
    {
      label: "$(tikoci-tikbook)   Create Notebook from System Scripts",
      cmd: "tikbook.new.notebook.router.scripts"
    },
    {
      label: "$(terminal-powershell)  Start Interactive REPL",
      cmd: "tikbook.new.notebook.repl"
    },
    ...quickPickBack("tikbook.show.menu.main")
  ], { title: "New RouterOS Document" }).then((item) => {
    if (!item)
      return;
    if (item.cmd)
      import_vscode10.commands.executeCommand(item.cmd);
    switch (item.id) {
      case "tikbook":
        import_vscode10.workspace.openNotebookDocument("tikbook").then((e) => import_vscode10.window.showNotebookDocument(e));
        break;
      case "routeros":
        import_vscode10.commands.executeCommand("workbench.action.files.newUntitledFile", { languageId: "routeros" });
        break;
      case "markdown-routeros":
        import_vscode10.workspace.openNotebookDocument("markdown-routeros").then((e) => import_vscode10.window.showNotebookDocument(e));
        break;
      default:
        log.warn("<menus.showMenuNew> no command found to run");
    }
  });
}
function showMenuConnection() {
  const settings = getSettings();
  import_vscode10.window.showQuickPick([
    {
      label: "Authentication",
      kind: import_vscode10.QuickPickItemKind.Separator
    },
    {
      label: " $(browser)  Set Base URL",
      description: `${settings.baseUrl}`,
      id: "baseUrl",
      cmd: "tikbook.show.menu.setup.baseurl"
    },
    {
      label: " $(account)  Set User",
      description: ` ${settings.username}`,
      id: "username",
      cmd: "tikbook.show.menu.setup.username"
    },
    {
      label: " $(key)  Set Password as Secret",
      description: ` ${import_vscode10.workspace.getConfiguration("tikbook", null).get("passwordInfo")}`,
      cmd: "tikoci.secrets.default.set"
    },
    {
      label: "Customize",
      kind: import_vscode10.QuickPickItemKind.Separator
    },
    {
      label: " $(refresh)  Set HTTP Request Timeout",
      description: ` ${settings.apiTimeout}`,
      cmd: "tikbook.show.menu.setup.apitimeout"
    },
    {
      label: " $(terminal)  Set SSH Command",
      description: ` ${settings.sshCommand}`,
      cmd: "tikbook.show.menu.setup.sshcommand"
    },
    {
      label: " $(clear-all)  Clear Password Secret",
      description: `and use empty password or JSON settings`,
      cmd: "tikoci.secrets.default.clear"
    },
    {
      label: " $(settings)  Go to TikBook Settings",
      cmd: "workbench.action.openSettings",
      args: ["@ext:tikoci.tikbook"]
    },
    {
      label: "RouterOS LSP",
      kind: import_vscode10.QuickPickItemKind.Separator
    },
    {
      label: " $(tasklist)  Test RouterOS LSP",
      cmd: "routeroslsp.cmd.testConnection"
    },
    {
      label: " $(settings)  Go to RouterOS LSP Settings",
      cmd: "workbench.action.openSettings",
      args: ["@ext:tikoci.lsp-routeros-ts"]
    },
    ...quickPickBack("tikbook.show.menu.main")
  ], { title: "RouterOS Connection Settings" }).then((item) => {
    if (item?.cmd)
      import_vscode10.commands.executeCommand(item.cmd, item.args && item.args.length > 0 ? item.args[0] : "tikbook.show.menu.setup");
  });
}
async function showSetupBaseUrl(back) {
  const input = import_vscode10.window.showInputBox({
    value: getSettings().baseUrl,
    title: "RouterOS Connection URL",
    placeHolder: "http://admin@192.168.88.1:80",
    ignoreFocusOut: true,
    prompt: "Enter the base URL to RouterOS HTTP/S service. ",
    validateInput: (text) => {
      if (!URL.canParse(text)) {
        return "Must be a valid URL, like https://192.168.88.1";
      }
      const url = new URL(text);
      if (!url)
        return "Must be a valid URL, like https://192.168.88.1";
      log.trace(`<MinuteNumbers.showSetupBaseUrl> found url`, url);
      const allowedProtocols = ["https:", "http:"];
      if (!allowedProtocols.includes(url.protocol))
        return `Protocol must be ${allowedProtocols.join(" or ")}`;
      if (!url.host)
        return `Host must be valid DNS or IP address`;
      if (url.pathname.match(/\/rest([/].*)?$/))
        return `Do not include /rest in URL`;
      if (url.pathname.length > 1)
        return "Do not include a path as /rest added automatically";
      return null;
    }
  }).then((urlString) => {
    if (!urlString)
      return;
    if (!URL.canParse(urlString)) {
      log.info(`<menus.showSetupBaseUrl> got bad url after validation using '${urlString}', user likely cancelled`);
      import_vscode10.window.showWarningMessage(` Nothing updated.  URL '${urlString}' is not valid.`);
      return;
    }
    const conf = import_vscode10.workspace.getConfiguration("tikbook", null);
    const url = URL.parse(urlString);
    if (!url)
      return;
    const newSettings = {};
    if (conf.get("baseUrl") !== newSettings.baseUrl)
      newSettings.baseUrl = `${url.protocol}//${url.host}`;
    if (conf.get("username") !== newSettings.username && url.username.length > 0)
      newSettings.username = url.username;
    if (conf.get("password") !== SecretManager.default.getPassword() && url.password.length > 0)
      newSettings.password = url.password;
    const updatedAttributes = [];
    if (newSettings.baseUrl)
      updatedAttributes.push("baseUrl");
    if (newSettings.username)
      updatedAttributes.push("username");
    if (newSettings.password)
      updatedAttributes.push("password");
    let msg;
    const updateSettings = (settingName, msg2) => {
      return conf.update(settingName, newSettings[settingName], import_vscode10.ConfigurationTarget.Global).then(() => {
        if (msg2) {
          import_vscode10.window.showInformationMessage(msg2);
          log.debug(`<menus.showSetupBaseUrl> notified: ${msg2}`);
        }
      });
    };
    if (updatedAttributes.length > 0) {
      if (newSettings.baseUrl) {
        msg = `TikBook using RouterOS connection URL: ${newSettings.baseUrl}`;
        updateSettings("baseUrl", msg).then(() => {
          if (updatedAttributes.length === 1) {
            if (back)
              import_vscode10.commands.executeCommand(back);
          }
        });
      }
      if (newSettings.username) {
        msg = `Updated TikBook's RouterOS username to '${newSettings.username}'`;
        updateSettings("username").then(async () => {
          if (newSettings.password) {
            await SecretManager.default.setPassword(newSettings.password);
            msg = msg + " and password";
          }
          import_vscode10.window.showInformationMessage(msg);
          log.debug(`<menus.showSetupBaseUrl> notified: ${msg}`);
          if (back)
            import_vscode10.commands.executeCommand(back);
        });
      }
    }
  });
  if (!input && back)
    import_vscode10.commands.executeCommand(back);
  return input;
}
async function showSetupUsername(back) {
  const input = import_vscode10.window.showInputBox({
    value: getSettings().username,
    title: "RouterOS Username",
    placeHolder: "admin",
    ignoreFocusOut: true,
    prompt: `Enter the username for RouterOS HTTP/S connection
`,
    validateInput: (text) => {
      if (text.match(/^[A-Za-z0-9-.]{1,64}$/))
        return null;
      else
        return `The provided username does not appear to be valid.`;
    }
  }).then((username) => {
    let msg;
    const conf = import_vscode10.workspace.getConfiguration("tikbook", null);
    if (conf.get("username") !== username && username && username.length > 0) {
      conf.update("username", username, import_vscode10.ConfigurationTarget.Global).then(() => {
        msg = `Updated TikBook's RouterOS username: ${username}`;
        import_vscode10.window.showInformationMessage(msg);
        log.debug(`<menus.showSetupUsername> notified: ${msg}`);
        if (back)
          import_vscode10.commands.executeCommand(back);
      });
    } else {
      msg = `Nothing to update for TikBook's RouterOS credentials`;
      import_vscode10.window.showInformationMessage(msg);
      log.debug(`<menus.showSetupUsername> showed: ${msg}`);
      if (back)
        import_vscode10.commands.executeCommand(back);
    }
  });
  if (!input && back)
    import_vscode10.commands.executeCommand(back);
  return input;
}
async function showSetupApiTimeout(back) {
  const input = await import_vscode10.window.showInputBox({
    value: getSettings().apiTimeout.toString(10),
    title: "HTTP Request Timeout (in Seconds)",
    placeHolder: "60",
    ignoreFocusOut: true,
    prompt: `Enter the timeout for HTTP/S connections to RouterOS
`,
    validateInput: (text) => {
      const num = Number(text);
      if (!num)
        return "Must be number, in seconds";
      if (num > 0 && num <= 120)
        return null;
      if (num > 120)
        return "Must be less than 120 seconds";
      if (num <= 0)
        return "No time traveling allowed.  Must be > 0 seconds.";
    }
  }).then((timeout) => {
    import_vscode10.workspace.getConfiguration("tikbook", null).update("apiTimeout", Number(timeout), import_vscode10.ConfigurationTarget.Global).then(() => {
      const msg = `Updated timeout to ${Number(timeout).toPrecision(1)}s when connecting to RouterOS`;
      import_vscode10.window.showInformationMessage(msg);
      log.debug(`<menus.showSetupBaseUrl> notified: ${msg}`);
      if (back)
        import_vscode10.commands.executeCommand(back);
    });
  });
  return input;
}
async function showSetupSshCommand(back) {
  const input = await import_vscode10.window.showInputBox({
    value: getSettings().sshCommand,
    title: "Set SSH Command to Launch Terminal",
    placeHolder: "ssh",
    ignoreFocusOut: true,
    prompt: `Unless you have custom configuration, use 'ssh'.
Do not include user@address part as that is provided automatically
`,
    validateInput: (text) => {
      if (!text)
        return `SSH command cannot be empty.  Use 'ssh' if unsure.`;
      if (text.length > 128)
        return "SSH command must be less than 128 characters";
    }
  }).then((text) => {
    import_vscode10.workspace.getConfiguration("tikbook", null).update("sshCommand", text, import_vscode10.ConfigurationTarget.Global).then(() => {
      const msg = `Updated SSH command used in Terminal to '${text}'`;
      import_vscode10.window.showInformationMessage(msg);
      log.debug(`<menus.showSetupBaseUrl> notified: ${msg}`);
      if (back)
        import_vscode10.commands.executeCommand(back);
    });
  });
  return input;
}
function showMenuOutputs() {
  import_vscode10.window.showQuickPick([
    {
      label: "$(tikoci-tikbook) TikBook Logs",
      id: "tikbook"
    },
    {
      label: "$(markdown)  Markdown 'RouterOS Run' Output",
      id: "markdown-run"
    },
    {
      label: "$(mikrotik-icon-line)  RouterOS LSP Logs",
      id: "routeroslsp"
    },
    {
      label: "",
      kind: import_vscode10.QuickPickItemKind.Separator
    },
    {
      label: "$(settings)  Set Log Level",
      description: `currently ${import_vscode10.LogLevel[log.logLevel]}`,
      cmd: "workbench.action.setLogLevel"
    },
    ...quickPickBack("tikbook.show.menu.main")
  ], { title: "Show TikBook Logs (Outputs)" }).then((item) => {
    if (!item)
      return;
    if (item.cmd)
      import_vscode10.commands.executeCommand(item.cmd);
    switch (item.id) {
      case "tikbook":
        log.show();
        break;
      case "markdown-run":
        MarkdownHandlers.log.show();
        break;
      case "routeroslsp":
        import_vscode10.window.showWarningMessage("Unimplemented: cannot show RouterOS LSP logs yet.");
        log.debug("<menus.showMenuOutput> warned user about unimplemented show RouterOS LSP logs");
        break;
      default:
        log.error("<menus.showMenuOutput> show output menu has no command to run");
    }
  });
}
async function showRouterAdminMenu() {
  return import_vscode10.window.showQuickPick([
    {
      label: "Admin Tools",
      kind: import_vscode10.QuickPickItemKind.Separator
    },
    {
      label: "$(globe)  Launch RouterOS Web Admin",
      cmd: "tikbook.browse.router.webfig"
    },
    {
      label: "$(remote)  Open SSH Terminal",
      cmd: "tikbook.open.terminal.router"
    },
    {
      label: "Configuration Files",
      kind: import_vscode10.QuickPickItemKind.Separator
    },
    {
      label: "$(export)  Show Configuration (:export)",
      cmd: "tikbook.show.menu.router.export"
    },
    {
      label: "$(git-pull-request)  Show Default Configuration",
      cmd: "tikbook.open.router.default-configuration.script"
    },
    {
      label: "CSV Exports",
      kind: import_vscode10.QuickPickItemKind.Separator
    },
    {
      label: `$(table)  Show Interfaces as CSV`,
      cmd: "tikbook.open.router.csv",
      args: ["/interface/print detail", "interface.ip"]
    },
    {
      label: `$(table)  Show Interface Statistics as CSV`,
      cmd: "tikbook.open.router.csv",
      args: ["/interface/monitor-traffic [find] once", "monitor-traffic.interface.ip"]
    },
    {
      label: `$(table)  Show IP Neighbors as CSV`,
      cmd: "tikbook.open.router.csv",
      args: ["/ip/neighbor/print detail", "neighbor.ip"]
    },
    {
      label: `$(table)  Show Firewall Connections as CSV`,
      cmd: "tikbook.open.router.csv",
      args: ["/ip/firewall/connection/print detail", "connection.firewall.ip"]
    },
    {
      label: `$(table)  Show DHCP Leases as CSV`,
      cmd: "tikbook.open.router.csv",
      args: ["/ip/dhcp-server/lease/print detail", "lease.dhcp-server.ip"]
    },
    {
      label: "System Scripts",
      kind: import_vscode10.QuickPickItemKind.Separator
    },
    {
      label: "$(code)  View System Scripts",
      cmd: "tikbook.show.menu.router.scripts"
    },
    {
      label: "$(tikoci-tikbook)   Create Notebook from System Scripts",
      cmd: "tikbook.new.notebook.router.scripts"
    },
    {
      label: "$(variable-group)  View and Copy Variables (:global)",
      cmd: "tikbook.show.menu.variables.global"
    },
    {
      label: "$(list-unordered)  Show Scripts as :global functions",
      cmd: "tikbook.open.router.scripts.globals"
    },
    ...quickPickBack("tikbook.show.menu.main")
  ], { title: "RouterOS Management" }).then((item) => {
    if (!item)
      return;
    if (item.cmd) {
      if (item.args && item.args.length > 0)
        import_vscode10.commands.executeCommand(item.cmd, ...item.args);
      else
        import_vscode10.commands.executeCommand(item.cmd);
    }
  });
}
async function showConfigurationExportMenu() {
  const exportTypes = [
    ["compact", "without defaults"],
    ["verbose", "include defaults"],
    ["terse", "'flattened' without default"]
  ];
  const menuitems = exportTypes.map((type) => {
    return {
      label: `$(export)  :export ${type[0]}`,
      description: ` ${type[1]}`,
      cmd: "tikbook.open.router.export",
      args: [type[0]]
    };
  });
  menuitems.push(...quickPickBack("tikbook.show.menu.router.admin"));
  import_vscode10.window.showQuickPick(menuitems, {}).then((item) => {
    if (!item)
      return;
    if (item.cmd)
      import_vscode10.commands.executeCommand(item.cmd, ...item.args ?? []);
  });
}
async function showScriptListMenu() {
  const scripts = await RouterRestClient.default.systemScripts;
  let menuitems = [];
  if (scripts) {
    menuitems = scripts.map((item) => {
      return {
        label: `${item.name}`,
        id: `${item[".id"]}`,
        description: ` ${item.comment}`,
        cmd: "tikbook.open.router.script"
      };
    });
  } else {
    log.error("<menus.showScriptListMenu> {_fetchSystemScripts}");
  }
  menuitems.push(...quickPickBack("tikbook.show.menu.router.admin"));
  import_vscode10.window.showQuickPick(menuitems, { title: "Show System Script as Text Document" }).then((item) => {
    if (!item)
      return;
    if (item.cmd)
      import_vscode10.commands.executeCommand(item.cmd, item.label, item.id);
  });
}
async function showRouterVariableGlobalForClipboard() {
  const keyValues = await RouterRestClient.default.scriptEnvironment();
  if (!keyValues || typeof keyValues !== "object") {
    const msg2 = "No RouterOS variables found to insert";
    import_vscode10.window.showWarningMessage(msg2);
    log.info(`[tikbook.show.menu.variables.global] warned '${msg2}`);
    return;
  }
  const items = keyValues.map((envvar) => ({
    label: `${envvar.name}`,
    description: `  ${envvar.value.length > 64 ? envvar.value.substring(0, 64) + "..." : envvar.value}`
  }));
  items.push(...quickPickBack("tikbook.show.menu.router.admin"));
  const selection = await import_vscode10.window.showQuickPick(items, {
    title: "Copy RouterOS :global Variable",
    canPickMany: false,
    placeHolder: "Select variable name to copy to clipboard"
  });
  if (!selection)
    return;
  const variable = `$${selection.label}`;
  await import_vscode10.env.clipboard.writeText(variable);
  const msg = `Copied RouterOS ${variable} to clipboard`;
  import_vscode10.window.showInformationMessage(msg);
  log.debug(`[tikbook.show.menu.variables.global] notified user '${msg}'`);
}
async function showHelpMenu() {
  const menuitems = [];
  const mikrotikUrls = [
    ["https://forum.mikrotik.com", "MikroTik Forum", "comment-discussion"],
    ["https://help.mikrotik.com/servicedesk/servicedesk", "MikroTik Issue Reporting", "bug"],
    ["https://help.mikrotik.com/docs/x/XQDWAg", "RouterOS Scripting Manual", "code"],
    ["https://help.mikrotik.com/docs", "MikroTik Documentation", "mikrotik-icon-line"]
  ];
  const tikociUrls = [
    ["https://tikoci.github.io", "TIKOCI Homepage", "home"],
    ["https://tikoci.github.io/restraml/", "RouterOS Schema Tools", "diff-multiple", "including diff tool"]
  ];
  menuitems.push({ kind: import_vscode10.QuickPickItemKind.Separator, label: "MikroTik" });
  menuitems.push(...mikrotikUrls.map((item) => {
    return {
      label: `$(${item[2]}) Browse ${item[1]}`,
      url: item[0]
    };
  }));
  menuitems.push({ kind: import_vscode10.QuickPickItemKind.Separator, label: "TIKOCI GitHub" });
  menuitems.push({
    label: `$(tikoci-tikbook) Browse TIKOCI Projects`,
    id: "gitbrowse"
  });
  menuitems.push({
    label: `$(git-fetch) Git Clone TIKOCI Project`,
    id: "gitclone"
  });
  menuitems.push(...tikociUrls.map((item) => {
    return {
      label: `$(${item[2]}) Browse ${item[1]}`,
      url: item[0],
      description: item[3] || undefined
    };
  }));
  menuitems.push({ kind: import_vscode10.QuickPickItemKind.Separator, label: "TikTube Videos" });
  menuitems.push({
    label: `$(device-camera-video)  Scripting: Basics, Part 1`,
    cmd: `tikbook.test.video.embedded`,
    args: [{ name: "Make_your_router_run_Scripts-[GJ-57ByVMWk]", group: "test", chapters: true, languages: ["en", "hu"] }]
  }, {
    label: `$(device-camera-video)  Scripting: Basics, Part 2`,
    cmd: `tikbook.test.video.embedded`,
    args: [{ name: "Make_your_router_run_scripts_pt.2-[2WsFhkLVaMY]", group: "test", chapters: false, languages: ["en"] }]
  }, {
    label: `$(device-camera-video)  Scripting: Data Types`,
    cmd: `tikbook.test.video.embedded`,
    args: [{ name: "Scripting_-_variable_data_types-[9SeYC_s95rw]", group: "test", chapters: true, languages: ["en"] }]
  }, {
    label: `$(device-camera-video)  Scripting: Arrays`,
    cmd: `tikbook.test.video.embedded`,
    args: [{ name: "Scripting_-_working_with_Arrays-[eWCJw0uZ-lE]", group: "test", chapters: true, languages: ["en", "pl"] }]
  }, {
    label: `$(device-camera-video)  RouterOS REST API Setup and Use`,
    cmd: `tikbook.test.video.embedded`,
    args: [{ name: "REST_API_in_RouterOS_v7-[dwEcUa2KXNc]", group: "test", chapters: false, languages: [] }]
  });
  menuitems.push(...quickPickBack("tikbook.show.menu.main"));
  import_vscode10.window.showQuickPick(menuitems, { title: "Help Resources" }).then((item) => {
    if (!item)
      return;
    if (item.cmd && item.args && item.args.length) {
      return import_vscode10.commands.executeCommand(item.cmd, ...item.args);
    } else {
      if (item.cmd)
        return import_vscode10.commands.executeCommand(item.cmd, item.args);
    }
    if (item.url)
      return import_vscode10.env.openExternal(import_vscode10.Uri.parse(item.url));
    switch (item.id) {
      case "gitclone": {
        import_vscode10.commands.executeCommand("tikbook.menu.showTikociRepoPicker", "tikbook.browse.mikrotik.help", false).then((e) => {
          if (e && typeof e === "object" && "git_url" in e) {
            import_vscode10.commands.executeCommand("git.clone", e.git_url);
          }
        });
        break;
      }
      case "gitbrowse":
        import_vscode10.commands.executeCommand("tikbook.menu.showTikociRepoPicker", "tikbook.browse.mikrotik.help", true);
        break;
      default:
    }
  });
}
async function showTikociRepoPicker(back, browse = true) {
  const organization = "tikoci";
  try {
    return await import_vscode10.window.withProgress({
      location: import_vscode10.ProgressLocation.Notification,
      title: `Fetching repositories for ${organization}...`,
      cancellable: false
    }, async () => {
      try {
        const repos = await fetchGitHubRepos(organization);
        if (repos.length === 0) {
          const msg = `No public repositories found for organization: ${organization}`;
          import_vscode10.window.showWarningMessage(msg);
          log.debug(`[tikbook.menu.showTikociRepoPicker] warned user ${msg}`);
          return;
        }
        const options = repos.map((repo) => ({
          label: `${repo.name}`,
          description: repo.language ? `${repo.language} • ⭐ ${repo.stargazers_count}` : `⭐ ${repo.stargazers_count}`,
          detail: repo.description || "No description available",
          repo
        }));
        options.push(...quickPickBack(back));
        const selected = await import_vscode10.window.showQuickPick(options, {
          placeHolder: `Select a repository from ${organization}`,
          matchOnDescription: true,
          matchOnDetail: true
        });
        if (selected) {
          if (selected.cmd)
            return import_vscode10.commands.executeCommand(selected.cmd);
          const selectedRepo = selected.repo;
          if (browse && selectedRepo)
            import_vscode10.env.openExternal(import_vscode10.Uri.parse(selectedRepo.html_url));
          return selectedRepo;
        }
      } catch (error) {
        const msg = `Menu skipped, failed to fetch repositories to show`;
        import_vscode10.window.showWarningMessage(msg);
        log.warn(`[tikbook.menu.showTikociRepoPicker] warned user ${msg}`, error);
      }
    });
  } catch (error) {
    log.warn(`[tikbook.menu.showTikociRepoPicker] got exception`, error);
    import_vscode10.window.showWarningMessage(`Got an unexpected error trying to show menu. Check logs`);
  }
}

// src/commands.ts
var import_vscode11 = require("vscode");
function initializeCommands() {
  const killswitch = new import_vscode11.CancellationTokenSource;
  return [
    import_vscode11.commands.registerCommand("tikoci.secrets.default.set", async (_) => {
      log.trace("[tikoci.secrets.default.set] invoked");
      await SecretManager.default.setPassword(_);
    }),
    import_vscode11.commands.registerCommand("tikoci.secrets.default.clear", async (_) => {
      log.trace("[tikoci.secrets.default.clear] invoked");
      await SecretManager.default.clearPassword(_);
    }),
    import_vscode11.commands.registerCommand("tikbook.show.output.tikbook", async () => {
      log.trace("[tikbook.show.output.tikbook] invoked");
      log.show();
    }),
    import_vscode11.commands.registerCommand("tikbook.show.output.routeroslsp", async () => {
      log.info("[tikbook.show.output.routeroslsp] is not implemented, skipping");
      import_vscode11.window.showWarningMessage(`Show RouterOS LSP Logs is not supported.
Use Output panel and select "RouterOS LSP" as output type.`);
    }),
    import_vscode11.commands.registerCommand("tikbook.routeros.reopen.notebook.routeros", async (_uri) => {
      const uri = _uri || import_vscode11.window.activeTextEditor?.document.uri;
      const openNotebooksMatching = import_vscode11.window.visibleNotebookEditors.filter((e) => e.notebook.uri.path === uri?.path);
      if (openNotebooksMatching.length > 0) {
        import_vscode11.window.showNotebookDocument(openNotebooksMatching[0].notebook, { preserveFocus: false });
      } else {
        import_vscode11.commands.executeCommand("vscode.openWith", uri, "tikbook", import_vscode11.ViewColumn.Beside);
      }
    }),
    import_vscode11.commands.registerCommand("tikbook.vdoc.clone.tikbook", async () => {
      const vdoc = import_vscode11.window.activeTextEditor?.document;
      if (!vdoc)
        return;
      const content = vdoc.getText();
      const buffer = new TextEncoder().encode(content);
      const notebookData = await new ScriptSerializer().deserializeNotebook(buffer, killswitch.token);
      import_vscode11.window.showNotebookDocument(await import_vscode11.workspace.openNotebookDocument("tikbook", notebookData));
    }),
    import_vscode11.commands.registerCommand("tikbook.vdoc.clone.markdown", async () => {
      const vdoc = import_vscode11.window.activeTextEditor?.document;
      if (!vdoc)
        return;
      const content = vdoc.getText();
      const buffer = new TextEncoder().encode(content);
      const notebookData = await new MarkdownSerializer().deserializeNotebook(buffer, killswitch.token);
      const notebookDoc = await import_vscode11.workspace.openNotebookDocument("markdown-routeros", notebookData);
      import_vscode11.window.showNotebookDocument(notebookDoc);
    }),
    import_vscode11.commands.registerCommand("tikbook.markdown.reopen.notebook", async (uri) => {
      const activeEditor = import_vscode11.window.activeTextEditor;
      const targetUri = uri || activeEditor?.document.uri;
      if (!targetUri) {
        const msg = "No file uri was found.  Cannot reopen as Markdown RouterOS notebook.";
        import_vscode11.window.showWarningMessage(msg);
        log.info(`[tikbook.markdown.reopen.notebook] not possible editorLangId '${activeEditor?.document.languageId}', warned user '${msg}'`);
        return;
      }
      try {
        await import_vscode11.commands.executeCommand("vscode.openWith", targetUri, "markdown-routeros");
        import_vscode11.window.showInformationMessage(`Opened '${targetUri.fsPath}' with RouterOS Notebook.`);
        log.debug(`[tikbook.markdown.reopen.notebook] opened ${targetUri.toString()}`);
      } catch (error) {
        const msg = `Failed to open notebook, got exception '${error instanceof Error ? error.cause : String(error)}'`;
        import_vscode11.window.showWarningMessage(msg);
        log.warn(`[tikbook.markdown.reopen.notebook] got exception and warned user '${msg}'`, error);
      }
    }),
    import_vscode11.commands.registerCommand("tikbook.browse.mikrotikstatus", () => {
      import_vscode11.env.openExternal(import_vscode11.Uri.parse("https://mikrotikstat.us"));
    }),
    import_vscode11.commands.registerCommand("tikbook.browse.tikoci.home", () => {
      import_vscode11.env.openExternal(import_vscode11.Uri.parse("https://tikoci.github.io"));
    }),
    import_vscode11.commands.registerCommand("tikbook.browse.mikrotik.forum", () => {
      import_vscode11.env.openExternal(import_vscode11.Uri.parse("https://forum.mikrotik.com"));
    }),
    import_vscode11.commands.registerCommand("tikbook.browse.mikrotik.issues", () => {
      import_vscode11.env.openExternal(import_vscode11.Uri.parse("https://help.mikrotik.com/servicedesk/servicedesk"));
    }),
    import_vscode11.commands.registerCommand("tikbook.browse.mikrotik.docs.scripting", () => {
      import_vscode11.env.openExternal(import_vscode11.Uri.parse("https://help.mikrotik.com/docs/x/XQDWAg"));
    }),
    import_vscode11.commands.registerCommand("tikbook.browse.mikrotik.docs", () => {
      import_vscode11.env.openExternal(import_vscode11.Uri.parse("https://help.mikrotik.com/docs"));
    }),
    import_vscode11.commands.registerCommand("tikbook.browse.router.webfig", () => {
      import_vscode11.env.openExternal(import_vscode11.Uri.parse(`${getSettings().baseUrl}`));
    })
  ];
}

// src/converters.ts
var import_vscode12 = require("vscode");
function initializeConverters() {
  return [
    import_vscode12.commands.registerCommand("tikbook.fn.copyJsonAsRouterArray", async () => {
      const editor = import_vscode12.window.activeTextEditor;
      if (!editor) {
        const msg = "JSON to RouterOS array needs a JSON document as source";
        import_vscode12.window.showWarningMessage(msg);
        log.info(`[tikbook.fn.copyJsonAsRouterArray] called but found no editor, warned '${msg}'`);
        return;
      }
      try {
        import_vscode12.env.clipboard.writeText(routerosArrayFromJson(JSON.parse(editor.document.getText(editor.selection.isEmpty ? undefined : editor.selection))));
        const msg = "RouterOS array copied to clipboard from JSON";
        import_vscode12.window.showInformationMessage(msg);
        log.debug(`[tikbook.fn.copyJsonAsRouterArray] notified user '${msg}'`);
      } catch {
        const msg = "Invalid JSON cannot be copied as RouterOS array";
        import_vscode12.window.showWarningMessage(msg);
        log.warn(`[tikbook.fn.copyJsonAsRouterArray] warned user '${msg}'`);
      }
    }),
    import_vscode12.commands.registerCommand("tikbook.convert.escapedRouterString.clipboard", async () => {
      const editor = import_vscode12.window.activeTextEditor;
      if (!editor) {
        const msg2 = "Nothing copied. To copy an escaped RouterOS string, some document or selection is needed.";
        import_vscode12.window.showWarningMessage(msg2);
        log.info(`[tikbook.convert.escapedRouterString.clipboard] warned user '${msg2}'`);
        return;
      }
      import_vscode12.env.clipboard.writeText(escapeRouterString(editor.document.getText(editor.selection.isEmpty ? undefined : editor.selection)));
      const msg = "RouterOS array copied to clipboard";
      import_vscode12.window.showInformationMessage(msg);
      log.debug(`[tikbook.convert.escapedRouterString.clipboard] notified user '${msg}'`);
    })
  ];
}
function escapeRouterString(text) {
  if (typeof text !== "string") {
    throw new TypeError("Input must be a string");
  }
  let result = "";
  for (const char of text) {
    const charCode = char.charCodeAt(0);
    switch (char) {
      case '"':
        result += "\\\"";
        break;
      case "$":
        result += "\\$";
        break;
      case "\\":
        result += "\\\\";
        break;
      default:
        if (charCode < 32 || charCode === 127 || charCode > 127) {
          switch (char) {
            case `
`:
            case "\t":
            case "\r":
              result += char;
              break;
            default:
              result += `\\${charCode.toString(16).toUpperCase().padStart(2, "0")}`;
          }
        } else {
          result += char;
        }
        break;
    }
  }
  return result;
}
function routerosArrayFromJson(data) {
  if (data === null || typeof data === "undefined") {
    return "[:nothing]";
  }
  if (typeof data === "string") {
    const escapedString = escapeRouterString(data);
    return `"${escapedString}"`;
  }
  if (typeof data === "number") {
    if (Number.isInteger(data) && data > 0) {
      return data.toString();
    } else {
      return `"${data.toString()}"`;
    }
  }
  if (typeof data === "boolean") {
    return data ? "true" : "false";
  }
  if (Array.isArray(data)) {
    const elements = data.map((item) => routerosArrayFromJson(item)).join(";");
    return `{${elements}}`;
  }
  if (typeof data === "object") {
    const keys = Object.keys(data);
    if (keys.length === 0) {
      return '[:toarray ""]';
    }
    const keyValuePairs = keys.map((key) => {
      const value = routerosArrayFromJson(data[key]);
      return `"${key}"=${value}`;
    });
    return `{${keyValuePairs.join(";")}}`;
  }
  return '""';
}

// src/extension.ts
function activate(context) {
  log.info("TikBook <activate> started");
  context.subscriptions.push(SecretManager.start(context), ...initializeLogging(), ...initializeMenus(), ...initializeCommands(), ...initializeNotebookEngines(), ...initializeVirtualDocs(), ...initializeSSH(), ...initializeConverters(), new MarkdownHandlers(context), new StatusWatchdog(context), new VideoViewer(context));
  log.info("TikBook <activate> ended");
}
function deactivate() {
  log.info("TikBook <deactivate> invoked");
}

//# debugId=03EF333C4E443AD764756E2164756E21
//# sourceMappingURL=extension-web.js.map
