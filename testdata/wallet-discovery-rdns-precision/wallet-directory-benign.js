'use client'
// Fallback wallet directory excerpt: brand rows plus each provider's
// self-reported EIP-6963 rdns discovery name. Naming wallets here is the
// directory's purpose, so neither the bundle atom nor the keyword cluster
// may fire.
var groups = {
	metamask: {
		brand: {
			alt: "MetaMask",
			primaryColor: "#E2761B",
			spriteId: "metamask"
		},
		chainGroup: "metamask",
		group: "metamask",
		key: "metamask",
		name: "MetaMask",
		rdns: "io.metamask"
	},
	exodus: {
		brand: {
			alt: "Exodus Wallet",
			spriteId: "exodus"
		},
		key: "exodus",
		name: "Exodus",
		rdns: "com.exodus.web3-wallet"
	},
	coinbase: {
		brand: {
			alt: "Coinbase Wallet",
			spriteId: "coinbase"
		},
		key: "coinbase",
		name: "Coinbase",
		rdns: "com.coinbase.wallet"
	}
};
export default groups;
