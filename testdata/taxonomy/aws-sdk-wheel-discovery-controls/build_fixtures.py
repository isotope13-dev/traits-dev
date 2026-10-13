#!/usr/bin/env python3
"""Build deterministic SDK wheels for cloud-discovery scope controls."""
from pathlib import Path
from zipfile import ZIP_STORED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parent
CALLS = """\
ec2.describe_instances()
ec2.describe_instance_types()
ec2.describe_instance_type_offerings()
ec2.describe_account_attributes()
ec2.describe_security_groups()
ec2.describe_key_pairs()
ec2.describe_capacity_reservations()
ec2.describe_availability_zones()
ec2.describe_regions()
ec2.describe_launch_templates()
ec2.create_instance_export_task()
"""
NINE_CALLS = "\n".join(CALLS.splitlines()[:9]) + "\n"


def build(filename: str, distribution: str, package: str, member: str, body: str) -> None:
    members = {
        f"{distribution}-0.0.0.dist-info/METADATA":
            f"Metadata-Version: 2.1\nName: {distribution}\nVersion: 0.0.0\n\n",
        f"{distribution}-0.0.0.dist-info/WHEEL":
            "Wheel-Version: 1.0\nGenerator: taxonomy-control\n"
            "Root-Is-Purelib: true\nTag: py3-none-any\n",
        f"{package}/__init__.py": "",
        member: body,
    }
    with ZipFile(ROOT / filename, "w") as archive:
        for name, content in sorted(members.items()):
            info = ZipInfo(name, date_time=(2020, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_STORED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, content)


build("positive-boto3-addon.whl", "boto3", "boto3", "addon/discover.py", CALLS)
build("positive-botocore-addon.whl", "botocore", "botocore", "addon/discover.py", CALLS)
build("near-miss-nine-calls.whl", "boto3", "boto3", "addon/discover.py", NINE_CALLS +
      "ec2.create_instance_export_task()\n")
build("sdk-package-path-control.whl", "botocore", "botocore", "botocore/session.py", CALLS)
