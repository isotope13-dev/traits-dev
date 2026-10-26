package compose

// Comms-staging module reference: a stager.go filename mention stages
// nothing by itself; only the compiled-hidden-stager composite carries
// staging intent.

// See internal/compose/commsstager.go for the message staging pass.
func refuseAtStaging() bool {
	return false
}
