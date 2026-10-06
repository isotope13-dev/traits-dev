package common

import "strings"

// esxcli runs a command on the ESXi host over SSH and returns its output.
// The --formatter flag requests machine-readable CSV output for parsing.
func (d *ESX5Driver) esxcli(args ...string) (string, error) {
	stdout, err := d.ssh("esxcli --formatter csv "+strings.Join(args, " "), nil)
	if err != nil {
		return "", err
	}
	return stdout, nil
}
