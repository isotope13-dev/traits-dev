// assets-sdk setup reads the deploy wallet mnemonic from env.
// See github.com/ton-community/assets-sdk (assets-cli setup-env).
import { AssetsSDK } from "@ton-community/assets-sdk";

const mnemonic = process.env.WALLET_MNEMONIC;
export function wallet() {
  return { mnemonic };
}
export { AssetsSDK };
