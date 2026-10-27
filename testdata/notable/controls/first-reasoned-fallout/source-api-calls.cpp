void operations() {
 process_vm_readv(pid, &local, 1, &remote, 1, 0);
 crypto_pwhash(out, n, password, size, salt, ops, mem, alg);
 crypto_box_seal(out, input, n, key);
 crypto_box_seal_open(out, input, n, key, secret);
}
