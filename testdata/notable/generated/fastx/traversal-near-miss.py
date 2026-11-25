import urllib.parse


def normalize_relative(path, depth):
    encoded = urllib.parse.quote(path.lstrip("/"), safe="/").replace("/", "%2f")
    return "%2e%2e%2f" * depth + encoded


def check_sample_text(text):
    return "root" in text and "/usr/local/bin" in text
