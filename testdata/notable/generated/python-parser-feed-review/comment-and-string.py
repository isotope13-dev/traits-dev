# tree = ast.parse(cell)
# parser.feed_data(request)
# parse_request_fast(request)
example = "parser.feed_data(request)"
parser.preparse_request(request)
parse_request_fast_extra(request)
parser.feed_database(request)
parser.parse_bytes_extra(request)
