from setuptools import setup

setup(
    name="wallet-helper",
    version="1.0",
    py_modules=["wallet_helper"],
    entry_points={"console_scripts": ["herewalletbot=herewalletbot.herewalletbot:main"]},
)
