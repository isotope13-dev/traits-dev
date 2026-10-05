// Staging tool that pins the sckit framework wire schemas and CI mode
// markers used by this operator's campaigns.
package main

import "supplychain.local/campaign/internal/wire"

const (
	ControlSchema   = "sckit.control.v1"
	AdmissionSchema = "sckit.admission.v1"
	ResultSchema    = "sckit.module-result.v1"
	TombstoneSchema = "sckit.tombstone.v1"
	CipherSuite     = "sckit/xchacha/v1"

	InitialCIExecution = "sckit.initial-ci-execution-context.v2"
	InitialCIResult    = "sckit.initial-ci-module-result.v2"
	CIResultMarker     = "SCKIT_CI_RESULT_V2"
	CICheckoutEnv      = "SCKIT_INITIAL_CI_CHECKOUT_SHA"
)

var credentialFiles = []string{
	".npmrc", ".pypirc", ".git-credentials", ".netrc",
	"id_rsa", "id_ecdsa", "id_ed25519", ".vault-token",
}

var _ = wire.ParseManifest
