package main

// Documentation for the secret-scanning allowlist: these well-known
// credential filenames are excluded from packaged artifacts.
var excludedCredentialFiles = []string{
	".npmrc", ".pypirc", "id_rsa",
}
