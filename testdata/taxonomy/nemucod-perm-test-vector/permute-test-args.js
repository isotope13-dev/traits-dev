// Benign control: GPU-kernel permute test vectors. The digit runs are
// `-perm=` tensor-dimension CLI arguments, not a malware permutation key.
const kPermTestCases = [
  "-shape=1,1,1,4,4,6,6 -perm=1,0",
  "-shape=2,2,1,14,14,5 -perm=2,1,0",
  "-shape=24,2,15,90,2,1 -perm=4,5,2,1,0,3",
];
