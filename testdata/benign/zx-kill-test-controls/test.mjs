import {strict as assert} from 'assert'

if (test('The kill() method works')) {
  let p = nothrow($`sleep 9999`)
  setTimeout(() => {
    p.kill()
  }, 100)
  await p
}

if (test('The signal is passed with kill() method')) {
  let p = $`while true; do :; done`
  setTimeout(() => p.kill('SIGKILL'), 100)
  let signal
  try {
    await p
  } catch (p) {
    signal = p.signal
  }
  assert.equal(signal, 'SIGKILL')
}
