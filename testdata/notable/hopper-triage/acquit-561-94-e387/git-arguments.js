spawn('git', ['reset', '--hard', 'HEAD']);
spawn('git', ['apply', '--index', '--recount', '--cached', '--binary', '-3']);
