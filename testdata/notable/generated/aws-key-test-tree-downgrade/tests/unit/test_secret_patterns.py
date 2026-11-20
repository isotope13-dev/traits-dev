"""Secret-pattern unit test: an AWS-shaped literal inside a test tree."""

import re

AWS_PATTERN = re.compile(r"AKIA[0-9A-Z]{16}")


def test_detects_aws_key_shape() -> None:
    aws_access_key = "AKIAJKLMNOPQRSTUVWXY"
    assert AWS_PATTERN.search(aws_access_key)
