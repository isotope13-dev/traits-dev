package chain

import "os"

// Mirrors Ignite CLI's InitChain (ignite/services/chain/init.go): home is
// the blockchain node's data dir returned by a `.Home()` accessor, removed
// as documented pre-init cleanup -- not the user's home root.
func (c *Chain) InitChain() error {
	home, err := c.Home()
	if err != nil {
		return err
	}
	if err := os.RemoveAll(home); err != nil {
		return err
	}
	return nil
}
