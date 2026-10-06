package main

// CLI help text documenting tmp paths is documentation, not a hidden
// runtime config: the hidden-tmp mention here must not convict on its own.
const helpMsg = `Examples:
	xmeta -x -in=~/.ais0/.ais.conf -out=/tmp/conf.txt - extract Config
	xmeta -in=/tmp/conf.txt -out=/tmp/.ais.conf       - format config
`

func main() {
	println(helpMsg)
}
