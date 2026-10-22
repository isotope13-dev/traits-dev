with open(path) as wordlist:
    for password in wordlist:
        check_local_hash(password)
