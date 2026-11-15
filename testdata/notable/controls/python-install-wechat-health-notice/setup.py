import requests
from setuptools import setup


def send_health_notice():
    requests.post(
        "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=00000000-0000-0000-0000-000000000000",
        json={"status": "ready"},
    )


setup(name="fixture", version="0.0.0", packages=[])
