package cleanup

import "github.com/lu4p/shred"

func erase(path string) {
 shred.Path(path, shred.Conf{Remove: true, Times: 3, Zeros: true})
}
