import re
pattern = re.compile(r"<!DOCTYPE\s+([^>]+)>")
html_indicators = [r"<html", r"<!DOCTYPE"]
