package diskfsfixture

// Regression fixture for the go-diskfs library identity traits: the module
// import path below must resolve to the go-diskfs library identity, never to
// a hostile verdict. This fixture never opens a device or a disk image.
import _ "github.com/diskfs/go-diskfs/disk"
