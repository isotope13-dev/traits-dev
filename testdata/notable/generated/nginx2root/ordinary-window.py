from hyperframe.frame import SettingsFrame, WindowUpdateFrame, PingFrame, HeadersFrame, RstStreamFrame
from hpack import Encoder


def queued_credit_probe(authority, resource, body_size=4096):
    yield b'PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n'
    settings = SettingsFrame(0)
    settings.settings[4] = 65535
    yield settings.serialize()
    credit = WindowUpdateFrame(0)
    credit.window_increment = 65535
    yield credit.serialize()
    headers = HeadersFrame(1)
    headers.flags.add('END_HEADERS')
    headers.flags.add('END_STREAM')
    headers.data = Encoder().encode([
        (':method', 'GET'), (':scheme', 'https'),
        (':authority', authority), (':path', resource)])
    yield headers.serialize()
    ping = PingFrame(0)
    ping.opaque_data = b'12345678'
    for counter in range(3):
        yield ping.serialize()
    stream_credit = WindowUpdateFrame(1)
    stream_credit.window_increment = body_size
    yield stream_credit.serialize()
    credit.window_increment = body_size
    yield credit.serialize()
    reset = RstStreamFrame(1)
    reset.error_code = 8
    yield reset.serialize()
