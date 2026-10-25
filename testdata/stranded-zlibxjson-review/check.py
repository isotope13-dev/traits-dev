"""Check directory binding and the limits of literal-URL exclusion."""
import json
from pathlib import Path
import sys

directory = "micro-behaviors/fs/directory/create::python-create-missing-directory"
url = "micro-behaviors/communications/http/get::requests-get-without-reserved-literal-prefix"
expected = {
    "guarded-cache.py": ({directory}, set()),
    "different-directory.py": (set(), {directory}),
    "existing-directory.py": (set(), {directory}),
    "reserved-literal.py": (set(), {url}),
    # The call's written argument is an identifier, even though its binding
    # happens to contain a reserved URL. The rule does not resolve that value.
    "reserved-variable.py": ({url}, set()),
}
seen = set()
for line in Path(sys.argv[1]).read_text().splitlines():
    for file in json.loads(line)["files"]:
        name = Path(file["path"]).name
        if name not in expected:
            continue
        present, absent = expected[name]
        actual = {trait["id"] for trait in file.get("traits", [])}
        assert present <= actual and not absent & actual, (name, actual)
        seen.add(name)
        print("PASS", name)
assert seen == set(expected), ("missing fixtures", set(expected) - seen)
