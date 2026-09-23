// Benign control: virtualization API bindings that name wipe-algorithm
// standards (DoD 5220.22-M, Gutmann) as enum constants, after libvirt-go's
// storage_volume.go. Naming a standard is not wiping: no
// objectives/impact/wipe finding is valid here.
package libvirt

/*
#cgo pkg-config: libvirt
#include <stdlib.h>
*/
import "C"

type StorageVolWipeAlgorithm int

const (
	STORAGE_VOL_WIPE_ALG_ZERO    = StorageVolWipeAlgorithm(C.VIR_STORAGE_VOL_WIPE_ALG_ZERO)
	STORAGE_VOL_WIPE_ALG_DOD     = StorageVolWipeAlgorithm(C.VIR_STORAGE_VOL_WIPE_ALG_DOD)
	STORAGE_VOL_WIPE_ALG_GUTMANN = StorageVolWipeAlgorithm(C.VIR_STORAGE_VOL_WIPE_ALG_GUTMANN)
)
