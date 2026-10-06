// Operator wallet setup (cf. @ton-community/assets-sdk CLI): the SDK deploys
// the operator's own token assets, so reading the documented WALLET_TYPE
// deploy selector is expected dev-tool behavior, not secret harvesting.
const { AssetsSDK } = require("./assets-sdk-shim");

async function createEnv() {
    if (process.env.WALLET_TYPE === undefined)
        throw new Error("No WALLET_TYPE in env!");
    if (process.env.WALLET_TYPE !== "highload-v2")
        throw new Error(`Unknown wallet type: ${process.env.WALLET_TYPE}`);
    return AssetsSDK.create({ walletType: process.env.WALLET_TYPE });
}

module.exports = { createEnv };
