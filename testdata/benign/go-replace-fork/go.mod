module github.com/example-org/service

go 1.23

require (
	github.com/google/btree v1.1.3
	golang.org/x/net v0.27.0
	gopkg.in/yaml.v3 v3.0.1
)

// Carry a bugfix until it lands upstream; develop the client locally.
replace github.com/google/btree => github.com/example-org/btree v1.1.4-fix
replace github.com/example-org/client => ../client
