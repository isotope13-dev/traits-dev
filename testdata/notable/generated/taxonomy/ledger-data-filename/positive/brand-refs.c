// Positive control: genuine hardware-wallet brand references with no ledger
// data filename present. The brand-family atom must fire.
static const char brands[] = "Ledger Live device bridge; Trezor Suite peer";

const char *brand_at(int i) {
    return brands + i;
}

int main(void) {
    return (int)brand_at(0)[0];
}
