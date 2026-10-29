package observation

func observe(builder Writer, reader Reader, source Reader) {
	go worker()
	builder.WriteString("LIMIT ")
	reader.ReadFrom(source)
	antidebug.IsDebuggerPresent()
	cpuidHypervisorReport()
	RDTSCDelta(9)
}
