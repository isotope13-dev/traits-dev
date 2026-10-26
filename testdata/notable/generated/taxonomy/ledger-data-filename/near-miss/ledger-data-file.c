// Near-miss control: an application data file reference (accounting-style
// ingestion ledger) with no wallet meaning. The brand-family atom must stay
// silent despite the "ledger" substring.
static const char store[] = "ingestion-ledger.json";

const char *store_at(int i) {
    return store + i;
}

int main(void) {
    return (int)store_at(0)[0];
}
