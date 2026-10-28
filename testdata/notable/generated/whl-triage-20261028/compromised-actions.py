from dataclasses import dataclass
@dataclass
class CompromisedAction:
    malicious_refs: tuple[str,...]
    advisory: str
    def matches(self, ref):
        return ref in self.malicious_refs
CATALOG=[CompromisedAction(('bad-ref',),'aquasecurtiy typosquat incident')]
