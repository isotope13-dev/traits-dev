var test = require('tap').test
var spawn = require('child_process').spawn
var SIGSEGV = require('constants').SIGSEGV

var payload = "process.kill(process.pid, 'SIGSEGV')"

test('lifecycle signal abort', function (t) {
  var child = spawn(process.execPath, ['-e', payload])
  child.on('close', function (code, signal) {
    t.ok((code === 128 + SIGSEGV) || signal === 'SIGSEGV')
    t.end()
  })
})
