package example

func useWebsockets() bool {
    return envknob.Bool("TS_DEBUG_DERP_WS_CLIENT")
}
