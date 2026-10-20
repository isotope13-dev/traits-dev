# Resource acronyms retain their semantic ID suffix in generated SDKs.
class ResourceArgs:
    @property
    def bgpvpn_id(self):
        return self._bgpvpn_id

    @bgpvpn_id.setter
    def bgpvpn_id(self, value):
        self._bgpvpn_id = value

    @property
    def vxlan_id(self):
        return self._vxlan_id

    @vxlan_id.setter
    def vxlan_id(self, value):
        self._vxlan_id = value

class ResourceState(ResourceArgs):
    @property
    def bgpvpn_id(self):
        return self._bgpvpn_id

# These declarations and prose do not describe prompts or resolver APIs.
# Ordinary cloud SDK docs mention a storage backend without identifying a tool.
SDK_DOC = """container_sync_key: pulumi.Input[str]: The secret key for container
example = cloud.dns.Zone("example")
"""

def register_modules(resource_modules):
    import json
    modules = json.loads(resource_modules)
    for module in modules:
        yield module
