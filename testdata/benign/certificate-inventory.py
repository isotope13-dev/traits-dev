import requests


def certificate_names(domain):
    response = requests.get(f"https://crt.sh/?q=%25.{domain}&output=json", timeout=10)
    names = set()
    for entry in response.json():
        name_value = entry.get("name_value", "")
        names.update(name_value.split("\n"))
    return names
