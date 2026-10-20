package example

func run() {
    os.Setenv("TS_DEBUG_DERP_WS_CLIENT", "true")
    BeaconDataParse()
    start("userspace-networking", "-no-logs-no-support")
}
