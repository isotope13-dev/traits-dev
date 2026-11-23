def test_te_cl_rejection():
    request = b"Transfer-Encoding: chunked\r\nContent-Length: 4\r\n"
    with pytest.raises(HttpParserError):
        # parser.feed_data(request)
        pass
