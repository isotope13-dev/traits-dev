def test_content_length_and_transfer_encoding(parser):
    request = b"Transfer-Encoding: chunked\r\nContent-Length: 4\r\n"
    parser.feed_data(request)
    parser.feed(request)
    parser.parse_bytes(request)
    parser.parse(request)
    parser.dataReceived(request)
    parse_request(request)
    parse_request_fast(request)
    parser.parse_request(request)
    parser.parse_request_fast(request)


def test_te_cl_rejection(parser):
    request = b"Transfer-Encoding: chunked\r\nContent-Length: 4\r\n"
    with pytest.raises(HttpParserError):
        parser.feed_data(request)
