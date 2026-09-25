// Regression fixture for the Tonkeeper TonAPI library identity traits: the
// client import and the tonapi-adapter marker below must resolve to the
// @ton-api SDK identity. This fixture opens no contract and sends nothing.
const { TonApiClient } = require("@ton-api/client");
module.exports = { TonApiClient };
