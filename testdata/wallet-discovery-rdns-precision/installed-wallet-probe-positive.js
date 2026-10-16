// Installed-wallet probe: checks packages and data dirs for wallet
// artifacts without declaring any provider rdns names. Both the bundle
// atom and the keyword cluster MUST still fire here.
function findWallets() {
	checkPackage("metamask");
	checkDataDir("metamask");
	checkExtension("metamask");
	checkProcess("metamask");
	checkPackage("com.exodus");
	return collected;
}
