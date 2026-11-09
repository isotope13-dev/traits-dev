from os.path import dirname, join, exists
from dotenv import load_dotenv


def up(d):
    while d != dirname(d):
        if exists(join(d, ".env")):
            return join(d, ".env")
        d = dirname(d)


load_dotenv(up("."))
