// Installed-wallet probe: checks packages and data dirs for wallet
// artifacts without declaring any provider rdns names. The bundle reference
// remains; without file reads this does not establish credential acquisition.
function findWallets() {
	checkPackage("metamask");
	checkDataDir("metamask");
	checkExtension("metamask");
	checkProcess("metamask");
	checkPackage("com.exodus");
	return collected;
}
