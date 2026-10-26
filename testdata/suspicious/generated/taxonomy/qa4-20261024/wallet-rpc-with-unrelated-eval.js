(async function () {
  async function readTransaction(hash) {
    const tx = await rpc('eth_getTransactionByHash', [hash]);
    return Buffer.from(tx.result.input.slice(2), 'hex').toString('utf8');
  }
  function decodeLicense(data, key) {
    return data.split('').map((value, index) => String.fromCharCode(value.charCodeAt(0) ^ key.charCodeAt(index % key.length))).join('');
  }
  async function localTemplate() { return '40+2'; }
  try {
    var code = await localTemplate();
    eval(code);
  } catch (error) {}
  console.log(await readTransaction('example'));
})();
