package fixture

import (
    "flag"
    "os/exec"
)

func negative(prog, archive, output string) {
    _ = exec.Command(prog, "-q", archive, "-d", output)
    fs := flag.NewFlagSet("archiver", flag.ContinueOnError)
    var encryptCD bool
    var seekChunkSize int
    fs.BoolVar(&encryptCD, "e", false, "Encrypt Central Directory (CDE)")
    fs.IntVar(&seekChunkSize, "seek-chunk", 0, "Seek chunk size for solid archives")
    _ = "pycharm.application"
    _ = "pycharm.shell"
}
