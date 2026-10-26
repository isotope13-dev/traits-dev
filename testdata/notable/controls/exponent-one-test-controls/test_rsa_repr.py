"""Degenerate RSA public-number unit tests, as shipped by crypto libraries to
verify repr, equality, and validation behavior on toy inputs."""
from cryptography.hazmat.primitives.asymmetric.rsa import (
    RSAPrivateNumbers,
    RSAPublicNumbers,
)


def test_public_number_repr():
    num = RSAPublicNumbers(1, 1)
    assert repr(num) == "<RSAPublicNumbers(e=1, n=1)>"


def test_public_numbers_equality():
    num = RSAPublicNumbers(1, 2)
    num2 = RSAPublicNumbers(1, 2)
    assert num == num2
    assert num != RSAPublicNumbers(1, 3)


def test_private_numbers_equality():
    priv1 = RSAPrivateNumbers(1, 2, 3, 4, 5, 6, RSAPublicNumbers(1, 2))
    priv2 = RSAPrivateNumbers(1, 2, 3, 4, 5, 6, RSAPublicNumbers(1, 2))
    assert priv1 == priv2
