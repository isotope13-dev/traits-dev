package consent

// Sales-objection domain language: a bare "objection" string is an ordinary
// English word (sales objections, GDPR right-to-object enums), not mobile
// instrumentation discovery on its own.

type ClaimKind string

const (
	ClaimKindObjection ClaimKind = "objection"
	ClaimKindNoObjection ClaimKind = "no_objection"
)

func objectionReason(kind ClaimKind) string {
	switch kind {
	case ClaimKindObjection:
		return "common_objections"
	default:
		return "none"
	}
}
