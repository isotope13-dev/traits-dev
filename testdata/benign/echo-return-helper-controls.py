"""Benign echo-and-return helper: prints its input and returns it unchanged."""


def echo_and_return(text):
    print(text)
    return text


if __name__ == "__main__":
    echo_and_return("hello")
