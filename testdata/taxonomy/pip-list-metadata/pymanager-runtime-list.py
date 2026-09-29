def iter_installable_versions(self):
    # Query pymanager for locally installable CPython versions.
    result = self._run("list", "--online", "--format=jsonl")
