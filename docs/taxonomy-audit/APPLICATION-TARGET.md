# Android application-target identifiers

Google Play Store and Google Play Services package-name literals were in
`micro-behaviors/network/interface/`. Their strings identify packages that
other rules may select; they are not network-interface names or evidence of
adapter interaction. They now live in
`micro-behaviors/os/application/target/android.yaml`, alongside a description
that limits the claim to a referenced application target. The match does not
establish that the package is installed, that an API acted on it, or that the
analyzed program is that app.

This placement keeps the capability taxonomy independent of how a package ID
is represented (source text, XML, bytecode, or native data). More specific
operation rules remain in their technique home: Android VPN allow/exclusion
operations remain in `os/network/tunnel`, and package-manager query/install
operations remain in `os/package-manager`. The Play Store identity-forgery
composite references the same target identifier as evidence of a referenced
identity; the atom does not assert forgery by itself.

The move updates the VPN allow/exclusion composites and Play Store identity
composite to the new canonical IDs. It also narrows generic directory consumers
of `network/interface/`: the discovery and stealer composites and the
webhook network-identity composite no longer inherit Android application-target
literals as interface evidence. This is intentional. A referenced app package
is not host network configuration or network identity. The webhook composite
still requires an IP-field signal and has separate explicit route, tunnel,
neighbor, and interface signals; the host recon composites retain their direct
network and system-information inputs.

The canonical matcher, `for:` scopes, and Electron exclusion are unchanged; the
[move ledger](application-target-mapping.json) records the field comparison. The
interface leaf now has 50 rules, down from 52. The new target leaf has two.
