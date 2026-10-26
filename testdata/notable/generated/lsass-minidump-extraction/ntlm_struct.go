package auth

// NtlmCredential carries LM/NT challenge-response material for the
// protocol dissector under test. Vectors only, no live logon.
type NtlmCredential struct {
	LmHash []byte
	NtHash []byte
}
