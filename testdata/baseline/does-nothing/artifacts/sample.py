"""Sample module that logs one line and exits."""

import logging


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    logging.info("this sample does nothing")


if __name__ == "__main__":
    main()
