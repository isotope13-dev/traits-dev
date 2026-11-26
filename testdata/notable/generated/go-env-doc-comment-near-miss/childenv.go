package main

import "os"

// childEnvironment applies overrides to a copy of os.Environ(): "KEY=VALUE" sets or overrides.
func childEnvironment(overrides []string) []string {
	var env []string
	for _, kv := range os.Environ() {
		env = append(env, kv)
	}
	return append(env, overrides...)
}
